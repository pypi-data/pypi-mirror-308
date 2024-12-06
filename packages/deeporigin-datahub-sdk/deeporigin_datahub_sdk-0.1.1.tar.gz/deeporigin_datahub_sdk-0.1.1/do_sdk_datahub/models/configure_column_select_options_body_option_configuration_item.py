from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.configure_column_select_options_body_option_configuration_item_op import (
    ConfigureColumnSelectOptionsBodyOptionConfigurationItemOp,
)

T = TypeVar("T", bound="ConfigureColumnSelectOptionsBodyOptionConfigurationItem")


@_attrs_define
class ConfigureColumnSelectOptionsBodyOptionConfigurationItem:
    """
    Attributes:
        option (str):
        op (ConfigureColumnSelectOptionsBodyOptionConfigurationItemOp):
    """

    option: str
    op: ConfigureColumnSelectOptionsBodyOptionConfigurationItemOp
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        option = self.option

        op = self.op.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "option": option,
                "op": op,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        option = d.pop("option")

        op = ConfigureColumnSelectOptionsBodyOptionConfigurationItemOp(d.pop("op"))

        configure_column_select_options_body_option_configuration_item = cls(
            option=option,
            op=op,
        )

        configure_column_select_options_body_option_configuration_item.additional_properties = d
        return configure_column_select_options_body_option_configuration_item

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
