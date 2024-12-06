from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.database_row_validation_status import DatabaseRowValidationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field_boolean import FieldBoolean
    from ..models.field_date import FieldDate
    from ..models.field_editor import FieldEditor
    from ..models.field_expression import FieldExpression
    from ..models.field_file import FieldFile
    from ..models.field_float import FieldFloat
    from ..models.field_integer import FieldInteger
    from ..models.field_lookup import FieldLookup
    from ..models.field_reference import FieldReference
    from ..models.field_select import FieldSelect
    from ..models.field_text import FieldText
    from ..models.field_url import FieldUrl
    from ..models.field_user import FieldUser


T = TypeVar("T", bound="DatabaseRow")


@_attrs_define
class DatabaseRow:
    """
    Attributes:
        id (str): Deep Origin system ID.
        type (Literal['row']):
        hid (str):
        date_created (str):
        name (Union[Unset, str]):
        date_updated (Union[Unset, str]):
        created_by_user_drn (Union[Unset, str]):
        edited_by_user_drn (Union[Unset, str]):
        parent_id (Union[Unset, str]):
        creation_parent_id (Union[Unset, str]):
        creation_block_id (Union[Unset, str]):
        fields (Union[Unset, List[Union['FieldBoolean', 'FieldDate', 'FieldEditor', 'FieldExpression', 'FieldFile',
            'FieldFloat', 'FieldInteger', 'FieldLookup', 'FieldReference', 'FieldSelect', 'FieldText', 'FieldUrl',
            'FieldUser']]]):
        is_template (Union[Unset, bool]):
        validation_status (Union[Unset, DatabaseRowValidationStatus]):
    """

    id: str
    type: Literal["row"]
    hid: str
    date_created: str
    name: Union[Unset, str] = UNSET
    date_updated: Union[Unset, str] = UNSET
    created_by_user_drn: Union[Unset, str] = UNSET
    edited_by_user_drn: Union[Unset, str] = UNSET
    parent_id: Union[Unset, str] = UNSET
    creation_parent_id: Union[Unset, str] = UNSET
    creation_block_id: Union[Unset, str] = UNSET
    fields: Union[
        Unset,
        List[
            Union[
                "FieldBoolean",
                "FieldDate",
                "FieldEditor",
                "FieldExpression",
                "FieldFile",
                "FieldFloat",
                "FieldInteger",
                "FieldLookup",
                "FieldReference",
                "FieldSelect",
                "FieldText",
                "FieldUrl",
                "FieldUser",
            ]
        ],
    ] = UNSET
    is_template: Union[Unset, bool] = UNSET
    validation_status: Union[Unset, DatabaseRowValidationStatus] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.field_boolean import FieldBoolean
        from ..models.field_date import FieldDate
        from ..models.field_editor import FieldEditor
        from ..models.field_expression import FieldExpression
        from ..models.field_file import FieldFile
        from ..models.field_float import FieldFloat
        from ..models.field_integer import FieldInteger
        from ..models.field_reference import FieldReference
        from ..models.field_select import FieldSelect
        from ..models.field_text import FieldText
        from ..models.field_url import FieldUrl
        from ..models.field_user import FieldUser

        id = self.id

        type = self.type

        hid = self.hid

        date_created = self.date_created

        name = self.name

        date_updated = self.date_updated

        created_by_user_drn = self.created_by_user_drn

        edited_by_user_drn = self.edited_by_user_drn

        parent_id = self.parent_id

        creation_parent_id = self.creation_parent_id

        creation_block_id = self.creation_block_id

        fields: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item: Dict[str, Any]
                if isinstance(fields_item_data, FieldText):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldInteger):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldFloat):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldBoolean):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldReference):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldEditor):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldFile):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldSelect):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldDate):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldUrl):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldUser):
                    fields_item = fields_item_data.to_dict()
                elif isinstance(fields_item_data, FieldExpression):
                    fields_item = fields_item_data.to_dict()
                else:
                    fields_item = fields_item_data.to_dict()

                fields.append(fields_item)

        is_template = self.is_template

        validation_status: Union[Unset, str] = UNSET
        if not isinstance(self.validation_status, Unset):
            validation_status = self.validation_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type,
                "hid": hid,
                "dateCreated": date_created,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if date_updated is not UNSET:
            field_dict["dateUpdated"] = date_updated
        if created_by_user_drn is not UNSET:
            field_dict["createdByUserDrn"] = created_by_user_drn
        if edited_by_user_drn is not UNSET:
            field_dict["editedByUserDrn"] = edited_by_user_drn
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if creation_parent_id is not UNSET:
            field_dict["creationParentId"] = creation_parent_id
        if creation_block_id is not UNSET:
            field_dict["creationBlockId"] = creation_block_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if is_template is not UNSET:
            field_dict["isTemplate"] = is_template
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.field_boolean import FieldBoolean
        from ..models.field_date import FieldDate
        from ..models.field_editor import FieldEditor
        from ..models.field_expression import FieldExpression
        from ..models.field_file import FieldFile
        from ..models.field_float import FieldFloat
        from ..models.field_integer import FieldInteger
        from ..models.field_lookup import FieldLookup
        from ..models.field_reference import FieldReference
        from ..models.field_select import FieldSelect
        from ..models.field_text import FieldText
        from ..models.field_url import FieldUrl
        from ..models.field_user import FieldUser

        d = src_dict.copy()
        id = d.pop("id")

        type = d.pop("type")

        hid = d.pop("hid")

        date_created = d.pop("dateCreated")

        name = d.pop("name", UNSET)

        date_updated = d.pop("dateUpdated", UNSET)

        created_by_user_drn = d.pop("createdByUserDrn", UNSET)

        edited_by_user_drn = d.pop("editedByUserDrn", UNSET)

        parent_id = d.pop("parentId", UNSET)

        creation_parent_id = d.pop("creationParentId", UNSET)

        creation_block_id = d.pop("creationBlockId", UNSET)

        fields = []
        _fields = d.pop("fields", UNSET)
        for fields_item_data in _fields or []:

            def _parse_fields_item(
                data: object,
            ) -> Union[
                "FieldBoolean",
                "FieldDate",
                "FieldEditor",
                "FieldExpression",
                "FieldFile",
                "FieldFloat",
                "FieldInteger",
                "FieldLookup",
                "FieldReference",
                "FieldSelect",
                "FieldText",
                "FieldUrl",
                "FieldUser",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_0 = FieldText.from_dict(data)

                    return componentsschemas_field_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_1 = FieldInteger.from_dict(data)

                    return componentsschemas_field_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_2 = FieldFloat.from_dict(data)

                    return componentsschemas_field_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_3 = FieldBoolean.from_dict(data)

                    return componentsschemas_field_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_4 = FieldReference.from_dict(data)

                    return componentsschemas_field_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_5 = FieldEditor.from_dict(data)

                    return componentsschemas_field_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_6 = FieldFile.from_dict(data)

                    return componentsschemas_field_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_7 = FieldSelect.from_dict(data)

                    return componentsschemas_field_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_8 = FieldDate.from_dict(data)

                    return componentsschemas_field_type_8
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_9 = FieldUrl.from_dict(data)

                    return componentsschemas_field_type_9
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_10 = FieldUser.from_dict(data)

                    return componentsschemas_field_type_10
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_field_type_11 = FieldExpression.from_dict(data)

                    return componentsschemas_field_type_11
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_field_type_12 = FieldLookup.from_dict(data)

                return componentsschemas_field_type_12

            fields_item = _parse_fields_item(fields_item_data)

            fields.append(fields_item)

        is_template = d.pop("isTemplate", UNSET)

        _validation_status = d.pop("validationStatus", UNSET)
        validation_status: Union[Unset, DatabaseRowValidationStatus]
        if isinstance(_validation_status, Unset):
            validation_status = UNSET
        else:
            validation_status = DatabaseRowValidationStatus(_validation_status)

        database_row = cls(
            id=id,
            type=type,
            hid=hid,
            date_created=date_created,
            name=name,
            date_updated=date_updated,
            created_by_user_drn=created_by_user_drn,
            edited_by_user_drn=edited_by_user_drn,
            parent_id=parent_id,
            creation_parent_id=creation_parent_id,
            creation_block_id=creation_block_id,
            fields=fields,
            is_template=is_template,
            validation_status=validation_status,
        )

        database_row.additional_properties = d
        return database_row

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
