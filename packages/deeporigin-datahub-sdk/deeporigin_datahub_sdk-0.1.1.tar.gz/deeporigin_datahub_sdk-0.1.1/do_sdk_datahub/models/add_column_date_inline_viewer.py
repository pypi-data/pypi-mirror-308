from enum import Enum


class AddColumnDateInlineViewer(str, Enum):
    MOLECULE2D = "molecule2d"

    def __str__(self) -> str:
        return str(self.value)
