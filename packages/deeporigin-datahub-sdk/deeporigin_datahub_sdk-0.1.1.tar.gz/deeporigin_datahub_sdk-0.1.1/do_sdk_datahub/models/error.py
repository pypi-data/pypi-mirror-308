from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_meta import ErrorMeta


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """
    Attributes:
        status (float):
        id (Union[Unset, str]):
        code (Union[Unset, str]):
        title (Union[Unset, str]):
        detail (Union[Unset, str]):
        meta (Union[Unset, ErrorMeta]):
    """

    status: float
    id: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    detail: Union[Unset, str] = UNSET
    meta: Union[Unset, "ErrorMeta"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status

        id = self.id

        code = self.code

        title = self.title

        detail = self.detail

        meta: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if code is not UNSET:
            field_dict["code"] = code
        if title is not UNSET:
            field_dict["title"] = title
        if detail is not UNSET:
            field_dict["detail"] = detail
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error_meta import ErrorMeta

        d = src_dict.copy()
        status = d.pop("status")

        id = d.pop("id", UNSET)

        code = d.pop("code", UNSET)

        title = d.pop("title", UNSET)

        detail = d.pop("detail", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, ErrorMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = ErrorMeta.from_dict(_meta)

        error = cls(
            status=status,
            id=id,
            code=code,
            title=title,
            detail=detail,
            meta=meta,
        )

        error.additional_properties = d
        return error

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
