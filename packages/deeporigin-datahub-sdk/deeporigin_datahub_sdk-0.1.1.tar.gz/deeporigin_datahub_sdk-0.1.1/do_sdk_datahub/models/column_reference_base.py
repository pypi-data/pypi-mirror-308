from typing import Any, Dict, List, Literal, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ColumnReferenceBase")


@_attrs_define
class ColumnReferenceBase:
    """
    Attributes:
        type (Literal['reference']):
        reference_database_row_id (str):
    """

    type: Literal["reference"]
    reference_database_row_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        reference_database_row_id = self.reference_database_row_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "referenceDatabaseRowId": reference_database_row_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        reference_database_row_id = d.pop("referenceDatabaseRowId")

        column_reference_base = cls(
            type=type,
            reference_database_row_id=reference_database_row_id,
        )

        column_reference_base.additional_properties = d
        return column_reference_base

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
