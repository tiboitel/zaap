"""In-memory rate limiter for auth endpoints."""

import threading
import time
from collections import defaultdict


class RateLimitError(Exception):
    """Rate limit exceeded."""

    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded, retry after {retry_after}s")


class RateLimiter:
    """Sliding window rate limiter."""

    def __init__(
        self, ip_limit: int, ip_window: int, account_limit: int, account_window: int
    ):
        self.ip_limit = ip_limit
        self.ip_window = ip_window
        self.account_limit = account_limit
        self.account_window = account_window
        self._lock = threading.Lock()
        self._ip_timestamps: dict[str, list[float]] = defaultdict(list)
        self._account_timestamps: dict[str, list[float]] = defaultdict(list)

    def _clean_old(self, timestamps: list[float], window: int) -> None:
        now = time.monotonic()
        cutoff = now - window
        timestamps[:] = [t for t in timestamps if t > cutoff]

    def _get_retry_after(self, timestamps: list[float], window: int) -> int:
        if len(timestamps) < 1:
            return 0
        oldest = min(timestamps)
        retry_after = int(oldest + window - time.monotonic()) + 1
        return max(0, retry_after)

    def check(self, ip: str, account_id: str | None = None) -> int:
        now = time.monotonic()
        with self._lock:
            self._clean_old(self._ip_timestamps[ip], self.ip_window)
            if len(self._ip_timestamps[ip]) >= self.ip_limit:
                raise RateLimitError(
                    self._get_retry_after(self._ip_timestamps[ip], self.ip_window)
                )
            self._ip_timestamps[ip].append(now)

            if account_id:
                self._clean_old(
                    self._account_timestamps[account_id], self.account_window
                )
                if len(self._account_timestamps[account_id]) >= self.account_limit:
                    raise RateLimitError(
                        self._get_retry_after(
                            self._account_timestamps[account_id],
                            self.account_window,
                        )
                    )
                self._account_timestamps[account_id].append(now)

        return 0


auth_limiter = RateLimiter(
    ip_limit=12,
    ip_window=60,
    account_limit=6,
    account_window=600,
)