from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetTargetResponse200VariablesItem")


@_attrs_define
class GetTargetResponse200VariablesItem:
    """
    Attributes:
        key (str):
        value (Union[bool, float, str]):
        sensitive (Union[Unset, bool]):  Default: False.
    """

    key: str
    value: Union[bool, float, str]
    sensitive: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key

        value: Union[bool, float, str]
        value = self.value

        sensitive = self.sensitive

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )
        if sensitive is not UNSET:
            field_dict["sensitive"] = sensitive

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        def _parse_value(data: object) -> Union[bool, float, str]:
            return cast(Union[bool, float, str], data)

        value = _parse_value(d.pop("value"))

        sensitive = d.pop("sensitive", UNSET)

        get_target_response_200_variables_item = cls(
            key=key,
            value=value,
            sensitive=sensitive,
        )

        get_target_response_200_variables_item.additional_properties = d
        return get_target_response_200_variables_item

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
