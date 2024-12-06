from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_agent_running_job_response_200_item_config import GetAgentRunningJobResponse200ItemConfig
    from ..models.get_agent_running_job_response_200_item_deployment import GetAgentRunningJobResponse200ItemDeployment
    from ..models.get_agent_running_job_response_200_item_environment import (
        GetAgentRunningJobResponse200ItemEnvironment,
    )
    from ..models.get_agent_running_job_response_200_item_job_agent_config import (
        GetAgentRunningJobResponse200ItemJobAgentConfig,
    )
    from ..models.get_agent_running_job_response_200_item_release import GetAgentRunningJobResponse200ItemRelease
    from ..models.get_agent_running_job_response_200_item_runbook import GetAgentRunningJobResponse200ItemRunbook
    from ..models.get_agent_running_job_response_200_item_target import GetAgentRunningJobResponse200ItemTarget


T = TypeVar("T", bound="GetAgentRunningJobResponse200Item")


@_attrs_define
class GetAgentRunningJobResponse200Item:
    """
    Attributes:
        id (str):
        status (str):
        message (str):
        job_agent_id (str):
        job_agent_config (GetAgentRunningJobResponse200ItemJobAgentConfig):
        external_id (Union[None, str]):
        config (GetAgentRunningJobResponse200ItemConfig):
        release (Union[Unset, GetAgentRunningJobResponse200ItemRelease]):
        deployment (Union[Unset, GetAgentRunningJobResponse200ItemDeployment]):
        runbook (Union[Unset, GetAgentRunningJobResponse200ItemRunbook]):
        target (Union[Unset, GetAgentRunningJobResponse200ItemTarget]):
        environment (Union[Unset, GetAgentRunningJobResponse200ItemEnvironment]):
    """

    id: str
    status: str
    message: str
    job_agent_id: str
    job_agent_config: "GetAgentRunningJobResponse200ItemJobAgentConfig"
    external_id: Union[None, str]
    config: "GetAgentRunningJobResponse200ItemConfig"
    release: Union[Unset, "GetAgentRunningJobResponse200ItemRelease"] = UNSET
    deployment: Union[Unset, "GetAgentRunningJobResponse200ItemDeployment"] = UNSET
    runbook: Union[Unset, "GetAgentRunningJobResponse200ItemRunbook"] = UNSET
    target: Union[Unset, "GetAgentRunningJobResponse200ItemTarget"] = UNSET
    environment: Union[Unset, "GetAgentRunningJobResponse200ItemEnvironment"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        status = self.status

        message = self.message

        job_agent_id = self.job_agent_id

        job_agent_config = self.job_agent_config.to_dict()

        external_id: Union[None, str]
        external_id = self.external_id

        config = self.config.to_dict()

        release: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.release, Unset):
            release = self.release.to_dict()

        deployment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deployment, Unset):
            deployment = self.deployment.to_dict()

        runbook: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.runbook, Unset):
            runbook = self.runbook.to_dict()

        target: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.target, Unset):
            target = self.target.to_dict()

        environment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "message": message,
                "jobAgentId": job_agent_id,
                "jobAgentConfig": job_agent_config,
                "externalId": external_id,
                "config": config,
            }
        )
        if release is not UNSET:
            field_dict["release"] = release
        if deployment is not UNSET:
            field_dict["deployment"] = deployment
        if runbook is not UNSET:
            field_dict["runbook"] = runbook
        if target is not UNSET:
            field_dict["target"] = target
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_agent_running_job_response_200_item_config import GetAgentRunningJobResponse200ItemConfig
        from ..models.get_agent_running_job_response_200_item_deployment import (
            GetAgentRunningJobResponse200ItemDeployment,
        )
        from ..models.get_agent_running_job_response_200_item_environment import (
            GetAgentRunningJobResponse200ItemEnvironment,
        )
        from ..models.get_agent_running_job_response_200_item_job_agent_config import (
            GetAgentRunningJobResponse200ItemJobAgentConfig,
        )
        from ..models.get_agent_running_job_response_200_item_release import GetAgentRunningJobResponse200ItemRelease
        from ..models.get_agent_running_job_response_200_item_runbook import GetAgentRunningJobResponse200ItemRunbook
        from ..models.get_agent_running_job_response_200_item_target import GetAgentRunningJobResponse200ItemTarget

        d = src_dict.copy()
        id = d.pop("id")

        status = d.pop("status")

        message = d.pop("message")

        job_agent_id = d.pop("jobAgentId")

        job_agent_config = GetAgentRunningJobResponse200ItemJobAgentConfig.from_dict(d.pop("jobAgentConfig"))

        def _parse_external_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        external_id = _parse_external_id(d.pop("externalId"))

        config = GetAgentRunningJobResponse200ItemConfig.from_dict(d.pop("config"))

        _release = d.pop("release", UNSET)
        release: Union[Unset, GetAgentRunningJobResponse200ItemRelease]
        if isinstance(_release, Unset):
            release = UNSET
        else:
            release = GetAgentRunningJobResponse200ItemRelease.from_dict(_release)

        _deployment = d.pop("deployment", UNSET)
        deployment: Union[Unset, GetAgentRunningJobResponse200ItemDeployment]
        if isinstance(_deployment, Unset):
            deployment = UNSET
        else:
            deployment = GetAgentRunningJobResponse200ItemDeployment.from_dict(_deployment)

        _runbook = d.pop("runbook", UNSET)
        runbook: Union[Unset, GetAgentRunningJobResponse200ItemRunbook]
        if isinstance(_runbook, Unset):
            runbook = UNSET
        else:
            runbook = GetAgentRunningJobResponse200ItemRunbook.from_dict(_runbook)

        _target = d.pop("target", UNSET)
        target: Union[Unset, GetAgentRunningJobResponse200ItemTarget]
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = GetAgentRunningJobResponse200ItemTarget.from_dict(_target)

        _environment = d.pop("environment", UNSET)
        environment: Union[Unset, GetAgentRunningJobResponse200ItemEnvironment]
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = GetAgentRunningJobResponse200ItemEnvironment.from_dict(_environment)

        get_agent_running_job_response_200_item = cls(
            id=id,
            status=status,
            message=message,
            job_agent_id=job_agent_id,
            job_agent_config=job_agent_config,
            external_id=external_id,
            config=config,
            release=release,
            deployment=deployment,
            runbook=runbook,
            target=target,
            environment=environment,
        )

        get_agent_running_job_response_200_item.additional_properties = d
        return get_agent_running_job_response_200_item

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
