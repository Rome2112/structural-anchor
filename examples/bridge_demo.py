import json

from structural_anchor import LLMStructuralBridge, StructuralAnchor, StructuralValidator


class DemoLLM:
    def generate_sparse(self, prompt: str, schema: list[str]) -> dict:
        payload = {
            "request_id": "REQ_2026_001",
            "status": "200_OK",
            "currency": "USD",
        }
        if "payload_hash" in schema:
            payload["payload_hash"] = "sha256:demo"
        return payload


schema = [
    "request_id",
    "status",
    "payload_hash",
    "execution_metric",
    "currency",
    "metadata",
]

anchor = StructuralAnchor(schema)
partial = {"request_id": "REQ_2026_001", "status": "200_OK"}
parsed, latency = anchor.parse_isomorphic(partial)
print("[anchor]")
print(json.dumps({"latency_ms": round(latency, 4), "output": parsed}, indent=2))

bridge = LLMStructuralBridge(schema, DemoLLM())
full_ast, diagnostics = bridge.parse_with_llm_assistance("Create a payment result payload")
print("\n[bridge]")
print(json.dumps({"filled_fields": diagnostics["filled_fields"], "output": full_ast}, indent=2))

validator = StructuralValidator(anchor)
print("\n[validator]")
print(json.dumps(validator.diagnose(full_ast, {"request_id": "REQ_2026_001", "status": "200_OK", "currency": "USD"}), indent=2))
