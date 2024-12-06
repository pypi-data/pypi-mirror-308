from enum import Enum


class RowFilterTextOperator(str, Enum):
    CONTAINS = "contains"
    ENDSWITH = "endsWith"
    EQUALS = "equals"
    NOTCONTAINS = "notContains"
    NOTEQUAL = "notEqual"
    STARTSWITH = "startsWith"

    def __str__(self) -> str:
        return str(self.value)
