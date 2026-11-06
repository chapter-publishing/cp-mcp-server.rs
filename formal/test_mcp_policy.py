"""Adversarial regression suite for fail-closed, abstract MCP/AttoLang policy."""
import sys
import unittest
from pathlib import Path
from itertools import product

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_mcp_policy import (  # noqa: E402
    TOOLS, ROOT, PolicyError, check_reference, check_policy,
    admit_tool, admit_stdout,
)


class MCPPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / "README.md").read_text()
        cls.source = (ROOT / "src/main.rs").read_text()

    def test_finite_model_nonvacuous(self):
        self.assertEqual(check_policy(), 64)
        ok = [(a, b, c, d, e, f) for a, b, c, d, e, f in product((False, True), repeat=6)
              if admit_tool(a, b, c) and admit_stdout(d, e, f)]
        self.assertEqual(ok, [(True, False, False, True, False, False)])

    def test_tool_boundary_rejects_mutation_credentials_and_unknown(self):
        for known, mutating, credential in product((False, True), repeat=3):
            self.assertEqual(admit_tool(known, mutating, credential),
                             known and not mutating and not credential)

    def test_truthy_nonboolean_inputs_fail_closed(self):
        for value in (1, "true", [], object()):
            with self.subTest(value=repr(value)):
                self.assertFalse(admit_tool(value, False, False))
                self.assertFalse(admit_tool(True, value, False))
                self.assertFalse(admit_stdout(value, False, False))
                self.assertFalse(admit_stdout(True, value, False))

    def test_readme_and_source_are_wired(self):
        self.assertIsNone(check_reference(self.readme, self.source))

    def test_missing_tool_documentation_is_rejected(self):
        for name in TOOLS:
            with self.subTest(name=name):
                with self.assertRaises(PolicyError):
                    check_reference(self.readme.replace(chr(96) + name + chr(96), "omitted"),
                                    self.source)

    def test_unreviewed_tool_surface_is_rejected(self):
        for extra in ("execute_shell", "delete_repository", "list_secrets"):
            with self.subTest(extra=extra):
                with self.assertRaises(PolicyError):
                    check_reference(self.readme, self.source, (*TOOLS, extra))

    def test_duplicate_tool_is_not_accepted(self):
        with self.assertRaises(PolicyError):
            check_reference(self.readme, self.source, (*TOOLS[:-1], TOOLS[0]))

    def test_mcp_stdio_wiring_cannot_be_removed(self):
        for bad in (
            self.source.replace("run_stdio(OrgSpec", "run_http(OrgSpec"),
            self.source.replace('organization: "chapter-publishing"',
                                'organization: "other"'),
            self.source.replace('repository: "chapter-publishing/cp-mcp-server.rs"',
                                'repository: "other/repo"'),
        ):
            with self.assertRaises(PolicyError):
                check_reference(self.readme, bad)

    def test_secret_frames_and_diagnostics_rejected(self):
        for protocol, secret, diag in product((False, True), repeat=3):
            self.assertEqual(admit_stdout(protocol, secret, diag),
                             protocol and not secret and not diag)


if __name__ == "__main__":
    unittest.main()
