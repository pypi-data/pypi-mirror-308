from enum import Enum


class CodeExeuctionStatus(str, Enum):
    FAIL = "fail"
    PENDING = "pending"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
