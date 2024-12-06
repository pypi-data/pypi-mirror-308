from typing import TYPE_CHECKING, Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.field_expression_system_type import FieldExpressionSystemType
from ..models.field_expression_validation_status import FieldExpressionValidationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field_expression_value import FieldExpressionValue
    from ..models.invalid_data import InvalidData


T = TypeVar("T", bound="FieldExpression")


@_attrs_define
class FieldExpression:
    """
    Attributes:
        column_id (str):
        validation_status (FieldExpressionValidationStatus):
        type (Literal['expression']):
        value (FieldExpressionValue):
        version (Union[Unset, float]):
        invalid_data (Union[Unset, InvalidData]):
        system_type (Union[Unset, FieldExpressionSystemType]):
    """

    column_id: str
    validation_status: FieldExpressionValidationStatus
    type: Literal["expression"]
    value: "FieldExpressionValue"
    version: Union[Unset, float] = UNSET
    invalid_data: Union[Unset, "InvalidData"] = UNSET
    system_type: Union[Unset, FieldExpressionSystemType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        column_id = self.column_id

        validation_status = self.validation_status.value

        type = self.type

        value = self.value.to_dict()

        version = self.version

        invalid_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.invalid_data, Unset):
            invalid_data = self.invalid_data.to_dict()

        system_type: Union[Unset, str] = UNSET
        if not isinstance(self.system_type, Unset):
            system_type = self.system_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "columnId": column_id,
                "validationStatus": validation_status,
                "type": type,
                "value": value,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version
        if invalid_data is not UNSET:
            field_dict["invalidData"] = invalid_data
        if system_type is not UNSET:
            field_dict["systemType"] = system_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.field_expression_value import FieldExpressionValue
        from ..models.invalid_data import InvalidData

        d = src_dict.copy()
        column_id = d.pop("columnId")

        validation_status = FieldExpressionValidationStatus(d.pop("validationStatus"))

        type = d.pop("type")

        value = FieldExpressionValue.from_dict(d.pop("value"))

        version = d.pop("version", UNSET)

        _invalid_data = d.pop("invalidData", UNSET)
        invalid_data: Union[Unset, InvalidData]
        if isinstance(_invalid_data, Unset):
            invalid_data = UNSET
        else:
            invalid_data = InvalidData.from_dict(_invalid_data)

        _system_type = d.pop("systemType", UNSET)
        system_type: Union[Unset, FieldExpressionSystemType]
        if isinstance(_system_type, Unset):
            system_type = UNSET
        else:
            system_type = FieldExpressionSystemType(_system_type)

        field_expression = cls(
            column_id=column_id,
            validation_status=validation_status,
            type=type,
            value=value,
            version=version,
            invalid_data=invalid_data,
            system_type=system_type,
        )

        field_expression.additional_properties = d
        return field_expression

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
