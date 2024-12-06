from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_workspace_body_workspace import UpdateWorkspaceBodyWorkspace


T = TypeVar("T", bound="UpdateWorkspaceBody")


@_attrs_define
class UpdateWorkspaceBody:
    """
    Attributes:
        id (str):
        workspace (UpdateWorkspaceBodyWorkspace):
    """

    id: str
    workspace: "UpdateWorkspaceBodyWorkspace"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        workspace = self.workspace.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "workspace": workspace,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_workspace_body_workspace import UpdateWorkspaceBodyWorkspace

        d = src_dict.copy()
        id = d.pop("id")

        workspace = UpdateWorkspaceBodyWorkspace.from_dict(d.pop("workspace"))

        update_workspace_body = cls(
            id=id,
            workspace=workspace,
        )

        update_workspace_body.additional_properties = d
        return update_workspace_body

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
