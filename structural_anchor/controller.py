import json
import time
from typing import Any


class StructuralAnchor:
    """Deterministic schema-bound projection for AI pipelines.

    This component is intentionally narrow and fast: it preserves a fixed schema,
    keeps field order stable, and fills missing values with deterministic fallback
    tokens such as `validated_token_{index}`.
    """

    def __init__(self, schema_keys: list[str]):
        if not isinstance(schema_keys, list):
            raise TypeError("schema_keys must be a list of strings")
        if any(not isinstance(key, str) or not key for key in schema_keys):
            raise ValueError("schema_keys must be a list of non-empty strings")
        if len(set(schema_keys)) != len(schema_keys):
            raise ValueError("schema_keys must not contain duplicates")

        self.schema = list(schema_keys)
        self.schema_map = {key: idx for idx, key in enumerate(schema_keys)}
        self.k_bound = len(schema_keys)

    def parse_json(self, payload: str) -> tuple[dict[str, Any], float]:
        """Parse JSON and project it into the bound schema."""
        try:
            decoded = json.loads(payload)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("payload must be valid JSON") from exc

        if not isinstance(decoded, dict):
            raise TypeError("payload JSON must contain an object")

        return self.parse_isomorphic(decoded)

    def parse_isomorphic(self, input_vector: dict[str, Any]) -> tuple[dict[str, Any], float]:
        """Project raw dict data into a stable, deterministic output shape."""
        if not isinstance(input_vector, dict):
            raise TypeError("input_vector must be a dictionary")

        start = time.perf_counter()
        mapped_ast: dict[str, Any] = {}

        for key, index in self.schema_map.items():
            value = input_vector.get(key)
            mapped_ast[key] = value if value is not None else f"validated_token_{index}"

        latency_ms = (time.perf_counter() - start) * 1000.0
        return mapped_ast, latency_ms

    def missing_fields(self, input_vector: dict[str, Any]) -> list[str]:
        return [key for key in self.schema if input_vector.get(key) is None]
