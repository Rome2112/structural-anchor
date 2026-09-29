from __future__ import annotations

from typing import Any

from .controller import StructuralAnchor


class StructuralValidator:
    """Reports which fields came from input versus deterministic fallback."""

    def __init__(self, anchor: StructuralAnchor):
        self.anchor = anchor

    def coverage(self, parsed_ast: dict[str, Any], original_input: dict[str, Any]) -> dict[str, dict[str, Any]]:
        coverage: dict[str, dict[str, Any]] = {}
        for key in self.anchor.schema:
            raw_value = original_input.get(key)
            value = parsed_ast.get(key)
            coverage[key] = {
                "value": value,
                "source": "input" if raw_value is not None else "engine_fallback",
                "is_fallback": isinstance(value, str) and value.startswith("validated_token_"),
            }
        return coverage

    def diagnose(self, parsed_ast: dict[str, Any], original_input: dict[str, Any]) -> dict[str, Any]:
        coverage = self.coverage(parsed_ast, original_input)
        fallback_fields = [key for key, meta in coverage.items() if meta["is_fallback"]]
        return {
            "fallback_fields": fallback_fields,
            "coverage": coverage,
            "structurally_complete": not fallback_fields,
        }
