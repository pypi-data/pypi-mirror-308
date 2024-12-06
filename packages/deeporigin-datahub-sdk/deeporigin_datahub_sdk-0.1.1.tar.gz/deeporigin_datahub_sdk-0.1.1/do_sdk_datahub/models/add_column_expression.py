from typing import Any, Dict, List, Literal, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.add_column_expression_cardinality import AddColumnExpressionCardinality
from ..models.add_column_expression_enabled_viewers_item import AddColumnExpressionEnabledViewersItem
from ..models.add_column_expression_expression_return_type import AddColumnExpressionExpressionReturnType
from ..models.add_column_expression_inline_viewer import AddColumnExpressionInlineViewer
from ..models.add_column_expression_system_type import AddColumnExpressionSystemType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddColumnExpression")


@_attrs_define
class AddColumnExpression:
    """
    Attributes:
        type (Literal['expression']):
        expression_code (str):
        expression_return_type (AddColumnExpressionExpressionReturnType):
        name (str):
        cardinality (AddColumnExpressionCardinality):
        system_type (Union[Unset, AddColumnExpressionSystemType]):
        is_required (Union[Unset, bool]):
        enabled_viewers (Union[Unset, List[AddColumnExpressionEnabledViewersItem]]):
        cell_json_schema (Union[Unset, Any]):
        inline_viewer (Union[Unset, AddColumnExpressionInlineViewer]):
    """

    type: Literal["expression"]
    expression_code: str
    expression_return_type: AddColumnExpressionExpressionReturnType
    name: str
    cardinality: AddColumnExpressionCardinality
    system_type: Union[Unset, AddColumnExpressionSystemType] = UNSET
    is_required: Union[Unset, bool] = UNSET
    enabled_viewers: Union[Unset, List[AddColumnExpressionEnabledViewersItem]] = UNSET
    cell_json_schema: Union[Unset, Any] = UNSET
    inline_viewer: Union[Unset, AddColumnExpressionInlineViewer] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        expression_code = self.expression_code

        expression_return_type = self.expression_return_type.value

        name = self.name

        cardinality = self.cardinality.value

        system_type: Union[Unset, str] = UNSET
        if not isinstance(self.system_type, Unset):
            system_type = self.system_type.value

        is_required = self.is_required

        enabled_viewers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.enabled_viewers, Unset):
            enabled_viewers = []
            for enabled_viewers_item_data in self.enabled_viewers:
                enabled_viewers_item = enabled_viewers_item_data.value
                enabled_viewers.append(enabled_viewers_item)

        cell_json_schema = self.cell_json_schema

        inline_viewer: Union[Unset, str] = UNSET
        if not isinstance(self.inline_viewer, Unset):
            inline_viewer = self.inline_viewer.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "expressionCode": expression_code,
                "expressionReturnType": expression_return_type,
                "name": name,
                "cardinality": cardinality,
            }
        )
        if system_type is not UNSET:
            field_dict["systemType"] = system_type
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if enabled_viewers is not UNSET:
            field_dict["enabledViewers"] = enabled_viewers
        if cell_json_schema is not UNSET:
            field_dict["cellJsonSchema"] = cell_json_schema
        if inline_viewer is not UNSET:
            field_dict["inlineViewer"] = inline_viewer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        expression_code = d.pop("expressionCode")

        expression_return_type = AddColumnExpressionExpressionReturnType(d.pop("expressionReturnType"))

        name = d.pop("name")

        cardinality = AddColumnExpressionCardinality(d.pop("cardinality"))

        _system_type = d.pop("systemType", UNSET)
        system_type: Union[Unset, AddColumnExpressionSystemType]
        if isinstance(_system_type, Unset):
            system_type = UNSET
        else:
            system_type = AddColumnExpressionSystemType(_system_type)

        is_required = d.pop("isRequired", UNSET)

        enabled_viewers = []
        _enabled_viewers = d.pop("enabledViewers", UNSET)
        for enabled_viewers_item_data in _enabled_viewers or []:
            enabled_viewers_item = AddColumnExpressionEnabledViewersItem(enabled_viewers_item_data)

            enabled_viewers.append(enabled_viewers_item)

        cell_json_schema = d.pop("cellJsonSchema", UNSET)

        _inline_viewer = d.pop("inlineViewer", UNSET)
        inline_viewer: Union[Unset, AddColumnExpressionInlineViewer]
        if isinstance(_inline_viewer, Unset):
            inline_viewer = UNSET
        else:
            inline_viewer = AddColumnExpressionInlineViewer(_inline_viewer)

        add_column_expression = cls(
            type=type,
            expression_code=expression_code,
            expression_return_type=expression_return_type,
            name=name,
            cardinality=cardinality,
            system_type=system_type,
            is_required=is_required,
            enabled_viewers=enabled_viewers,
            cell_json_schema=cell_json_schema,
            inline_viewer=inline_viewer,
        )

        add_column_expression.additional_properties = d
        return add_column_expression

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
