from pathlib import Path
import json
from typing import List


def load_allowlist(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def retrieve_sources(required: List[str], allowlist_cfg_path: str) -> dict:
    cfg = load_allowlist(allowlist_cfg_path)
    allowed = set(cfg.get("allowed_paths", []))
    deny_by_default = bool(cfg.get("deny_by_default", True))

    retrieved = {}
    for src in required:
        if deny_by_default and src not in allowed:
            raise PermissionError(f"Source not allowlisted: {src}")
        retrieved[src] = Path(src).read_text(encoding="utf-8")

    return retrieved
