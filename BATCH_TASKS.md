# 20-Task Autonomous Benchmark: Korea Digital Twin Block Builder

Welcome to the 20-Task Autonomous Benchmark suite!

This benchmark evaluates the end-to-end data construction, validation, and submission throughput of autonomous agents across South Korea's administrative districts.

---

## 📋 Benchmark Rules & Quality Requirements

1. **One Task = One Branch = One PR**:
   - For each assigned task, create an isolated branch named `add-<block_code>`.
   - Construct `incoming/<block_code>/block.json` adhering strictly to `schema/block.schema.json`.
   - Validate locally using `python tools/validate_block.py incoming/<block_code>`.
   - Submit a Pull Request targeting `main` with title `[Block] Add <block_name> (<block_code>)`.

2. **Quality Standards (Strict)**:
   - **Landmark Count**: Each block must contain **at least 5 prominent landmarks**.
   - **Detailed Source URLs**: Each landmark's `source_url` must point to a **specific detail/subpage** (e.g., `https://www.tour.go.kr/...`, `https://visit.../subpage`, `https://www.heritage.go.kr/...`), NOT just the root domain homepage.

3. **Sequential Execution**:
   - Process tasks sequentially from Task 01 to Task 20.
   - In each PR description, include:
     - Start timestamp (UTC/KST)
     - Finish timestamp (UTC/KST)
     - Local 7-Gate validation result summary

4. **Failure Handling**:
   - If a task encounters unresolvable errors, document the root cause as a comment on the corresponding Issue, then proceed to the next task.
   - If 3 consecutive tasks fail due to the same error or an authentication failure occurs, halt execution and await instructions.

---

## 🗺️ 20-Task Assignment List (Non-overlapping Districts)

| Task No. | District Code | Administrative District Name | Target Branch |
| :---: | :---: | :--- | :--- |
| **Task 01** | `11200` | 서울특별시 성동구 | `add-11200` |
| **Task 02** | `11305` | 서울특별시 강북구 | `add-11305` |
| **Task 03** | `28177` | 인천광역시 미추홀구 | `add-28177` |
| **Task 04** | `28710` | 인천광역시 강화군 | `add-28710` |
| **Task 05** | `41285` | 경기도 고양시 일산동구 | `add-41285` |
| **Task 06** | `41830` | 경기도 양평군 | `add-41830` |
| **Task 07** | `42150` | 강원특별자치도 강릉시 | `add-42150` |
| **Task 08** | `42720` | 강원특별자치도 홍천군 | `add-42720` |
| **Task 09** | `43111` | 충청북도 청주시 상당구 | `add-43111` |
| **Task 10** | `43745` | 충청북도 영동군 | `add-43745` |
| **Task 11** | `44131` | 충청남도 천안시 동남구 | `add-44131` |
| **Task 12** | `44770` | 충청남도 서천군 | `add-44770` |
| **Task 13** | `30200` | 대전광역시 유성구 | `add-30200` |
| **Task 14** | `27260` | 대구광역시 수성구 | `add-27260` |
| **Task 15** | `26500` | 부산광역시 수영구 | `add-26500` |
| **Task 16** | `31140` | 울산광역시 남구 | `add-31140` |
| **Task 17** | `29110` | 광주광역시 동구 | `add-29110` |
| **Task 18** | `45111` | 전북특별자치도 전주시 완산구 | `add-45111` |
| **Task 19** | `46130` | 전라남도 여수시 | `add-46130` |
| **Task 20** | `50130` | 제주특별자치도 서귀포시 | `add-50130` |

---

## 🛡️ Evaluation Metrics

The following metrics are audited independently upon PR submission:
- Total completed PR count and execution duration per block
- 7-Gate CI pass rate
- Landmark detail source URL accessibility (HTTP 200 on public domains)
- Bounding box and coordinate boundary validity
