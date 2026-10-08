# Onshape ChatGPT Connector — Project State

Updated: 2026-10-08 (Central Time)

## Source of truth
Repository: nathanb87-a11y/onshape-chatgpt-connector
Fork upstream: ReshefElisha/jarvis-onshape-mcp
Upstream foundation credited in NOTICE: hedless/onshape-mcp
Baseline: upstream fork main; this development branch now contains read-only MCP pilot code, offline tests, and deployment scaffolding.

## Verified by repository inspection
- Fork exists and GitHub reports write access.
- pyproject.toml identifies package onshape-mcp v1.2.0, Python >=3.10.
- Existing LICENSE and NOTICE attribute MIT terms and upstream work.
- README describes API-key authentication, local stdio MCP, variable editing, feature operations, rendering, and export.

## Not yet verified
- No Onshape account connection, API calls, runtime tests, or live model edits performed.
- ChatGPT HTTPS MCP transport, authentication, and deployment have not been validated.
- No proof yet that arbitrary existing sketch dimensions can be safely edited.
- README functionality claims are not acceptance-test results.

## Target milestones
1. Inventory server/tool architecture and security boundaries.
2. Add authenticated HTTPS MCP transport compatible with ChatGPT, without exposing API keys.
3. Connect read-only to Onshape and inspect a disposable Part Studio.
4. Change one named variable on a disposable model, verify regeneration, and compare geometry.
5. Export STL and STEP; verify geometry and units.
6. Document deployment, rollback, and reproducible smoke tests.

## Current status
- Implemented: isolated two-tool read-only Streamable HTTP endpoint with bearer guard.
- Added: offline middleware/tool allowlist tests, Dockerfile.readonly, Render blueprint, cloud deployment instructions.
- VERIFIED IN GITHUB ACTIONS (2026-10-08): Python 3.11 read-only security/tool tests passed and Docker image build passed for commit 3caf9ddb59a3001bca28c5a2086c978f5be155b5. These are offline checks, not live protocol or Onshape integration tests.
- VERIFIED on commit 537c465d35eabfd9ba86112f2c5e02af1a8025bb: Python 3.11 tests (including real in-process MCP initialize and tools/list) and Docker image build passed. The .dockerignore change was included.
- NOT DEPLOYED: no Render account connection, Onshape credentials, HTTPS endpoint, or ChatGPT MCP connection has been configured.
- Security: static bearer-token approach requires explicit compatibility verification; OAuth resource-server support is preferable before production use.
- Upstream/general Tests workflow currently fails lint with 1,061 findings in the broader codebase; separate from successful targeted read-only checks.
- AUDITED: docs/CLOUD_DEPLOYMENT.md now identifies public-host transport validation, ChatGPT authentication compatibility, shared-identity document authorization, TLS/proxy configuration, and secret management as release gates.
- Next: implement explicit public-host transport configuration and document access restrictions, validate authentication mode against ChatGPT, then stage a secure deployment with user-managed secrets.
