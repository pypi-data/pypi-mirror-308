import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_job_response_200_status import GetJobResponse200Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_job_response_200_approval_type_0 import GetJobResponse200ApprovalType0
    from ..models.get_job_response_200_deployment import GetJobResponse200Deployment
    from ..models.get_job_response_200_environment import GetJobResponse200Environment
    from ..models.get_job_response_200_job_agent_config import GetJobResponse200JobAgentConfig
    from ..models.get_job_response_200_release import GetJobResponse200Release
    from ..models.get_job_response_200_runbook import GetJobResponse200Runbook
    from ..models.get_job_response_200_target import GetJobResponse200Target
    from ..models.get_job_response_200_variables import GetJobResponse200Variables


T = TypeVar("T", bound="GetJobResponse200")


@_attrs_define
class GetJobResponse200:
    """
    Attributes:
        id (str):
        status (GetJobResponse200Status):
        variables (GetJobResponse200Variables):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        job_agent_config (GetJobResponse200JobAgentConfig): Configuration for the Job Agent
        external_id (Union[None, Unset, str]): External job identifier (e.g. GitHub workflow run ID)
        release (Union[Unset, GetJobResponse200Release]):
        deployment (Union[Unset, GetJobResponse200Deployment]):
        runbook (Union[Unset, GetJobResponse200Runbook]):
        target (Union[Unset, GetJobResponse200Target]):
        environment (Union[Unset, GetJobResponse200Environment]):
        approval (Union['GetJobResponse200ApprovalType0', None, Unset]):
    """

    id: str
    status: GetJobResponse200Status
    variables: "GetJobResponse200Variables"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    job_agent_config: "GetJobResponse200JobAgentConfig"
    external_id: Union[None, Unset, str] = UNSET
    release: Union[Unset, "GetJobResponse200Release"] = UNSET
    deployment: Union[Unset, "GetJobResponse200Deployment"] = UNSET
    runbook: Union[Unset, "GetJobResponse200Runbook"] = UNSET
    target: Union[Unset, "GetJobResponse200Target"] = UNSET
    environment: Union[Unset, "GetJobResponse200Environment"] = UNSET
    approval: Union["GetJobResponse200ApprovalType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_job_response_200_approval_type_0 import GetJobResponse200ApprovalType0

        id = self.id

        status = self.status.value

        variables = self.variables.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        job_agent_config = self.job_agent_config.to_dict()

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

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

        approval: Union[Dict[str, Any], None, Unset]
        if isinstance(self.approval, Unset):
            approval = UNSET
        elif isinstance(self.approval, GetJobResponse200ApprovalType0):
            approval = self.approval.to_dict()
        else:
            approval = self.approval

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "status": status,
                "variables": variables,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "jobAgentConfig": job_agent_config,
            }
        )
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
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
        if approval is not UNSET:
            field_dict["approval"] = approval

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_job_response_200_approval_type_0 import GetJobResponse200ApprovalType0
        from ..models.get_job_response_200_deployment import GetJobResponse200Deployment
        from ..models.get_job_response_200_environment import GetJobResponse200Environment
        from ..models.get_job_response_200_job_agent_config import GetJobResponse200JobAgentConfig
        from ..models.get_job_response_200_release import GetJobResponse200Release
        from ..models.get_job_response_200_runbook import GetJobResponse200Runbook
        from ..models.get_job_response_200_target import GetJobResponse200Target
        from ..models.get_job_response_200_variables import GetJobResponse200Variables

        d = src_dict.copy()
        id = d.pop("id")

        status = GetJobResponse200Status(d.pop("status"))

        variables = GetJobResponse200Variables.from_dict(d.pop("variables"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        job_agent_config = GetJobResponse200JobAgentConfig.from_dict(d.pop("jobAgentConfig"))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("externalId", UNSET))

        _release = d.pop("release", UNSET)
        release: Union[Unset, GetJobResponse200Release]
        if isinstance(_release, Unset):
            release = UNSET
        else:
            release = GetJobResponse200Release.from_dict(_release)

        _deployment = d.pop("deployment", UNSET)
        deployment: Union[Unset, GetJobResponse200Deployment]
        if isinstance(_deployment, Unset):
            deployment = UNSET
        else:
            deployment = GetJobResponse200Deployment.from_dict(_deployment)

        _runbook = d.pop("runbook", UNSET)
        runbook: Union[Unset, GetJobResponse200Runbook]
        if isinstance(_runbook, Unset):
            runbook = UNSET
        else:
            runbook = GetJobResponse200Runbook.from_dict(_runbook)

        _target = d.pop("target", UNSET)
        target: Union[Unset, GetJobResponse200Target]
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = GetJobResponse200Target.from_dict(_target)

        _environment = d.pop("environment", UNSET)
        environment: Union[Unset, GetJobResponse200Environment]
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = GetJobResponse200Environment.from_dict(_environment)

        def _parse_approval(data: object) -> Union["GetJobResponse200ApprovalType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                approval_type_0 = GetJobResponse200ApprovalType0.from_dict(data)

                return approval_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GetJobResponse200ApprovalType0", None, Unset], data)

        approval = _parse_approval(d.pop("approval", UNSET))

        get_job_response_200 = cls(
            id=id,
            status=status,
            variables=variables,
            created_at=created_at,
            updated_at=updated_at,
            job_agent_config=job_agent_config,
            external_id=external_id,
            release=release,
            deployment=deployment,
            runbook=runbook,
            target=target,
            environment=environment,
            approval=approval,
        )

        get_job_response_200.additional_properties = d
        return get_job_response_200

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
