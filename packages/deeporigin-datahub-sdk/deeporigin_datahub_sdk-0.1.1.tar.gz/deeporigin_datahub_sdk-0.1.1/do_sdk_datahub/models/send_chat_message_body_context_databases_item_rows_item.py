from typing import Any, Dict, Type, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SendChatMessageBodyContextDatabasesItemRowsItem")


@_attrs_define
class SendChatMessageBodyContextDatabasesItemRowsItem:
    """
    Attributes:
        hid (str): ID of the row.
        name (Union[Unset, str]): Display name of the row.
    """

    hid: str
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        hid = self.hid

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "hid": hid,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hid = d.pop("hid")

        name = d.pop("name", UNSET)

        send_chat_message_body_context_databases_item_rows_item = cls(
            hid=hid,
            name=name,
        )

        return send_chat_message_body_context_databases_item_rows_item
