from enum import Enum


class RowFilterNullityOperator(str, Enum):
    ISNOTNULL = "isNotNull"
    ISNULL = "isNull"

    def __str__(self) -> str:
        return str(self.value)
