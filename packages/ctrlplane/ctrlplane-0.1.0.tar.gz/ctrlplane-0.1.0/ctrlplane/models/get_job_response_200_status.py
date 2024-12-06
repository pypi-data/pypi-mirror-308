from enum import Enum


class GetJobResponse200Status(str, Enum):
    ACTION_REQUIRED = "action_required"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    EXTERNAL_RUN_NOT_FOUND = "external_run_not_found"
    FAILURE = "failure"
    INVALID_INTEGRATION = "invalid_integration"
    INVALID_JOB_AGENT = "invalid_job_agent"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    SKIPPED = "skipped"

    def __str__(self) -> str:
        return str(self.value)
