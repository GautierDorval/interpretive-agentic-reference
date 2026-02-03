import argparse
from rich import print

from .pipeline import run_pipeline
from .llm_adapter import MockAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, help="Path to typed request JSON")
    parser.add_argument("--mock", action="store_true", help="Run with mock adapter (no API)")
    args = parser.parse_args()

    adapter = MockAdapter()

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
