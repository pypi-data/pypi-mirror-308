from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_column_boolean import AddColumnBoolean
    from ..models.add_column_date import AddColumnDate
    from ..models.add_column_editor import AddColumnEditor
    from ..models.add_column_expression import AddColumnExpression
    from ..models.add_column_file import AddColumnFile
    from ..models.add_column_float import AddColumnFloat
    from ..models.add_column_integer import AddColumnInteger
    from ..models.add_column_lookup import AddColumnLookup
    from ..models.add_column_reference import AddColumnReference
    from ..models.add_column_select import AddColumnSelect
    from ..models.add_column_text import AddColumnText
    from ..models.add_column_url import AddColumnUrl
    from ..models.add_column_user import AddColumnUser


T = TypeVar("T", bound="ImportRowsBody")


@_attrs_define
class ImportRowsBody:
    """
    Attributes:
        database_id (str):
        creation_parent_id (Union[Unset, str]):
        creation_block_id (Union[Unset, str]):
        add_columns (Union[Unset, List[Union['AddColumnBoolean', 'AddColumnDate', 'AddColumnEditor',
            'AddColumnExpression', 'AddColumnFile', 'AddColumnFloat', 'AddColumnInteger', 'AddColumnLookup',
            'AddColumnReference', 'AddColumnSelect', 'AddColumnText', 'AddColumnUrl', 'AddColumnUser']]]): Optionally add
            additional columns to the database during import.
    """

    database_id: str
    creation_parent_id: Union[Unset, str] = UNSET
    creation_block_id: Union[Unset, str] = UNSET
    add_columns: Union[
        Unset,
        List[
            Union[
                "AddColumnBoolean",
                "AddColumnDate",
                "AddColumnEditor",
                "AddColumnExpression",
                "AddColumnFile",
                "AddColumnFloat",
                "AddColumnInteger",
                "AddColumnLookup",
                "AddColumnReference",
                "AddColumnSelect",
                "AddColumnText",
                "AddColumnUrl",
                "AddColumnUser",
            ]
        ],
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.add_column_boolean import AddColumnBoolean
        from ..models.add_column_date import AddColumnDate
        from ..models.add_column_editor import AddColumnEditor
        from ..models.add_column_expression import AddColumnExpression
        from ..models.add_column_file import AddColumnFile
        from ..models.add_column_float import AddColumnFloat
        from ..models.add_column_integer import AddColumnInteger
        from ..models.add_column_lookup import AddColumnLookup
        from ..models.add_column_reference import AddColumnReference
        from ..models.add_column_select import AddColumnSelect
        from ..models.add_column_text import AddColumnText
        from ..models.add_column_url import AddColumnUrl

        database_id = self.database_id

        creation_parent_id = self.creation_parent_id

        creation_block_id = self.creation_block_id

        add_columns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.add_columns, Unset):
            add_columns = []
            for add_columns_item_data in self.add_columns:
                add_columns_item: Dict[str, Any]
                if isinstance(add_columns_item_data, AddColumnLookup):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnBoolean):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnDate):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnEditor):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnExpression):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnFile):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnFloat):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnInteger):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnReference):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnSelect):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnText):
                    add_columns_item = add_columns_item_data.to_dict()
                elif isinstance(add_columns_item_data, AddColumnUrl):
                    add_columns_item = add_columns_item_data.to_dict()
                else:
                    add_columns_item = add_columns_item_data.to_dict()

                add_columns.append(add_columns_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "databaseId": database_id,
            }
        )
        if creation_parent_id is not UNSET:
            field_dict["creationParentId"] = creation_parent_id
        if creation_block_id is not UNSET:
            field_dict["creationBlockId"] = creation_block_id
        if add_columns is not UNSET:
            field_dict["addColumns"] = add_columns

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.add_column_boolean import AddColumnBoolean
        from ..models.add_column_date import AddColumnDate
        from ..models.add_column_editor import AddColumnEditor
        from ..models.add_column_expression import AddColumnExpression
        from ..models.add_column_file import AddColumnFile
        from ..models.add_column_float import AddColumnFloat
        from ..models.add_column_integer import AddColumnInteger
        from ..models.add_column_lookup import AddColumnLookup
        from ..models.add_column_reference import AddColumnReference
        from ..models.add_column_select import AddColumnSelect
        from ..models.add_column_text import AddColumnText
        from ..models.add_column_url import AddColumnUrl
        from ..models.add_column_user import AddColumnUser

        d = src_dict.copy()
        database_id = d.pop("databaseId")

        creation_parent_id = d.pop("creationParentId", UNSET)

        creation_block_id = d.pop("creationBlockId", UNSET)

        add_columns = []
        _add_columns = d.pop("addColumns", UNSET)
        for add_columns_item_data in _add_columns or []:

            def _parse_add_columns_item(
                data: object,
            ) -> Union[
                "AddColumnBoolean",
                "AddColumnDate",
                "AddColumnEditor",
                "AddColumnExpression",
                "AddColumnFile",
                "AddColumnFloat",
                "AddColumnInteger",
                "AddColumnLookup",
                "AddColumnReference",
                "AddColumnSelect",
                "AddColumnText",
                "AddColumnUrl",
                "AddColumnUser",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_0 = AddColumnLookup.from_dict(data)

                    return componentsschemas_add_column_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_1 = AddColumnBoolean.from_dict(data)

                    return componentsschemas_add_column_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_2 = AddColumnDate.from_dict(data)

                    return componentsschemas_add_column_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_3 = AddColumnEditor.from_dict(data)

                    return componentsschemas_add_column_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_4 = AddColumnExpression.from_dict(data)

                    return componentsschemas_add_column_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_5 = AddColumnFile.from_dict(data)

                    return componentsschemas_add_column_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_6 = AddColumnFloat.from_dict(data)

                    return componentsschemas_add_column_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_7 = AddColumnInteger.from_dict(data)

                    return componentsschemas_add_column_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_8 = AddColumnReference.from_dict(data)

                    return componentsschemas_add_column_type_8
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_9 = AddColumnSelect.from_dict(data)

                    return componentsschemas_add_column_type_9
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_10 = AddColumnText.from_dict(data)

                    return componentsschemas_add_column_type_10
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_add_column_type_11 = AddColumnUrl.from_dict(data)

                    return componentsschemas_add_column_type_11
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_add_column_type_12 = AddColumnUser.from_dict(data)

                return componentsschemas_add_column_type_12

            add_columns_item = _parse_add_columns_item(add_columns_item_data)

            add_columns.append(add_columns_item)

        import_rows_body = cls(
            database_id=database_id,
            creation_parent_id=creation_parent_id,
            creation_block_id=creation_block_id,
            add_columns=add_columns,
        )

        import_rows_body.additional_properties = d
        return import_rows_body

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
