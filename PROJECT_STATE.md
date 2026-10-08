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
- NOT VERIFIED: tests could not run because mcp is unavailable and PyPI DNS/network access failed in the execution environment.
- NOT DEPLOYED: no Render account connection, Onshape credentials, HTTPS endpoint, or ChatGPT MCP connection has been configured.
- Security: static bearer-token approach requires explicit compatibility verification; OAuth resource-server support is preferable before production use.
- Next: run tests and MCP protocol handshake in a networked CI runner, audit API client credential handling, then stage cloud deployment.
