from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatThread")


@_attrs_define
class ChatThread:
    """
    Attributes:
        id (str): Deep Origin system ID.
        openai_id (str):
        created_at (str):
        created_by_user_drn (Union[Unset, str]):
    """

    id: str
    openai_id: str
    created_at: str
    created_by_user_drn: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        openai_id = self.openai_id

        created_at = self.created_at

        created_by_user_drn = self.created_by_user_drn

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "openaiId": openai_id,
                "createdAt": created_at,
            }
        )
        if created_by_user_drn is not UNSET:
            field_dict["createdByUserDrn"] = created_by_user_drn

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        openai_id = d.pop("openaiId")

        created_at = d.pop("createdAt")

        created_by_user_drn = d.pop("createdByUserDrn", UNSET)

        chat_thread = cls(
            id=id,
            openai_id=openai_id,
            created_at=created_at,
            created_by_user_drn=created_by_user_drn,
        )

        chat_thread.additional_properties = d
        return chat_thread

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
