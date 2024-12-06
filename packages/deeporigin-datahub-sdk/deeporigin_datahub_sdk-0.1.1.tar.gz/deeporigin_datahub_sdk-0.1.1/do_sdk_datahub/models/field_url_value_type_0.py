from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.field_url_value_type_0_urls_item import FieldUrlValueType0UrlsItem


T = TypeVar("T", bound="FieldUrlValueType0")


@_attrs_define
class FieldUrlValueType0:
    """
    Attributes:
        urls (List['FieldUrlValueType0UrlsItem']):
    """

    urls: List["FieldUrlValueType0UrlsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        urls = []
        for urls_item_data in self.urls:
            urls_item = urls_item_data.to_dict()
            urls.append(urls_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "urls": urls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.field_url_value_type_0_urls_item import FieldUrlValueType0UrlsItem

        d = src_dict.copy()
        urls = []
        _urls = d.pop("urls")
        for urls_item_data in _urls:
            urls_item = FieldUrlValueType0UrlsItem.from_dict(urls_item_data)

            urls.append(urls_item)

        field_url_value_type_0 = cls(
            urls=urls,
        )

        field_url_value_type_0.additional_properties = d
        return field_url_value_type_0

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
