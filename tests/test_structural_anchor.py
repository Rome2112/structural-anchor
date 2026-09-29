import unittest

from structural_anchor import LLMStructuralBridge, StructuralAnchor, StructuralValidator


class DemoLLM:
    def generate_sparse(self, prompt: str, schema: list[str]) -> dict:
        base = {"request_id": "REQ_7", "status": "200_OK"}
        if "currency" in schema:
            base["currency"] = "USD"
        return base


class StructuralAnchorTests(unittest.TestCase):
    def test_anchor_fills_missing_fields(self):
        schema = ["request_id", "status", "payload_hash", "execution_metric"]
        anchor = StructuralAnchor(schema)

        parsed, latency = anchor.parse_isomorphic({"request_id": "REQ_7", "status": "200_OK"})
        self.assertEqual(parsed["request_id"], "REQ_7")
        self.assertEqual(parsed["status"], "200_OK")
        self.assertEqual(parsed["payload_hash"], "validated_token_2")
        self.assertGreaterEqual(latency, 0.0)

    def test_bridge_completes_sparse_llm_data(self):
        schema = ["request_id", "status", "payload_hash", "currency"]
        bridge = LLMStructuralBridge(schema, DemoLLM())
        full_ast, diagnostics = bridge.parse_with_llm_assistance("make a result")

        self.assertIn("request_id", full_ast)
        self.assertIn("status", full_ast)
        self.assertIn("currency", full_ast)
        self.assertIn("payload_hash", full_ast)
        self.assertTrue("filled_fields" in diagnostics)

    def test_validator_tracks_fallback_sources(self):
        schema = ["request_id", "status", "payload_hash"]
        anchor = StructuralAnchor(schema)
        validator = StructuralValidator(anchor)

        parsed, _ = anchor.parse_isomorphic({"request_id": "REQ_1"})
        result = validator.diagnose(parsed, {"request_id": "REQ_1"})
        self.assertTrue(result["fallback_fields"])
        self.assertFalse(result["structurally_complete"])


if __name__ == "__main__":
    unittest.main()
