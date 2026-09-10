# Chapter Publishing MCP access and separate admin-server plan

Tracking: DEN-1248. Audited original head: `903b6f8be005138b2730bd47bbc0f48997e1777a`. Original CI failed formatting of generated Rust before lint/tests/stdio could run. This change corrects the compiled repository identity after the rename to `chapter-publishing/cp-mcp-server.rs`, preserving the existing binary/service/environment names for compatibility.

## Implemented regular surface

The process reuses the canonical template's `ore-mcp-org-server` runtime. Admin and non-admin callers admitted to the same stdio process can perform exactly the same six no-argument reads:

| Tool | Admitted non-admin | Admitted admin |
| --- | --- | --- |
| `org_identity` | Compiled organization, repository and service identity | Same |
| `zed_dependency_graph` | Declared dependencies/materialization policy | Same |
| `telemetry_status` | Non-sensitive telemetry initialization flags | Same |
| `shared_auth_policy` | Auth policy and configuration-presence guidance | Same |
| `environment_policy` | Environment encryption policy | Same |
| `security_baseline` | Baseline security declarations | Same |

This does not authenticate an MCP caller, prove production health, expose customer manuscripts/logs, change membership, publish/delete works, change payouts, or decrypt/export credentials. Process launch permission is not per-user authorization. A role or tenant value supplied in a tool argument must not grant privileges. The pinned template action tests the actual complete six-tool catalog, compiled identity, forged identity arguments, unknown actions and clean stdio shutdown; it does not certify JWT/session/tenant authorization.

## Planned `chapter-publishing/cp-admin-mcp-server.rs`

Plan only: no admin endpoint or credentials are enabled. Both repository families must reuse `ORESoftware/org-mcp-server-template.rs`, with a reviewed immutable template revision and the shared MCP crates. The current regular CI directly consumes the reusable action at `c52be23e082753c27ca392fb2f439c764d3ca95e`, merged by template PR #9. Preserve package/service names unless a separate compatibility migration is reviewed.

The admin sibling needs independent repository membership, service/workload identity, secrets, OAuth audience, VPC/network access and release approval. Regular credentials must not access its backends. Share contracts from interfaces (independent TypeSpec and JSON Schema), domain/config through lib-core and Diesel/SeaORM operations through orm-core.

Potential typed admin actions include scoped publishing approval/revocation, membership/role management, retention/legal-hold management and approved financial adjustments. These are design candidates, not existing features. Keep them off the regular six-tool surface. Require verified shared-auth claims and current tenant/resource membership on each call, step-up human approval for publishing/destructive/financial effects, idempotency, appropriate transaction/fencing/money invariants and redacted ores-otel audit events. No arbitrary shell, SQL, secret export or implicit cross-tenant superuser access.

Acceptance requires same-tenant authorized admin success and anonymous, ordinary-user, forged-role, wrong-audience, expired/revoked, cross-tenant, replay and regular-credential denial, plus unchanged legitimate ordinary-user reads. Run full paired-test-org protocol/auth tests and separate deployed endpoint checks before activation. Documentation, read-only annotations and a green template smoke test do not satisfy all of these requirements.
