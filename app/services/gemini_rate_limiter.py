"""Rolling-minute + daily call budget for the free-tier Gemini test path.

Not used by the Claude/Vertex path — only wired in when
settings.llm_provider == "gemini". Persists the daily count to a small
JSON file so it survives across separate pipeline runs on the same day.
"""
import json
import tempfile
import time
from datetime import date
from pathlib import Path
from threading import Lock

_STATE_PATH = Path(tempfile.gettempdir()) / "slrai_gemini_rate_state.json"


class DailyCapExceeded(RuntimeError):
    pass


class GeminiRateLimiter:
    def __init__(self, rpm_limit: int, rpd_limit: int, state_path: Path = _STATE_PATH):
        self.rpm_limit = rpm_limit
        self.rpd_limit = rpd_limit
        self._state_path = state_path
        self._lock = Lock()
        self._call_times: list[float] = []  # rolling 60s window

    def _load_daily_count(self) -> int:
        if not self._state_path.exists():
            return 0
        try:
            data = json.loads(self._state_path.read_text())
        except (json.JSONDecodeError, OSError):
            return 0
        if data.get("date") != date.today().isoformat():
            return 0
        return data.get("count", 0)

    def _save_daily_count(self, count: int) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(json.dumps({
            "date": date.today().isoformat(),
            "count": count,
        }))

    def before_call(self) -> None:
        """Blocks (sleeps) to stay under RPM; raises if the daily cap is hit."""
        with self._lock:
            daily_count = self._load_daily_count()
            if daily_count >= self.rpd_limit:
                raise DailyCapExceeded(
                    f"Gemini free-tier daily cap ({self.rpd_limit}) reached — "
                    "stop or resume tomorrow."
                )

            now = time.monotonic()
            self._call_times = [t for t in self._call_times if now - t < 60]
            if len(self._call_times) >= self.rpm_limit:
                sleep_for = 60 - (now - self._call_times[0]) + 0.1
                time.sleep(max(sleep_for, 0))
                now = time.monotonic()
                self._call_times = [t for t in self._call_times if now - t < 60]

            self._call_times.append(time.monotonic())
            self._save_daily_count(daily_count + 1)
