# Allowlist maintenance (non-normative notes)

The retrieval allowlist (`configs/retrieval_allowlist.json`) is intentionally strict.
It exists to demonstrate that **the model does not choose what it reads**.

## Operational reality

In real deployments, allowlists require maintenance:

- sources may change over time,
- new sources may become relevant,
- sources may degrade in quality or become compromised.

## A practical pattern: propose / approve

One way to keep the allowlist “alive” without making it model-controlled:

1. The agent MAY *propose* a candidate source (as a suggestion only).
2. A human (or a separate governed approval workflow) validates the source.
3. Only then is the source added to the allowlist.

This preserves the core constraint:
**allowlist updates are governed by an authority outside the model.**
