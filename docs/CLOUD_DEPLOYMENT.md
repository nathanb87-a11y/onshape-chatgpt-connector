# Cloud deployment preparation

Updated: 2026-10-08 (Central Time)

## Status
Prepared only; not deployed. The current endpoint requires a static bearer
token and must not be assumed compatible with ChatGPT's remote MCP connection
flow until tested. For a production multi-user integration, implement OAuth
resource-server validation, audience checking, and least-privilege access.

## Verified offline baseline (2026-10-08)
- GitHub Actions read-only MCP workflow passed on commit 537c465d35eabfd9ba86112f2c5e02af1a8025bb: Python 3.11 tests and Docker build.
- The offline tests exercise authenticated MCP initialize and tools/list over ASGI HTTP, plus unauthorized request rejection.
- This does **not** prove a real public HTTPS endpoint, ChatGPT connection, or Onshape API access.
- The separate upstream/general workflow still fails during linting.

## Deployment blockers and security decisions
1. **Public hostname:** MCP transport host/origin protections rejected test hosts until the expected localhost:3000 address was used. Before deployment, configure the exact public Render host in the MCP SDK transport-security allowlist and test it behind Render's HTTPS proxy. Do not globally disable DNS rebinding or origin protection. The implementation and API of the installed MCP SDK version must be checked first.
2. **Authentication:** The pilot requires an Authorization: Bearer header. Confirm that the user's ChatGPT custom MCP connector supports this authentication mode. If it does not, implement standards-compliant OAuth with token issuer/audience/scope validation before connecting ChatGPT; never embed the Onshape API key in ChatGPT.
3. **Document authorization:** The service uses a shared Onshape identity. Before accessing real documents, add an explicit document allowlist or equivalent least-privilege restriction; list_documents currently enumerates documents visible to the API key.
4. **Transport and exposure:** Confirm Render's host, forwarded-header, proxy, TLS and health-check behavior. Test rejected requests, malformed payloads, and error redaction. Keep the read-only tool allowlist unchanged.
5. **Secrets:** Store Onshape keys and MCP tokens only as Render secrets, not in GitHub, images, CI logs, or chat. Rotate compromised secrets.
6. **Release gate:** Do not merge or deploy as production-ready until the above controls and an authenticated live smoke test have passed.

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
project dependencies. The CI suite now tests initialize and tools/list over the in-process ASGI HTTP transport. A separate test against the deployed HTTPS hostname and a real ChatGPT connector remains required.

## Rollback
Disable the Render service or roll back its deployment. No Onshape writes
are exposed through this pilot.
