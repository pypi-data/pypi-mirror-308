from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EnsureRowsBodyRowsItemCellsItem")


@_attrs_define
class EnsureRowsBodyRowsItemCellsItem:
    """
    Attributes:
        column_id (str): The column's name or system ID.
        value (Any):
        previous_version (Union[Unset, float]): The previous version of the cell. When `checkPreviousValue` is true, the
            insertion will atomically ensure an incremental update to `previousVersion`.
    """

    column_id: str
    value: Any
    previous_version: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        column_id = self.column_id

        value = self.value

        previous_version = self.previous_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "columnId": column_id,
                "value": value,
            }
        )
        if previous_version is not UNSET:
            field_dict["previousVersion"] = previous_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        column_id = d.pop("columnId")

        value = d.pop("value")

        previous_version = d.pop("previousVersion", UNSET)

        ensure_rows_body_rows_item_cells_item = cls(
            column_id=column_id,
            value=value,
            previous_version=previous_version,
        )

        ensure_rows_body_rows_item_cells_item.additional_properties = d
        return ensure_rows_body_rows_item_cells_item

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
