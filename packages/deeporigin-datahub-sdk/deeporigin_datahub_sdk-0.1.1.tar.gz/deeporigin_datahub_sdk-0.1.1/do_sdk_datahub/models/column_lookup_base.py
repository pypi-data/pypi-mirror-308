from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.column_primitive import ColumnPrimitive


T = TypeVar("T", bound="ColumnLookupBase")


@_attrs_define
class ColumnLookupBase:
    """
    Attributes:
        type (Literal['lookup']):
        lookup_source_column_id (str):
        lookup_external_column_id (str):
        lookup_external_column (ColumnPrimitive):
    """

    type: Literal["lookup"]
    lookup_source_column_id: str
    lookup_external_column_id: str
    lookup_external_column: "ColumnPrimitive"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        lookup_source_column_id = self.lookup_source_column_id

        lookup_external_column_id = self.lookup_external_column_id

        lookup_external_column = self.lookup_external_column.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "lookupSourceColumnId": lookup_source_column_id,
                "lookupExternalColumnId": lookup_external_column_id,
                "lookupExternalColumn": lookup_external_column,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column_primitive import ColumnPrimitive

        d = src_dict.copy()
        type = d.pop("type")

        lookup_source_column_id = d.pop("lookupSourceColumnId")

        lookup_external_column_id = d.pop("lookupExternalColumnId")

        lookup_external_column = ColumnPrimitive.from_dict(d.pop("lookupExternalColumn"))

        column_lookup_base = cls(
            type=type,
            lookup_source_column_id=lookup_source_column_id,
            lookup_external_column_id=lookup_external_column_id,
            lookup_external_column=lookup_external_column,
        )

        column_lookup_base.additional_properties = d
        return column_lookup_base

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
