import json
import uuid
from enum import Enum
from functools import reduce
from typing import List, Optional

from pydantic import BaseModel, computed_field, ConfigDict, Field
from keble_helpers import PydanticModelConfig
from redis import Redis


class ProgressTaskStage(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class ProgressReport(BaseModel):
    model_config = PydanticModelConfig.default()
    progress: float
    success: int
    failure: int
    pending: int
    errors: List[str] = []


class ProgressTask(BaseModel):

    model_config = ConfigDict(**PydanticModelConfig.default_dict(), arbitrary_types_allowed=True)
    stage: ProgressTaskStage = ProgressTaskStage.PENDING
    subtasks: List["ProgressTask"] = []
    error: Optional[str] = None
    redis: Optional[Redis] = None
    key: Optional[str] = None
    root: Optional["ProgressTask"] = None

    @classmethod
    def get_from_redis(cls, redis: Redis, *, key: str) -> Optional["ProgressTask"]:

        h = redis.get(key)
        if h is None: return None
        return ProgressTask(**json.loads(h))


    def _refresh_redis(self):
        if self.root is not None:
            self.root._refresh_redis()
        else:
            assert self.key is not None and self.redis is not None, "[Helpers] You must provide redis and key for progress task to refresh redis cache"
            self.redis.set(
                self.key,
                json.dumps(self.model_dump_circular_reference_safe()),
                ex=24 * 60 * 60 # expire after 24 hours
            )

    def new_subtask(self) -> "ProgressTask":
        # Avoid setting root to self, set it only to the rootmost instance
        root_task = self if self.root is None else self.root
        subtask = ProgressTask(root=root_task)
        self.subtasks.append(subtask)
        self._refresh_redis()
        return subtask

    # def new_subtask(self) -> "ProgressTask":
    #     t = ProgressTask(root=self if self.root is None else self.root)
    #     self.subtasks.append(t)
    #     self._refresh_redis()
    #     return t

    def success(self):

        self.stage = ProgressTaskStage.SUCCESS
        self._refresh_redis()

    def failure(self, error: Optional[str] = None):
        self.stage = ProgressTaskStage.FAILURE
        self.error = error
        # all pending subtask need to mark as failure
        for s in self.subtasks:
            if s.stage == ProgressTaskStage.PENDING:
                s.failure()
        self._refresh_redis()

    # @computed_field
    @property
    def progress_report(self) -> ProgressReport:
        subtask_progress = [s.progress_report for s in self.subtasks]
        total = 1 + len(self.subtasks)
        progress_floats = [p.progress * (1 / total) for p in subtask_progress]

        success = sum([p.success for p in subtask_progress]) if len(subtask_progress) > 0 else 0
        failure = sum([p.failure for p in subtask_progress]) if len(subtask_progress) > 0 else 0
        pending = sum([p.pending for p in subtask_progress]) if len(subtask_progress) > 0 else 0
        errors = reduce(lambda a, b: a + b, [p.errors for p in subtask_progress]) if len(subtask_progress) > 0 else []
        if self.stage == ProgressTaskStage.SUCCESS:
            success += 1
            progress_floats.append(1 / total)
        if self.stage == ProgressTaskStage.FAILURE:
            failure += 1
            if self.error is not None:
                errors.append(self.error)
        if self.stage == ProgressTaskStage.PENDING:
            pending += 1

        return ProgressReport(
            progress=sum(progress_floats) if len(progress_floats) > 0 else 0,
            success=success,
            failure=failure,
            pending=pending,
            errors=errors
        )

    def model_dump_circular_reference_safe(self) -> dict:
        """Custom model dump that excludes circular references."""
        return {
            "stage": self.stage,
            "error": self.error,
            "key": self.key,
            "subtasks": [s.model_dump_circular_reference_safe() for s in self.subtasks]
        }
        # return self.model_dump(exclude={"root", "subtasks", "redis"}, mode="json")
