# 🚀 Pimang Sandbox: Advanced Progressive Enhancement Roadmap (Phase 9 to 12)
> **Author**: 3AI Team (Auditor Gemini & PM Manbok)  
> **Directive Source**: 바로보기님 09:04 지시 ("5~8은 이미 피망이가 접수 했으니 나머지는 그 다음 phase로 진행해")  
> **Design Philosophy**: 전국 250개 보편 공통 데이터(Phase 5~8) 100% 안착 후, 맞춤형 추가 설계가 필요한 심화 특화 옵션을 단계별로 체계화하여 릴레이 구축.

---

## 🏛️ Phase 9: Real-Time Traffic & Public CCTV Streaming Layer (도시 관제 & 실시간 도로)
- **목적**: 3D 블록 내 주요 교차로 및 고속도로/간선도로의 실시간 소통 현황 및 공공 오픈 CCTV HLS/RTSP 스트림 연동.
- **필수 스키마 확장 (`realtime_traffic_cctv`)**:
  - `cctv_id`: 공공데이터포털(UTIC) 국가교통정보센터 표준 식별자
  - `cctv_name`: 교차로/지점 명칭 (예: 서울 강남역 사거리, 부산 해운대 해변로)
  - `coordinates`: [lng, lat] 정밀 위경도
  - `stream_url`: HTTPS HLS 라이브 비디오 스트림 URL (웹 브라우저 즉시 재생용)
  - `traffic_status`: "smooth" | "slow" | "congested"

---

## ♿ Phase 10: Barrier-Free Mobility & Safe Accessibility (배리어프리 무장애 보행망)
- **목적**: 휠체어, 유모차, 교통약자를 위한 계단 없는 경사로, 지하철/육교 엘리베이터 정밀 동선 및 안심 보행로 매핑.
- **필수 스키마 확장 (`barrier_free_routes`)**:
  - `ramp_locations`: 경사로 및 단차 제거 구역 좌표 배열
  - `elevator_access`: 지하철/지상 연결 승강기 실시간 운행 좌표
  - `accessible_restrooms`: 장애인 공용 화장실 및 기저귀 교환대 위치
  - `grade_level`: "flat" (< 3%) | "gentle" (3~5%) | "steep" (> 8%, 경고)

---

## 🌦️ Phase 11: Dynamic Weather, Air Quality & Atmospheric Particles (실시간 환경 & 계절 파티클)
- **목적**: 기상청 단기예보 및 에어코리아 미세먼지 실시간 API 연동 + 3D 뷰포트 내 동적 날씨 이펙트(비, 눈, 안개, 야경 조명).
- **필수 스키마 확장 (`weather_station_anchor`)**:
  - `station_id`: 기상청/에어코리아 측정소 고유 ID
  - `temperature_celsius`: 기온 실시간 캐시
  - `pm10_grade`: "good" | "normal" | "bad" | "very_bad"
  - `shader_effect`: "clear_sky" | "rain_droplets" | "snow_fall" | "autumn_leaves"

---

## 🎪 Phase 12: Local Festivals, Cultural Events & Gamified Quests (지역 축제 & 스탬프투어 퀘스트)
- **목적**: 매월 갱신되는 250개 시·군·구 대표 문화 축제 캘린더 및 방문객 체류 시간을 극대화하는 게이미피케이션 탐험 퀘스트.
- **필수 스키마 확장 (`festival_quests`)**:
  - `festival_name`: 축제 명칭 (예: 보령머드축제, 진주남강유등축제)
  - `event_period`: [YYYY-MM-DD, YYYY-MM-DD]
  - `quest_targets`: 3D 블록 내 지정 랜드마크 3개 방문 시 디지털 스탬프 획득
  - `badge_reward`: "explorer_bronze" | "explorer_silver" | "master_gold"

---

### 📋 3AI 거버넌스 릴레이 원칙
1. 피망팀은 현재 할당된 **Phase 5~8 보편 공통 데이터(대중교통, 주차, 대피소, 사계절, 3개국어)**를 차질 없이 완주합니다.
2. Phase 5~8 완료 및 3AI 전수 교차검증 통과 즉시, 본 **Phase 9~12 심화 명세서**가 자동으로 Issue 트리거되어 차기 릴레이로 오픈됩니다.
