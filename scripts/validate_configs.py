import json
from pathlib import Path
from jsonschema import validate

REPO_ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ("configs/runtime.json", "schemas/runtime.schema.json"),
    ("configs/retrieval_allowlist.json", "schemas/retrieval_allowlist.schema.json"),
    ("configs/abstention_policy.json", "schemas/abstention_policy.schema.json"),
]

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> None:
    failures = []
    for cfg_rel, schema_rel in TARGETS:
        cfg_path = REPO_ROOT / cfg_rel
        schema_path = REPO_ROOT / schema_rel
        payload = load_json(cfg_path)
        schema = load_json(schema_path)
        try:
            validate(instance=payload, schema=schema)
        except Exception as e:
            failures.append((cfg_rel, schema_rel, str(e)))

    # Validate example requests are syntactically valid JSON
    req_dir = REPO_ROOT / "examples" / "requests"
    for p in sorted(req_dir.glob("*.json")):
        try:
            load_json(p)
        except Exception as e:
            failures.append((str(p.relative_to(REPO_ROOT)), "JSON syntax", str(e)))

    if failures:
        print("Config validation failed:")
        for cfg, schema, err in failures:
            print(f"- {cfg} -> {schema}: {err}")
        raise SystemExit(1)

    print("Config validation OK.")

if __name__ == "__main__":
    main()
