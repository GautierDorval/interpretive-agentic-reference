import json
import tempfile
import unittest
from pathlib import Path

from src.pipeline import run_pipeline
from src.llm_adapter import MockAdapter


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = MockAdapter()
        self.runtime = "configs/runtime.json"
        self.schema = "configs/output_schema.json"
        self.abstention = "configs/abstention_policy.json"
        self.allowlist = "configs/retrieval_allowlist.json"

    def test_success_path_company_profile(self) -> None:
        ok, payload = run_pipeline(
            request_path="examples/requests/company_profile.json",
            runtime_cfg_path=self.runtime,
            allowlist_cfg_path=self.allowlist,
            schema_path=self.schema,
            abstention_policy_path=self.abstention,
            adapter=self.adapter
        )
        self.assertTrue(ok)
        self.assertFalse(payload.get("abstained", False))
        self.assertEqual(payload.get("type"), "governed_output")
        self.assertIsInstance(payload.get("observed"), list)

    def test_out_of_scope_abstains(self) -> None:
        ok, payload = run_pipeline(
            request_path="examples/requests/unknowns_test.json",
            runtime_cfg_path=self.runtime,
            allowlist_cfg_path=self.allowlist,
            schema_path=self.schema,
            abstention_policy_path=self.abstention,
            adapter=self.adapter
        )
        self.assertFalse(ok)
        self.assertTrue(payload.get("abstained", False))
        self.assertIn("LEGITIMATE_NON_RESPONSE", payload.get("unknown", []))

    def test_non_allowlisted_source_abstains(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            req = {
                "request_type": "company_profile",
                "question": "What is Montesco?",
                "required_sources": ["examples/sources/canonical_source_1.md"]
            }
            req_path = Path(td) / "req.json"
            req_path.write_text(json.dumps(req), encoding="utf-8")

            deny_all_allowlist = {"allowed_paths": [], "deny_by_default": True}
            allowlist_path = Path(td) / "allowlist.json"
            allowlist_path.write_text(json.dumps(deny_all_allowlist), encoding="utf-8")

            ok, payload = run_pipeline(
                request_path=str(req_path),
                runtime_cfg_path=self.runtime,
                allowlist_cfg_path=str(allowlist_path),
                schema_path=self.schema,
                abstention_policy_path=self.abstention,
                adapter=self.adapter
            )

            self.assertFalse(ok)
            self.assertTrue(payload.get("abstained", False))
            self.assertIn("LEGITIMATE_NON_RESPONSE", payload.get("unknown", []))


if __name__ == "__main__":
    unittest.main()
