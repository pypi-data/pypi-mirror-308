from typing import Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Workspace")


@_attrs_define
class Workspace:
    """
    Attributes:
        id (str): Deep Origin system ID.
        type (Literal['workspace']):
        hid (str):
        name (str):
        date_created (str):
        date_updated (Union[Unset, str]):
        created_by_user_drn (Union[Unset, str]):
        edited_by_user_drn (Union[Unset, str]):
        parent_id (Union[Unset, str]):
        creation_parent_id (Union[Unset, str]):
        creation_block_id (Union[Unset, str]):
        editor (Union[Unset, Any]):
    """

    id: str
    type: Literal["workspace"]
    hid: str
    name: str
    date_created: str
    date_updated: Union[Unset, str] = UNSET
    created_by_user_drn: Union[Unset, str] = UNSET
    edited_by_user_drn: Union[Unset, str] = UNSET
    parent_id: Union[Unset, str] = UNSET
    creation_parent_id: Union[Unset, str] = UNSET
    creation_block_id: Union[Unset, str] = UNSET
    editor: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        type = self.type

        hid = self.hid

        name = self.name

        date_created = self.date_created

        date_updated = self.date_updated

        created_by_user_drn = self.created_by_user_drn

        edited_by_user_drn = self.edited_by_user_drn

        parent_id = self.parent_id

        creation_parent_id = self.creation_parent_id

        creation_block_id = self.creation_block_id

        editor = self.editor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "hid": hid,
                "name": name,
                "dateCreated": date_created,
            }
        )
        if date_updated is not UNSET:
            field_dict["dateUpdated"] = date_updated
        if created_by_user_drn is not UNSET:
            field_dict["createdByUserDrn"] = created_by_user_drn
        if edited_by_user_drn is not UNSET:
            field_dict["editedByUserDrn"] = edited_by_user_drn
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if creation_parent_id is not UNSET:
            field_dict["creationParentId"] = creation_parent_id
        if creation_block_id is not UNSET:
            field_dict["creationBlockId"] = creation_block_id
        if editor is not UNSET:
            field_dict["editor"] = editor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        hid = d.pop("hid")

        name = d.pop("name")

        date_created = d.pop("dateCreated")

        date_updated = d.pop("dateUpdated", UNSET)

        created_by_user_drn = d.pop("createdByUserDrn", UNSET)

        edited_by_user_drn = d.pop("editedByUserDrn", UNSET)

        parent_id = d.pop("parentId", UNSET)

        creation_parent_id = d.pop("creationParentId", UNSET)

        creation_block_id = d.pop("creationBlockId", UNSET)

        editor = d.pop("editor", UNSET)

        workspace = cls(
            id=id,
            type=type,
            hid=hid,
            name=name,
            date_created=date_created,
            date_updated=date_updated,
            created_by_user_drn=created_by_user_drn,
            edited_by_user_drn=edited_by_user_drn,
            parent_id=parent_id,
            creation_parent_id=creation_parent_id,
            creation_block_id=creation_block_id,
            editor=editor,
        )

        workspace.additional_properties = d
        return workspace

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
