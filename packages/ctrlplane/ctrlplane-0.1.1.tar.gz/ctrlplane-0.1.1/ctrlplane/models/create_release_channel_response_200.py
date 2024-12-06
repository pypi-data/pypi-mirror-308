import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_release_channel_response_200_release_filter import CreateReleaseChannelResponse200ReleaseFilter


T = TypeVar("T", bound="CreateReleaseChannelResponse200")


@_attrs_define
class CreateReleaseChannelResponse200:
    """
    Attributes:
        id (str):
        deployment_id (str):
        name (str):
        created_at (datetime.datetime):
        description (Union[None, Unset, str]):
        release_filter (Union[Unset, CreateReleaseChannelResponse200ReleaseFilter]):
    """

    id: str
    deployment_id: str
    name: str
    created_at: datetime.datetime
    description: Union[None, Unset, str] = UNSET
    release_filter: Union[Unset, "CreateReleaseChannelResponse200ReleaseFilter"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        deployment_id = self.deployment_id

        name = self.name

        created_at = self.created_at.isoformat()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        release_filter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.release_filter, Unset):
            release_filter = self.release_filter.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "deploymentId": deployment_id,
                "name": name,
                "createdAt": created_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if release_filter is not UNSET:
            field_dict["releaseFilter"] = release_filter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_release_channel_response_200_release_filter import (
            CreateReleaseChannelResponse200ReleaseFilter,
        )

        d = src_dict.copy()
        id = d.pop("id")

        deployment_id = d.pop("deploymentId")

        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _release_filter = d.pop("releaseFilter", UNSET)
        release_filter: Union[Unset, CreateReleaseChannelResponse200ReleaseFilter]
        if isinstance(_release_filter, Unset):
            release_filter = UNSET
        else:
            release_filter = CreateReleaseChannelResponse200ReleaseFilter.from_dict(_release_filter)

        create_release_channel_response_200 = cls(
            id=id,
            deployment_id=deployment_id,
            name=name,
            created_at=created_at,
            description=description,
            release_filter=release_filter,
        )

        create_release_channel_response_200.additional_properties = d
        return create_release_channel_response_200

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
