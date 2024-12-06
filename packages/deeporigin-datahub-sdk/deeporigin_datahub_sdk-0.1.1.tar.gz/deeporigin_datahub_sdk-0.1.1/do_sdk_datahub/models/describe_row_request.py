from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column_selection import ColumnSelection


T = TypeVar("T", bound="DescribeRowRequest")


@_attrs_define
class DescribeRowRequest:
    """
    Attributes:
        row_id (str):
        fields (Union[Unset, bool]):
        column_selection (Union[Unset, ColumnSelection]): Select columns for inclusion/exclusion.
    """

    row_id: str
    fields: Union[Unset, bool] = UNSET
    column_selection: Union[Unset, "ColumnSelection"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        row_id = self.row_id

        fields = self.fields

        column_selection: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.column_selection, Unset):
            column_selection = self.column_selection.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rowId": row_id,
            }
        )
        if fields is not UNSET:
            field_dict["fields"] = fields
        if column_selection is not UNSET:
            field_dict["columnSelection"] = column_selection

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column_selection import ColumnSelection

        d = src_dict.copy()
        row_id = d.pop("rowId")

        fields = d.pop("fields", UNSET)

        _column_selection = d.pop("columnSelection", UNSET)
        column_selection: Union[Unset, ColumnSelection]
        if isinstance(_column_selection, Unset):
            column_selection = UNSET
        else:
            column_selection = ColumnSelection.from_dict(_column_selection)

        describe_row_request = cls(
            row_id=row_id,
            fields=fields,
            column_selection=column_selection,
        )

        describe_row_request.additional_properties = d
        return describe_row_request

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
