from enum import Enum


class RowFilterBooleanOperator(str, Enum):
    EQUALS = "equals"
    NOTEQUAL = "notEqual"

    def __str__(self) -> str:
        return str(self.value)
