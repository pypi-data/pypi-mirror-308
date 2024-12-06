from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.row_filter_join_join_type import RowFilterJoinJoinType

if TYPE_CHECKING:
    from ..models.row_filter_boolean import RowFilterBoolean
    from ..models.row_filter_nullity import RowFilterNullity
    from ..models.row_filter_number import RowFilterNumber
    from ..models.row_filter_set import RowFilterSet
    from ..models.row_filter_substructure import RowFilterSubstructure
    from ..models.row_filter_text import RowFilterText


T = TypeVar("T", bound="RowFilterJoin")


@_attrs_define
class RowFilterJoin:
    """
    Attributes:
        filter_type (Literal['join']):
        join_type (RowFilterJoinJoinType):
        conditions (List[Union['RowFilterBoolean', 'RowFilterJoin', 'RowFilterNullity', 'RowFilterNumber',
            'RowFilterSet', 'RowFilterSubstructure', 'RowFilterText']]):
    """

    filter_type: Literal["join"]
    join_type: RowFilterJoinJoinType
    conditions: List[
        Union[
            "RowFilterBoolean",
            "RowFilterJoin",
            "RowFilterNullity",
            "RowFilterNumber",
            "RowFilterSet",
            "RowFilterSubstructure",
            "RowFilterText",
        ]
    ]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.row_filter_boolean import RowFilterBoolean
        from ..models.row_filter_nullity import RowFilterNullity
        from ..models.row_filter_number import RowFilterNumber
        from ..models.row_filter_set import RowFilterSet
        from ..models.row_filter_substructure import RowFilterSubstructure
        from ..models.row_filter_text import RowFilterText

        filter_type = self.filter_type

        join_type = self.join_type.value

        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item: Dict[str, Any]
            if isinstance(conditions_item_data, RowFilterText):
                conditions_item = conditions_item_data.to_dict()
            elif isinstance(conditions_item_data, RowFilterNumber):
                conditions_item = conditions_item_data.to_dict()
            elif isinstance(conditions_item_data, RowFilterBoolean):
                conditions_item = conditions_item_data.to_dict()
            elif isinstance(conditions_item_data, RowFilterNullity):
                conditions_item = conditions_item_data.to_dict()
            elif isinstance(conditions_item_data, RowFilterSet):
                conditions_item = conditions_item_data.to_dict()
            elif isinstance(conditions_item_data, RowFilterSubstructure):
                conditions_item = conditions_item_data.to_dict()
            else:
                conditions_item = conditions_item_data.to_dict()

            conditions.append(conditions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filterType": filter_type,
                "joinType": join_type,
                "conditions": conditions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.row_filter_boolean import RowFilterBoolean
        from ..models.row_filter_nullity import RowFilterNullity
        from ..models.row_filter_number import RowFilterNumber
        from ..models.row_filter_set import RowFilterSet
        from ..models.row_filter_substructure import RowFilterSubstructure
        from ..models.row_filter_text import RowFilterText

        d = src_dict.copy()
        filter_type = d.pop("filterType")

        join_type = RowFilterJoinJoinType(d.pop("joinType"))

        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:

            def _parse_conditions_item(
                data: object,
            ) -> Union[
                "RowFilterBoolean",
                "RowFilterJoin",
                "RowFilterNullity",
                "RowFilterNumber",
                "RowFilterSet",
                "RowFilterSubstructure",
                "RowFilterText",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_0_type_0 = RowFilterText.from_dict(data)

                    return conditions_item_type_0_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_0_type_1 = RowFilterNumber.from_dict(data)

                    return conditions_item_type_0_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_0_type_2 = RowFilterBoolean.from_dict(data)

                    return conditions_item_type_0_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_0_type_3 = RowFilterNullity.from_dict(data)

                    return conditions_item_type_0_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_1 = RowFilterSet.from_dict(data)

                    return conditions_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_2 = RowFilterSubstructure.from_dict(data)

                    return conditions_item_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                conditions_item_type_3 = RowFilterJoin.from_dict(data)

                return conditions_item_type_3

            conditions_item = _parse_conditions_item(conditions_item_data)

            conditions.append(conditions_item)

        row_filter_join = cls(
            filter_type=filter_type,
            join_type=join_type,
            conditions=conditions,
        )

        row_filter_join.additional_properties = d
        return row_filter_join

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
