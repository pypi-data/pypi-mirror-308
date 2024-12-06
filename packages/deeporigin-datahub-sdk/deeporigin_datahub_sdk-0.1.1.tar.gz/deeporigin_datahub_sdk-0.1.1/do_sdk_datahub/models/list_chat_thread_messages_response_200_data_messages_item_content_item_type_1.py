from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_1_image_file import (
        ListChatThreadMessagesResponse200DataMessagesItemContentItemType1ImageFile,
    )


T = TypeVar("T", bound="ListChatThreadMessagesResponse200DataMessagesItemContentItemType1")


@_attrs_define
class ListChatThreadMessagesResponse200DataMessagesItemContentItemType1:
    """
    Attributes:
        type (Literal['image_file']):
        image_file (ListChatThreadMessagesResponse200DataMessagesItemContentItemType1ImageFile):
    """

    type: Literal["image_file"]
    image_file: "ListChatThreadMessagesResponse200DataMessagesItemContentItemType1ImageFile"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        image_file = self.image_file.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "image_file": image_file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_1_image_file import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType1ImageFile,
        )

        d = src_dict.copy()
        type = d.pop("type")

        image_file = ListChatThreadMessagesResponse200DataMessagesItemContentItemType1ImageFile.from_dict(
            d.pop("image_file")
        )

        list_chat_thread_messages_response_200_data_messages_item_content_item_type_1 = cls(
            type=type,
            image_file=image_file,
        )

        list_chat_thread_messages_response_200_data_messages_item_content_item_type_1.additional_properties = d
        return list_chat_thread_messages_response_200_data_messages_item_content_item_type_1

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
