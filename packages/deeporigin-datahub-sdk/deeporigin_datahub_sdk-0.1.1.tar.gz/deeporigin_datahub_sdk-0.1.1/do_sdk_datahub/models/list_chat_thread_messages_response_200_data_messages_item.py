from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_chat_thread_messages_response_200_data_messages_item_role import (
    ListChatThreadMessagesResponse200DataMessagesItemRole,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_0 import (
        ListChatThreadMessagesResponse200DataMessagesItemContentItemType0,
    )
    from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_1 import (
        ListChatThreadMessagesResponse200DataMessagesItemContentItemType1,
    )
    from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_2 import (
        ListChatThreadMessagesResponse200DataMessagesItemContentItemType2,
    )
    from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_3 import (
        ListChatThreadMessagesResponse200DataMessagesItemContentItemType3,
    )


T = TypeVar("T", bound="ListChatThreadMessagesResponse200DataMessagesItem")


@_attrs_define
class ListChatThreadMessagesResponse200DataMessagesItem:
    """
    Attributes:
        id (str): Deep Origin system ID.
        role (ListChatThreadMessagesResponse200DataMessagesItemRole):
        content (Union[Unset, List[Union['ListChatThreadMessagesResponse200DataMessagesItemContentItemType0',
            'ListChatThreadMessagesResponse200DataMessagesItemContentItemType1',
            'ListChatThreadMessagesResponse200DataMessagesItemContentItemType2',
            'ListChatThreadMessagesResponse200DataMessagesItemContentItemType3']]]):
    """

    id: str
    role: ListChatThreadMessagesResponse200DataMessagesItemRole
    content: Union[
        Unset,
        List[
            Union[
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType0",
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType1",
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType2",
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType3",
            ]
        ],
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_0 import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType0,
        )
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_1 import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType1,
        )
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_2 import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType2,
        )

        id = self.id

        role = self.role.value

        content: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item: Dict[str, Any]
                if isinstance(content_item_data, ListChatThreadMessagesResponse200DataMessagesItemContentItemType0):
                    content_item = content_item_data.to_dict()
                elif isinstance(content_item_data, ListChatThreadMessagesResponse200DataMessagesItemContentItemType1):
                    content_item = content_item_data.to_dict()
                elif isinstance(content_item_data, ListChatThreadMessagesResponse200DataMessagesItemContentItemType2):
                    content_item = content_item_data.to_dict()
                else:
                    content_item = content_item_data.to_dict()

                content.append(content_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "role": role,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_0 import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType0,
        )
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_1 import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType1,
        )
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_2 import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType2,
        )
        from ..models.list_chat_thread_messages_response_200_data_messages_item_content_item_type_3 import (
            ListChatThreadMessagesResponse200DataMessagesItemContentItemType3,
        )

        d = src_dict.copy()
        id = d.pop("id")

        role = ListChatThreadMessagesResponse200DataMessagesItemRole(d.pop("role"))

        content = []
        _content = d.pop("content", UNSET)
        for content_item_data in _content or []:

            def _parse_content_item(
                data: object,
            ) -> Union[
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType0",
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType1",
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType2",
                "ListChatThreadMessagesResponse200DataMessagesItemContentItemType3",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    content_item_type_0 = ListChatThreadMessagesResponse200DataMessagesItemContentItemType0.from_dict(
                        data
                    )

                    return content_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    content_item_type_1 = ListChatThreadMessagesResponse200DataMessagesItemContentItemType1.from_dict(
                        data
                    )

                    return content_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    content_item_type_2 = ListChatThreadMessagesResponse200DataMessagesItemContentItemType2.from_dict(
                        data
                    )

                    return content_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                content_item_type_3 = ListChatThreadMessagesResponse200DataMessagesItemContentItemType3.from_dict(data)

                return content_item_type_3

            content_item = _parse_content_item(content_item_data)

            content.append(content_item)

        list_chat_thread_messages_response_200_data_messages_item = cls(
            id=id,
            role=role,
            content=content,
        )

        list_chat_thread_messages_response_200_data_messages_item.additional_properties = d
        return list_chat_thread_messages_response_200_data_messages_item

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
