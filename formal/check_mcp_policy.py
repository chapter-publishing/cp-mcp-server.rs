#!/usr/bin/env python3
"""Finite MCP read-only policy explorer; abstract model, not runtime proof."""
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = (
    "org_identity", "zed_dependency_graph", "telemetry_status",
    "shared_auth_policy", "environment_policy", "security_baseline",
)


def admit_tool(declared, mutation, credential):
    return declared and not mutation and not credential


def admit_stdout(protocol_frame, secret, diagnostic):
    return protocol_frame and not secret and not diagnostic


def run():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    source = (ROOT / "src/main.rs").read_text(encoding="utf-8")
    assert "run_stdio(OrgSpec" in source
    assert 'organization: "chapter-publishing"' in source
    assert "read-only" in readme.lower()
    assert len(TOOLS) == len(set(TOOLS))
    for name in TOOLS:
        assert readme.count(chr(96) + name + chr(96)) >= 1, name

    cases = 0
    admitted = 0
    for known, mutation, credential, jsonrpc, secret, diagnostic in product(
        (False, True), repeat=6
    ):
        tool_ok = admit_tool(known, mutation, credential)
        wire_ok = admit_stdout(jsonrpc, secret, diagnostic)
        if tool_ok and wire_ok:
            admitted += 1
            assert known and not mutation and not credential
            assert jsonrpc and not secret and not diagnostic
        if mutation or credential or not known or secret or diagnostic or not jsonrpc:
            assert not (tool_ok and wire_ok)
        cases += 1
    assert cases == 64 and admitted == 1
    for forbidden in ("delete_repository", "write_file", "list_secrets"):
        assert forbidden not in TOOLS
        assert not admit_tool(forbidden in TOOLS, False, False)
    print(f"MCP read-only/AttoLang reference policy: {cases} abstract cases, 3 negative controls")


if __name__ == "__main__":
    run()
