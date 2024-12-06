from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetJobResponse200Deployment")


@_attrs_define
class GetJobResponse200Deployment:
    """
    Attributes:
        id (str):
        slug (str):
        system_id (str):
        job_agent_id (str):
        name (Union[Unset, str]):
    """

    id: str
    slug: str
    system_id: str
    job_agent_id: str
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        slug = self.slug

        system_id = self.system_id

        job_agent_id = self.job_agent_id

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "slug": slug,
                "systemId": system_id,
                "jobAgentId": job_agent_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        slug = d.pop("slug")

        system_id = d.pop("systemId")

        job_agent_id = d.pop("jobAgentId")

        name = d.pop("name", UNSET)

        get_job_response_200_deployment = cls(
            id=id,
            slug=slug,
            system_id=system_id,
            job_agent_id=job_agent_id,
            name=name,
        )

        get_job_response_200_deployment.additional_properties = d
        return get_job_response_200_deployment

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
