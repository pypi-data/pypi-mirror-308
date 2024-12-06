from enum import Enum


class GetJobResponse200ApprovalType0Status(str, Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
