from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeqAnnotation")


@_attrs_define
class SeqAnnotation:
    """
    Attributes:
        end (float):
        name (str):
        start (float):
        color (Union[Unset, str]):
        direction (Union[Literal[-1], Literal[0], Literal[1], Unset]):
        type (Union[Unset, str]):
    """

    end: float
    name: str
    start: float
    color: Union[Unset, str] = UNSET
    direction: Union[Literal[-1], Literal[0], Literal[1], Unset] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        end = self.end

        name = self.name

        start = self.start

        color = self.color

        direction: Union[Literal[-1], Literal[0], Literal[1], Unset]
        if isinstance(self.direction, Unset):
            direction = UNSET
        else:
            direction = self.direction

        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "end": end,
                "name": name,
                "start": start,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if direction is not UNSET:
            field_dict["direction"] = direction
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        end = d.pop("end")

        name = d.pop("name")

        start = d.pop("start")

        color = d.pop("color", UNSET)

        def _parse_direction(data: object) -> Union[Literal[-1], Literal[0], Literal[1], Unset]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Literal[-1], Literal[0], Literal[1], Unset], data)

        direction = _parse_direction(d.pop("direction", UNSET))

        type = d.pop("type", UNSET)

        seq_annotation = cls(
            end=end,
            name=name,
            start=start,
            color=color,
            direction=direction,
            type=type,
        )

        seq_annotation.additional_properties = d
        return seq_annotation

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
