from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_next_jobs_response_200_jobs_item_job_agent_config import (
        GetNextJobsResponse200JobsItemJobAgentConfig,
    )


T = TypeVar("T", bound="GetNextJobsResponse200JobsItem")


@_attrs_define
class GetNextJobsResponse200JobsItem:
    """
    Attributes:
        id (str): The job ID
        status (str):
        job_agent_id (str):
        job_agent_config (GetNextJobsResponse200JobsItemJobAgentConfig):
        message (str):
        release_job_trigger_id (str):
    """

    id: str
    status: str
    job_agent_id: str
    job_agent_config: "GetNextJobsResponse200JobsItemJobAgentConfig"
    message: str
    release_job_trigger_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        status = self.status

        job_agent_id = self.job_agent_id

        job_agent_config = self.job_agent_config.to_dict()

        message = self.message

        release_job_trigger_id = self.release_job_trigger_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "jobAgentId": job_agent_id,
                "jobAgentConfig": job_agent_config,
                "message": message,
                "releaseJobTriggerId": release_job_trigger_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_next_jobs_response_200_jobs_item_job_agent_config import (
            GetNextJobsResponse200JobsItemJobAgentConfig,
        )

        d = src_dict.copy()
        id = d.pop("id")

        status = d.pop("status")

        job_agent_id = d.pop("jobAgentId")

        job_agent_config = GetNextJobsResponse200JobsItemJobAgentConfig.from_dict(d.pop("jobAgentConfig"))

        message = d.pop("message")

        release_job_trigger_id = d.pop("releaseJobTriggerId")

        get_next_jobs_response_200_jobs_item = cls(
            id=id,
            status=status,
            job_agent_id=job_agent_id,
            job_agent_config=job_agent_config,
            message=message,
            release_job_trigger_id=release_job_trigger_id,
        )

        get_next_jobs_response_200_jobs_item.additional_properties = d
        return get_next_jobs_response_200_jobs_item

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
