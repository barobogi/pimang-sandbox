# AI Agent & Contributor Step-by-Step Guide

This guide is specifically written for AI agents (such as autonomous coding assistants) and human contributors to build and submit new block packages.

---

## 📋 Task Workflow

### Step 1: Check Target District
Find your assigned district code (5-digit string, e.g., `26350` for Haeundae-gu, Busan).

### Step 2: Create District Directory
Create a subfolder under `incoming/` named with the 5-digit block code:
```bash
mkdir -p incoming/26350
```

### Step 3: Author `block.json`
Inside your folder (`incoming/<block_code>/block.json`), generate the JSON file adhering strictly to `schema/block.schema.json`.

**Required Properties:**
1. `block_code`: 5-digit administrative district code string.
2. `block_name`: Official district name in Korean.
3. `bbox`: Geographic bounding box `[min_lng, min_lat, max_lng, max_lat]`.
4. `center`: Center coordinates `[lat, lng]`.
5. `landmarks`: Array of 3 to 10 prominent local attractions.
   - Each landmark must have: `name`, `lat`, `lng`, `category`, `description` (>=10 chars), `source_url`.
   - `source_url` must point to an official public/local government portal (e.g. `.go.kr`, `.or.kr`, `visitkorea.or.kr`).
6. `history_summary`: Cultural and geographic overview (>=30 chars).
7. `data_sources`: Attribution list specifying public data source, license (e.g., ODbL 1.0, KOGL Type 1), and URL.
8. `contributor`: Object containing `github_username` and optional `agent_name`.

Refer to `examples/sample_block.json` as the ground truth format.

### Step 4: Run Local Validation
Execute the built-in validator to test all 7 Gates before making a PR:
```bash
python tools/validate_block.py incoming/<block_code>
```
Ensure the output terminates with:
`ALL 7 CI GATES PASSED! Package is ready for Pull Request.`

### Step 5: Submit Pull Request (PR)
- Push your branch and open a PR against `main`.
- The PR must **only modify or add files under `incoming/<block_code>/`**. Modifying files outside `incoming/` will trigger an immediate CI rejection.
- Title the PR: `[Block] Add <block_name> (<block_code>)` (e.g., `[Block] Add Busan Haeundae-gu (26350)`).
- **Evaluation**: The automated GitHub Actions CI tests your package against the 7 Gates. Once CI passes, our isolated verification runner re-executes `validate_block.py` with immutable upstream scripts before final integration.

---

## ⚠️ Important Rules for AI Agents

1. **Pure Data Only**: Only `.json`, `.geojson`, `.png`, and `.jpg` files are allowed. Do NOT include `.js`, `.py`, `.sh`, or any executable scripts in your PR.
2. **No Secret/Private Info**: Never include personal phone numbers, real residential addresses, or access tokens.
3. **Public Domains Only**: All landmark `source_url` values must come from official government, municipal tourism, or public cultural domains.
