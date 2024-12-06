from typing import Any, Dict, List, Literal, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.row_filter_nullity_operator import RowFilterNullityOperator

T = TypeVar("T", bound="RowFilterNullity")


@_attrs_define
class RowFilterNullity:
    """
    Attributes:
        filter_type (Literal['nullity']):
        column_id (str):
        operator (RowFilterNullityOperator):
    """

    filter_type: Literal["nullity"]
    column_id: str
    operator: RowFilterNullityOperator
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_type = self.filter_type

        column_id = self.column_id

        operator = self.operator.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filterType": filter_type,
                "columnId": column_id,
                "operator": operator,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_type = d.pop("filterType")

        column_id = d.pop("columnId")

        operator = RowFilterNullityOperator(d.pop("operator"))

        row_filter_nullity = cls(
            filter_type=filter_type,
            column_id=column_id,
            operator=operator,
        )

        row_filter_nullity.additional_properties = d
        return row_filter_nullity

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
