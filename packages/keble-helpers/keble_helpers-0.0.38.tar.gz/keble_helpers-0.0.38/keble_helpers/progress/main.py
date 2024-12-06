from redis import Redis

from .schemas import ProgressTask, ProgressReport


class ProgressHandler:

    def __init__(self, redis: Redis):
        self._redis = redis

    def new(self, *, key: str) -> ProgressTask:
        return ProgressTask(redis=self._redis, key=key)

    def get(self, *, key: str) -> ProgressReport | None:
        t = ProgressTask.get_from_redis(redis=self._redis, key=key)
        if t is None: return None
        return t.progress_report
