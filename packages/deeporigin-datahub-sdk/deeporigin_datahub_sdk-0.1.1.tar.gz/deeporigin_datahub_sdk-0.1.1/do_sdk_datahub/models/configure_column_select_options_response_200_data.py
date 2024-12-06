from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.configure_column_select_options_response_200_data_config_select import (
        ConfigureColumnSelectOptionsResponse200DataConfigSelect,
    )


T = TypeVar("T", bound="ConfigureColumnSelectOptionsResponse200Data")


@_attrs_define
class ConfigureColumnSelectOptionsResponse200Data:
    """
    Attributes:
        id (str):
        config_select (ConfigureColumnSelectOptionsResponse200DataConfigSelect):
    """

    id: str
    config_select: "ConfigureColumnSelectOptionsResponse200DataConfigSelect"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        config_select = self.config_select.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "configSelect": config_select,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configure_column_select_options_response_200_data_config_select import (
            ConfigureColumnSelectOptionsResponse200DataConfigSelect,
        )

        d = src_dict.copy()
        id = d.pop("id")

        config_select = ConfigureColumnSelectOptionsResponse200DataConfigSelect.from_dict(d.pop("configSelect"))

        configure_column_select_options_response_200_data = cls(
            id=id,
            config_select=config_select,
        )

        configure_column_select_options_response_200_data.additional_properties = d
        return configure_column_select_options_response_200_data

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
