from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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


T = TypeVar("T", bound="AddDatabaseColumnBody")


@_attrs_define
class AddDatabaseColumnBody:
    """
    Attributes:
        database_id (str):
        column (Union['AddColumnBoolean', 'AddColumnDate', 'AddColumnEditor', 'AddColumnExpression', 'AddColumnFile',
            'AddColumnFloat', 'AddColumnInteger', 'AddColumnLookup', 'AddColumnReference', 'AddColumnSelect',
            'AddColumnText', 'AddColumnUrl', 'AddColumnUser']):
    """

    database_id: str
    column: Union[
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

        column: Dict[str, Any]
        if isinstance(self.column, AddColumnLookup):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnBoolean):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnDate):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnEditor):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnExpression):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnFile):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnFloat):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnInteger):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnReference):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnSelect):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnText):
            column = self.column.to_dict()
        elif isinstance(self.column, AddColumnUrl):
            column = self.column.to_dict()
        else:
            column = self.column.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "databaseId": database_id,
                "column": column,
            }
        )

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

        def _parse_column(
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

        column = _parse_column(d.pop("column"))

        add_database_column_body = cls(
            database_id=database_id,
            column=column,
        )

        add_database_column_body.additional_properties = d
        return add_database_column_body

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
