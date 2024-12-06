from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateFileUploadBody")


@_attrs_define
class CreateFileUploadBody:
    """
    Attributes:
        name (str):
        content_length (str):
        content_type (Union[Unset, str]):
        checksum_sha_256 (Union[Unset, str]): Base64 encoded SHA256 checksum of the file.
    """

    name: str
    content_length: str
    content_type: Union[Unset, str] = UNSET
    checksum_sha_256: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        content_length = self.content_length

        content_type = self.content_type

        checksum_sha_256 = self.checksum_sha_256

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "contentLength": content_length,
            }
        )
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if checksum_sha_256 is not UNSET:
            field_dict["checksumSha256"] = checksum_sha_256

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        content_length = d.pop("contentLength")

        content_type = d.pop("contentType", UNSET)

        checksum_sha_256 = d.pop("checksumSha256", UNSET)

        create_file_upload_body = cls(
            name=name,
            content_length=content_length,
            content_type=content_type,
            checksum_sha_256=checksum_sha_256,
        )

        create_file_upload_body.additional_properties = d
        return create_file_upload_body

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
