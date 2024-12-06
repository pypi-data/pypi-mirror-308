from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ColumnSelection")


@_attrs_define
class ColumnSelection:
    """Select columns for inclusion/exclusion.

    Attributes:
        include (Union[Unset, List[str]]):
        exclude (Union[Unset, List[str]]):
    """

    include: Union[Unset, List[str]] = UNSET
    exclude: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        include: Union[Unset, List[str]] = UNSET
        if not isinstance(self.include, Unset):
            include = self.include

        exclude: Union[Unset, List[str]] = UNSET
        if not isinstance(self.exclude, Unset):
            exclude = self.exclude

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include is not UNSET:
            field_dict["include"] = include
        if exclude is not UNSET:
            field_dict["exclude"] = exclude

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        include = cast(List[str], d.pop("include", UNSET))

        exclude = cast(List[str], d.pop("exclude", UNSET))

        column_selection = cls(
            include=include,
            exclude=exclude,
        )

        column_selection.additional_properties = d
        return column_selection

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
