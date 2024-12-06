from enum import Enum


class AddColumnFileSystemType(str, Enum):
    BODYDOCUMENT = "bodyDocument"
    NAME = "name"

    def __str__(self) -> str:
        return str(self.value)
