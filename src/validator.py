from pathlib import Path
import json
from jsonschema import validate


def load_schema(schema_path: str) -> dict:
    return json.loads(Path(schema_path).read_text(encoding="utf-8"))


def validate_output(payload: dict, schema_path: str) -> None:
    schema = load_schema(schema_path)
    validate(instance=payload, schema=schema)
