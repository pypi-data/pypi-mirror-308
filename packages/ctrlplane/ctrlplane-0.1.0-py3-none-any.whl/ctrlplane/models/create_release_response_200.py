from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_release_response_200_metadata import CreateReleaseResponse200Metadata


T = TypeVar("T", bound="CreateReleaseResponse200")


@_attrs_define
class CreateReleaseResponse200:
    """
    Attributes:
        id (Union[Unset, str]):
        version (Union[Unset, str]):
        metadata (Union[Unset, CreateReleaseResponse200Metadata]):
    """

    id: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    metadata: Union[Unset, "CreateReleaseResponse200Metadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        version = self.version

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if version is not UNSET:
            field_dict["version"] = version
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_release_response_200_metadata import CreateReleaseResponse200Metadata

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        version = d.pop("version", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, CreateReleaseResponse200Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateReleaseResponse200Metadata.from_dict(_metadata)

        create_release_response_200 = cls(
            id=id,
            version=version,
            metadata=metadata,
        )

        create_release_response_200.additional_properties = d
        return create_release_response_200

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
