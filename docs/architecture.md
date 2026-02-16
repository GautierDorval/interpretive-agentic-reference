# Architecture (single pipeline)

This repository demonstrates a single agentic-closed pipeline:

Typed request
  → bounded retrieval (allowlist)
  → LLM execution (runtime parameters fixed)
  → schema validation
  → accept OR abstain

Constraintive governance is expressed as:

- retrieval boundaries,
- execution parameter binding,
- validation and rejection logic,
- abstention policy.

Interpretive governance is expressed as:

- explicit claim typing (observed / derived / inferred / unknown),
- explicit non-response legitimacy.

See also:
- `configs/output_schema.json` (interpretive typing surface)
- `configs/abstention_policy.json` (legitimate non-response)
