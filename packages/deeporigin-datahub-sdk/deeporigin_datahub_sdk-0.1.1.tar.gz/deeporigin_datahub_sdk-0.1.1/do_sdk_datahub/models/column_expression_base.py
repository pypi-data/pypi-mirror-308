from typing import Any, Dict, List, Literal, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_expression_base_expression_return_type import ColumnExpressionBaseExpressionReturnType

T = TypeVar("T", bound="ColumnExpressionBase")


@_attrs_define
class ColumnExpressionBase:
    """
    Attributes:
        type (Literal['expression']):
        expression_code (str):
        expression_return_type (ColumnExpressionBaseExpressionReturnType):
    """

    type: Literal["expression"]
    expression_code: str
    expression_return_type: ColumnExpressionBaseExpressionReturnType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        expression_code = self.expression_code

        expression_return_type = self.expression_return_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "expressionCode": expression_code,
                "expressionReturnType": expression_return_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        expression_code = d.pop("expressionCode")

        expression_return_type = ColumnExpressionBaseExpressionReturnType(d.pop("expressionReturnType"))

        column_expression_base = cls(
            type=type,
            expression_code=expression_code,
            expression_return_type=expression_return_type,
        )

        column_expression_base.additional_properties = d
        return column_expression_base

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
