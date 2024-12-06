from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_job_response_200_target_config import GetJobResponse200TargetConfig
    from ..models.get_job_response_200_target_metadata import GetJobResponse200TargetMetadata


T = TypeVar("T", bound="GetJobResponse200Target")


@_attrs_define
class GetJobResponse200Target:
    """
    Attributes:
        id (str):
        name (str):
        version (str):
        kind (str):
        identifier (str):
        workspace_id (str):
        config (GetJobResponse200TargetConfig):
        metadata (GetJobResponse200TargetMetadata):
    """

    id: str
    name: str
    version: str
    kind: str
    identifier: str
    workspace_id: str
    config: "GetJobResponse200TargetConfig"
    metadata: "GetJobResponse200TargetMetadata"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        version = self.version

        kind = self.kind

        identifier = self.identifier

        workspace_id = self.workspace_id

        config = self.config.to_dict()

        metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "version": version,
                "kind": kind,
                "identifier": identifier,
                "workspaceId": workspace_id,
                "config": config,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_job_response_200_target_config import GetJobResponse200TargetConfig
        from ..models.get_job_response_200_target_metadata import GetJobResponse200TargetMetadata

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        version = d.pop("version")

        kind = d.pop("kind")

        identifier = d.pop("identifier")

        workspace_id = d.pop("workspaceId")

        config = GetJobResponse200TargetConfig.from_dict(d.pop("config"))

        metadata = GetJobResponse200TargetMetadata.from_dict(d.pop("metadata"))

        get_job_response_200_target = cls(
            id=id,
            name=name,
            version=version,
            kind=kind,
            identifier=identifier,
            workspace_id=workspace_id,
            config=config,
            metadata=metadata,
        )

        get_job_response_200_target.additional_properties = d
        return get_job_response_200_target

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
