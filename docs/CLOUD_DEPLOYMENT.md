# Cloud deployment preparation

Updated: 2026-10-08 (Central Time)

## Status
Prepared only; not deployed. The current endpoint requires a static bearer
token and must not be assumed compatible with ChatGPT's remote MCP connection
flow until tested. For a production multi-user integration, implement OAuth
resource-server validation, audience checking, and least-privilege access.

## Render deployment
1. Review the branch and merge only after tests pass.
2. In Render, create a Blueprint from the GitHub repository.
3. Supply ONSHAPE_ACCESS_KEY and ONSHAPE_SECRET_KEY as secret environment
   variables, not in GitHub or chat.
4. Generate a separate random MCP_BEARER_TOKEN with at least 32 characters.
5. Deploy the starter web service; Render terminates public HTTPS.
6. Confirm unauthenticated GET /mcp returns 401, and the endpoint lists
   only list_documents and get_document when authenticated.
7. Verify the exact authentication options available in ChatGPT's custom
   MCP connector before attempting connection. Static bearer headers may
   not be supported by every client or account configuration.

## Security review before connecting real documents
- This pilot uses a shared service identity; it has no per-user isolation.
- Restrict Onshape API credentials to minimum available scopes.
- Do not deploy the full Jarvis stdio tool catalog.
- Keep production credentials out of build-time environment and image layers.
- Apply cloud-side rate limits and logging redaction.
- Verify MCP transport origin validation, proxy behavior, and request limits.
- Add authenticated health checks without disclosing document information.
- Rotate credentials if exposed, and turn off the service if compromised.

## Smoke tests
Run `pytest -q -o addopts='' tests/test_remote_readonly.py` after installing
project dependencies. Then test real MCP initialization and list_tools using
an MCP client; neither is verified by the offline middleware tests alone.

## Rollback
Disable the Render service or roll back its deployment. No Onshape writes
are exposed through this pilot.
