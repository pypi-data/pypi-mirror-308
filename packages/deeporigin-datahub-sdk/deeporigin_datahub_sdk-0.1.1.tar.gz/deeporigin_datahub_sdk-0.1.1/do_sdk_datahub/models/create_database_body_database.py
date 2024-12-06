from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDatabaseBodyDatabase")


@_attrs_define
class CreateDatabaseBodyDatabase:
    """
    Attributes:
        hid (str):
        name (str):
        hid_prefix (str):
        parent_id (Union[None, Unset, str]):
        is_inline_database (Union[Unset, bool]):
        cols (Union[Unset, List[Any]]):
    """

    hid: str
    name: str
    hid_prefix: str
    parent_id: Union[None, Unset, str] = UNSET
    is_inline_database: Union[Unset, bool] = UNSET
    cols: Union[Unset, List[Any]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hid = self.hid

        name = self.name

        hid_prefix = self.hid_prefix

        parent_id: Union[None, Unset, str]
        if isinstance(self.parent_id, Unset):
            parent_id = UNSET
        else:
            parent_id = self.parent_id

        is_inline_database = self.is_inline_database

        cols: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.cols, Unset):
            cols = self.cols

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hid": hid,
                "name": name,
                "hidPrefix": hid_prefix,
            }
        )
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if is_inline_database is not UNSET:
            field_dict["isInlineDatabase"] = is_inline_database
        if cols is not UNSET:
            field_dict["cols"] = cols

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hid = d.pop("hid")

        name = d.pop("name")

        hid_prefix = d.pop("hidPrefix")

        def _parse_parent_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_id = _parse_parent_id(d.pop("parentId", UNSET))

        is_inline_database = d.pop("isInlineDatabase", UNSET)

        cols = cast(List[Any], d.pop("cols", UNSET))

        create_database_body_database = cls(
            hid=hid,
            name=name,
            hid_prefix=hid_prefix,
            parent_id=parent_id,
            is_inline_database=is_inline_database,
            cols=cols,
        )

        create_database_body_database.additional_properties = d
        return create_database_body_database

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
