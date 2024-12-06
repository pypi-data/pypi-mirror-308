from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetJobResponse200Runbook")


@_attrs_define
class GetJobResponse200Runbook:
    """
    Attributes:
        id (str):
        name (str):
        system_id (str):
        job_agent_id (str):
    """

    id: str
    name: str
    system_id: str
    job_agent_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        system_id = self.system_id

        job_agent_id = self.job_agent_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "systemId": system_id,
                "jobAgentId": job_agent_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        system_id = d.pop("systemId")

        job_agent_id = d.pop("jobAgentId")

        get_job_response_200_runbook = cls(
            id=id,
            name=name,
            system_id=system_id,
            job_agent_id=job_agent_id,
        )

        get_job_response_200_runbook.additional_properties = d
        return get_job_response_200_runbook

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
