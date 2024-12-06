from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddColumnFileConfigFile")


@_attrs_define
class AddColumnFileConfigFile:
    """
    Attributes:
        allowed_extensions (Union[Unset, List[str]]):
    """

    allowed_extensions: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        allowed_extensions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.allowed_extensions, Unset):
            allowed_extensions = self.allowed_extensions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_extensions is not UNSET:
            field_dict["allowedExtensions"] = allowed_extensions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allowed_extensions = cast(List[str], d.pop("allowedExtensions", UNSET))

        add_column_file_config_file = cls(
            allowed_extensions=allowed_extensions,
        )

        add_column_file_config_file.additional_properties = d
        return add_column_file_config_file

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
