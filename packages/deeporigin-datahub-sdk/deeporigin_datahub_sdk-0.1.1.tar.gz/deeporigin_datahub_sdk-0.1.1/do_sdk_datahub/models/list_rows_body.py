from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_rows_body_filters_item_type_0 import ListRowsBodyFiltersItemType0
    from ..models.list_rows_body_filters_item_type_1 import ListRowsBodyFiltersItemType1
    from ..models.list_rows_body_filters_item_type_2 import ListRowsBodyFiltersItemType2


T = TypeVar("T", bound="ListRowsBody")


@_attrs_define
class ListRowsBody:
    """
    Attributes:
        filters (List[Union['ListRowsBodyFiltersItemType0', 'ListRowsBodyFiltersItemType1',
            'ListRowsBodyFiltersItemType2']]):
    """

    filters: List[Union["ListRowsBodyFiltersItemType0", "ListRowsBodyFiltersItemType1", "ListRowsBodyFiltersItemType2"]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_rows_body_filters_item_type_0 import ListRowsBodyFiltersItemType0
        from ..models.list_rows_body_filters_item_type_1 import ListRowsBodyFiltersItemType1

        filters = []
        for filters_item_data in self.filters:
            filters_item: Dict[str, Any]
            if isinstance(filters_item_data, ListRowsBodyFiltersItemType0):
                filters_item = filters_item_data.to_dict()
            elif isinstance(filters_item_data, ListRowsBodyFiltersItemType1):
                filters_item = filters_item_data.to_dict()
            else:
                filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filters": filters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_rows_body_filters_item_type_0 import ListRowsBodyFiltersItemType0
        from ..models.list_rows_body_filters_item_type_1 import ListRowsBodyFiltersItemType1
        from ..models.list_rows_body_filters_item_type_2 import ListRowsBodyFiltersItemType2

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:

            def _parse_filters_item(
                data: object,
            ) -> Union["ListRowsBodyFiltersItemType0", "ListRowsBodyFiltersItemType1", "ListRowsBodyFiltersItemType2"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_0 = ListRowsBodyFiltersItemType0.from_dict(data)

                    return filters_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_1 = ListRowsBodyFiltersItemType1.from_dict(data)

                    return filters_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                filters_item_type_2 = ListRowsBodyFiltersItemType2.from_dict(data)

                return filters_item_type_2

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        list_rows_body = cls(
            filters=filters,
        )

        list_rows_body.additional_properties = d
        return list_rows_body

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
