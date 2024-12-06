from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_mentions_response_200_data_mentions_item import ListMentionsResponse200DataMentionsItem


T = TypeVar("T", bound="ListMentionsResponse200Data")


@_attrs_define
class ListMentionsResponse200Data:
    """
    Attributes:
        mentions (List['ListMentionsResponse200DataMentionsItem']):
    """

    mentions: List["ListMentionsResponse200DataMentionsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mentions = []
        for mentions_item_data in self.mentions:
            mentions_item = mentions_item_data.to_dict()
            mentions.append(mentions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mentions": mentions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_mentions_response_200_data_mentions_item import ListMentionsResponse200DataMentionsItem

        d = src_dict.copy()
        mentions = []
        _mentions = d.pop("mentions")
        for mentions_item_data in _mentions:
            mentions_item = ListMentionsResponse200DataMentionsItem.from_dict(mentions_item_data)

            mentions.append(mentions_item)

        list_mentions_response_200_data = cls(
            mentions=mentions,
        )

        list_mentions_response_200_data.additional_properties = d
        return list_mentions_response_200_data

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
