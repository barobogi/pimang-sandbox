# 🎯 [Pimang Official Directive] Phase 13 to 16: Nationwide 250 Districts Uniform Data Expansion (Part 2)
> **Author**: 3AI Team (Architect Barobogi, Auditor Gemini, PM Manbok)  
> **Target**: Pimang Agent  
> **Directive Source**: 바로보기님 11:09 지침 ("Phase 9~12 지시서 하나, Phase 13~16 지시서 하나 순차적으로 올리자")  
> **Trigger Condition**: Phase 9~12 완주 및 바로보기님의 차기 착수 지시 시 릴레이 실행.

---

## 📋 4대 마일스톤 상세 스펙

### ⚽ Phase 13: 250 Districts Public Sports & Community Fields (`public_sports_facilities`)
- **대상**: 전국 250개 시·군·구 전역
- **데이터 원천**: 국민체육진흥공단 공공체육포털 / 지자체 체육진흥과
- **필수 필드**:
  - `facility_name`: 관내 대표 국민체육센터, 공공 축구장, 풋살장, 테니스장, 파크골프장 명칭
  - `sports_types`: 지원 종목 배열 `["soccer", "tennis", "futsal", "badminton"]`
  - `coordinates`: 시설 정밀 실측 좌표 `[lng, lat]`
  - `reservation_url`: 공공 예약 시스템 웹 링크 (있을 경우)

### 📦 Phase 14: 250 Districts Smart Civic Kiosks & Safety Lockers (`smart_civic_kiosks`)
- **대상**: 전국 250개 시·군·구 전역
- **데이터 원천**: 행정안전부 / 지자체 스마트도시과
- **필수 필드**:
  - `kiosk_name`: 여성안심 무인택배함 또는 지하철/복지관 스마트 도서관 명칭
  - `kiosk_type`: `"safe_parcel_locker"` | `"smart_library"` | `"eco_collection_box"`
  - `coordinates`: 무인 부스 실측 좌표 `[lng, lat]`
  - `operating_hours`: 운영 시간 (예: "24 hours" 또는 "05:30 - 24:00")

### ⚡ Phase 15: 250 Districts Eco-Mobility Rapid Charging Hubs (`ev_charging_hubs`)
- **대상**: 전국 250개 시·군·구 전역
- **데이터 원천**: 환경부 무공해차 통합누리집
- **필수 필드**:
  - `station_name`: 급속/초급속(100kW 이상) 전기차 충전소 또는 수소충전소 명칭
  - `coordinates`: 충전소 정밀 실측 좌표 `[lng, lat]`
  - `charger_types`: 급속 커넥터 타입 `["DC_COMBO", "CHAdeMO"]`
  - `fast_charger_count`: 100kW 이상 급속 충전기 보유 면수

### 🍽️ Phase 16: 250 Districts Ministry-Certified Hygiene Dining (`certified_hygiene_dining`)
- **대상**: 전국 250개 시·군·구 전역
- **데이터 원천**: 식품의약품안전처 음식점 위생등급제 오픈데이터
- **필수 필드**:
  - `restaurant_name`: 식약처 위생평가 최고 등급 **'매우 우수(★★★)'** 인증 식당 명칭
  - `coordinates`: 식당 실측 좌표 `[lng, lat]`
  - `grade`: `"VERY_GOOD_3_STARS"` | `"MODEL_RESTAURANT"`
  - `specialty_menu`: 대표 메뉴 및 인증 유효기간

---

## 🛠️ 작업 및 제출 프로토콜
1. Phase 9~12 완료 승인 후 본 지시서 트리거.
2. 전국 250개 PR 브랜치(`add-<code>`)에 `[Phase 13~16]` 커밋으로 순차 푸시.
3. 250개 전역 BBox 경계선 내부 100% 안착 필수.
