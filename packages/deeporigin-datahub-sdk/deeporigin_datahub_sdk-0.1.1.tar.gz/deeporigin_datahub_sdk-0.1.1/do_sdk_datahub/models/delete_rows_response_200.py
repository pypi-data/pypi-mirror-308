from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delete_rows_response_200_data import DeleteRowsResponse200Data


T = TypeVar("T", bound="DeleteRowsResponse200")


@_attrs_define
class DeleteRowsResponse200:
    """
    Attributes:
        data (DeleteRowsResponse200Data):
    """

    data: "DeleteRowsResponse200Data"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.delete_rows_response_200_data import DeleteRowsResponse200Data

        d = src_dict.copy()
        data = DeleteRowsResponse200Data.from_dict(d.pop("data"))

        delete_rows_response_200 = cls(
            data=data,
        )

        delete_rows_response_200.additional_properties = d
        return delete_rows_response_200

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
