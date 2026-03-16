#!/usr/bin/env python3
# MIT License © 2025 Motohiro Suzuki

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from crypto.merkle import verify_inclusion_proof


def canonical_json_bytes(obj: Dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def leaf_hash_from_entry(entry: Dict[str, Any]) -> str:
    import hashlib

    minimal_entry = {
        "index": entry["index"],
        "path": entry["path"],
        "sha256": entry["sha256"],
        "size_bytes": entry["size_bytes"],
    }
    payload = b"\x00" + canonical_json_bytes(minimal_entry)
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a single inclusion proof.")
    parser.add_argument("proof_file", help="Path to *.proof.json")
    args = parser.parse_args()

    with open(args.proof_file, "r", encoding="utf-8") as f:
        doc = json.load(f)

    entry = doc["entry"]
    proof = doc["proof"]
    expected_root = doc["merkle_root"]

    leaf_hash_hex = leaf_hash_from_entry(entry)
    ok = verify_inclusion_proof(
        leaf_hash_hex=leaf_hash_hex,
        proof=proof,
        expected_root_hex=expected_root,
    )

    if not ok:
        raise SystemExit("[ERROR] inclusion proof verification failed")

    print("[OK] inclusion proof verified")
    print(f"[OK] path: {entry['path']}")
    print(f"[OK] index: {entry['index']}")
    print(f"[OK] leaf_hash: {leaf_hash_hex}")
    print(f"[OK] merkle_root: {expected_root}")


if __name__ == "__main__":
    main()
