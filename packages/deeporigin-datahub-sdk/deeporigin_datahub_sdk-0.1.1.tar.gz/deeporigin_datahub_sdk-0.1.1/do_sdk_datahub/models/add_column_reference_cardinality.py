from enum import Enum


class AddColumnReferenceCardinality(str, Enum):
    MANY = "many"
    ONE = "one"

    def __str__(self) -> str:
        return str(self.value)
