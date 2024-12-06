from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ensure_rows_body_rows_item_cells_item import EnsureRowsBodyRowsItemCellsItem
    from ..models.ensure_rows_body_rows_item_row import EnsureRowsBodyRowsItemRow


T = TypeVar("T", bound="EnsureRowsBodyRowsItem")


@_attrs_define
class EnsureRowsBodyRowsItem:
    """
    Attributes:
        row_id (Union[Unset, str]):
        row (Union[Unset, EnsureRowsBodyRowsItemRow]):
        cells (Union[Unset, List['EnsureRowsBodyRowsItemCellsItem']]):
    """

    row_id: Union[Unset, str] = UNSET
    row: Union[Unset, "EnsureRowsBodyRowsItemRow"] = UNSET
    cells: Union[Unset, List["EnsureRowsBodyRowsItemCellsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        row_id = self.row_id

        row: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.row, Unset):
            row = self.row.to_dict()

        cells: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.cells, Unset):
            cells = []
            for cells_item_data in self.cells:
                cells_item = cells_item_data.to_dict()
                cells.append(cells_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if row_id is not UNSET:
            field_dict["rowId"] = row_id
        if row is not UNSET:
            field_dict["row"] = row
        if cells is not UNSET:
            field_dict["cells"] = cells

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ensure_rows_body_rows_item_cells_item import EnsureRowsBodyRowsItemCellsItem
        from ..models.ensure_rows_body_rows_item_row import EnsureRowsBodyRowsItemRow

        d = src_dict.copy()
        row_id = d.pop("rowId", UNSET)

        _row = d.pop("row", UNSET)
        row: Union[Unset, EnsureRowsBodyRowsItemRow]
        if isinstance(_row, Unset):
            row = UNSET
        else:
            row = EnsureRowsBodyRowsItemRow.from_dict(_row)

        cells = []
        _cells = d.pop("cells", UNSET)
        for cells_item_data in _cells or []:
            cells_item = EnsureRowsBodyRowsItemCellsItem.from_dict(cells_item_data)

            cells.append(cells_item)

        ensure_rows_body_rows_item = cls(
            row_id=row_id,
            row=row,
            cells=cells,
        )

        ensure_rows_body_rows_item.additional_properties = d
        return ensure_rows_body_rows_item

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
