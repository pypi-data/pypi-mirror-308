from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.row_sort_item_sort import RowSortItemSort

T = TypeVar("T", bound="RowSortItem")


@_attrs_define
class RowSortItem:
    """
    Attributes:
        column_id (str):
        sort (RowSortItemSort):
    """

    column_id: str
    sort: RowSortItemSort
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        column_id = self.column_id

        sort = self.sort.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "columnId": column_id,
                "sort": sort,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column_id = d.pop("columnId")

        sort = RowSortItemSort(d.pop("sort"))

        row_sort_item = cls(
            column_id=column_id,
            sort=sort,
        )

        row_sort_item.additional_properties = d
        return row_sort_item

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
