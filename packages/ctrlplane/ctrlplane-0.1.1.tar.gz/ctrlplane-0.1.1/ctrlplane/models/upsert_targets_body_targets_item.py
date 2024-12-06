from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.upsert_targets_body_targets_item_config import UpsertTargetsBodyTargetsItemConfig
    from ..models.upsert_targets_body_targets_item_metadata import UpsertTargetsBodyTargetsItemMetadata
    from ..models.upsert_targets_body_targets_item_variables_item import UpsertTargetsBodyTargetsItemVariablesItem


T = TypeVar("T", bound="UpsertTargetsBodyTargetsItem")


@_attrs_define
class UpsertTargetsBodyTargetsItem:
    """
    Attributes:
        name (str):
        kind (str):
        identifier (str):
        version (str):
        config (UpsertTargetsBodyTargetsItemConfig):
        metadata (Union[Unset, UpsertTargetsBodyTargetsItemMetadata]):
        variables (Union[Unset, List['UpsertTargetsBodyTargetsItemVariablesItem']]):
    """

    name: str
    kind: str
    identifier: str
    version: str
    config: "UpsertTargetsBodyTargetsItemConfig"
    metadata: Union[Unset, "UpsertTargetsBodyTargetsItemMetadata"] = UNSET
    variables: Union[Unset, List["UpsertTargetsBodyTargetsItemVariablesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        kind = self.kind

        identifier = self.identifier

        version = self.version

        config = self.config.to_dict()

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        variables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                variables_item = variables_item_data.to_dict()
                variables.append(variables_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "kind": kind,
                "identifier": identifier,
                "version": version,
                "config": config,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.upsert_targets_body_targets_item_config import UpsertTargetsBodyTargetsItemConfig
        from ..models.upsert_targets_body_targets_item_metadata import UpsertTargetsBodyTargetsItemMetadata
        from ..models.upsert_targets_body_targets_item_variables_item import UpsertTargetsBodyTargetsItemVariablesItem

        d = src_dict.copy()
        name = d.pop("name")

        kind = d.pop("kind")

        identifier = d.pop("identifier")

        version = d.pop("version")

        config = UpsertTargetsBodyTargetsItemConfig.from_dict(d.pop("config"))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, UpsertTargetsBodyTargetsItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = UpsertTargetsBodyTargetsItemMetadata.from_dict(_metadata)

        variables = []
        _variables = d.pop("variables", UNSET)
        for variables_item_data in _variables or []:
            variables_item = UpsertTargetsBodyTargetsItemVariablesItem.from_dict(variables_item_data)

            variables.append(variables_item)

        upsert_targets_body_targets_item = cls(
            name=name,
            kind=kind,
            identifier=identifier,
            version=version,
            config=config,
            metadata=metadata,
            variables=variables,
        )

        upsert_targets_body_targets_item.additional_properties = d
        return upsert_targets_body_targets_item

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
