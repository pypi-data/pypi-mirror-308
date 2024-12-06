import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_environment_body_release_channels_item import CreateEnvironmentBodyReleaseChannelsItem
    from ..models.create_environment_body_target_filter import CreateEnvironmentBodyTargetFilter


T = TypeVar("T", bound="CreateEnvironmentBody")


@_attrs_define
class CreateEnvironmentBody:
    """
    Attributes:
        system_id (str):
        name (str):
        description (Union[Unset, str]):
        target_filter (Union[Unset, CreateEnvironmentBodyTargetFilter]):
        policy_id (Union[Unset, str]):
        release_channels (Union[Unset, List['CreateEnvironmentBodyReleaseChannelsItem']]):
        expires_at (Union[Unset, datetime.datetime]):
    """

    system_id: str
    name: str
    description: Union[Unset, str] = UNSET
    target_filter: Union[Unset, "CreateEnvironmentBodyTargetFilter"] = UNSET
    policy_id: Union[Unset, str] = UNSET
    release_channels: Union[Unset, List["CreateEnvironmentBodyReleaseChannelsItem"]] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        system_id = self.system_id

        name = self.name

        description = self.description

        target_filter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.target_filter, Unset):
            target_filter = self.target_filter.to_dict()

        policy_id = self.policy_id

        release_channels: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.release_channels, Unset):
            release_channels = []
            for release_channels_item_data in self.release_channels:
                release_channels_item = release_channels_item_data.to_dict()
                release_channels.append(release_channels_item)

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "systemId": system_id,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if target_filter is not UNSET:
            field_dict["targetFilter"] = target_filter
        if policy_id is not UNSET:
            field_dict["policyId"] = policy_id
        if release_channels is not UNSET:
            field_dict["releaseChannels"] = release_channels
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_environment_body_release_channels_item import CreateEnvironmentBodyReleaseChannelsItem
        from ..models.create_environment_body_target_filter import CreateEnvironmentBodyTargetFilter

        d = src_dict.copy()
        system_id = d.pop("systemId")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        _target_filter = d.pop("targetFilter", UNSET)
        target_filter: Union[Unset, CreateEnvironmentBodyTargetFilter]
        if isinstance(_target_filter, Unset):
            target_filter = UNSET
        else:
            target_filter = CreateEnvironmentBodyTargetFilter.from_dict(_target_filter)

        policy_id = d.pop("policyId", UNSET)

        release_channels = []
        _release_channels = d.pop("releaseChannels", UNSET)
        for release_channels_item_data in _release_channels or []:
            release_channels_item = CreateEnvironmentBodyReleaseChannelsItem.from_dict(release_channels_item_data)

            release_channels.append(release_channels_item)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        create_environment_body = cls(
            system_id=system_id,
            name=name,
            description=description,
            target_filter=target_filter,
            policy_id=policy_id,
            release_channels=release_channels,
            expires_at=expires_at,
        )

        create_environment_body.additional_properties = d
        return create_environment_body

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
