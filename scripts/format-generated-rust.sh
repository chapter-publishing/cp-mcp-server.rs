#!/usr/bin/env bash
# Deterministic post-generation normalization; no hand-maintained generated Rust.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
files=(generated/rust/env.rs generated/rust/runtime.rs)
for file in "${files[@]}"; do
  [[ -f "$file" && ! -L "$file" ]] || { echo 'Expected regular generated Rust files' >&2; exit 1; }
done
trap 'chmod a-w -- "${files[@]}"' EXIT
chmod u+w -- "${files[@]}"
rustfmt +1.88.0 --edition 2021 --emit files "${files[@]}"
