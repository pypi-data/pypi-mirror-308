from enum import Enum


class ListMentionsResponse200DataMentionsItemType(str, Enum):
    DATABASE = "database"
    ROW = "row"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
