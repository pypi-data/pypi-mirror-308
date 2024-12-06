from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

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
        name (str):
        description (Union[Unset, str]):
        release_filter (Union[Unset, CreateReleaseChannelBodyReleaseFilter]):
    """

    name: str
    description: Union[Unset, str] = UNSET
    release_filter: Union[Unset, "CreateReleaseChannelBodyReleaseFilter"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        release_filter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.release_filter, Unset):
            release_filter = self.release_filter.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if release_filter is not UNSET:
            field_dict["releaseFilter"] = release_filter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_release_channel_body_release_filter import CreateReleaseChannelBodyReleaseFilter

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description", UNSET)

        _release_filter = d.pop("releaseFilter", UNSET)
        release_filter: Union[Unset, CreateReleaseChannelBodyReleaseFilter]
        if isinstance(_release_filter, Unset):
            release_filter = UNSET
        else:
            release_filter = CreateReleaseChannelBodyReleaseFilter.from_dict(_release_filter)

        create_release_channel_body = cls(
            name=name,
            description=description,
            release_filter=release_filter,
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
