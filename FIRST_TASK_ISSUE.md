# [Task #1] Build and Submit Block Package for Busan Haeundae-gu (26350)

### 📌 Task Overview
Create and submit the official digital twin block data for **Haeundae-gu, Busan (District Code: 26350)** adhering to the project schema.

---

### 📋 Requirements & Constraints

1. **Target Folder**: `incoming/26350/block.json`
2. **Schema Compliance**: Must validate successfully against `schema/block.schema.json`.
3. **Landmarks**: Include 5 prominent landmarks in Haeundae-gu.
   - The 5 landmarks must be independently researched and selected from official and trusted public sources.
   - Each landmark must have accurate WGS84 coordinates (`lat`, `lng`).
   - Each landmark must cite an official reference `source_url` (e.g. local government portal `haeundae.go.kr`, Busan Tourism `visitbusan.net`, or other official domains).
4. **Data Sources**: State open public data sources with licenses (e.g. OpenStreetMap ODbL, Korea Open Government License).
5. **Local Validation**: Run `python tools/validate_block.py incoming/26350` and confirm all 7 Gates pass.
6. **Submission**: Submit via GitHub Pull Request targeting `main`.

---

### 📖 References
- Format sample: [examples/sample_block.json](examples/sample_block.json)
- Validation tool: [tools/validate_block.py](tools/validate_block.py)
- Step-by-step guide: [GUIDE.md](GUIDE.md)
