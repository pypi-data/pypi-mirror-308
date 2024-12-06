from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ensure_rows_body_rows_item import EnsureRowsBodyRowsItem


T = TypeVar("T", bound="EnsureRowsBody")


@_attrs_define
class EnsureRowsBody:
    """
    Attributes:
        database_id (str):
        rows (List['EnsureRowsBodyRowsItem']):
        check_previous_value (Union[Unset, bool]):
    """

    database_id: str
    rows: List["EnsureRowsBodyRowsItem"]
    check_previous_value: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        database_id = self.database_id

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()
            rows.append(rows_item)

        check_previous_value = self.check_previous_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "databaseId": database_id,
                "rows": rows,
            }
        )
        if check_previous_value is not UNSET:
            field_dict["checkPreviousValue"] = check_previous_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ensure_rows_body_rows_item import EnsureRowsBodyRowsItem

        d = src_dict.copy()
        database_id = d.pop("databaseId")

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = EnsureRowsBodyRowsItem.from_dict(rows_item_data)

            rows.append(rows_item)

        check_previous_value = d.pop("checkPreviousValue", UNSET)

        ensure_rows_body = cls(
            database_id=database_id,
            rows=rows,
            check_previous_value=check_previous_value,
        )

        ensure_rows_body.additional_properties = d
        return ensure_rows_body

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
