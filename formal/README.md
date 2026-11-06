# Chapter Publishing MCP formal and AttoLang policy

Run: python3 formal/check_mcp_policy.py

The script enumerates all 64 combinations of modeled tool and stdout
admission. It checks the six advertised read-only tool names against the real
README and validates that src/main.rs uses run_stdio(OrgSpec). Unknown tool
names, mutation requests, credentials, diagnostics and non-protocol stdout
are negative controls. No service credentials are required.

mcp_guards.atto contains pure AttoLang snake_case policy functions.
They are source-level **references**, not compiler-executed functions.
The concrete tools are implemented by an external pinned Rust dependency.
This abstract model does **not** prove that implementation conforms.

Promotion requires an exact AttoLang backend SHA; compiler-executed positive
and negative vectors; and real MCP stdio lifecycle tests with malformed
requests, credentials, prohibited mutations, and diagnostics. Require only
JSON-RPC frames on stdout and SHA-bound concrete runtime evidence.
