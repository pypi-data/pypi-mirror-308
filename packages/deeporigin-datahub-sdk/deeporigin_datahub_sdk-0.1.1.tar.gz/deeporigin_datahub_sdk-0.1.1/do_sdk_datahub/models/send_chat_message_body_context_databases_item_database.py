from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SendChatMessageBodyContextDatabasesItemDatabase")


@_attrs_define
class SendChatMessageBodyContextDatabasesItemDatabase:
    """The selected database.

    Attributes:
        name (str): Display name of the database.
        hid (str): ID of the database.
        hid_prefix (str): Prefix for rows created in the database.
    """

    name: str
    hid: str
    hid_prefix: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        hid = self.hid

        hid_prefix = self.hid_prefix

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "hid": hid,
                "hidPrefix": hid_prefix,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        hid = d.pop("hid")

        hid_prefix = d.pop("hidPrefix")

        send_chat_message_body_context_databases_item_database = cls(
            name=name,
            hid=hid,
            hid_prefix=hid_prefix,
        )

        return send_chat_message_body_context_databases_item_database
