from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_target_by_identifier_response_200_metadata import GetTargetByIdentifierResponse200Metadata
    from ..models.get_target_by_identifier_response_200_provider import GetTargetByIdentifierResponse200Provider
    from ..models.get_target_by_identifier_response_200_variables_item import (
        GetTargetByIdentifierResponse200VariablesItem,
    )


T = TypeVar("T", bound="GetTargetByIdentifierResponse200")


@_attrs_define
class GetTargetByIdentifierResponse200:
    """
    Attributes:
        id (str):
        identifier (str):
        workspace_id (str):
        provider_id (str):
        provider (Union[Unset, GetTargetByIdentifierResponse200Provider]):
        variables (Union[Unset, List['GetTargetByIdentifierResponse200VariablesItem']]):
        metadata (Union[Unset, GetTargetByIdentifierResponse200Metadata]):
    """

    id: str
    identifier: str
    workspace_id: str
    provider_id: str
    provider: Union[Unset, "GetTargetByIdentifierResponse200Provider"] = UNSET
    variables: Union[Unset, List["GetTargetByIdentifierResponse200VariablesItem"]] = UNSET
    metadata: Union[Unset, "GetTargetByIdentifierResponse200Metadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        identifier = self.identifier

        workspace_id = self.workspace_id

        provider_id = self.provider_id

        provider: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        variables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                variables_item = variables_item_data.to_dict()
                variables.append(variables_item)

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "identifier": identifier,
                "workspaceId": workspace_id,
                "providerId": provider_id,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if variables is not UNSET:
            field_dict["variables"] = variables
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_target_by_identifier_response_200_metadata import GetTargetByIdentifierResponse200Metadata
        from ..models.get_target_by_identifier_response_200_provider import GetTargetByIdentifierResponse200Provider
        from ..models.get_target_by_identifier_response_200_variables_item import (
            GetTargetByIdentifierResponse200VariablesItem,
        )

        d = src_dict.copy()
        id = d.pop("id")

        identifier = d.pop("identifier")

        workspace_id = d.pop("workspaceId")

        provider_id = d.pop("providerId")

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, GetTargetByIdentifierResponse200Provider]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = GetTargetByIdentifierResponse200Provider.from_dict(_provider)

        variables = []
        _variables = d.pop("variables", UNSET)
        for variables_item_data in _variables or []:
            variables_item = GetTargetByIdentifierResponse200VariablesItem.from_dict(variables_item_data)

            variables.append(variables_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, GetTargetByIdentifierResponse200Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = GetTargetByIdentifierResponse200Metadata.from_dict(_metadata)

        get_target_by_identifier_response_200 = cls(
            id=id,
            identifier=identifier,
            workspace_id=workspace_id,
            provider_id=provider_id,
            provider=provider,
            variables=variables,
            metadata=metadata,
        )

        get_target_by_identifier_response_200.additional_properties = d
        return get_target_by_identifier_response_200

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
