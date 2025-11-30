#!/usr/bin/env python

"""
Generate a simple evidence manifest for synthetic cases.

- Scans capstone/synthetic_evidence/<CASE_ID> directories
- Emits capstone/synthetic_evidence/manifest.json
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


EVIDENCE_ROOT = Path("capstone/synthetic_evidence")
MANIFEST_PATH = EVIDENCE_ROOT / "manifest.json"


@dataclass
class ManifestRecord:
    id: str              # "<case_id>/<relative_path>"
    case_id: str
    relative_path: str
    category: str
    title: str
    ext: str
    size_bytes: int


def discover_case_dirs(root: Path) -> List[Path]:
    if not root.exists():
        raise SystemExit(f"[ERROR] Evidence root does not exist: {root}")
    return [p for p in sorted(root.iterdir()) if p.is_dir()]


def build_manifest() -> List[ManifestRecord]:
    records: List[ManifestRecord] = []

    for case_dir in discover_case_dirs(EVIDENCE_ROOT):
        case_id = case_dir.name

        for file_path in case_dir.rglob("*"):
            if not file_path.is_file():
                continue

            rel_case = file_path.relative_to(case_dir)
            rel_global = file_path.relative_to(EVIDENCE_ROOT)

            parts = rel_case.parts
            if len(parts) > 1:
                category = parts[0]
            else:
                category = "uncategorized"

            record = ManifestRecord(
                id=f"{case_id}/{rel_case}",
                case_id=case_id,
                relative_path=str(rel_global),
                category=category,
                title=file_path.stem,
                ext=file_path.suffix.lower(),
                size_bytes=file_path.stat().st_size,
            )
            records.append(record)

    return records


def main() -> None:
    records = build_manifest()
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = [asdict(r) for r in records]
    MANIFEST_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"[OK] Wrote manifest with {len(records)} records to {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
