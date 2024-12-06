from enum import Enum


class ColumnExpressionBaseExpressionReturnType(str, Enum):
    FLOAT = "float"
    INTEGER = "integer"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
