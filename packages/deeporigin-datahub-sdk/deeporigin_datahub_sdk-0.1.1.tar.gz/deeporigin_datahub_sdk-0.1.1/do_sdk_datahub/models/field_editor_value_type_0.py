from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FieldEditorValueType0")


@_attrs_define
class FieldEditorValueType0:
    """
    Attributes:
        top_level_blocks (List[Any]):
    """

    top_level_blocks: List[Any]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        top_level_blocks = self.top_level_blocks

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topLevelBlocks": top_level_blocks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        top_level_blocks = cast(List[Any], d.pop("topLevelBlocks"))

        field_editor_value_type_0 = cls(
            top_level_blocks=top_level_blocks,
        )

        field_editor_value_type_0.additional_properties = d
        return field_editor_value_type_0

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
