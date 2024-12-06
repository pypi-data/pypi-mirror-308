from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.acknowledge_agent_job_response_200 import AcknowledgeAgentJobResponse200
from ...models.acknowledge_agent_job_response_401 import AcknowledgeAgentJobResponse401
from ...models.acknowledge_agent_job_response_404 import AcknowledgeAgentJobResponse404
from ...types import Response


def _get_kwargs(
    agent_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/v1/job-agents/{agent_id}/queue/acknowledge",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]:
    if response.status_code == 200:
        response_200 = AcknowledgeAgentJobResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = AcknowledgeAgentJobResponse401.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = AcknowledgeAgentJobResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]:
    """Acknowledge a job for an agent

     Marks a job as acknowledged by the agent

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]:
    """Acknowledge a job for an agent

     Marks a job as acknowledged by the agent

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]
    """

    return sync_detailed(
        agent_id=agent_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]:
    """Acknowledge a job for an agent

     Marks a job as acknowledged by the agent

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]]:
    """Acknowledge a job for an agent

     Marks a job as acknowledged by the agent

    Args:
        agent_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AcknowledgeAgentJobResponse200, AcknowledgeAgentJobResponse401, AcknowledgeAgentJobResponse404]
    """

    return (
        await asyncio_detailed(
            agent_id=agent_id,
            client=client,
        )
    ).parsed
