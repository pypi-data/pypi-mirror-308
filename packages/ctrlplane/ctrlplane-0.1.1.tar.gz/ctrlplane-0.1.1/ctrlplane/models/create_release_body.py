from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_release_body_metadata import CreateReleaseBodyMetadata


T = TypeVar("T", bound="CreateReleaseBody")


@_attrs_define
class CreateReleaseBody:
    """
    Attributes:
        version (str):
        deployment_id (str):
        metadata (Union[Unset, CreateReleaseBodyMetadata]):
    """

    version: str
    deployment_id: str
    metadata: Union[Unset, "CreateReleaseBodyMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version

        deployment_id = self.deployment_id

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "deploymentId": deployment_id,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_release_body_metadata import CreateReleaseBodyMetadata

        d = src_dict.copy()
        version = d.pop("version")

        deployment_id = d.pop("deploymentId")

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, CreateReleaseBodyMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateReleaseBodyMetadata.from_dict(_metadata)

        create_release_body = cls(
            version=version,
            deployment_id=deployment_id,
            metadata=metadata,
        )

        create_release_body.additional_properties = d
        return create_release_body

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
