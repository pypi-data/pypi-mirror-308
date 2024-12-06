from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.send_chat_message_body_context_databases_item import SendChatMessageBodyContextDatabasesItem


T = TypeVar("T", bound="SendChatMessageBodyContext")


@_attrs_define
class SendChatMessageBodyContext:
    """
    Attributes:
        databases (Union[Unset, List['SendChatMessageBodyContextDatabasesItem']]):
    """

    databases: Union[Unset, List["SendChatMessageBodyContextDatabasesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        databases: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.databases, Unset):
            databases = []
            for databases_item_data in self.databases:
                databases_item = databases_item_data.to_dict()
                databases.append(databases_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if databases is not UNSET:
            field_dict["databases"] = databases

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.send_chat_message_body_context_databases_item import SendChatMessageBodyContextDatabasesItem

        d = src_dict.copy()
        databases = []
        _databases = d.pop("databases", UNSET)
        for databases_item_data in _databases or []:
            databases_item = SendChatMessageBodyContextDatabasesItem.from_dict(databases_item_data)

            databases.append(databases_item)

        send_chat_message_body_context = cls(
            databases=databases,
        )

        send_chat_message_body_context.additional_properties = d
        return send_chat_message_body_context

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
