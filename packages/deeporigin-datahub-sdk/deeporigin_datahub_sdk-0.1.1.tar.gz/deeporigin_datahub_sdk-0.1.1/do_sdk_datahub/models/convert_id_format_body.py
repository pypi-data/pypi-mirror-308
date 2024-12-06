from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.convert_id_format_body_conversions_item_type_0 import ConvertIdFormatBodyConversionsItemType0
    from ..models.convert_id_format_body_conversions_item_type_1 import ConvertIdFormatBodyConversionsItemType1


T = TypeVar("T", bound="ConvertIdFormatBody")


@_attrs_define
class ConvertIdFormatBody:
    """
    Attributes:
        conversions (List[Union['ConvertIdFormatBodyConversionsItemType0', 'ConvertIdFormatBodyConversionsItemType1']]):
    """

    conversions: List[Union["ConvertIdFormatBodyConversionsItemType0", "ConvertIdFormatBodyConversionsItemType1"]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.convert_id_format_body_conversions_item_type_0 import ConvertIdFormatBodyConversionsItemType0

        conversions = []
        for conversions_item_data in self.conversions:
            conversions_item: Dict[str, Any]
            if isinstance(conversions_item_data, ConvertIdFormatBodyConversionsItemType0):
                conversions_item = conversions_item_data.to_dict()
            else:
                conversions_item = conversions_item_data.to_dict()

            conversions.append(conversions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conversions": conversions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.convert_id_format_body_conversions_item_type_0 import ConvertIdFormatBodyConversionsItemType0
        from ..models.convert_id_format_body_conversions_item_type_1 import ConvertIdFormatBodyConversionsItemType1

        d = src_dict.copy()
        conversions = []
        _conversions = d.pop("conversions")
        for conversions_item_data in _conversions:

            def _parse_conversions_item(
                data: object,
            ) -> Union["ConvertIdFormatBodyConversionsItemType0", "ConvertIdFormatBodyConversionsItemType1"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conversions_item_type_0 = ConvertIdFormatBodyConversionsItemType0.from_dict(data)

                    return conversions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                conversions_item_type_1 = ConvertIdFormatBodyConversionsItemType1.from_dict(data)

                return conversions_item_type_1

            conversions_item = _parse_conversions_item(conversions_item_data)

            conversions.append(conversions_item)

        convert_id_format_body = cls(
            conversions=conversions,
        )

        convert_id_format_body.additional_properties = d
        return convert_id_format_body

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
