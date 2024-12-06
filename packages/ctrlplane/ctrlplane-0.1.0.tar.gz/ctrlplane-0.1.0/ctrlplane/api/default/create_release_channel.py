from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_release_channel_body import CreateReleaseChannelBody
from ...models.create_release_channel_response_200 import CreateReleaseChannelResponse200
from ...models.create_release_channel_response_401 import CreateReleaseChannelResponse401
from ...models.create_release_channel_response_403 import CreateReleaseChannelResponse403
from ...types import Response


def _get_kwargs(
    deployment_id: str,
    *,
    body: CreateReleaseChannelBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/v1/deployments/{deployment_id}/release-channels",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]:
    if response.status_code == 200:
        response_200 = CreateReleaseChannelResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = CreateReleaseChannelResponse401.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = CreateReleaseChannelResponse403.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    deployment_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateReleaseChannelBody,
) -> Response[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]:
    """Create a release channel

    Args:
        deployment_id (str):
        body (CreateReleaseChannelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]
    """

    kwargs = _get_kwargs(
        deployment_id=deployment_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    deployment_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateReleaseChannelBody,
) -> Optional[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]:
    """Create a release channel

    Args:
        deployment_id (str):
        body (CreateReleaseChannelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]
    """

    return sync_detailed(
        deployment_id=deployment_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    deployment_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateReleaseChannelBody,
) -> Response[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]:
    """Create a release channel

    Args:
        deployment_id (str):
        body (CreateReleaseChannelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]
    """

    kwargs = _get_kwargs(
        deployment_id=deployment_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    deployment_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateReleaseChannelBody,
) -> Optional[Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]]:
    """Create a release channel

    Args:
        deployment_id (str):
        body (CreateReleaseChannelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateReleaseChannelResponse200, CreateReleaseChannelResponse401, CreateReleaseChannelResponse403]
    """

    return (
        await asyncio_detailed(
            deployment_id=deployment_id,
            client=client,
            body=body,
        )
    ).parsed
