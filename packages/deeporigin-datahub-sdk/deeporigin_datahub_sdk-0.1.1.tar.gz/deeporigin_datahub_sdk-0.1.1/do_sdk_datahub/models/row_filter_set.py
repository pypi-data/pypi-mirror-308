from typing import Any, Dict, List, Literal, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RowFilterSet")


@_attrs_define
class RowFilterSet:
    """
    Attributes:
        filter_type (Literal['set']):
        column_id (str):
        values (List[None]):
    """

    filter_type: Literal["set"]
    column_id: str
    values: List[None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_type = self.filter_type

        column_id = self.column_id

        values = self.values

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filterType": filter_type,
                "columnId": column_id,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_type = d.pop("filterType")

        column_id = d.pop("columnId")

        values = cast(List[None], d.pop("values"))

        row_filter_set = cls(
            filter_type=filter_type,
            column_id=column_id,
            values=values,
        )

        row_filter_set.additional_properties = d
        return row_filter_set

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
