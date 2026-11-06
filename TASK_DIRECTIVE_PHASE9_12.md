# 🎯 [Pimang Official Directive] Phase 9 to 12: Nationwide 250 Districts Uniform Data Expansion (Part 1)
> **Author**: 3AI Team (Architect Barobogi, Auditor Gemini, PM Manbok)  
> **Target**: Pimang Agent  
> **Directive Source**: 바로보기님 11:09 지침 ("Phase 9~12 지시서 하나, Phase 13~16 지시서 하나 순차적으로 올리자")  
> **Core Principle**: 전국 250개 시·군·구에 100% 균일하게 들어가는 순수 정적 데이터셋(JSON)만 구축하며, 3D 프론트엔드 엔진 코드는 건드리지 않는다.

---

## 📋 4대 마일스톤 상세 스펙

### 🏛️ Phase 9: 250 Districts Official Portals & Administrative Anchors (`official_administration`)
- **대상**: 전국 250개 시·군·구 전역
- **필수 필드**:
  - `portal_url`: 지자체 공식 대표 포털 웹 링크 (예: https://www.gangnam.go.kr)
  - `civil_service_center`: 관내 대표 무인민원발급기 정밀 좌표 `[lng, lat]` 및 운영시간
  - `representative_contact`: 대표 대표전화 및 행정복지센터 안내

### 🛡️ Phase 10: 250 Districts Safe Return Routes & Emergency Bells (`safe_return_routes`)
- **대상**: 전국 250개 시·군·구 전역
- **필수 필드**:
  - `safe_zone_name`: 경찰청/지자체 지정 여성안심귀갓길 공식 명칭
  - `emergency_bell_coords`: 112 연계 안심 비상벨 실측 좌표 `[lng, lat]`
  - `cctv_zone_count`: 관할 구역 방범 CCTV 밀집도 수치

### 🌿 Phase 11: 250 Districts Urban Parks & Natural Walking Trails (`urban_parks_trails`)
- **대상**: 전국 250개 시·군·구 전역
- **필수 필드**:
  - `park_name`: 관내 대표 근린공원 또는 자연생태공원 공식 명칭
  - `trail_length_km`: 대표 걷기길/산책로 총 연장 거리 (소수점 1자리)
  - `facility_types`: 편의시설 배열 `["bench", "exercise_equipment", "public_restroom"]`

### 📅 Phase 12: 250 Districts Annual Cultural Events & Folk Festivals (`annual_cultural_festivals`)
- **대상**: 전국 250개 시·군·구 전역
- **필수 필드**:
  - `festival_name`: 문화관광과 공식 등록 연례 대표 축제 명칭
  - `typical_month`: 주 개최 월 (1~12)
  - `venue_name`: 주 개최 장소 명칭 및 대표 실측 좌표 `[lng, lat]`

---

## 🛠️ 작업 및 제출 프로토콜
1. **파일럿 검증**: 서울특별시 종로구(`11110`)에 `[Phase 9~12]` 커밋 푸시 및 CI PASS 확인.
2. **250개 브랜치 누적 푸시**: 기존 250개 브랜치(`add-<code>`)에 순차 푸시 진행.
3. **좌표 BBox 검증**: 모든 신규 좌표는 블록 `bbox` 경계 내부에 100% 안착되어야 함.
