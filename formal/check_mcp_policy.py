#!/usr/bin/env python3
"""Fail-closed finite MCP policy explorer; model-only, not runtime proof.

Works under python -O. The real pinned Rust MCP server is separately tested
by the repository's access-boundary and JSON-RPC stdio tests.
"""
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = (
    "org_identity", "zed_dependency_graph", "telemetry_status",
    "shared_auth_policy", "environment_policy", "security_baseline",
)
FORBIDDEN_TOOLS = ("delete_repository", "write_file", "list_secrets",
                   "execute_shell", "read_credentials", "admin_mutate")


class PolicyError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PolicyError(message)


def admit_tool(declared, mutation, credential):
    return declared is True and mutation is False and credential is False


def admit_stdout(protocol_frame, secret, diagnostic):
    return protocol_frame is True and secret is False and diagnostic is False


def check_reference(readme, source, tools=TOOLS):
    require("run_stdio(OrgSpec" in source, "missing Rust MCP stdio boundary")
    require('organization: "chapter-publishing"' in source,
            "MCP organization mismatch")
    require('repository: "chapter-publishing/cp-mcp-server.rs"' in source,
            "MCP repository mismatch")
    require("read-only" in readme.lower(), "read-only promise missing")
    require(len(tools) == 6 and set(tools) == set(TOOLS),
            "MCP documented tool inventory drift")
    for name in tools:
        require(readme.count(chr(96) + name + chr(96)) >= 1,
                f"undocumented tool: {name}")
    for forbidden in FORBIDDEN_TOOLS:
        require(forbidden not in tools, f"forbidden tool: {forbidden}")


def check_policy():
    total = 0
    admitted = 0
    for known, mutation, credential, jsonrpc, secret, diagnostic in product(
        (False, True), repeat=6
    ):
        tool_ok = admit_tool(known, mutation, credential)
        wire_ok = admit_stdout(jsonrpc, secret, diagnostic)
        if tool_ok and wire_ok:
            admitted += 1
            require(known and not mutation and not credential,
                    "unsafe MCP method admitted")
            require(jsonrpc and not secret and not diagnostic,
                    "unsafe stdout frame admitted")
        if mutation or credential or not known or secret or diagnostic or not jsonrpc:
            require(not (tool_ok and wire_ok), "unsafe combined state")
        total += 1
    require(total == 64 and admitted == 1, "vacuous model")
    for forbidden in FORBIDDEN_TOOLS:
        require(not admit_tool(forbidden in TOOLS, False, False),
                "forbidden tool accepted")
    return total


def run():
    check_reference((ROOT / "README.md").read_text(encoding="utf-8"),
                    (ROOT / "src/main.rs").read_text(encoding="utf-8"))
    total = check_policy()
    print(f"MCP policy: {total} abstract states, {len(FORBIDDEN_TOOLS)} denied tools; guest NOT_EXECUTED")


if __name__ == "__main__":
    run()
