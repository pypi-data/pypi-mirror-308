import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_environment_response_200_environment_target_filter import (
        CreateEnvironmentResponse200EnvironmentTargetFilter,
    )


T = TypeVar("T", bound="CreateEnvironmentResponse200Environment")


@_attrs_define
class CreateEnvironmentResponse200Environment:
    """
    Attributes:
        system_id (str):
        expires_at (Union[None, Unset, datetime.datetime]):
        target_filter (Union[Unset, CreateEnvironmentResponse200EnvironmentTargetFilter]):
    """

    system_id: str
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    target_filter: Union[Unset, "CreateEnvironmentResponse200EnvironmentTargetFilter"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        system_id = self.system_id

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        target_filter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.target_filter, Unset):
            target_filter = self.target_filter.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "systemId": system_id,
            }
        )
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
        if target_filter is not UNSET:
            field_dict["targetFilter"] = target_filter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_environment_response_200_environment_target_filter import (
            CreateEnvironmentResponse200EnvironmentTargetFilter,
        )

        d = src_dict.copy()
        system_id = d.pop("systemId")

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expiresAt", UNSET))

        _target_filter = d.pop("targetFilter", UNSET)
        target_filter: Union[Unset, CreateEnvironmentResponse200EnvironmentTargetFilter]
        if isinstance(_target_filter, Unset):
            target_filter = UNSET
        else:
            target_filter = CreateEnvironmentResponse200EnvironmentTargetFilter.from_dict(_target_filter)

        create_environment_response_200_environment = cls(
            system_id=system_id,
            expires_at=expires_at,
            target_filter=target_filter,
        )

        create_environment_response_200_environment.additional_properties = d
        return create_environment_response_200_environment

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
