from enum import Enum


class ListChatThreadMessagesResponse200DataMessagesItemRole(str, Enum):
    ASSISTANT = "assistant"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
