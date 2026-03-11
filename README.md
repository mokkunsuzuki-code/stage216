# QSP Stage215 – Public Evidence Verification

MIT License © 2025 Motohiro Suzuki

---

## Overview

Stage215 extends Stage213 by making the signed evidence bundle easy for third parties to verify.

While Stage213 introduced:

- evidence bundle generation
- SHA256 hashing
- RSA signing
- public-key verification

Stage215 adds a clear public verification entry point so that anyone can verify the evidence bundle with a single command.

This stage focuses on **public verifiability**, **reviewability**, and **reproducible validation**.

---

## Motivation

Signed evidence is valuable, but review friction reduces its practical impact.

A reviewer, researcher, or external auditor should be able to:

1. clone the repository
2. run one command
3. verify that the evidence bundle has not been tampered with

Stage215 reduces that friction.

---

## Verification Model

Stage213 established:

Claim
↓
CI Job
↓
Evidence Artifact
↓
CI Run ID
↓
SHA256
↓
Signature
↓
Verification

Stage215 extends this into:

Claim
↓
CI Job
↓
Evidence Artifact
↓
CI Run ID
↓
SHA256
↓
Signature
↓
Public Verification Entry Point

This means the signed evidence is not only present, but also straightforward for third parties to validate.

---

## Repository Structure

```text
stage215
│
├─ evidence_bundle/
│   ├─ evidence_bundle.json
│   ├─ evidence_bundle.sha256
│   └─ summary.md
│
├─ signatures/
│   ├─ evidence_bundle.sig
│   └─ evidence_bundle.signature.json
│
├─ keys/
│   └─ evidence_signing_public.pem
│
├─ tools/
│   ├─ build_signed_evidence_bundle.py
│   ├─ write_bundle_sha256.py
│   ├─ sign_evidence_bundle.py
│   └─ run_stage215_bundle.sh
│
├─ verification/
│   └─ verify_signature.py
│
├─ verify_bundle.sh
├─ claims/
├─ tests/
├─ docs/
└─ out/
Public Verification

Anyone can verify the signed evidence bundle locally.

Verification command
./verify_bundle.sh
Expected result
[OK] signature verification passed
Verified OK

[OK] public verification complete
What is Verified

The verification checks that:

the evidence bundle exists

the signature exists

the public key exists

the RSA signature matches the evidence bundle

the evidence bundle has not been modified after signing

If the bundle is changed after signing, verification fails.

Quick Review Flow

A reviewer can verify the bundle with the following steps:

git clone https://github.com/mokkunsuzuki-code/stage215.git
cd stage215
./verify_bundle.sh

This is the intended review path for external readers.

Relation to Previous Stages
Stage	Feature
Stage210	Claim → Evidence mapping
Stage211	Evidence bundle generation
Stage212	CI linkage
Stage213	Signed Evidence Bundle
Stage215	Public Evidence Verification

Stage215 improves external reviewability by minimizing verification friction.

Security Properties

Stage215 provides:

tamper-evident evidence

cryptographic authenticity

public-key verification

external review readiness

reproducible validation entry point

Research Relevance

This stage is relevant to:

reproducible security research

verifiable evidence pipelines

CI-driven security validation

externally reviewable cryptographic artifacts

Stage215 helps move from “signed evidence exists” to “signed evidence can be independently checked with minimal effort.”

License

MIT License

Copyright (c) 2025 Motohiro Suzuki
