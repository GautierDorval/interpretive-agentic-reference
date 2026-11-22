# LLM adapter contract (minimal)

This repository is a **non-normative executable reference**. The purpose of the adapter contract
is not to standardize providers. It is to make a single point explicit:

**The orchestrator binds runtime parameters. The model does not choose them.**

## Interface

The adapter contract is intentionally minimal (`src/llm_adapter.py`):

- Method: `generate(prompt: str, runtime: dict) -> str`
- Input:
  - `prompt`: fully constructed by the orchestrator (includes allowlisted sources).
  - `runtime`: a dict loaded from `configs/runtime.json` (temperature, top_p, max_tokens).
- Output:
  - A JSON string matching `configs/output_schema.json`.

## Non-negotiables enforced by the pipeline

Even if an adapter calls a real provider, the reference pipeline still enforces:

- bounded retrieval (allowlist),
- runtime parameter binding (the adapter receives parameters, it should not override them),
- output schema validation (invalid outputs are rejected),
- policy-driven abstention (legitimate non-response).

## What schema validation does not establish

A JSON string that matches `configs/output_schema.json` passes the structural check. That check does not establish that its content is supported by the allowlisted sources, nor that an item is correctly placed under `observed`, `derived`, `inferred` or `unknown`. Whether an output preserves the meaning of its sources is a separate assessment, described in the README section "Structure validation is not a fidelity assessment".

`MockAdapter` (in `src/llm_adapter.py`) is a deterministic stub, not an LLM. It ignores the prompt and the runtime parameters and returns a fixed output, so that the pipeline can run without a provider.

## Boundary note

This contract only formalizes the adapter boundary for this repository.
It does not create a standard for the full ecosystem,
and it does not allocate authority between doctrinal, commercial, product,
or repository surfaces.

That higher-order allocation belongs elsewhere:
- `https://gautierdorval.com/distributed-authority-map.json`

## Implementation note

The adapter MAY be implemented as a thin wrapper around any provider SDK.

This repository intentionally does not ship a provider adapter, to avoid implying
production readiness or provider-specific guarantees.
