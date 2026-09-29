from __future__ import annotations

from typing import Any, Protocol

from .controller import StructuralAnchor


class SparseLLMAdapter(Protocol):
    def generate_sparse(self, prompt: str, schema: list[str]) -> dict[str, Any]:
        """Return a sparse dict of confident fields."""


class LLMStructuralBridge:
    """Bridge sparse LLM output into a stable structural anchor."""

    def __init__(self, schema_keys: list[str], llm_client: SparseLLMAdapter):
        self.anchor = StructuralAnchor(schema_keys)
        self.llm_client = llm_client

    def parse_with_llm_assistance(self, prompt: str) -> tuple[dict[str, Any], dict[str, Any]]:
        sparse_payload = self.llm_client.generate_sparse(prompt, self.anchor.schema)
        full_ast, latency_ms = self.anchor.parse_isomorphic(sparse_payload)

        diagnostics = {
            "schema": self.anchor.schema,
            "sparse_payload": sparse_payload,
            "output": full_ast,
            "latency_ms": latency_ms,
            "filled_fields": [
                key for key, value in full_ast.items()
                if isinstance(value, str) and value.startswith("validated_token_")
            ],
        }
        return full_ast, diagnostics
