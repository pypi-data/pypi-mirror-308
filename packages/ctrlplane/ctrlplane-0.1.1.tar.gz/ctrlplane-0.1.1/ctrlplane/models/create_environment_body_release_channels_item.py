from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateEnvironmentBodyReleaseChannelsItem")


@_attrs_define
class CreateEnvironmentBodyReleaseChannelsItem:
    """
    Attributes:
        channel_id (str):
        deployment_id (str):
    """

    channel_id: str
    deployment_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_id = self.channel_id

        deployment_id = self.deployment_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channelId": channel_id,
                "deploymentId": deployment_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel_id = d.pop("channelId")

        deployment_id = d.pop("deploymentId")

        create_environment_body_release_channels_item = cls(
            channel_id=channel_id,
            deployment_id=deployment_id,
        )

        create_environment_body_release_channels_item.additional_properties = d
        return create_environment_body_release_channels_item

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
