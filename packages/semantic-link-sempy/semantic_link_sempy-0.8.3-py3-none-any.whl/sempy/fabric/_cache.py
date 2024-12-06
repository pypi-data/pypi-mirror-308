import threading
from uuid import UUID

from sempy.fabric._token_provider import SynapseTokenProvider
from sempy.fabric._client import WorkspaceClient
from sempy.fabric._client._fabric_rest_api import _FabricRestAPI
from typing import Dict, Optional, Union


_workspace_clients: Dict[Optional[Union[str, UUID]], WorkspaceClient] = dict()
_workspace_clients_lock = threading.RLock()
_fabric_rest_api: Optional[_FabricRestAPI] = None
_fabric_rest_api_lock = threading.RLock()


def _get_or_create_workspace_client(workspace_name: Optional[Union[str, UUID]]) -> WorkspaceClient:
    global _workspace_clients

    if workspace_name in _workspace_clients:
        return _workspace_clients[workspace_name]

    with _workspace_clients_lock:
        if workspace_name in _workspace_clients:
            return _workspace_clients[workspace_name]
        client = WorkspaceClient(workspace_name)
        _workspace_clients[workspace_name] = client

    return client


def _get_fabric_rest_api() -> _FabricRestAPI:
    global _fabric_rest_api

    if _fabric_rest_api is not None:
        return _fabric_rest_api

    with _fabric_rest_api_lock:

        if _fabric_rest_api is not None:
            return _fabric_rest_api

        # cache FabricRestAPI client to re-use HTTP socket
        _fabric_rest_api = _FabricRestAPI(SynapseTokenProvider())

    return _fabric_rest_api
