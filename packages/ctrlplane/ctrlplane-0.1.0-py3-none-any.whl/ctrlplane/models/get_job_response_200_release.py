from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_job_response_200_release_config import GetJobResponse200ReleaseConfig
    from ..models.get_job_response_200_release_metadata import GetJobResponse200ReleaseMetadata


T = TypeVar("T", bound="GetJobResponse200Release")


@_attrs_define
class GetJobResponse200Release:
    """
    Attributes:
        id (str):
        version (str):
        metadata (GetJobResponse200ReleaseMetadata):
        config (GetJobResponse200ReleaseConfig):
    """

    id: str
    version: str
    metadata: "GetJobResponse200ReleaseMetadata"
    config: "GetJobResponse200ReleaseConfig"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        version = self.version

        metadata = self.metadata.to_dict()

        config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "version": version,
                "metadata": metadata,
                "config": config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_job_response_200_release_config import GetJobResponse200ReleaseConfig
        from ..models.get_job_response_200_release_metadata import GetJobResponse200ReleaseMetadata

        d = src_dict.copy()
        id = d.pop("id")

        version = d.pop("version")

        metadata = GetJobResponse200ReleaseMetadata.from_dict(d.pop("metadata"))

        config = GetJobResponse200ReleaseConfig.from_dict(d.pop("config"))

        get_job_response_200_release = cls(
            id=id,
            version=version,
            metadata=metadata,
            config=config,
        )

        get_job_response_200_release.additional_properties = d
        return get_job_response_200_release

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
