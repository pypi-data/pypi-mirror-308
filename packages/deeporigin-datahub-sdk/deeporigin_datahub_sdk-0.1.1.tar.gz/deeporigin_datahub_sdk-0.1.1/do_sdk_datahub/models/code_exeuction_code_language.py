from enum import Enum


class CodeExeuctionCodeLanguage(str, Enum):
    PYTHON = "python"

    def __str__(self) -> str:
        return str(self.value)
