#!/usr/bin/env bash
set -euo pipefail

echo "== Stage213: build signed evidence bundle =="

python3 tools/build_signed_evidence_bundle.py
python3 tools/write_bundle_sha256.py
python3 tools/sign_evidence_bundle.py
python3 verification/verify_signature.py

echo
echo "[OK] Stage213 signed evidence bundle complete"
