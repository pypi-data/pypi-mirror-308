import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_target_response_200_config import GetTargetResponse200Config
    from ..models.get_target_response_200_metadata import GetTargetResponse200Metadata
    from ..models.get_target_response_200_provider_type_0 import GetTargetResponse200ProviderType0
    from ..models.get_target_response_200_variables_item import GetTargetResponse200VariablesItem


T = TypeVar("T", bound="GetTargetResponse200")


@_attrs_define
class GetTargetResponse200:
    """
    Attributes:
        id (str):
        name (str):
        workspace_id (str):
        kind (str):
        identifier (str):
        version (str):
        config (GetTargetResponse200Config):
        updated_at (datetime.datetime):
        metadata (GetTargetResponse200Metadata):
        locked_at (Union[None, Unset, datetime.datetime]):
        provider (Union['GetTargetResponse200ProviderType0', None, Unset]):
        variables (Union[Unset, List['GetTargetResponse200VariablesItem']]):
    """

    id: str
    name: str
    workspace_id: str
    kind: str
    identifier: str
    version: str
    config: "GetTargetResponse200Config"
    updated_at: datetime.datetime
    metadata: "GetTargetResponse200Metadata"
    locked_at: Union[None, Unset, datetime.datetime] = UNSET
    provider: Union["GetTargetResponse200ProviderType0", None, Unset] = UNSET
    variables: Union[Unset, List["GetTargetResponse200VariablesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_target_response_200_provider_type_0 import GetTargetResponse200ProviderType0

        id = self.id

        name = self.name

        workspace_id = self.workspace_id

        kind = self.kind

        identifier = self.identifier

        version = self.version

        config = self.config.to_dict()

        updated_at = self.updated_at.isoformat()

        metadata = self.metadata.to_dict()

        locked_at: Union[None, Unset, str]
        if isinstance(self.locked_at, Unset):
            locked_at = UNSET
        elif isinstance(self.locked_at, datetime.datetime):
            locked_at = self.locked_at.isoformat()
        else:
            locked_at = self.locked_at

        provider: Union[Dict[str, Any], None, Unset]
        if isinstance(self.provider, Unset):
            provider = UNSET
        elif isinstance(self.provider, GetTargetResponse200ProviderType0):
            provider = self.provider.to_dict()
        else:
            provider = self.provider

        variables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                variables_item = variables_item_data.to_dict()
                variables.append(variables_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "workspaceId": workspace_id,
                "kind": kind,
                "identifier": identifier,
                "version": version,
                "config": config,
                "updatedAt": updated_at,
                "metadata": metadata,
            }
        )
        if locked_at is not UNSET:
            field_dict["lockedAt"] = locked_at
        if provider is not UNSET:
            field_dict["provider"] = provider
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_target_response_200_config import GetTargetResponse200Config
        from ..models.get_target_response_200_metadata import GetTargetResponse200Metadata
        from ..models.get_target_response_200_provider_type_0 import GetTargetResponse200ProviderType0
        from ..models.get_target_response_200_variables_item import GetTargetResponse200VariablesItem

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        workspace_id = d.pop("workspaceId")

        kind = d.pop("kind")

        identifier = d.pop("identifier")

        version = d.pop("version")

        config = GetTargetResponse200Config.from_dict(d.pop("config"))

        updated_at = isoparse(d.pop("updatedAt"))

        metadata = GetTargetResponse200Metadata.from_dict(d.pop("metadata"))

        def _parse_locked_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                locked_at_type_0 = isoparse(data)

                return locked_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        locked_at = _parse_locked_at(d.pop("lockedAt", UNSET))

        def _parse_provider(data: object) -> Union["GetTargetResponse200ProviderType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                provider_type_0 = GetTargetResponse200ProviderType0.from_dict(data)

                return provider_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetTargetResponse200ProviderType0", None, Unset], data)

        provider = _parse_provider(d.pop("provider", UNSET))

        variables = []
        _variables = d.pop("variables", UNSET)
        for variables_item_data in _variables or []:
            variables_item = GetTargetResponse200VariablesItem.from_dict(variables_item_data)

            variables.append(variables_item)

        get_target_response_200 = cls(
            id=id,
            name=name,
            workspace_id=workspace_id,
            kind=kind,
            identifier=identifier,
            version=version,
            config=config,
            updated_at=updated_at,
            metadata=metadata,
            locked_at=locked_at,
            provider=provider,
            variables=variables,
        )

        get_target_response_200.additional_properties = d
        return get_target_response_200

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
