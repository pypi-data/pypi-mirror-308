from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_target_by_identifier_response_200 import DeleteTargetByIdentifierResponse200
from ...models.delete_target_by_identifier_response_404 import DeleteTargetByIdentifierResponse404
from ...types import Response


def _get_kwargs(
    workspace_id: str,
    identifier: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/v1/workspaces/{workspace_id}/targets/identifier/{identifier}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]:
    if response.status_code == 200:
        response_200 = DeleteTargetByIdentifierResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = DeleteTargetByIdentifierResponse404.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]:
    """Delete a target by identifier

    Args:
        workspace_id (str):
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        identifier=identifier,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]:
    """Delete a target by identifier

    Args:
        workspace_id (str):
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        identifier=identifier,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]:
    """Delete a target by identifier

    Args:
        workspace_id (str):
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        identifier=identifier,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: str,
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]]:
    """Delete a target by identifier

    Args:
        workspace_id (str):
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DeleteTargetByIdentifierResponse200, DeleteTargetByIdentifierResponse404]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            identifier=identifier,
            client=client,
        )
    ).parsed
