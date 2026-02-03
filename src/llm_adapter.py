from typing import Dict, Protocol


class LLMAdapter(Protocol):
    def generate(self, prompt: str, runtime: Dict) -> str:
        ...


class MockAdapter:
    def generate(self, prompt: str, runtime: Dict) -> str:
        # Minimal deterministic mock respecting the schema shape.
        # This is NOT an LLM. It is a stub used to demonstrate the pipeline.
        return """
{
  "type": "governed_output",
  "observed": ["Montesco is a fictional example name in this repository."],
  "derived": [],
  "inferred": [],
  "unknown": ["Any real-world corporate details are not available in the allowlisted sources."],
  "abstained": false,
  "notes": "Mock output generated without external API."
}
""".strip()
