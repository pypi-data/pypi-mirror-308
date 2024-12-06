from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chat_thread import ChatThread


T = TypeVar("T", bound="CreateChatThreadResponse200Data")


@_attrs_define
class CreateChatThreadResponse200Data:
    """
    Attributes:
        chat_thread (ChatThread):
    """

    chat_thread: "ChatThread"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chat_thread = self.chat_thread.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chatThread": chat_thread,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_thread import ChatThread

        d = src_dict.copy()
        chat_thread = ChatThread.from_dict(d.pop("chatThread"))

        create_chat_thread_response_200_data = cls(
            chat_thread=chat_thread,
        )

        create_chat_thread_response_200_data.additional_properties = d
        return create_chat_thread_response_200_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
