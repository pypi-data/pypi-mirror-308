from enum import Enum


class FileStatus(str, Enum):
    ARCHIVED = "archived"
    READY = "ready"

    def __str__(self) -> str:
        return str(self.value)
