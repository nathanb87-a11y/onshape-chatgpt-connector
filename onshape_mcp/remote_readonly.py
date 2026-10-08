"""Read-only remote MCP endpoint for ChatGPT.

Updated: 2026-10-08 (Central Time)
This is intentionally a separate MCP server: Jarvis's original server exposes
mutating tools, which must never be reachable through this read-only endpoint.
"""

import hmac
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.responses import PlainTextResponse

from .api.client import OnshapeClient, OnshapeCredentials
from .api.documents import DocumentManager

load_dotenv()
mcp = FastMCP("onshape-readonly", stateless_http=True, json_response=True)


def _allowed_documents() -> set[str]:
    ids = os.getenv("ONSHAPE_ALLOWED_DOCUMENT_IDS", "")
    values = [value.strip() for value in ids.split(",")]
    if not ids or any(len(value) != 24 or not all(ch in "0123456789abcdefABCDEF" for ch in value) for value in values):
        raise RuntimeError("Configure valid ONSHAPE_ALLOWED_DOCUMENT_IDS")
    return set(values)



def _documents() -> DocumentManager:
    """Construct an API client without ever returning credentials to MCP."""
    access = os.getenv("ONSHAPE_ACCESS_KEY") or os.getenv("ONSHAPE_API_KEY")
    secret = os.getenv("ONSHAPE_SECRET_KEY") or os.getenv("ONSHAPE_API_SECRET")
    if not access or not secret:
        raise RuntimeError("Onshape credentials are not configured")
    return DocumentManager(OnshapeClient(OnshapeCredentials(access_key=access, secret_key=secret)))


@mcp.tool()
async def list_documents(limit: int = 20) -> list[dict]:
    """List Onshape documents (read-only; maximum 50)."""
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")
    allowed = _allowed_documents()
    docs = [await _documents().get_document(doc_id) for doc_id in sorted(allowed)[:limit]]
    return [{"id": d.id, "name": d.name, "public": d.public} for d in docs]


@mcp.tool()
async def get_document(document_id: str) -> dict:
    """Read a document's basic metadata; does not modify geometry."""
    if not document_id or len(document_id) > 128 or not document_id.isalnum():
        raise ValueError("Invalid document ID")
    if document_id not in _allowed_documents():
        raise ValueError("Document not authorized")
    d = await _documents().get_document(document_id)
    return {"id": d.id, "name": d.name, "public": d.public}


class BearerGuard:
    """Reject unauthenticated requests before MCP sees them.

    Use a TLS-terminating trusted reverse proxy for internet deployment.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        token = os.getenv("MCP_BEARER_TOKEN", "")
        headers = dict(scope.get("headers", []))
        supplied = headers.get(b"authorization", b"").decode("latin-1")
        valid = len(token) >= 32 and hmac.compare_digest(supplied, "Bearer " + token)
        if not valid:
            response = PlainTextResponse("Unauthorized", status_code=401)
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)


# Expose ASGI app for: uvicorn onshape_mcp.remote_readonly:app --host 127.0.0.1 --port 3000
app = BearerGuard(mcp.streamable_http_app())
