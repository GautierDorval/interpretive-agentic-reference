import argparse
import importlib
from typing import Any

from rich import print

from .pipeline import run_pipeline
from .llm_adapter import MockAdapter


def load_adapter(spec: str) -> Any:
    """Load an adapter class using a `module:ClassName` spec.

    This is intentionally minimal and non-normative. The goal is to allow
    developers to plug a concrete provider adapter without changing the
    reference pipeline.
    """
    if ":" not in spec:
        raise ValueError("Invalid adapter spec. Expected format: module:ClassName")

    module_name, class_name = spec.split(":", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, help="Path to typed request JSON")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run with mock adapter (no external API). Alias for --adapter src.llm_adapter:MockAdapter."
    )
    parser.add_argument(
        "--adapter",
        default="src.llm_adapter:MockAdapter",
        help="Adapter spec in the format `module:ClassName` implementing LLMAdapter."
    )
    args = parser.parse_args()

    adapter = MockAdapter() if args.mock else load_adapter(args.adapter)

    ok, payload = run_pipeline(
        request_path=args.request,
        runtime_cfg_path="configs/runtime.json",
        allowlist_cfg_path="configs/retrieval_allowlist.json",
        schema_path="configs/output_schema.json",
        abstention_policy_path="configs/abstention_policy.json",
        adapter=adapter
    )

    print("[bold]OK:[/bold]", ok)
    print(payload)


if __name__ == "__main__":
    main()
