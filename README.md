# Korea Digital Twin Block Builder (Sandbox)

Welcome to the **Korea Digital Twin Open Block Builder Sandbox**!

This repository is an open collaboration workspace for creating, testing, and submitting geographic block packages for the 3D Digital Twin Korea project.

---

> [!IMPORTANT]
> **🚀 ACTIVE TASK (2026-11-07): 종로구 1차 최우선 12대 시그니처 앵커 블록 구현**
> - **최우선 12대 지시서**: [`TASK_REQUEST_20261107_JONGNO_LEGO_PRIORITY12.md`](TASK_REQUEST_20261107_JONGNO_LEGO_PRIORITY12.md)
> - **50대 블록 마스터 설계안**: [`TASK_REQUEST_20261107_JONGNO_LEGO_50BLOCKS.md`](TASK_REQUEST_20261107_JONGNO_LEGO_50BLOCKS.md)
> - **종로구 1,000대 시그니처 마스터 DB**: [`examples/jongno_1000_signature_master.json`](examples/jongno_1000_signature_master.json)
> - **작업 브랜치**: `feature/jongno-signature-lego-blocks` (PR 대상: `main`)

---

## 🎯 Purpose

- Provide an open specification for administrative district blocks in South Korea.
- Enable human contributors and automated agents to submit new geographic data via GitHub Pull Requests.
- Ensure strict data quality, licensing compliance, and security through automated 7-Gate CI checks.

---

## 📁 Repository Structure

```
.
├── schema/
│   └── block.schema.json      # Official JSON Schema for block data
├── examples/
│   └── sample_block.json      # Reference example (Jongno-gu, Seoul - Code 11110)
├── tools/
│   └── validate_block.py      # Automated 7-Gate validator
├── incoming/                  # Directory for incoming PRs (1 folder per district)
├── GUIDE.md                   # Step-by-step contribution guide for agents and humans
└── LICENSE                    # MIT License
```

---

## 🚀 How to Contribute

Please read [GUIDE.md](GUIDE.md) before starting your task.

1. Pick an unbuilt administrative district code (e.g. `26350`).
2. Construct `incoming/<block_code>/block.json` following [schema/block.schema.json](schema/block.schema.json).
3. Validate locally: `python tools/validate_block.py incoming/<block_code>`
4. Submit a Pull Request.

All submitted PRs will be evaluated by automated CI workflows. Once verified, approved packages are reviewed and integrated into the main digital twin service.

---

## 🛡️ CI Verification & Security Isolation Policy

To protect both contributors and upstream services, the following verification model is enforced:

1. **Strict File Perimeter**:
   - Pull requests are **strictly restricted to files inside `incoming/<block_code>/`**.
   - Any pull request modifying files outside `incoming/` (e.g. `.github/`, `tools/`, `schema/`, `README.md`) will be immediately rejected by the CI perimeter guard.

2. **Advisory CI vs. Authoritative Isolated Re-verification**:
   - The GitHub Actions CI run on a Pull Request provides **advisory 1st-stage feedback** to the contributor.
   - Because a PR's execution context can potentially alter local workflow definitions, **final merge authorization is solely determined by an isolated re-verification**:
     Our upstream daemon fetches the raw data from `incoming/` and runs the immutable master-branch validator (`python tools/validate_block.py`) in an isolated sandbox environment before any data is admitted.

3. **Zero Secrets Architecture**:
   - This public repository contains **zero repository secrets and zero environment credentials**.
   - Contributors and external agents operate in an entirely credential-free open sandbox.

---

## 📜 License & Compliance

- All code in this repository is licensed under the [MIT License](LICENSE).
- Geographic and landmark data must cite proper open public data licenses (e.g., OpenStreetMap ODbL, Korea Open Government License Type 1).
