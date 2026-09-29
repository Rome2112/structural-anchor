# Structural Anchor

A lightweight deterministic structural anchor for AI pipelines.

This project is intentionally narrow and practical:

- preserve a known schema deterministically
- fill missing values with `validated_token_{index}`
- reduce token waste and structural drift in LLM-driven workflows
- keep output shape stable even when the model supplies only sparse intent

## Why this exists

Large language models are powerful at intent extraction, but they can drift when asked to produce full structured output from scratch. Structural Anchor solves that by separating the two concerns:

- the LLM handles meaning
- the engine preserves shape

## Core behavior

```python
from structural_anchor import StructuralAnchor

schema = ["request_id", "status", "payload_hash", "execution_metric"]
anchor = StructuralAnchor(schema)

output, latency_ms = anchor.parse_isomorphic({
    "request_id": "REQ_1001",
    "status": "200_OK",
})

print(output)
# {
#   "request_id": "REQ_1001",
#   "status": "200_OK",
#   "payload_hash": "validated_token_2",
#   "execution_metric": "validated_token_3",
# }
```

## Use cases

- API payload completion
- LLM-to-JSON shape enforcement
- schema-constrained workflow steps
- deterministic downstream processing

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m unittest discover -s tests -v
```

## Design principle

This is not a universal graph matcher or a general-purpose AST engine.
It is a deterministic structural anchor built to reduce token waste and stabilize output shape in AI pipelines.
