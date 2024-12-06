from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.database import Database
    from ..models.database_row import DatabaseRow
    from ..models.workspace import Workspace


T = TypeVar("T", bound="DescribeRowResponse")


@_attrs_define
class DescribeRowResponse:
    """
    Attributes:
        data (Union['Database', 'DatabaseRow', 'Workspace']):
    """

    data: Union["Database", "DatabaseRow", "Workspace"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.database import Database
        from ..models.database_row import DatabaseRow

        data: Dict[str, Any]
        if isinstance(self.data, Database):
            data = self.data.to_dict()
        elif isinstance(self.data, DatabaseRow):
            data = self.data.to_dict()
        else:
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
        from ..models.database import Database
        from ..models.database_row import DatabaseRow
        from ..models.workspace import Workspace

        d = src_dict.copy()

        def _parse_data(data: object) -> Union["Database", "DatabaseRow", "Workspace"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_type_0 = Database.from_dict(data)

                return componentsschemas_row_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_row_type_1 = DatabaseRow.from_dict(data)

                return componentsschemas_row_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_row_type_2 = Workspace.from_dict(data)

            return componentsschemas_row_type_2

        data = _parse_data(d.pop("data"))

        describe_row_response = cls(
            data=data,
        )

        describe_row_response.additional_properties = d
        return describe_row_response

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
