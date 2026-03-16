#!/usr/bin/env python3
# MIT License © 2025 Motohiro Suzuki

from __future__ import annotations

import argparse
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from crypto.merkle import (
    build_merkle_levels,
    hash_leaf,
    inclusion_proof,
    levels_as_hex,
    merkle_root,
)


def canonical_json_bytes(obj: Dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files(input_dir: Path) -> List[Path]:
    files = [p for p in input_dir.rglob("*") if p.is_file()]
    return sorted(files, key=lambda p: str(p).replace("\\", "/"))


def safe_filename(rel_path: str) -> str:
    return rel_path.replace("/", "__").replace("\\", "__")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build transparency log + Merkle tree + inclusion proofs from a directory."
    )
    parser.add_argument(
        "--input-dir",
        default="out/evidence_bundle",
        help="Directory containing evidence files (default: out/evidence_bundle)",
    )
    parser.add_argument(
        "--output-dir",
        default="out/transparency",
        help="Output directory (default: out/transparency)",
    )
    args = parser.parse_args()

    repo_root = Path(".").resolve()
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    proofs_dir = output_dir / "inclusion_proofs"

    if not input_dir.exists():
        raise SystemExit(f"[ERROR] input directory not found: {input_dir}")

    files = collect_files(input_dir)
    if not files:
        raise SystemExit(f"[ERROR] no files found under: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    proofs_dir.mkdir(parents=True, exist_ok=True)

    entries: List[Dict[str, Any]] = []
    leaf_hashes = []

    for index, file_path in enumerate(files):
        rel_path = str(file_path.relative_to(repo_root)).replace("\\", "/")
        file_sha256 = sha256_file(file_path)
        size_bytes = file_path.stat().st_size

        entry = {
            "index": index,
            "path": rel_path,
            "sha256": file_sha256,
            "size_bytes": size_bytes,
        }
        entry_bytes = canonical_json_bytes(entry)
        leaf_hash = hash_leaf(entry_bytes).hex()

        entry["leaf_hash"] = leaf_hash
        entries.append(entry)
        leaf_hashes.append(bytes.fromhex(leaf_hash))

    levels = build_merkle_levels(leaf_hashes)
    root_hex = merkle_root(levels).hex()

    log_doc = {
        "schema_version": "stage216.transparency_log.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "leaf_hash_definition": "SHA256(0x00 || canonical_json(entry))",
        "node_hash_definition": "SHA256(0x01 || left || right)",
        "entry_count": len(entries),
        "merkle_root": root_hex,
        "entries": entries,
    }

    tree_doc = {
        "schema_version": "stage216.merkle_tree.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(entries),
        "merkle_root": root_hex,
        "levels": levels_as_hex(levels),
    }

    (output_dir / "transparency_log.json").write_text(
        json.dumps(log_doc, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (output_dir / "merkle_tree.json").write_text(
        json.dumps(tree_doc, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (output_dir / "root.txt").write_text(root_hex + "\n", encoding="utf-8")

    for entry in entries:
        proof_doc = {
            "schema_version": "stage216.inclusion_proof.v1",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "merkle_root": root_hex,
            "entry": entry,
            "proof": inclusion_proof(entry["index"], levels),
        }
        out_name = safe_filename(entry["path"]) + ".proof.json"
        (proofs_dir / out_name).write_text(
            json.dumps(proof_doc, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    checkpoint = {
        "schema_version": "stage216.checkpoint.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "entry_count": len(entries),
        "merkle_root": root_hex,
        "log_path": str(output_dir / "transparency_log.json"),
        "tree_path": str(output_dir / "merkle_tree.json"),
        "proofs_dir": str(proofs_dir),
    }
    (output_dir / "checkpoint.json").write_text(
        json.dumps(checkpoint, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"[OK] wrote: {output_dir / 'transparency_log.json'}")
    print(f"[OK] wrote: {output_dir / 'merkle_tree.json'}")
    print(f"[OK] wrote: {output_dir / 'root.txt'}")
    print(f"[OK] wrote proofs: {proofs_dir}")
    print(f"[OK] merkle_root: {root_hex}")
    print(f"[OK] entry_count: {len(entries)}")


if __name__ == "__main__":
    main()
