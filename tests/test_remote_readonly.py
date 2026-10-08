"""Offline smoke tests for the isolated read-only MCP endpoint.

Updated: 2026-10-08 (Central Time)
No external network or Onshape credentials required.
"""
import importlib

import httpx

import pytest
from starlette.responses import PlainTextResponse


async def request_status(app, authorization=None):
    messages = []
    headers = []
    if authorization is not None:
        headers.append((b"authorization", authorization.encode("ascii")))
    scope = {"type": "http", "method": "GET", "path": "/mcp", "headers": headers}

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    await app(scope, receive, send)
    return next(m["status"] for m in messages if m["type"] == "http.response.start")


@pytest.mark.asyncio
@pytest.mark.parametrize("provided,expected", [(None, 401), ("Bearer wrong", 401), ("Bearer " + "a" * 40, 200)])
async def test_authentication(monkeypatch, provided, expected):
    remote = importlib.import_module("onshape_mcp.remote_readonly")
    monkeypatch.setenv("MCP_BEARER_TOKEN", "a" * 40)
    guard = remote.BearerGuard(PlainTextResponse("ok"))
    assert await request_status(guard, provided) == expected


@pytest.mark.asyncio
async def test_weak_server_token_is_rejected(monkeypatch):
    remote = importlib.import_module("onshape_mcp.remote_readonly")
    monkeypatch.setenv("MCP_BEARER_TOKEN", "short")
    assert await request_status(remote.BearerGuard(PlainTextResponse("ok")), "Bearer short") == 401


@pytest.mark.asyncio
async def test_read_only_tool_allowlist():
    remote = importlib.import_module("onshape_mcp.remote_readonly")
    registered = remote.mcp._tool_manager.list_tools()
    assert {tool.name for tool in registered} == {"list_documents", "get_document"}


@pytest.mark.asyncio
async def test_real_mcp_initialize_and_tool_discovery(monkeypatch):
    """Exercise JSON-RPC over actual ASGI HTTP transport, without Onshape keys.

    Start the MCP session manager explicitly, as an ASGI server's lifespan
    normally does. This catches protocol and startup problems that a simple
    tool-registry inspection cannot detect.
    """
    remote = importlib.import_module("onshape_mcp.remote_readonly")
    token = "t" * 40
    monkeypatch.setenv("MCP_BEARER_TOKEN", token)
    transport = httpx.ASGITransport(app=remote.app)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2025-03-26",
    }
    async with remote.mcp.session_manager.run():
        async with httpx.AsyncClient(transport=transport, base_url="http://localhost:3000") as client:
            initialize = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "offline-ci", "version": "1.0"},
                },
            }
            response = await client.post("/mcp", headers=headers, json=initialize)
            assert response.status_code == 200, response.text
            result = response.json()
            assert result["result"]["serverInfo"]["name"] == "onshape-readonly"
            assert "error" not in result

            discovered = await client.post(
                "/mcp",
                headers=headers,
                json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            )
            assert discovered.status_code == 200, discovered.text
            names = {tool["name"] for tool in discovered.json()["result"]["tools"]}
            assert names == {"list_documents", "get_document"}


@pytest.mark.asyncio
async def test_real_mcp_rejects_unauthorized_initialize(monkeypatch):
    """Verify the authentication middleware also protects the real MCP route."""
    remote = importlib.import_module("onshape_mcp.remote_readonly")
    monkeypatch.setenv("MCP_BEARER_TOKEN", "t" * 40)
    transport = httpx.ASGITransport(app=remote.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://localhost:3000") as client:
        response = await client.post(
            "/mcp",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
        )
        assert response.status_code == 401
