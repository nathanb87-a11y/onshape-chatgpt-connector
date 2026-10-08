# Read-only ChatGPT MCP pilot

Updated: 2026-10-08 (Central Time)

This pilot deliberately exposes only `list_documents` and `get_document`.
The original Jarvis stdio server is unchanged and must **not** be published
directly to the internet.

## Prerequisites
- Python 3.10+ and project dependencies (`uv sync`).
- Onshape API access/secret key, stored in environment variables, not Git.
- A separate randomly generated bearer token of at least 32 characters.
- A trusted HTTPS reverse proxy or authenticated tunnel to localhost.

## Run locally

Set `ONSHAPE_ACCESS_KEY`, `ONSHAPE_SECRET_KEY`, and `MCP_BEARER_TOKEN`
in your process environment. Then:

```sh
uv run uvicorn onshape_mcp.remote_readonly:app --host 127.0.0.1 --port 3000
```

The endpoint is `/mcp`. Requests must carry
`Authorization: Bearer <MCP_BEARER_TOKEN>`.

## Safety and deployment constraints
- Do not publish port 3000 directly. HTTPS is mandatory outside localhost.
- Do not put secrets in a URL, commit, chat, screenshot, or log.
- Keep the token secret; rotate it if exposed.
- The remote endpoint has no write tools; Onshape API credentials should
  additionally be scoped read-only where Onshape supports that scope.
- Before using with ChatGPT, verify the ChatGPT connector's supported
  authentication mechanism. This pilot expects an Authorization bearer
  header; connector compatibility has **not** been tested.
- This implementation has not undergone live integration, security, or
  penetration testing. It is not production-ready.
- Do not deploy the full Jarvis `server.py` to a public endpoint.

## Acceptance tests (pending)
1. Server starts with valid dependencies.
2. Missing/incorrect bearer token receives HTTP 401.
3. Valid bearer token completes MCP initialization.
4. MCP lists exactly two read-only tools.
5. `list_documents` succeeds using test Onshape credentials.
6. `get_document` returns the expected test document.
7. No mutation tools are discoverable or callable.
8. External HTTPS + ChatGPT connector authentication is verified.
