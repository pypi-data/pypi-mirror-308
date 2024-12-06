from enum import Enum


class ColumnPrimitiveCardinality(str, Enum):
    MANY = "many"
    ONE = "one"

    def __str__(self) -> str:
        return str(self.value)
