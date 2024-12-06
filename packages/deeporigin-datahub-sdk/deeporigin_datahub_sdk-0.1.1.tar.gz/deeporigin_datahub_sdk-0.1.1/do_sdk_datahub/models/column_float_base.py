from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column_float_base_config_numeric import ColumnFloatBaseConfigNumeric


T = TypeVar("T", bound="ColumnFloatBase")


@_attrs_define
class ColumnFloatBase:
    """
    Attributes:
        type (Literal['float']):
        config_numeric (Union[Unset, ColumnFloatBaseConfigNumeric]):
    """

    type: Literal["float"]
    config_numeric: Union[Unset, "ColumnFloatBaseConfigNumeric"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        config_numeric: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config_numeric, Unset):
            config_numeric = self.config_numeric.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if config_numeric is not UNSET:
            field_dict["configNumeric"] = config_numeric

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column_float_base_config_numeric import ColumnFloatBaseConfigNumeric

        d = src_dict.copy()
        type = d.pop("type")

        _config_numeric = d.pop("configNumeric", UNSET)
        config_numeric: Union[Unset, ColumnFloatBaseConfigNumeric]
        if isinstance(_config_numeric, Unset):
            config_numeric = UNSET
        else:
            config_numeric = ColumnFloatBaseConfigNumeric.from_dict(_config_numeric)

        column_float_base = cls(
            type=type,
            config_numeric=config_numeric,
        )

        column_float_base.additional_properties = d
        return column_float_base

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
