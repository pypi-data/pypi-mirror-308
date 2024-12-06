from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.convert_id_format_response_200_data_item import ConvertIdFormatResponse200DataItem


T = TypeVar("T", bound="ConvertIdFormatResponse200")


@_attrs_define
class ConvertIdFormatResponse200:
    """
    Attributes:
        data (List['ConvertIdFormatResponse200DataItem']):
    """

    data: List["ConvertIdFormatResponse200DataItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.convert_id_format_response_200_data_item import ConvertIdFormatResponse200DataItem

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ConvertIdFormatResponse200DataItem.from_dict(data_item_data)

            data.append(data_item)

        convert_id_format_response_200 = cls(
            data=data,
        )

        convert_id_format_response_200.additional_properties = d
        return convert_id_format_response_200

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
