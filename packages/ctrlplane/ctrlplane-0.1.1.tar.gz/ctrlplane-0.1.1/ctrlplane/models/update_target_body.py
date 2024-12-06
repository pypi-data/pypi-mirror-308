from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_target_body_metadata import UpdateTargetBodyMetadata
    from ..models.update_target_body_variables_item import UpdateTargetBodyVariablesItem


T = TypeVar("T", bound="UpdateTargetBody")


@_attrs_define
class UpdateTargetBody:
    """
    Attributes:
        name (Union[Unset, str]):
        version (Union[Unset, str]):
        kind (Union[Unset, str]):
        identifier (Union[Unset, str]):
        workspace_id (Union[Unset, str]):
        metadata (Union[Unset, UpdateTargetBodyMetadata]):
        variables (Union[Unset, List['UpdateTargetBodyVariablesItem']]):
    """

    name: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    kind: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "UpdateTargetBodyMetadata"] = UNSET
    variables: Union[Unset, List["UpdateTargetBodyVariablesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        version = self.version

        kind = self.kind

        identifier = self.identifier

        workspace_id = self.workspace_id

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        variables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                variables_item = variables_item_data.to_dict()
                variables.append(variables_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version
        if kind is not UNSET:
            field_dict["kind"] = kind
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if workspace_id is not UNSET:
            field_dict["workspaceId"] = workspace_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_target_body_metadata import UpdateTargetBodyMetadata
        from ..models.update_target_body_variables_item import UpdateTargetBodyVariablesItem

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        version = d.pop("version", UNSET)

        kind = d.pop("kind", UNSET)

        identifier = d.pop("identifier", UNSET)

        workspace_id = d.pop("workspaceId", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, UpdateTargetBodyMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = UpdateTargetBodyMetadata.from_dict(_metadata)

        variables = []
        _variables = d.pop("variables", UNSET)
        for variables_item_data in _variables or []:
            variables_item = UpdateTargetBodyVariablesItem.from_dict(variables_item_data)

            variables.append(variables_item)

        update_target_body = cls(
            name=name,
            version=version,
            kind=kind,
            identifier=identifier,
            workspace_id=workspace_id,
            metadata=metadata,
            variables=variables,
        )

        update_target_body.additional_properties = d
        return update_target_body

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
