//! Fleet-generated organization MCP server entry point.

#[path = "../generated/rust/env.rs"]
mod env;
#[path = "../generated/rust/runtime.rs"]
mod env_runtime;

use ore_mcp_org_server::{run_stdio, OrgSpec};

const DEPENDENCIES: &[&str] = &[
    "ORESoftware/mcp-rust-libs",
    "ores-otel/ores-mcp-server-core-libs.rs",
    "shared-auth/shared-auth-clients",
    "shared-auth/shared-auth-interfaces",
    "shared-auth/shared-auth-lib",
    "zed-pkg/zed-cli",
];

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    run_stdio(OrgSpec {
        organization: "chapter-publishing",
        repository: "chapter-publishing/chapter-publishing-mcp-server.rs",
        service_name: "chapter-publishing-mcp-server",
        package_name: "chapter-publishing-mcp-server",
        dependencies: DEPENDENCIES,
        version: env!("CARGO_PKG_VERSION"),
    })
    .await
}
