#!/usr/bin/env sh

project="${1:-.}"
if command -v uv >/dev/null 2>&1; then
    uv run --project="$project" tieba-sign
else
    PYTHONPATH="$project" python "$project/src/tieba_sign"
fi
