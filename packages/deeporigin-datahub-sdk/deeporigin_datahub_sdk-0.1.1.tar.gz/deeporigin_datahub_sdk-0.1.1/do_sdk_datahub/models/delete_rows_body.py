from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteRowsBody")


@_attrs_define
class DeleteRowsBody:
    """
    Attributes:
        database_id (str):
        delete_all (Union[Unset, bool]): When true, deletes all rows in the table except rows with the specified
            `rowIds`.
        row_ids (Union[Unset, List[str]]): List of row IDs to delete.
    """

    database_id: str
    delete_all: Union[Unset, bool] = UNSET
    row_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database_id = self.database_id

        delete_all = self.delete_all

        row_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.row_ids, Unset):
            row_ids = self.row_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "databaseId": database_id,
            }
        )
        if delete_all is not UNSET:
            field_dict["deleteAll"] = delete_all
        if row_ids is not UNSET:
            field_dict["rowIds"] = row_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        database_id = d.pop("databaseId")

        delete_all = d.pop("deleteAll", UNSET)

        row_ids = cast(List[str], d.pop("rowIds", UNSET))

        delete_rows_body = cls(
            database_id=database_id,
            delete_all=delete_all,
            row_ids=row_ids,
        )

        delete_rows_body.additional_properties = d
        return delete_rows_body

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
