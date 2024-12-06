from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.configure_column_select_options_body_option_configuration_item import (
        ConfigureColumnSelectOptionsBodyOptionConfigurationItem,
    )


T = TypeVar("T", bound="ConfigureColumnSelectOptionsBody")


@_attrs_define
class ConfigureColumnSelectOptionsBody:
    """
    Attributes:
        database_id (str):
        column_id (str):
        option_configuration (List['ConfigureColumnSelectOptionsBodyOptionConfigurationItem']):
    """

    database_id: str
    column_id: str
    option_configuration: List["ConfigureColumnSelectOptionsBodyOptionConfigurationItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database_id = self.database_id

        column_id = self.column_id

        option_configuration = []
        for option_configuration_item_data in self.option_configuration:
            option_configuration_item = option_configuration_item_data.to_dict()
            option_configuration.append(option_configuration_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "databaseId": database_id,
                "columnId": column_id,
                "optionConfiguration": option_configuration,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.configure_column_select_options_body_option_configuration_item import (
            ConfigureColumnSelectOptionsBodyOptionConfigurationItem,
        )

        d = src_dict.copy()
        database_id = d.pop("databaseId")

        column_id = d.pop("columnId")

        option_configuration = []
        _option_configuration = d.pop("optionConfiguration")
        for option_configuration_item_data in _option_configuration:
            option_configuration_item = ConfigureColumnSelectOptionsBodyOptionConfigurationItem.from_dict(
                option_configuration_item_data
            )

            option_configuration.append(option_configuration_item)

        configure_column_select_options_body = cls(
            database_id=database_id,
            column_id=column_id,
            option_configuration=option_configuration,
        )

        configure_column_select_options_body.additional_properties = d
        return configure_column_select_options_body

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
