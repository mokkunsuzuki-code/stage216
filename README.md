# QSP Stage215

## Evidence Transparency Log

**QSP (Quantum Security Protocol)** explores how security claims, formal reasoning, and executable validation can be connected through verifiable evidence.

Stage215 introduces an **append-only transparency log for security evidence**, extending signed evidence verification with tamper-evident publication history.

This stage focuses on **evidence transparency and reproducibility**.

---

# Overview

Security claims are only meaningful if their supporting evidence can be inspected and verified.

QSP structures verification as a traceable pipeline:

```
Claim
↓
CI Job
↓
Evidence Artifact
↓
SHA256
↓
Cryptographic Signature
↓
Public Verification
↓
Transparency Log
```

Stage215 ensures that **evidence publication itself becomes verifiable**.

---

# Evidence Transparency Log

Stage215 introduces an **append-only transparency log** for evidence artifacts.

Evidence entries are recorded as log entries containing:

```
Evidence
↓
SHA256
↓
Log Entry
```

Each new piece of evidence becomes a **new log entry**, ensuring:

* evidence cannot be silently replaced
* publication history is visible
* verification is reproducible

Example structure:

```
Log Entry 1
Evidence1
hash1

Log Entry 2
Evidence2
hash2

Log Entry 3
Evidence3
hash3
```

Previous entries are **not meant to be modified**.

---

# Why Transparency Matters

Researchers reviewing security systems often ask:

> Can the evidence be replaced later?

Digital signatures alone prove authenticity, but they do not prove that earlier evidence was not replaced.

Transparency logs address this by recording **evidence publication history**.

Stage215 draws inspiration from:

* Certificate Transparency
* Sigstore
* Software Supply Chain Security

---

# Repository Structure

```
examples/
  evidence/
    summary.md
    summary.sha256.txt
    summary.sig

tools/
  generate_transparency_log.py
  verify_transparency_log.py
  run_stage215_bundle.sh

tests/
  test_transparency_log.py

out/  (generated artifacts – ignored by git)
```

Example evidence artifacts are stored under:

```
examples/evidence/
```

Runtime-generated outputs are written to:

```
out/
```

The `out/` directory is intentionally excluded from version control.

---

# Running the Evidence Bundle

Generate a transparency log entry:

```
bash tools/run_stage215_bundle.sh
```

This will:

1. compute evidence hash
2. record evidence metadata
3. append entry to the transparency log
4. verify log integrity

---

# Verifying the Transparency Log

To verify the log:

```
python3 tools/verify_transparency_log.py \
  --log out/transparency/transparency_log.jsonl
```

Verification checks:

* evidence file existence
* hash consistency
* log entry sequence
* signature metadata integrity

---

# Security Claim Validation

QSP connects protocol claims to executable validation.

Example flow:

```
Security Claim
↓
CI Validation
↓
Evidence Artifact
↓
Transparency Log Entry
```

This structure helps ensure that:

* claims remain testable
* evidence is traceable
* verification can be reproduced

---

# Key Management Policy

Evidence artifacts may be signed to support authenticity verification.

Key management rules:

* **Private signing keys are never committed to the repository**
* Only **public verification keys** are stored in `keys/`
* If a private key is exposed, it must be **rotated immediately**
* Evidence signatures can always be verified using the published public key

---

# Research Goal

The purpose of QSP is not to claim new cryptographic primitives.

Instead, the goal is to explore:

* explicit security assumptions
* traceable verification pipelines
* reproducible security evidence

Stage215 focuses on **transparency of evidence publication**.

---

# Inspiration

The design philosophy of Stage215 is influenced by:

* Certificate Transparency
* Sigstore
* Reproducible security research
* Software supply chain verification

---

# License

MIT License
© 2025 Motohiro Suzuki

---

## Stage216: Transparency Log + Merkle Tree + Inclusion Proof

Stage216 introduces a research-grade transparency layer for evidence artifacts.

### What this stage adds

- **Transparency Log**
  - Records each evidence artifact with:
    - relative path
    - SHA-256 digest
    - size in bytes
    - Merkle leaf hash
- **Merkle Tree**
  - Builds a Merkle tree over canonicalized log entries
  - Produces a single **Merkle Root** representing the full evidence set
- **Inclusion Proof**
  - Generates a proof for each artifact
  - Enables third parties to verify that a given artifact is included in the committed transparency log

### Output files

- `out/transparency/transparency_log.json`
- `out/transparency/merkle_tree.json`
- `out/transparency/root.txt`
- `out/transparency/checkpoint.json`
- `out/transparency/inclusion_proofs/*.proof.json`

### Security meaning

This stage upgrades the project from:

- signed evidence bundle

to:

- **tamper-evident, inclusion-verifiable transparency structure**

That is a substantial step toward a research-level transparency foundation.

### Build

```bash
python3 tools/build_transparency_log.py --input-dir out/evidence_bundle --output-dir out/transparency
Verify one proof
python3 tools/verify_inclusion_proof.py out/transparency/inclusion_proofs/<proof-file>.proof.json

