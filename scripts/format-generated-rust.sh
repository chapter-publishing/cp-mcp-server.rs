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

python3 - <<'PY'
from pathlib import Path
import re
import tomllib

contract = tomllib.loads(Path('.cli-flags.toml').read_text())
env_files = contract.get('env', {}).get('files', [])
if not isinstance(env_files, list) or not all(isinstance(item, str) for item in env_files):
    raise SystemExit('[env].files must be an array of strings')

# flags-2-env emits generic helpers used across many contracts. Keep strict
# crate-wide Clippy while allowing only the known generated-helper style lints.
runtime = Path('generated/rust/runtime.rs')
runtime_text = runtime.read_text()
if '#![allow(dead_code)]' in runtime_text:
    runtime_text = runtime_text.replace(
        '#![allow(dead_code)]',
        '#![allow(\n'
        '    dead_code,\n'
        '    clippy::needless_pass_by_value,\n'
        '    clippy::map_unwrap_or,\n'
        '    clippy::match_like_matches_macro,\n'
        '    clippy::unnecessary_wraps\n'
        ')]',
        1,
    )
serialized = ', '.join(repr(item).replace("'", '"') for item in env_files)
runtime_text, count = re.subn(
    r'load_dotenv_files\(&\[[^\]]*\]\)',
    f'load_dotenv_files(&[{serialized}])',
    runtime_text,
    count=1,
)
if count != 1:
    raise SystemExit('expected one generated load_dotenv_files call')
runtime_text = runtime_text.replace(
    '/// Effectful overlay: `.env` files then the process environment, ranked per key.',
    '/// Effectful overlay: configured env files then the process environment, ranked per key.',
)
runtime.write_text(runtime_text)

env = Path('generated/rust/env.rs')
env_text = env.read_text()
if '#![allow(dead_code)]' in env_text:
    env_text = env_text.replace('#![allow(dead_code)]', '#![allow(dead_code, clippy::doc_markdown)]', 1)
env_text = re.sub(
    r'/// Runtime environment key ([A-Z][A-Z0-9_]+)\.',
    r'/// Runtime environment key `\1`.',
    env_text,
)
env.write_text(env_text)
PY

rustfmt +1.88.0 --edition 2021 --emit files "${files[@]}"
