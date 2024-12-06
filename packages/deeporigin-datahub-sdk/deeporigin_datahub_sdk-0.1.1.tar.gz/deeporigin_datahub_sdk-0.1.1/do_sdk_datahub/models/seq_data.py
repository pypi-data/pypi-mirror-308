from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.seq_data_type import SeqDataType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.seq_annotation import SeqAnnotation


T = TypeVar("T", bound="SeqData")


@_attrs_define
class SeqData:
    """
    Attributes:
        seq (str):
        annotations (Union[Unset, List['SeqAnnotation']]):
        name (Union[Unset, str]):
        type (Union[Unset, SeqDataType]):
    """

    seq: str
    annotations: Union[Unset, List["SeqAnnotation"]] = UNSET
    name: Union[Unset, str] = UNSET
    type: Union[Unset, SeqDataType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        seq = self.seq

        annotations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()
                annotations.append(annotations_item)

        name = self.name

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seq": seq,
            }
        )
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.seq_annotation import SeqAnnotation

        d = src_dict.copy()
        seq = d.pop("seq")

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = SeqAnnotation.from_dict(annotations_item_data)

            annotations.append(annotations_item)

        name = d.pop("name", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, SeqDataType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = SeqDataType(_type)

        seq_data = cls(
            seq=seq,
            annotations=annotations,
            name=name,
            type=type,
        )

        seq_data.additional_properties = d
        return seq_data

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
