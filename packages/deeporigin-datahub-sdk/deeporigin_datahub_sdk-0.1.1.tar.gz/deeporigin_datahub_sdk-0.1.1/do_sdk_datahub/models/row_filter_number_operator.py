from enum import Enum


class RowFilterNumberOperator(str, Enum):
    EQUALS = "equals"
    GREATERTHAN = "greaterThan"
    GREATERTHANOREQUAL = "greaterThanOrEqual"
    LESSTHAN = "lessThan"
    LESSTHANOREQUAL = "lessThanOrEqual"
    NOTEQUAL = "notEqual"

    def __str__(self) -> str:
        return str(self.value)
