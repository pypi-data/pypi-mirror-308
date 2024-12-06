from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file import File
    from ..models.list_files_response_200_data_item_assignments_item import ListFilesResponse200DataItemAssignmentsItem


T = TypeVar("T", bound="ListFilesResponse200DataItem")


@_attrs_define
class ListFilesResponse200DataItem:
    """
    Attributes:
        file (File):
        assignments (Union[Unset, List['ListFilesResponse200DataItemAssignmentsItem']]):
    """

    file: "File"
    assignments: Union[Unset, List["ListFilesResponse200DataItemAssignmentsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_dict()

        assignments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.assignments, Unset):
            assignments = []
            for assignments_item_data in self.assignments:
                assignments_item = assignments_item_data.to_dict()
                assignments.append(assignments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )
        if assignments is not UNSET:
            field_dict["assignments"] = assignments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file import File
        from ..models.list_files_response_200_data_item_assignments_item import (
            ListFilesResponse200DataItemAssignmentsItem,
        )

        d = src_dict.copy()
        file = File.from_dict(d.pop("file"))

        assignments = []
        _assignments = d.pop("assignments", UNSET)
        for assignments_item_data in _assignments or []:
            assignments_item = ListFilesResponse200DataItemAssignmentsItem.from_dict(assignments_item_data)

            assignments.append(assignments_item)

        list_files_response_200_data_item = cls(
            file=file,
            assignments=assignments,
        )

        list_files_response_200_data_item.additional_properties = d
        return list_files_response_200_data_item

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
