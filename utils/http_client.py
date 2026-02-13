import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class RetryConfig:
    timeout_seconds: int = 20
    max_retries: int = 2
    backoff_base_seconds: float = 0.8

class HttpClient:
    def __init__(self, retry: RetryConfig):
        self.retry = retry
        self.session = requests.Session()

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        last_exc: Optional[Exception] = None
        for attempt in range(self.retry.max_retries + 1):
            try:
                return self.session.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    timeout=self.retry.timeout_seconds,
                )
            except requests.RequestException as e:
                last_exc = e
                wait = self.retry.backoff_base_seconds * (2 ** attempt)
                logger.warning("HTTP error (attempt %s/%s): %s; backoff %.2fs",
                               attempt + 1, self.retry.max_retries + 1, str(e), wait)
                time.sleep(wait)
        raise RuntimeError(f"HTTP request failed after retries: {last_exc}")
