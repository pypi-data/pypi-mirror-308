from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EnsureRowsBodyRowsItemRow")


@_attrs_define
class EnsureRowsBodyRowsItemRow:
    """
    Attributes:
        creation_parent_id (Union[Unset, str]):
        creation_block_id (Union[Unset, str]):
        is_template (Union[Unset, bool]):
    """

    creation_parent_id: Union[Unset, str] = UNSET
    creation_block_id: Union[Unset, str] = UNSET
    is_template: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        creation_parent_id = self.creation_parent_id

        creation_block_id = self.creation_block_id

        is_template = self.is_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if creation_parent_id is not UNSET:
            field_dict["creationParentId"] = creation_parent_id
        if creation_block_id is not UNSET:
            field_dict["creationBlockId"] = creation_block_id
        if is_template is not UNSET:
            field_dict["isTemplate"] = is_template

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        creation_parent_id = d.pop("creationParentId", UNSET)

        creation_block_id = d.pop("creationBlockId", UNSET)

        is_template = d.pop("isTemplate", UNSET)

        ensure_rows_body_rows_item_row = cls(
            creation_parent_id=creation_parent_id,
            creation_block_id=creation_block_id,
            is_template=is_template,
        )

        ensure_rows_body_rows_item_row.additional_properties = d
        return ensure_rows_body_rows_item_row

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
