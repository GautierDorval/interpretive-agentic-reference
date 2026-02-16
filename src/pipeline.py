import json
from pathlib import Path
from typing import Dict, Tuple

from .retrieval import retrieve_sources
from .validator import validate_output
from .abstention import should_abstain
from .types import TypedRequest, GovernedOutput
from .llm_adapter import LLMAdapter


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_prompt(req: TypedRequest, sources: Dict[str, str]) -> str:
    src_block = "\n\n".join([f"== SOURCE: {k} ==\n{v}" for k, v in sources.items()])
    return f"""You must output STRICT JSON matching the provided schema.
You must keep unknowns explicit. Do not invent facts.

QUESTION:
{req.question}

SOURCES (allowlisted):
{src_block}
"""


def run_pipeline(
    request_path: str,
    runtime_cfg_path: str,
    allowlist_cfg_path: str,
    schema_path: str,
    abstention_policy_path: str,
    adapter: LLMAdapter
) -> Tuple[bool, dict]:
    req = TypedRequest(**load_json(request_path))
    runtime = load_json(runtime_cfg_path)
    abstention_policy = load_json(abstention_policy_path)

    # Out-of-scope example rule (minimal): block requests for personal phone numbers
    out_of_scope_request = "phone number" in req.question.lower()

    # Retrieval
    missing_required_sources = False
    conflicting_sources = False  # stub: in real system you would detect contradictions

    sources = {}
    try:
        sources = retrieve_sources(req.required_sources, allowlist_cfg_path)
    except Exception:
        missing_required_sources = True

    # Early abstention
    abstain_msg = should_abstain(
        missing_required_sources=missing_required_sources,
        conflicting_sources=conflicting_sources,
        out_of_scope_request=out_of_scope_request,
        schema_invalid=False,
        policy=abstention_policy
    )
    if abstain_msg:
        payload = GovernedOutput(
            observed=[],
            derived=[],
            inferred=[],
            unknown=[abstain_msg],
            abstained=True,
            notes="Abstained before model execution."
        ).model_dump()
        return False, payload

    # Build prompt and call model
    prompt = build_prompt(req, sources)
    raw = adapter.generate(prompt, runtime)

    # Parse JSON
    schema_invalid = False
    try:
        payload = json.loads(raw)
        validate_output(payload, schema_path)
    except Exception:
        schema_invalid = True
        payload = GovernedOutput(
            observed=[],
            derived=[],
            inferred=[],
            unknown=["LEGITIMATE_NON_RESPONSE"],
            abstained=True,
            notes="Schema invalid or unparsable output."
        ).model_dump()

    # Post-validation abstention
    abstain_msg = should_abstain(
        missing_required_sources=False,
        conflicting_sources=conflicting_sources,
        out_of_scope_request=out_of_scope_request,
        schema_invalid=schema_invalid,
        policy=abstention_policy
    )
    if abstain_msg:
        payload["abstained"] = True
        if "unknown" not in payload or not isinstance(payload["unknown"], list):
            payload["unknown"] = []
        payload["unknown"].append(abstain_msg)

    accepted = not bool(payload.get("abstained", False))

    return accepted, payload
