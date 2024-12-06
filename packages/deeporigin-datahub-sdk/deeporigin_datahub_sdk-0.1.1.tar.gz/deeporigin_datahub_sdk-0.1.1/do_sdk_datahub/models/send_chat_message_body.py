from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.send_chat_message_body_context import SendChatMessageBodyContext
    from ..models.send_chat_message_body_messages_item import SendChatMessageBodyMessagesItem


T = TypeVar("T", bound="SendChatMessageBody")


@_attrs_define
class SendChatMessageBody:
    """
    Attributes:
        thread_id (str):
        messages (List['SendChatMessageBodyMessagesItem']):
        context (Union[Unset, SendChatMessageBodyContext]):
    """

    thread_id: str
    messages: List["SendChatMessageBodyMessagesItem"]
    context: Union[Unset, "SendChatMessageBodyContext"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        thread_id = self.thread_id

        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "threadId": thread_id,
                "messages": messages,
            }
        )
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.send_chat_message_body_context import SendChatMessageBodyContext
        from ..models.send_chat_message_body_messages_item import SendChatMessageBodyMessagesItem

        d = src_dict.copy()
        thread_id = d.pop("threadId")

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = SendChatMessageBodyMessagesItem.from_dict(messages_item_data)

            messages.append(messages_item)

        _context = d.pop("context", UNSET)
        context: Union[Unset, SendChatMessageBodyContext]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = SendChatMessageBodyContext.from_dict(_context)

        send_chat_message_body = cls(
            thread_id=thread_id,
            messages=messages,
            context=context,
        )

        send_chat_message_body.additional_properties = d
        return send_chat_message_body

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
