from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column_selection import ColumnSelection
    from ..models.row_filter_boolean import RowFilterBoolean
    from ..models.row_filter_join import RowFilterJoin
    from ..models.row_filter_nullity import RowFilterNullity
    from ..models.row_filter_number import RowFilterNumber
    from ..models.row_filter_set import RowFilterSet
    from ..models.row_filter_substructure import RowFilterSubstructure
    from ..models.row_filter_text import RowFilterText
    from ..models.row_sort_item import RowSortItem


T = TypeVar("T", bound="ListDatabaseRowsBody")


@_attrs_define
class ListDatabaseRowsBody:
    """
    Attributes:
        database_row_id (str):
        filter_ (Union['RowFilterBoolean', 'RowFilterJoin', 'RowFilterNullity', 'RowFilterNumber', 'RowFilterSet',
            'RowFilterSubstructure', 'RowFilterText', Unset]):
        column_selection (Union[Unset, ColumnSelection]): Select columns for inclusion/exclusion.
        row_sort (Union[Unset, List['RowSortItem']]): Sort rows by column.
        limit (Union[Unset, int]):
        offset (Union[Unset, int]):
    """

    database_row_id: str
    filter_: Union[
        "RowFilterBoolean",
        "RowFilterJoin",
        "RowFilterNullity",
        "RowFilterNumber",
        "RowFilterSet",
        "RowFilterSubstructure",
        "RowFilterText",
        Unset,
    ] = UNSET
    column_selection: Union[Unset, "ColumnSelection"] = UNSET
    row_sort: Union[Unset, List["RowSortItem"]] = UNSET
    limit: Union[Unset, int] = UNSET
    offset: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.row_filter_boolean import RowFilterBoolean
        from ..models.row_filter_nullity import RowFilterNullity
        from ..models.row_filter_number import RowFilterNumber
        from ..models.row_filter_set import RowFilterSet
        from ..models.row_filter_substructure import RowFilterSubstructure
        from ..models.row_filter_text import RowFilterText

        database_row_id = self.database_row_id

        filter_: Union[Dict[str, Any], Unset]
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, RowFilterText):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, RowFilterNumber):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, RowFilterBoolean):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, RowFilterNullity):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, RowFilterSet):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, RowFilterSubstructure):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_.to_dict()

        column_selection: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.column_selection, Unset):
            column_selection = self.column_selection.to_dict()

        row_sort: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.row_sort, Unset):
            row_sort = []
            for componentsschemas_row_sort_item_data in self.row_sort:
                componentsschemas_row_sort_item = componentsschemas_row_sort_item_data.to_dict()
                row_sort.append(componentsschemas_row_sort_item)

        limit = self.limit

        offset = self.offset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "databaseRowId": database_row_id,
            }
        )
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if column_selection is not UNSET:
            field_dict["columnSelection"] = column_selection
        if row_sort is not UNSET:
            field_dict["rowSort"] = row_sort
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column_selection import ColumnSelection
        from ..models.row_filter_boolean import RowFilterBoolean
        from ..models.row_filter_join import RowFilterJoin
        from ..models.row_filter_nullity import RowFilterNullity
        from ..models.row_filter_number import RowFilterNumber
        from ..models.row_filter_set import RowFilterSet
        from ..models.row_filter_substructure import RowFilterSubstructure
        from ..models.row_filter_text import RowFilterText
        from ..models.row_sort_item import RowSortItem

        d = src_dict.copy()
        database_row_id = d.pop("databaseRowId")

        def _parse_filter_(
            data: object,
        ) -> Union[
            "RowFilterBoolean",
            "RowFilterJoin",
            "RowFilterNullity",
            "RowFilterNumber",
            "RowFilterSet",
            "RowFilterSubstructure",
            "RowFilterText",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_filter_type_0_type_0 = RowFilterText.from_dict(data)

                return componentsschemas_row_filter_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_filter_type_0_type_1 = RowFilterNumber.from_dict(data)

                return componentsschemas_row_filter_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_filter_type_0_type_2 = RowFilterBoolean.from_dict(data)

                return componentsschemas_row_filter_type_0_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_filter_type_0_type_3 = RowFilterNullity.from_dict(data)

                return componentsschemas_row_filter_type_0_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_filter_type_1 = RowFilterSet.from_dict(data)

                return componentsschemas_row_filter_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_filter_type_2 = RowFilterSubstructure.from_dict(data)

                return componentsschemas_row_filter_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_row_filter_type_3 = RowFilterJoin.from_dict(data)

            return componentsschemas_row_filter_type_3

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        _column_selection = d.pop("columnSelection", UNSET)
        column_selection: Union[Unset, ColumnSelection]
        if isinstance(_column_selection, Unset):
            column_selection = UNSET
        else:
            column_selection = ColumnSelection.from_dict(_column_selection)

        row_sort = []
        _row_sort = d.pop("rowSort", UNSET)
        for componentsschemas_row_sort_item_data in _row_sort or []:
            componentsschemas_row_sort_item = RowSortItem.from_dict(componentsschemas_row_sort_item_data)

            row_sort.append(componentsschemas_row_sort_item)

        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        list_database_rows_body = cls(
            database_row_id=database_row_id,
            filter_=filter_,
            column_selection=column_selection,
            row_sort=row_sort,
            limit=limit,
            offset=offset,
        )

        list_database_rows_body.additional_properties = d
        return list_database_rows_body

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
