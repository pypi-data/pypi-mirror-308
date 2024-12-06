from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.acknowledge_agent_job_response_200_job import AcknowledgeAgentJobResponse200Job


T = TypeVar("T", bound="AcknowledgeAgentJobResponse200")


@_attrs_define
class AcknowledgeAgentJobResponse200:
    """
    Attributes:
        job (Union[Unset, AcknowledgeAgentJobResponse200Job]):
    """

    job: Union[Unset, "AcknowledgeAgentJobResponse200Job"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.job, Unset):
            job = self.job.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job is not UNSET:
            field_dict["job"] = job

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.acknowledge_agent_job_response_200_job import AcknowledgeAgentJobResponse200Job

        d = src_dict.copy()
        _job = d.pop("job", UNSET)
        job: Union[Unset, AcknowledgeAgentJobResponse200Job]
        if isinstance(_job, Unset):
            job = UNSET
        else:
            job = AcknowledgeAgentJobResponse200Job.from_dict(_job)

        acknowledge_agent_job_response_200 = cls(
            job=job,
        )

        acknowledge_agent_job_response_200.additional_properties = d
        return acknowledge_agent_job_response_200

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
