from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_release_channel_body_release_filter import CreateReleaseChannelBodyReleaseFilter


T = TypeVar("T", bound="CreateReleaseChannelBody")


@_attrs_define
class CreateReleaseChannelBody:
    """
    Attributes:
        deployment_id (str):
        name (str):
        release_filter (CreateReleaseChannelBodyReleaseFilter):
        description (Union[None, Unset, str]):
    """

    deployment_id: str
    name: str
    release_filter: "CreateReleaseChannelBodyReleaseFilter"
    description: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deployment_id = self.deployment_id

        name = self.name

        release_filter = self.release_filter.to_dict()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deploymentId": deployment_id,
                "name": name,
                "releaseFilter": release_filter,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_release_channel_body_release_filter import CreateReleaseChannelBodyReleaseFilter

        d = src_dict.copy()
        deployment_id = d.pop("deploymentId")

        name = d.pop("name")

        release_filter = CreateReleaseChannelBodyReleaseFilter.from_dict(d.pop("releaseFilter"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        create_release_channel_body = cls(
            deployment_id=deployment_id,
            name=name,
            release_filter=release_filter,
            description=description,
        )

        create_release_channel_body.additional_properties = d
        return create_release_channel_body

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
