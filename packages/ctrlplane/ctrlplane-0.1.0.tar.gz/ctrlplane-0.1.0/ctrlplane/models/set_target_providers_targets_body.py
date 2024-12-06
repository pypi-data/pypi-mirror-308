from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.set_target_providers_targets_body_targets_item import SetTargetProvidersTargetsBodyTargetsItem


T = TypeVar("T", bound="SetTargetProvidersTargetsBody")


@_attrs_define
class SetTargetProvidersTargetsBody:
    """
    Attributes:
        targets (List['SetTargetProvidersTargetsBodyTargetsItem']):
    """

    targets: List["SetTargetProvidersTargetsBodyTargetsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "targets": targets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.set_target_providers_targets_body_targets_item import SetTargetProvidersTargetsBodyTargetsItem

        d = src_dict.copy()
        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:
            targets_item = SetTargetProvidersTargetsBodyTargetsItem.from_dict(targets_item_data)

            targets.append(targets_item)

        set_target_providers_targets_body = cls(
            targets=targets,
        )

        set_target_providers_targets_body.additional_properties = d
        return set_target_providers_targets_body

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
