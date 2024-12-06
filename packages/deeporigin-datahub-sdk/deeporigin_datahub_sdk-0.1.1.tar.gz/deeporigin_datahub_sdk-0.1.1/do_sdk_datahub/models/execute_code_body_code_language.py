from enum import Enum


class ExecuteCodeBodyCodeLanguage(str, Enum):
    PYTHON = "python"

    def __str__(self) -> str:
        return str(self.value)
