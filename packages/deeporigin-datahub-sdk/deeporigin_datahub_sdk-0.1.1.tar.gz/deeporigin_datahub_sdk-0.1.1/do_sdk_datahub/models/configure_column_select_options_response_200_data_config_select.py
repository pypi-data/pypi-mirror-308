from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConfigureColumnSelectOptionsResponse200DataConfigSelect")


@_attrs_define
class ConfigureColumnSelectOptionsResponse200DataConfigSelect:
    """
    Attributes:
        options (List[str]):
        can_create (Union[Unset, bool]):
    """

    options: List[str]
    can_create: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        options = self.options

        can_create = self.can_create

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "options": options,
            }
        )
        if can_create is not UNSET:
            field_dict["canCreate"] = can_create

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        options = cast(List[str], d.pop("options"))

        can_create = d.pop("canCreate", UNSET)

        configure_column_select_options_response_200_data_config_select = cls(
            options=options,
            can_create=can_create,
        )

        configure_column_select_options_response_200_data_config_select.additional_properties = d
        return configure_column_select_options_response_200_data_config_select

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
