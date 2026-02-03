from typing import Optional


def should_abstain(
    missing_required_sources: bool,
    conflicting_sources: bool,
    out_of_scope_request: bool,
    schema_invalid: bool,
    policy: dict
) -> Optional[str]:
    rules = policy.get("abstain_if", {})
    if rules.get("missing_required_sources", False) and missing_required_sources:
        return policy.get("message", "LEGITIMATE_NON_RESPONSE")
    if rules.get("conflicting_sources", False) and conflicting_sources:
        return policy.get("message", "LEGITIMATE_NON_RESPONSE")
    if rules.get("out_of_scope_request", False) and out_of_scope_request:
        return policy.get("message", "LEGITIMATE_NON_RESPONSE")
    if rules.get("schema_invalid", False) and schema_invalid:
        return policy.get("message", "LEGITIMATE_NON_RESPONSE")
    return None
