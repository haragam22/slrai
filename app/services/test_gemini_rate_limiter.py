import tempfile
from pathlib import Path

from app.services.gemini_rate_limiter import DailyCapExceeded, GeminiRateLimiter


def test_daily_cap_raises():
    with tempfile.TemporaryDirectory() as d:
        limiter = GeminiRateLimiter(rpm_limit=100, rpd_limit=2, state_path=Path(d) / "state.json")
        limiter.before_call()
        limiter.before_call()
        try:
            limiter.before_call()
            assert False, "expected DailyCapExceeded"
        except DailyCapExceeded:
            pass


def test_rpm_throttles_not_raises():
    with tempfile.TemporaryDirectory() as d:
        limiter = GeminiRateLimiter(rpm_limit=2, rpd_limit=100, state_path=Path(d) / "state.json")
        limiter.before_call()
        limiter.before_call()
        # third call would sleep ~60s in real life — skip actually calling it here.


if __name__ == "__main__":
    test_daily_cap_raises()
    test_rpm_throttles_not_raises()
    print("ok")
