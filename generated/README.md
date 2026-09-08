# Generated environment bindings — do not edit by hand

These environment bindings originate from flags-2-env declarations in the repository's `.cli-flags.toml`. They are not hand-authored application contracts. Public/shared API contracts still belong in the sibling interfaces repository as independently maintained TypeSpec and JSON Schema.

After running the approved upstream flags-2-env generator at a reviewed revision, run:

```sh
bash scripts/format-generated-rust.sh
cargo fmt --all -- --check
```

The formatter uses Rust 1.88.0, matching this repository's required CI toolchain, and leaves Rust outputs read-only in the working directory. Git does not preserve read-only permission bits across fresh checkouts; rerun the generation/normalization pipeline to apply them. Do not bypass this by maintaining a second handwritten copy.

The formatter is a deterministic post-generation step, not the generator and not a TypeSpec/JSON Schema parity verifier. The September 2026 repair normalizes existing generated Rust with actual rustfmt output; it does not claim that the upstream generator was rerun. Future regeneration must run the same postprocessor to avoid restoring the formatting failure.

The `mcp-access-boundary` workflow preserves normalized Rust and its diff as an artifact, and then checks for drift. Commit the exact formatter output through a PR; never make CI silently format away an uncommitted difference or skip the existing lint/test chain.
