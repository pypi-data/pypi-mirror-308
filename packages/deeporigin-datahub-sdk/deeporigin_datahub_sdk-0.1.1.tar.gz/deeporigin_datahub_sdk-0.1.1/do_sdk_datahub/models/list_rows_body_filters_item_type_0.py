from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_rows_body_filters_item_type_0_parent_type_0 import ListRowsBodyFiltersItemType0ParentType0
    from ..models.list_rows_body_filters_item_type_0_parent_type_1 import ListRowsBodyFiltersItemType0ParentType1


T = TypeVar("T", bound="ListRowsBodyFiltersItemType0")


@_attrs_define
class ListRowsBodyFiltersItemType0:
    """
    Attributes:
        parent (Union['ListRowsBodyFiltersItemType0ParentType0', 'ListRowsBodyFiltersItemType0ParentType1']):
    """

    parent: Union["ListRowsBodyFiltersItemType0ParentType0", "ListRowsBodyFiltersItemType0ParentType1"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_rows_body_filters_item_type_0_parent_type_0 import ListRowsBodyFiltersItemType0ParentType0

        parent: Dict[str, Any]
        if isinstance(self.parent, ListRowsBodyFiltersItemType0ParentType0):
            parent = self.parent.to_dict()
        else:
            parent = self.parent.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parent": parent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_rows_body_filters_item_type_0_parent_type_0 import ListRowsBodyFiltersItemType0ParentType0
        from ..models.list_rows_body_filters_item_type_0_parent_type_1 import ListRowsBodyFiltersItemType0ParentType1

        d = src_dict.copy()

        def _parse_parent(
            data: object,
        ) -> Union["ListRowsBodyFiltersItemType0ParentType0", "ListRowsBodyFiltersItemType0ParentType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_type_0 = ListRowsBodyFiltersItemType0ParentType0.from_dict(data)

                return parent_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            parent_type_1 = ListRowsBodyFiltersItemType0ParentType1.from_dict(data)

            return parent_type_1

        parent = _parse_parent(d.pop("parent"))

        list_rows_body_filters_item_type_0 = cls(
            parent=parent,
        )

        list_rows_body_filters_item_type_0.additional_properties = d
        return list_rows_body_filters_item_type_0

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
