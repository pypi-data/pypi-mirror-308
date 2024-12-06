from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.column_select_base_config_select import ColumnSelectBaseConfigSelect


T = TypeVar("T", bound="ColumnSelectBase")


@_attrs_define
class ColumnSelectBase:
    """
    Attributes:
        type (Literal['select']):
        config_select (ColumnSelectBaseConfigSelect):
    """

    type: Literal["select"]
    config_select: "ColumnSelectBaseConfigSelect"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        config_select = self.config_select.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "configSelect": config_select,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column_select_base_config_select import ColumnSelectBaseConfigSelect

        d = src_dict.copy()
        type = d.pop("type")

        config_select = ColumnSelectBaseConfigSelect.from_dict(d.pop("configSelect"))

        column_select_base = cls(
            type=type,
            config_select=config_select,
        )

        column_select_base.additional_properties = d
        return column_select_base

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
