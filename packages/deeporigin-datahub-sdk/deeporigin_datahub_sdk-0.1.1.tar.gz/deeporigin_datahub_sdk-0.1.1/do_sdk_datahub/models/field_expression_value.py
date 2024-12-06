from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldExpressionValue")


@_attrs_define
class FieldExpressionValue:
    """
    Attributes:
        result (Union[Unset, float, str]): The return value from executing the expression.
        invalid_result (Union[Unset, Any]): Expression result that is not a valid return value type.
        error_message (Union[Unset, str]): The error message from executing the expression, if one occurred.
    """

    result: Union[Unset, float, str] = UNSET
    invalid_result: Union[Unset, Any] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result: Union[Unset, float, str]
        if isinstance(self.result, Unset):
            result = UNSET
        else:
            result = self.result

        invalid_result = self.invalid_result

        error_message = self.error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if result is not UNSET:
            field_dict["result"] = result
        if invalid_result is not UNSET:
            field_dict["invalidResult"] = invalid_result
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_result(data: object) -> Union[Unset, float, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, float, str], data)

        result = _parse_result(d.pop("result", UNSET))

        invalid_result = d.pop("invalidResult", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        field_expression_value = cls(
            result=result,
            invalid_result=invalid_result,
            error_message=error_message,
        )

        field_expression_value.additional_properties = d
        return field_expression_value

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
