# Interpretive agentic reference — executable proof (non-normative)

This repository provides a **minimal executable reference pipeline** demonstrating how
**constraintive governance** operates as a **runtime substrate** for **interpretive governance**
in **agentic-closed** systems.

This is **not** a product, not a framework, and not a certification tool.

## What this demonstrates

A single pipeline with four non-negotiable properties:

1. **Bounded retrieval** (allowlisted sources only)
2. **Fixed inference configuration** (runtime parameters are set by the orchestrator)
3. **Schema-validated output** (reject invalid outputs)
4. **Policy-driven abstention** (legitimate non-response when conditions fail)

The purpose is to show that constraintive governance is **not a prompt technique**.
It is a **runtime configuration and enforcement layer**.

## What this does not claim

- No claim of correctness, completeness, or safety.
- No claim that a model “follows” governance.
- No claim that the outputs are “approved”.
- No claim that this implementation is production-ready.

## Regime boundary

- **Web-open**: constraintive governance is inapplicable (no runtime control).
- **Agentic-closed**: constraintive governance is applicable (runtime control exists).

This repository is explicitly scoped to **agentic-closed** systems.

## Architecture (single pipeline)

Typed request
  → bounded retrieval (allowlist)
  → LLM call (runtime config fixed)
  → schema validation
  → accept OR abstain

See: `docs/architecture.md`

## Quickstart

### 1) Setup

Python 3.11+ recommended.

```bash
pip install -r requirements.txt

### 2) Run in mock mode (no API required)

python -m src.main --request examples/requests/company_profile.json --mock

### 3) Run with a real LLM adapter

This repository includes a minimal adapter interface (src/llm_adapter.py).
You may implement a concrete adapter for a specific provider.

## The reference pipeline will still enforce:

- retrieval boundaries,
- runtime parameter binding,
- output schema validation,
- abstention policy.

## Core files

- configs/runtime.json — runtime constraints (temperature, top_p, max_tokens)
- configs/retrieval_allowlist.json — allowed sources for retrieval
- configs/output_schema.json — strict output schema
- configs/abstention_policy.json — legitimate non-response conditions

## Relationship to the manifest

This repository is a non-normative reference implementation.
The normative definition of Interpretive Governance is maintained in:

https://github.com/GautierDorval/interpretive-governance-manifest

This repository must not redefine that manifest.

---

# 4) LICENSE (recommandation)

Pour ce type de repo, je recommande **MIT** (simple, permissif, compatible démonstrateur).

MIT License

Copyright (c) 2026 Gautier Dorval

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



