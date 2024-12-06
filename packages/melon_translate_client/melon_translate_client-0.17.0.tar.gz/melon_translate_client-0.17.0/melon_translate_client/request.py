import concurrent.futures
import time
from itertools import product
from math import ceil
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode, urlparse

import gevent
import requests
from melon_translate_client.settings import (
    TRANSLATE_REQUESTS_TIMEOUT,
    TRANSLATE_URL,
    TRANSLATE_WORKER_POOL_SIZE,
    TRANSLATE_HTTPS_PROXY,
    TRANSLATE_HTTP_PROXY,
    TRANSLATE_USE_PROXY,
    log,
)


def translate_url(language, target_url: str = None) -> str:
    """Get target translate service URL."""
    target_url = target_url or TRANSLATE_URL

    _url = urlparse(f"{target_url}/api/v2/translations/{language}/")
    return _url.geturl()


def build_params(
    views: List[str],
    timestamp: int = None,
    page_size: int = None,
    page: int = None,
) -> dict:
    """Build HTTP params."""
    params = {}
    if timestamp:
        params["timestamp"] = timestamp

    if views:
        params["views"] = views

    if page_size and page:
        params["page_size"] = page_size
        params["page"] = page

    return params


def get_proxies() -> Dict[str, str]:
    """Return proxy configuration if enabled."""
    return {"http": TRANSLATE_HTTP_PROXY, "https": TRANSLATE_HTTPS_PROXY} if TRANSLATE_USE_PROXY else {}


def parse_response(response: requests.Response, url: str) -> Dict[str, Any]:
    """Parse JSON response with error handling."""
    try:
        return response.json()
    except ValueError as e:
        log.error(f"Invalid JSON from {url}: {str(e)}")
        raise


def make_request(
    session: requests.Session,
    url: str,
    headers: Dict[str, str] = None,
    timeout: int = TRANSLATE_REQUESTS_TIMEOUT,
) -> Tuple[str, Dict[str, Any]]:

    headers = headers or {"Cache-Control": "no-cache"}
    try:
        response = session.get(url, timeout=timeout, proxies=get_proxies(), headers=headers)
        response.raise_for_status()
        return response.url, parse_response(response, url)
    except requests.RequestException as e:
        log.error(f"Failed to fetch {url}: {str(e)}")
        raise


def fetch(url):
    """Fetch data from url."""
    with requests.Session() as session:
        _, response = make_request(session, url)
        return url, response


def fetch_all(language: str, views: List[str], page_size: int = 500, timestamp=None) -> Optional[list]:
    """Return all pages for specified query."""

    params = build_params(views, timestamp, page_size, 1)

    with requests.Session() as session:
        url = translate_url(language)

        full_url, response = make_request(session, url)

        results = response.get("results")

        if not results:
            log.error(f"[error] url={url}, params={params}, response={response}")
            return None

        count = response.get("count")

        pages = ceil(count / page_size)
        urls = [full_url.replace("page=1", f"page={idx}") for idx in range(2, pages + 1)]

        greenlets = [gevent.spawn(fetch, url) for url in urls]
        for greenlet in gevent.iwait(greenlets):
            url, response_json = greenlet.value
            log.debug(
                f"answer from {url} received {len(response_json.get('results', []))} objects\n",
                url,
            )
            results += response_json.get("results", [])

        # note: should be optimized.
        for response in results:
            response["language"] = language

        return results


def fetch_all_par(
    languages: List[str],
    # NOTE: views_par is a list of strings chained together with OR operator in parallel requests mode
    views_par: List[str],
    page_size: int = 1000,
):
    """Return all pages for for product of languages and views."""
    pairs = list(product(languages, views_par))
    timestamp = int(time.time())

    # TODO: Use gevent here as well, no need for context switching.
    with concurrent.futures.ThreadPoolExecutor(max_workers=TRANSLATE_WORKER_POOL_SIZE or None) as executor:
        result_future = (
            executor.submit(lambda p: fetch_all(p[0], [p[1]], page_size, timestamp), pair) for pair in pairs
        )

        for future in concurrent.futures.as_completed(result_future):
            try:
                result = future.result()
            except Exception as exc:  # TODO: find correct exception to catch
                log.exception(exc)
            else:
                if result:
                    yield result
