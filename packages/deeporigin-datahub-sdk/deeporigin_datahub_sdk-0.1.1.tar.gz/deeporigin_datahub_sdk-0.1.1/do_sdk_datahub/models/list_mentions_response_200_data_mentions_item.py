from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_mentions_response_200_data_mentions_item_type import ListMentionsResponse200DataMentionsItemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListMentionsResponse200DataMentionsItem")


@_attrs_define
class ListMentionsResponse200DataMentionsItem:
    """
    Attributes:
        type (ListMentionsResponse200DataMentionsItemType):
        id (str):
        hid (str):
        name (Union[Unset, str]):
        parent_id (Union[Unset, str]):
    """

    type: ListMentionsResponse200DataMentionsItemType
    id: str
    hid: str
    name: Union[Unset, str] = UNSET
    parent_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        hid = self.hid

        name = self.name

        parent_id = self.parent_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "hid": hid,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = ListMentionsResponse200DataMentionsItemType(d.pop("type"))

        id = d.pop("id")

        hid = d.pop("hid")

        name = d.pop("name", UNSET)

        parent_id = d.pop("parentId", UNSET)

        list_mentions_response_200_data_mentions_item = cls(
            type=type,
            id=id,
            hid=hid,
            name=name,
            parent_id=parent_id,
        )

        list_mentions_response_200_data_mentions_item.additional_properties = d
        return list_mentions_response_200_data_mentions_item

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
