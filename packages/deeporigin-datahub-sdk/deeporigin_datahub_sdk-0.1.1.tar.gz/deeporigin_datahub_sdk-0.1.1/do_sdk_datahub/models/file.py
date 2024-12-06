from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.file_status import FileStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="File")


@_attrs_define
class File:
    """
    Attributes:
        id (str): Deep Origin system ID.
        uri (str):
        name (str):
        status (FileStatus):
        content_length (float):
        date_created (str):
        content_type (Union[Unset, str]):
        date_updated (Union[Unset, str]):
        created_by_user_drn (Union[Unset, str]):
    """

    id: str
    uri: str
    name: str
    status: FileStatus
    content_length: float
    date_created: str
    content_type: Union[Unset, str] = UNSET
    date_updated: Union[Unset, str] = UNSET
    created_by_user_drn: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        uri = self.uri

        name = self.name

        status = self.status.value

        content_length = self.content_length

        date_created = self.date_created

        content_type = self.content_type

        date_updated = self.date_updated

        created_by_user_drn = self.created_by_user_drn

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uri": uri,
                "name": name,
                "status": status,
                "contentLength": content_length,
                "dateCreated": date_created,
            }
        )
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if date_updated is not UNSET:
            field_dict["dateUpdated"] = date_updated
        if created_by_user_drn is not UNSET:
            field_dict["createdByUserDrn"] = created_by_user_drn

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        uri = d.pop("uri")

        name = d.pop("name")

        status = FileStatus(d.pop("status"))

        content_length = d.pop("contentLength")

        date_created = d.pop("dateCreated")

        content_type = d.pop("contentType", UNSET)

        date_updated = d.pop("dateUpdated", UNSET)

        created_by_user_drn = d.pop("createdByUserDrn", UNSET)

        file = cls(
            id=id,
            uri=uri,
            name=name,
            status=status,
            content_length=content_length,
            date_created=date_created,
            content_type=content_type,
            date_updated=date_updated,
            created_by_user_drn=created_by_user_drn,
        )

        file.additional_properties = d
        return file

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
