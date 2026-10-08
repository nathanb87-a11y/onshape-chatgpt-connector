"""Offline smoke tests for the isolated read-only MCP endpoint.

Updated: 2026-10-08 (Central Time)
No external network or Onshape credentials required.
"""
import importlib

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
