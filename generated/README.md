# Generated environment bindings — do not edit by hand

These environment bindings originate from flags-2-env declarations in the repository's `.cli-flags.toml`. They are not hand-authored application contracts. Public/shared API contracts still belong in the sibling interfaces repository as independently maintained TypeSpec and JSON Schema.

After running the approved upstream flags-2-env generator at a reviewed revision, run:

```sh
bash scripts/format-generated-rust.sh
cargo fmt --all -- --check
cargo clippy --locked --all-targets -- -D warnings
```

The postprocessor is deterministic and contract-aware. It uses Rust 1.88.0, applies rustfmt, preserves the `.cli-flags.toml` `[env].files` selection in generated runtime loading, and scopes a small set of style-only Clippy allowances to generic generated helper functions. The crate-wide `-D warnings` gate remains unchanged for handwritten Rust. It also normalizes generated rustdoc markup so machine-emitted environment-key names do not fail `doc_markdown`.

The repository intentionally declares `[env].files = []`: this MCP server must not silently discover a plaintext root `.env`. Runtime secrets/configuration come from approved environment/secret delivery, and encrypted `env/enc/*.env.enc` remains the version-controlled lifecycle. If the contract later names a decrypted runtime file explicitly, regeneration plus this normalizer must reproduce that exact list.

The formatter leaves Rust outputs read-only in the working directory. Git does not preserve read-only permission bits across fresh checkouts; rerun the generation/normalization pipeline to apply them. Do not bypass this by maintaining a second handwritten copy.

The `mcp-access-boundary` workflow preserves normalized Rust and its diff as an artifact, and then checks for drift. Commit exact generator + normalizer output through a PR; never make CI silently format away an uncommitted difference or skip the existing lint/test chain.
