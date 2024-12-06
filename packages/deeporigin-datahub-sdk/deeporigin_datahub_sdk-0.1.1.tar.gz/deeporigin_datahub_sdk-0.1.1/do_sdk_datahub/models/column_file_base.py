from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column_file_base_config_file import ColumnFileBaseConfigFile


T = TypeVar("T", bound="ColumnFileBase")


@_attrs_define
class ColumnFileBase:
    """
    Attributes:
        type (Literal['file']):
        config_file (Union[Unset, ColumnFileBaseConfigFile]):
    """

    type: Literal["file"]
    config_file: Union[Unset, "ColumnFileBaseConfigFile"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        config_file: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config_file, Unset):
            config_file = self.config_file.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if config_file is not UNSET:
            field_dict["configFile"] = config_file

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column_file_base_config_file import ColumnFileBaseConfigFile

        d = src_dict.copy()
        type = d.pop("type")

        _config_file = d.pop("configFile", UNSET)
        config_file: Union[Unset, ColumnFileBaseConfigFile]
        if isinstance(_config_file, Unset):
            config_file = UNSET
        else:
            config_file = ColumnFileBaseConfigFile.from_dict(_config_file)

        column_file_base = cls(
            type=type,
            config_file=config_file,
        )

        column_file_base.additional_properties = d
        return column_file_base

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
