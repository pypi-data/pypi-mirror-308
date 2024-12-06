from enum import Enum


class ColumnPrimitiveType(str, Enum):
    BOOLEAN = "boolean"
    DATE = "date"
    EDITOR = "editor"
    EXPRESSION = "expression"
    FILE = "file"
    FLOAT = "float"
    INTEGER = "integer"
    LOOKUP = "lookup"
    REFERENCE = "reference"
    SELECT = "select"
    TEXT = "text"
    URL = "url"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
