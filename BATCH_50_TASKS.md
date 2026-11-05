# 50-Task Autonomous Benchmark: Korea Digital Twin Block Builder

Welcome to the 50-Task Autonomous Benchmark suite for AI Agents!

This benchmark evaluates the end-to-end 24-hour data construction, validation, and submission throughput of autonomous agents across 50 South Korean administrative districts.

---

## 📋 Benchmark Rules & Quality Standards

1. **One Task = One Branch = One PR**:
   - For each task, create an isolated branch named `add-<block_code>`.
   - Construct `incoming/<block_code>/block.json` adhering strictly to `schema/block.schema.json`.
   - Validate locally: `python tools/validate_block.py incoming/<block_code>`.
   - Submit a Pull Request targeting `main` with title `[Block] Add <block_name> (<block_code>)`.

2. **Quality Standards (Strict)**:
   - **Landmark Count**: Minimum **5 prominent landmarks** per block.
   - **Detailed Source URLs**: Each landmark's `source_url` must point to an official detail/subpage (e.g. tourism subpage, cultural heritage portal), NOT just a root domain homepage.
   - **BBox & Center**: Accurately bounded around the district boundaries in WGS84 coordinates.

3. **Sequential Execution**:
   - Process sequentially from Task 01 to Task 50.
   - Document start timestamp, end timestamp, and local validation status in each PR body.

4. **Failure Handling**:
   - If an error occurs, record details as an Issue comment and move to the next task.
   - If 3 consecutive tasks encounter the same error or an authentication failure occurs, halt and await instructions.

---

## 🗺️ 50-Task Assignment List

| Task No. | District Code | Administrative District Name | Target Branch |
| :---: | :---: | :--- | :--- |
| **Task 01** | `11200` | 서울특별시 성동구 | `add-11200` |
| **Task 02** | `11305` | 서울특별시 강북구 | `add-11305` |
| **Task 03** | `11230` | 서울특별시 동대문구 | `add-11230` |
| **Task 04** | `11260` | 서울특별시 중랑구 | `add-11260` |
| **Task 05** | `11350` | 서울특별시 노원구 | `add-11350` |
| **Task 06** | `11470` | 서울특별시 양천구 | `add-11470` |
| **Task 07** | `11500` | 서울특별시 강서구 | `add-11500` |
| **Task 08** | `11560` | 서울특별시 영등포구 | `add-11560` |
| **Task 09** | `11590` | 서울특별시 동작구 | `add-11590` |
| **Task 10** | `11620` | 서울특별시 관악구 | `add-11620` |
| **Task 11** | `28177` | 인천광역시 미추홀구 | `add-28177` |
| **Task 12** | `28185` | 인천광역시 연수구 | `add-28185` |
| **Task 13** | `28200` | 인천광역시 남동구 | `add-28200` |
| **Task 14** | `28237` | 인천광역시 부평구 | `add-28237` |
| **Task 15** | `28710` | 인천광역시 강화군 | `add-28710` |
| **Task 16** | `41285` | 경기도 고양시 일산동구 | `add-41285` |
| **Task 17** | `41190` | 경기도 부천시 | `add-41190` |
| **Task 18** | `41271` | 경기도 안산시 상록구 | `add-41271` |
| **Task 19** | `41390` | 경기도 시흥시 | `add-41390` |
| **Task 20** | `41450` | 경기도 하남시 | `add-41450` |
| **Task 21** | `41480` | 경기도 파주시 | `add-41480` |
| **Task 22** | `41590` | 경기도 화성시 | `add-41590` |
| **Task 23** | `41830` | 경기도 양평군 | `add-41830` |
| **Task 24** | `41800` | 경기도 연천군 | `add-41800` |
| **Task 25** | `42150` | 강원특별자치도 강릉시 | `add-42150` |
| **Task 26** | `42110` | 강원특별자치도 춘천시 | `add-42110` |
| **Task 27** | `42130` | 강원특별자치도 원주시 | `add-42130` |
| **Task 28** | `42720` | 강원특별자치도 홍천군 | `add-42720` |
| **Task 29** | `42820` | 강원특별자치도 고성군 | `add-42820` |
| **Task 30** | `43111` | 충청북도 청주시 상당구 | `add-43111` |
| **Task 31** | `43130` | 충청북도 충주시 | `add-43130` |
| **Task 32** | `43745` | 충청북도 영동군 | `add-43745` |
| **Task 33** | `43770` | 충청북도 음성군 | `add-43770` |
| **Task 34** | `44131` | 충청남도 천안시 동남구 | `add-44131` |
| **Task 35** | `44200` | 충청남도 아산시 | `add-44200` |
| **Task 36** | `44770` | 충청남도 서천군 | `add-44770` |
| **Task 37** | `44800` | 충청남도 예산군 | `add-44800` |
| **Task 38** | `30200` | 대전광역시 유성구 | `add-30200` |
| **Task 39** | `30140` | 대전광역시 중구 | `add-30140` |
| **Task 40** | `27260` | 대구광역시 수성구 | `add-27260` |
| **Task 41** | `27290` | 대구광역시 달서구 | `add-27290` |
| **Task 42** | `26500` | 부산광역시 수영구 | `add-26500` |
| **Task 43** | `26440` | 부산광역시 강서구 | `add-26440` |
| **Task 44** | `31140` | 울산광역시 남구 | `add-31140` |
| **Task 45** | `31710` | 울산광역시 울주군 | `add-31710` |
| **Task 46** | `29110` | 광주광역시 동구 | `add-29110` |
| **Task 47** | `45111` | 전북특별자치도 전주시 완산구 | `add-45111` |
| **Task 48** | `46130` | 전라남도 여수시 | `add-46130` |
| **Task 49** | `47130` | 경상북도 경주시 | `add-47130` |
| **Task 50** | `50130` | 제주특별자치도 서귀포시 | `add-50130` |

---

## 🛡️ Evaluation Metrics

The following metrics are audited independently upon PR submission:
- Completed PR throughput count over 24 hours
- 7-Gate CI pass rate
- Landmark detail source URL accessibility (HTTP 200 on public domains)
- Bounding box and coordinate boundary validity
