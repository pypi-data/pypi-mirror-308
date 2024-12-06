from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListFilesBodyFiltersItem")


@_attrs_define
class ListFilesBodyFiltersItem:
    """
    Attributes:
        assigned_row_ids (Union[Unset, List[str]]):
        is_unassigned (Union[Unset, bool]):
        file_ids (Union[Unset, List[str]]):
    """

    assigned_row_ids: Union[Unset, List[str]] = UNSET
    is_unassigned: Union[Unset, bool] = UNSET
    file_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        assigned_row_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.assigned_row_ids, Unset):
            assigned_row_ids = self.assigned_row_ids

        is_unassigned = self.is_unassigned

        file_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.file_ids, Unset):
            file_ids = self.file_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if assigned_row_ids is not UNSET:
            field_dict["assignedRowIds"] = assigned_row_ids
        if is_unassigned is not UNSET:
            field_dict["isUnassigned"] = is_unassigned
        if file_ids is not UNSET:
            field_dict["fileIds"] = file_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assigned_row_ids = cast(List[str], d.pop("assignedRowIds", UNSET))

        is_unassigned = d.pop("isUnassigned", UNSET)

        file_ids = cast(List[str], d.pop("fileIds", UNSET))

        list_files_body_filters_item = cls(
            assigned_row_ids=assigned_row_ids,
            is_unassigned=is_unassigned,
            file_ids=file_ids,
        )

        list_files_body_filters_item.additional_properties = d
        return list_files_body_filters_item

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
