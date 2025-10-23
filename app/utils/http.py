from __future__ import annotations

import time
from typing import Any, Optional

import httpx
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings

_session = httpx.Client(timeout=settings.request_timeout_seconds)
_cache: TTLCache[str, tuple[float, Any]] = TTLCache(maxsize=1024, ttl=settings.cache_ttl_seconds)


def _cache_key(method: str, url: str, params: Optional[dict[str, Any]]) -> str:
    base = f"{method}:{url}"
    if not params:
        return base
    # simple stable representation
    items = ",".join(f"{k}={v}" for k, v in sorted(params.items()))
    return f"{base}?{items}"


@retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=4), stop=stop_after_attempt(3))
def fetch_json(url: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, str]] = None) -> Any:
    key = _cache_key("GET", url, params)
    now = time.time()

    if key in _cache:
        cached_at, data = _cache[key]
        return data

    response = _session.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    _cache[key] = (now, data)
    return data
