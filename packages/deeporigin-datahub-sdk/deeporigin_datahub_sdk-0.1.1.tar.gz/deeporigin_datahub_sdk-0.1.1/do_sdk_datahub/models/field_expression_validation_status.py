from enum import Enum


class FieldExpressionValidationStatus(str, Enum):
    INVALID = "invalid"
    VALID = "valid"

    def __str__(self) -> str:
        return str(self.value)
