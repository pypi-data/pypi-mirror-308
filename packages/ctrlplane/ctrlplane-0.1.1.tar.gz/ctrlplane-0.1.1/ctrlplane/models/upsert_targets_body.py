from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.upsert_targets_body_targets_item import UpsertTargetsBodyTargetsItem


T = TypeVar("T", bound="UpsertTargetsBody")


@_attrs_define
class UpsertTargetsBody:
    """
    Attributes:
        workspace_id (UUID):
        targets (List['UpsertTargetsBodyTargetsItem']):
    """

    workspace_id: UUID
    targets: List["UpsertTargetsBodyTargetsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workspace_id = str(self.workspace_id)

        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workspaceId": workspace_id,
                "targets": targets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.upsert_targets_body_targets_item import UpsertTargetsBodyTargetsItem

        d = src_dict.copy()
        workspace_id = UUID(d.pop("workspaceId"))

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:
            targets_item = UpsertTargetsBodyTargetsItem.from_dict(targets_item_data)

            targets.append(targets_item)

        upsert_targets_body = cls(
            workspace_id=workspace_id,
            targets=targets,
        )

        upsert_targets_body.additional_properties = d
        return upsert_targets_body

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
