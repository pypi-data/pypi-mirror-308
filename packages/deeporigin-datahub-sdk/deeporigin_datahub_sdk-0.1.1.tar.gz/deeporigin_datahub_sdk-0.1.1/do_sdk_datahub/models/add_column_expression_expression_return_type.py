from enum import Enum


class AddColumnExpressionExpressionReturnType(str, Enum):
    FLOAT = "float"
    INTEGER = "integer"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
