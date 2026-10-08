# Agent instructions

Updated: 2026-10-08 (Central Time)

## Repository purpose
This fork of ReshefElisha/jarvis-onshape-mcp is an independent project to evaluate and implement a secure ChatGPT-to-Onshape MCP integration. Do not modify the Fourier DIW repository here.

## Before changing code
1. Read this file and PROJECT_STATE.md completely.
2. Confirm branch, commit, working tree, and upstream status.
3. Inspect affected implementations and tests. Never infer successful behavior from README claims alone.
4. Preserve LICENSE and NOTICE and upstream attribution.
5. Do not commit credentials, tokens, browser cookies, private document contents, or exported proprietary geometry.
6. Use a feature branch and pull request; keep main stable.
7. Put a Central Time date/time stamp at the top of every modified Python file and document nontrivial changes.
8. Run targeted tests and a smoke test; report exact commands, results, and limitations.

## Safety rules
- Read-only Onshape discovery is the first integration milestone.
- No live CAD edits without explicit user approval and a disposable test document.
- Never log API secrets or expose an unauthenticated public MCP endpoint.
- Require authentication, narrow authorization, and confirmation for mutations; prevent arbitrary document access where feasible.
- Prefer deterministic API operations over browser-coordinate interactions.
- Validate regeneration status and export geometry before reporting success.
