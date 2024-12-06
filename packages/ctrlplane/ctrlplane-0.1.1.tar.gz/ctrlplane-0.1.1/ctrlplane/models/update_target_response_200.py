from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_target_response_200_config import UpdateTargetResponse200Config
    from ..models.update_target_response_200_metadata import UpdateTargetResponse200Metadata


T = TypeVar("T", bound="UpdateTargetResponse200")


@_attrs_define
class UpdateTargetResponse200:
    """
    Attributes:
        id (str):
        name (str):
        workspace_id (str):
        kind (str):
        identifier (str):
        version (str):
        config (UpdateTargetResponse200Config):
        metadata (UpdateTargetResponse200Metadata):
    """

    id: str
    name: str
    workspace_id: str
    kind: str
    identifier: str
    version: str
    config: "UpdateTargetResponse200Config"
    metadata: "UpdateTargetResponse200Metadata"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        workspace_id = self.workspace_id

        kind = self.kind

        identifier = self.identifier

        version = self.version

        config = self.config.to_dict()

        metadata = self.metadata.to_dict()

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
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_target_response_200_config import UpdateTargetResponse200Config
        from ..models.update_target_response_200_metadata import UpdateTargetResponse200Metadata

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        workspace_id = d.pop("workspaceId")

        kind = d.pop("kind")

        identifier = d.pop("identifier")

        version = d.pop("version")

        config = UpdateTargetResponse200Config.from_dict(d.pop("config"))

        metadata = UpdateTargetResponse200Metadata.from_dict(d.pop("metadata"))

        update_target_response_200 = cls(
            id=id,
            name=name,
            workspace_id=workspace_id,
            kind=kind,
            identifier=identifier,
            version=version,
            config=config,
            metadata=metadata,
        )

        update_target_response_200.additional_properties = d
        return update_target_response_200

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
