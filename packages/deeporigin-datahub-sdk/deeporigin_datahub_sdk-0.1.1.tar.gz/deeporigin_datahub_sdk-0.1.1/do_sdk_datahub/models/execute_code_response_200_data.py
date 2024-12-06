from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.code_exeuction import CodeExeuction


T = TypeVar("T", bound="ExecuteCodeResponse200Data")


@_attrs_define
class ExecuteCodeResponse200Data:
    """
    Attributes:
        code_execution (CodeExeuction):
    """

    code_execution: "CodeExeuction"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code_execution = self.code_execution.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "codeExecution": code_execution,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.code_exeuction import CodeExeuction

        d = src_dict.copy()
        code_execution = CodeExeuction.from_dict(d.pop("codeExecution"))

        execute_code_response_200_data = cls(
            code_execution=code_execution,
        )

        execute_code_response_200_data.additional_properties = d
        return execute_code_response_200_data

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
