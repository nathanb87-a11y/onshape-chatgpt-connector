# Onshape ChatGPT Connector — Project State

Updated: 2026-10-08 (Central Time)

## Source of truth
Repository: nathanb87-a11y/onshape-chatgpt-connector
Fork upstream: ReshefElisha/jarvis-onshape-mcp
Upstream foundation credited in NOTICE: hedless/onshape-mcp
Baseline: unmodified fork main at project initialization; this branch adds documentation only.

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
Documentation baseline only. No runtime implementation changed in this branch.
