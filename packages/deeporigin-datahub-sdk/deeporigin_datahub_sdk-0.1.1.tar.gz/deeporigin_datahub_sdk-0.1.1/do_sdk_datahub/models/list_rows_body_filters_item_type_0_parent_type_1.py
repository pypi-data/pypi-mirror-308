from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListRowsBodyFiltersItemType0ParentType1")


@_attrs_define
class ListRowsBodyFiltersItemType0ParentType1:
    """
    Attributes:
        is_root (bool):
    """

    is_root: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_root = self.is_root

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "isRoot": is_root,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_root = d.pop("isRoot")

        list_rows_body_filters_item_type_0_parent_type_1 = cls(
            is_root=is_root,
        )

        list_rows_body_filters_item_type_0_parent_type_1.additional_properties = d
        return list_rows_body_filters_item_type_0_parent_type_1

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
