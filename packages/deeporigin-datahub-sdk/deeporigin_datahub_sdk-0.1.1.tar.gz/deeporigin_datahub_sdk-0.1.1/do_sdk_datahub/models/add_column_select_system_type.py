from enum import Enum


class AddColumnSelectSystemType(str, Enum):
    BODYDOCUMENT = "bodyDocument"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
