from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDatabaseBodyDatabase")


@_attrs_define
class UpdateDatabaseBodyDatabase:
    """
    Attributes:
        hid (Union[Unset, str]):
        name (Union[Unset, str]):
        parent_id (Union[None, Unset, str]):
        hid_prefix (Union[Unset, str]):
        editor (Union[Unset, Any]):
    """

    hid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    parent_id: Union[None, Unset, str] = UNSET
    hid_prefix: Union[Unset, str] = UNSET
    editor: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hid = self.hid

        name = self.name

        parent_id: Union[None, Unset, str]
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        hid_prefix = self.hid_prefix

        editor = self.editor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hid is not UNSET:
            field_dict["hid"] = hid
        if name is not UNSET:
            field_dict["name"] = name
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if hid_prefix is not UNSET:
            field_dict["hidPrefix"] = hid_prefix
        if editor is not UNSET:
            field_dict["editor"] = editor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hid = d.pop("hid", UNSET)

        name = d.pop("name", UNSET)

        def _parse_parent_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_id = _parse_parent_id(d.pop("parentId", UNSET))

        hid_prefix = d.pop("hidPrefix", UNSET)

        editor = d.pop("editor", UNSET)

        update_database_body_database = cls(
            hid=hid,
            name=name,
            parent_id=parent_id,
            hid_prefix=hid_prefix,
            editor=editor,
        )

        update_database_body_database.additional_properties = d
        return update_database_body_database

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
