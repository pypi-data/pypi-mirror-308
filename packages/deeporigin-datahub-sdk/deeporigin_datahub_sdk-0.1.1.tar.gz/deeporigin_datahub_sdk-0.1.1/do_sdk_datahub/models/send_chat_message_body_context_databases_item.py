from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.send_chat_message_body_context_databases_item_columns_item import (
        SendChatMessageBodyContextDatabasesItemColumnsItem,
    )
    from ..models.send_chat_message_body_context_databases_item_database import (
        SendChatMessageBodyContextDatabasesItemDatabase,
    )
    from ..models.send_chat_message_body_context_databases_item_rows_item import (
        SendChatMessageBodyContextDatabasesItemRowsItem,
    )


T = TypeVar("T", bound="SendChatMessageBodyContextDatabasesItem")


@_attrs_define
class SendChatMessageBodyContextDatabasesItem:
    """
    Attributes:
        database (SendChatMessageBodyContextDatabasesItemDatabase): The selected database.
        rows (Union[Unset, List['SendChatMessageBodyContextDatabasesItemRowsItem']]): List of rows to filter the
            dataframe by.
        columns (Union[Unset, List['SendChatMessageBodyContextDatabasesItemColumnsItem']]): List of columns to filter
            the dataframe by.
    """

    database: "SendChatMessageBodyContextDatabasesItemDatabase"
    rows: Union[Unset, List["SendChatMessageBodyContextDatabasesItemRowsItem"]] = UNSET
    columns: Union[Unset, List["SendChatMessageBodyContextDatabasesItemColumnsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database = self.database.to_dict()

        rows: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()
                rows.append(rows_item)

        columns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()
                columns.append(columns_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "database": database,
            }
        )
        if rows is not UNSET:
            field_dict["rows"] = rows
        if columns is not UNSET:
            field_dict["columns"] = columns

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.send_chat_message_body_context_databases_item_columns_item import (
            SendChatMessageBodyContextDatabasesItemColumnsItem,
        )
        from ..models.send_chat_message_body_context_databases_item_database import (
            SendChatMessageBodyContextDatabasesItemDatabase,
        )
        from ..models.send_chat_message_body_context_databases_item_rows_item import (
            SendChatMessageBodyContextDatabasesItemRowsItem,
        )

        d = src_dict.copy()
        database = SendChatMessageBodyContextDatabasesItemDatabase.from_dict(d.pop("database"))

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = SendChatMessageBodyContextDatabasesItemRowsItem.from_dict(rows_item_data)

            rows.append(rows_item)

        columns = []
        _columns = d.pop("columns", UNSET)
        for columns_item_data in _columns or []:
            columns_item = SendChatMessageBodyContextDatabasesItemColumnsItem.from_dict(columns_item_data)

            columns.append(columns_item)

        send_chat_message_body_context_databases_item = cls(
            database=database,
            rows=rows,
            columns=columns,
        )

        send_chat_message_body_context_databases_item.additional_properties = d
        return send_chat_message_body_context_databases_item

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
