from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.set_target_providers_targets_body_targets_item_config import (
        SetTargetProvidersTargetsBodyTargetsItemConfig,
    )
    from ..models.set_target_providers_targets_body_targets_item_metadata import (
        SetTargetProvidersTargetsBodyTargetsItemMetadata,
    )


T = TypeVar("T", bound="SetTargetProvidersTargetsBodyTargetsItem")


@_attrs_define
class SetTargetProvidersTargetsBodyTargetsItem:
    """
    Attributes:
        identifier (str):
        name (str):
        version (str):
        kind (str):
        config (SetTargetProvidersTargetsBodyTargetsItemConfig):
        metadata (SetTargetProvidersTargetsBodyTargetsItemMetadata):
    """

    identifier: str
    name: str
    version: str
    kind: str
    config: "SetTargetProvidersTargetsBodyTargetsItemConfig"
    metadata: "SetTargetProvidersTargetsBodyTargetsItemMetadata"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier

        name = self.name

        version = self.version

        kind = self.kind

        config = self.config.to_dict()

        metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identifier": identifier,
                "name": name,
                "version": version,
                "kind": kind,
                "config": config,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.set_target_providers_targets_body_targets_item_config import (
            SetTargetProvidersTargetsBodyTargetsItemConfig,
        )
        from ..models.set_target_providers_targets_body_targets_item_metadata import (
            SetTargetProvidersTargetsBodyTargetsItemMetadata,
        )

        d = src_dict.copy()
        identifier = d.pop("identifier")

        name = d.pop("name")

        version = d.pop("version")

        kind = d.pop("kind")

        config = SetTargetProvidersTargetsBodyTargetsItemConfig.from_dict(d.pop("config"))

        metadata = SetTargetProvidersTargetsBodyTargetsItemMetadata.from_dict(d.pop("metadata"))

        set_target_providers_targets_body_targets_item = cls(
            identifier=identifier,
            name=name,
            version=version,
            kind=kind,
            config=config,
            metadata=metadata,
        )

        set_target_providers_targets_body_targets_item.additional_properties = d
        return set_target_providers_targets_body_targets_item

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
