from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_2_image_url import (
        ListChatThreadMessagesResponse200DataMessagesItemContentItemType2ImageUrl,
    )


T = TypeVar("T", bound="ListChatThreadMessagesResponse200DataMessagesItemContentItemType2")


@_attrs_define
class ListChatThreadMessagesResponse200DataMessagesItemContentItemType2:
    """
    Attributes:
        type (Literal['image_url']):
        image_url (ListChatThreadMessagesResponse200DataMessagesItemContentItemType2ImageUrl):
    """

    type: Literal["image_url"]
    image_url: "ListChatThreadMessagesResponse200DataMessagesItemContentItemType2ImageUrl"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        image_url = self.image_url.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "image_url": image_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_2_image_url import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType2ImageUrl,
        )

        d = src_dict.copy()
        type = d.pop("type")

        image_url = ListChatThreadMessagesResponse200DataMessagesItemContentItemType2ImageUrl.from_dict(
            d.pop("image_url")
        )

        list_chat_thread_messages_response_200_data_messages_item_content_item_type_2 = cls(
            type=type,
            image_url=image_url,
        )

        list_chat_thread_messages_response_200_data_messages_item_content_item_type_2.additional_properties = d
        return list_chat_thread_messages_response_200_data_messages_item_content_item_type_2

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
