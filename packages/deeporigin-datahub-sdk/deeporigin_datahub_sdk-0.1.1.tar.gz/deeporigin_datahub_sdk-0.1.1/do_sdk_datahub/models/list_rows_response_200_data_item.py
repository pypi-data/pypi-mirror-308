from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_rows_response_200_data_item_type import ListRowsResponse200DataItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListRowsResponse200DataItem")


@_attrs_define
class ListRowsResponse200DataItem:
    """
    Attributes:
        id (str): Deep Origin system ID.
        hid (str):
        type (ListRowsResponse200DataItemType):
        parent_id (Union[Unset, str]):
        name (Union[Unset, str]):
    """

    id: str
    hid: str
    type: ListRowsResponse200DataItemType
    parent_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        hid = self.hid

        type = self.type.value

        parent_id = self.parent_id

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "hid": hid,
                "type": type,
            }
        )
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        hid = d.pop("hid")

        type = ListRowsResponse200DataItemType(d.pop("type"))

        parent_id = d.pop("parentId", UNSET)

        name = d.pop("name", UNSET)

        list_rows_response_200_data_item = cls(
            id=id,
            hid=hid,
            type=type,
            parent_id=parent_id,
            name=name,
        )

        list_rows_response_200_data_item.additional_properties = d
        return list_rows_response_200_data_item

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
