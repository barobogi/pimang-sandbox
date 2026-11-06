# 🚀 Pimang Sandbox: Advanced 250-District Uniform Data Roadmap (Phase 9 to 12)
> **Author**: 3AI Team (Auditor Gemini & PM Manbok)  
> **Directive Source**: 바로보기님 09:09 지시 ("250개 블럭에 동일하게 적용 가능한 건 Phase 9~ 이후로 순차 선배치하고, 별도 구현 설계가 필요한 건 1106_N 등 별도 Task로 구분")  
> **Core Principle**: 피망(Pimang) 파이프라인은 **전국 250개 시·군·구에 100% 동일하게 들어가는 순수 정적 데이터(GeoJSON/JSON)**에만 집중하며, 복잡한 프론트엔드 엔진/셰이더/플레이어 구현 코드는 절대 건드리지 않는다.

---

## 🏛️ Phase 9: 250 Districts Official Public Portals & Administrative Anchors (250개 공식 행정 포털 및 민원 앵커)
- **목적**: 250개 모든 지자체의 공식 대표 웹사이트, 구정/군정 소식, 무인민원발급기 위치 데이터 일괄 구축.
- **250개 공통 스키마 (`official_administration`)**:
  - `portal_url`: 지자체 공식 대표 포털 링크 (예: https://www.gangnam.go.kr)
  - `civil_service_center`: 관내 대표 무인민원발급기 좌표 [lng, lat] 및 운영시간
  - `representative_contact`: 대표 대표전화 및 행정복지센터 안내

---

## 🛡️ Phase 10: 250 Districts Civil Defense & Safe Return Routes (250개 안심 귀갓길 및 공식 대피소)
- **목적**: 전국 250개 지자체 경찰청/행안부 지정 공식 여성안심귀갓길 및 민방위/지진 옥외대피장소 보편 데이터.
- **250개 공통 스키마 (`safe_return_routes`)**:
  - `safe_zone_name`: 안심귀갓길 공식 지정 명칭
  - `emergency_bell_coords`: 112 연계 비상벨 위치 좌표 [lng, lat]
  - `cctv_zone_count`: 관할 구역 내 방범 CCTV 밀집도 수치

---

## 🌿 Phase 11: 250 Districts Urban Parks & Natural Walking Trails (250개 도시공원 및 걷기길 공통 DB)
- **목적**: 250개 시군구 전역에 존재하는 근린공원, 산책로, 둘레길 기본 메타데이터.
- **250개 공통 스키마 (`urban_parks_trails`)**:
  - `park_name`: 공원 또는 산책길 공식 명칭
  - `trail_length_km`: 총 연장 거리
  - `facility_types`: ["bench", "exercise_equipment", "public_restroom"]

---

## 📅 Phase 12: 250 Districts Annual Cultural Events & Folk Festivals (250개 연간 대표 축제/행사 메타데이터)
- **목적**: 250개 시군구 문화관광과 공식 등록 연례 대표 축제 및 계절 행사 메타데이터.
- **250개 공통 스키마 (`annual_cultural_festivals`)**:
  - `festival_name`: 대표 축제 명칭
  - `typical_month`: 주 개최 월 (1~12)
  - `venue_name`: 주 개최 장소 및 대표 좌표 [lng, lat]

---

### ⚠️ 엔진/UI 구현 분리 안내 (3AI 독립 Task 배정)
- 본 로드맵(Phase 9~12)은 **순수 데이터셋**만을 다룹니다.
- 실시간 비디오 스트리밍, 3D 카툰 셰이더, 미니맵 레이더 등 **엔진 및 UI 구현**은 3AI 팀의 `[TASK_1106_2]`, `[TASK_1106_3]`, `[TASK_1106_CCTV]`로 별도 분리되어 안티/클라인이 독립 개발합니다.
