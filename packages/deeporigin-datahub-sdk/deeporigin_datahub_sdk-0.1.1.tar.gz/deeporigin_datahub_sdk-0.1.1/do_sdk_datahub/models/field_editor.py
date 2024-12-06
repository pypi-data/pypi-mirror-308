from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.field_editor_system_type import FieldEditorSystemType
from ..models.field_editor_validation_status import FieldEditorValidationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field_editor_value_type_0 import FieldEditorValueType0
    from ..models.invalid_data import InvalidData


T = TypeVar("T", bound="FieldEditor")


@_attrs_define
class FieldEditor:
    """
    Attributes:
        column_id (str):
        validation_status (FieldEditorValidationStatus):
        type (Literal['editor']):
        version (Union[Unset, float]):
        invalid_data (Union[Unset, InvalidData]):
        system_type (Union[Unset, FieldEditorSystemType]):
        value (Union['FieldEditorValueType0', None, Unset]):
    """

    column_id: str
    validation_status: FieldEditorValidationStatus
    type: Literal["editor"]
    version: Union[Unset, float] = UNSET
    invalid_data: Union[Unset, "InvalidData"] = UNSET
    system_type: Union[Unset, FieldEditorSystemType] = UNSET
    value: Union["FieldEditorValueType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.field_editor_value_type_0 import FieldEditorValueType0

        column_id = self.column_id

        validation_status = self.validation_status.value

        type = self.type

        version = self.version

        invalid_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.invalid_data, Unset):
            invalid_data = self.invalid_data.to_dict()

        system_type: Union[Unset, str] = UNSET
        if not isinstance(self.system_type, Unset):
            system_type = self.system_type.value

        value: Union[Dict[str, Any], None, Unset]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, FieldEditorValueType0):
            value = self.value.to_dict()
        else:
            value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "columnId": column_id,
                "validationStatus": validation_status,
                "type": type,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version
        if invalid_data is not UNSET:
            field_dict["invalidData"] = invalid_data
        if system_type is not UNSET:
            field_dict["systemType"] = system_type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.field_editor_value_type_0 import FieldEditorValueType0
        from ..models.invalid_data import InvalidData

        d = src_dict.copy()
        column_id = d.pop("columnId")

        validation_status = FieldEditorValidationStatus(d.pop("validationStatus"))

        type = d.pop("type")

        version = d.pop("version", UNSET)

        _invalid_data = d.pop("invalidData", UNSET)
        invalid_data: Union[Unset, InvalidData]
        if isinstance(_invalid_data, Unset):
            invalid_data = UNSET
        else:
            invalid_data = InvalidData.from_dict(_invalid_data)

        _system_type = d.pop("systemType", UNSET)
        system_type: Union[Unset, FieldEditorSystemType]
        if isinstance(_system_type, Unset):
            system_type = UNSET
        else:
            system_type = FieldEditorSystemType(_system_type)

        def _parse_value(data: object) -> Union["FieldEditorValueType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0 = FieldEditorValueType0.from_dict(data)

                return value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FieldEditorValueType0", None, Unset], data)

        value = _parse_value(d.pop("value", UNSET))

        field_editor = cls(
            column_id=column_id,
            validation_status=validation_status,
            type=type,
            version=version,
            invalid_data=invalid_data,
            system_type=system_type,
            value=value,
        )

        field_editor.additional_properties = d
        return field_editor

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
