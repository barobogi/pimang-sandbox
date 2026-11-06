# 📜 [TASK DIRECTIVE] Phase 17 ~ 20 스마트 모바일 혁신 패키지 구축 지시서 (v1.1)

> **수신**: 피망 (Pimang Mobile Assistant)  
> **발신**: 3AI 총괄 아키텍처 팀 (바로보기, 감사관 제미나이, 기획 PM 만복, 엔진 개발 안티)  
> **근거**: 피망 역제안 `docs/GLOBAL_DEEP_SEARCH_MOBILE_250_DIGITAL_TWIN.md` (Issue #255) 전격 수용 & 안티 15:00 공학 엔진 요구사항 100% 통합  
> **문서 버전**: v1.1 (Phase 17~20 공식 확정 지시서)  

---

## 🎯 미션 개요: 250개 시·군·구 "모바일 킬러 UX & 3D 엔진 결합" 4대 데이터 패키지

피망이 제안한 7대 혁신 기능과 안티의 3D 뷰어 엔진이 완벽히 맞물려 작동할 수 있도록, 250개 전 시·군·구에 걸쳐 다음 **4대 후속 데이터 패키지(Phase 17~20)**를 추가 구축합니다.

---

## 📋 4대 세부 과업 규격

### 🚗 Phase 17: 외부 내비게이션 딥링크 스키마 (`external_navigation_links`)
- **목적**: 250개 시군구의 랜드마크, EV급속충전소, 체육시설 핀 터치 시 즉시 스마트폰 내비게이션 길안내로 연결.
- **필드 스펙**:
  ```json
  "external_navigation_links": {
    "tmap_url": "tmap://route?goalname={명칭}&goalx={lng}&goaly={lat}",
    "kakaonavi_url": "kakaonavi://navigate?name={명칭}&x={lng}&y={lat}&coord_type=wgs84",
    "navermap_url": "nmap://navigation?dname={명칭}&dlng={lng}&dlat={lat}&appname=barobogi_3d_map"
  }
  ```
- **필수 준수**: 각 지자체 대표 청사 및 Phase 15 EV급속충전소 실측 좌표 기반 100% 매핑.

---

### ☀️ Phase 18: 4D 일조·일몰 천문 프로필 (`astronomical_sunlight_profile`)
- **목적**: 4D 타임 슬라이더(06:00~24:00) 조작 시 Three.js WebGL 조명 셰이더의 태양 위치와 그림자 길이를 과학적으로 시뮬레이션.
- **필드 스펙**:
  ```json
  "astronomical_sunlight_profile": {
    "spring_equinox": {"sunrise": "06:35", "sunset": "18:45", "noon_altitude_deg": 52.5},
    "summer_solstice": {"sunrise": "05:12", "sunset": "19:55", "noon_altitude_deg": 76.0},
    "autumn_equinox": {"sunrise": "06:20", "sunset": "18:30", "noon_altitude_deg": 52.0},
    "winter_solstice": {"sunrise": "07:42", "sunset": "17:15", "noon_altitude_deg": 29.0}
  }
  ```
- **필수 준수**: 250개 지자체 중심좌표(`center`) 위·경도에 기반한 천문 계산 수치 반영.

---

### 🛡️ Phase 19: 안심귀가 HUD 네온패스 선형 좌표 (`safe_return_neon_paths`)
- **목적**: 야간 '심야 세이프티 모드' 전환 시 3D 지도 바닥에 야광 네온 안전 경로(LineString)를 그리기 위한 선형 노드 좌표.
- **필드 스펙**:
  ```json
  "safe_return_neon_paths": [
    {
      "path_name": "종로 관철동 여성안심귀갓길",
      "path_nodes": [
        [126.9831, 37.5695],
        [126.9845, 37.5698],
        [126.9860, 37.5702]
      ],
      "cctv_linked_count": 8,
      "bell_node_index": 1
    }
  ]
  ```
- **필수 준수**: 3~5개 굴절 노드로 구성된 경량 LineString 좌표 (지자체 BBox 내부 실측 안착).

---

### 🚶 Phase 20: 도톤보리형 200m 마이크로존 보행거리 앵커 (`micro_walk_zone_anchors`)
- **목적**: 바로보기님 14:09 디렉팅(도톤보리 스트리트뷰 아바타 보행) 구현을 위해 지자체별 핵심 핫스팟 골목길을 1인칭 모드로 즉시 줌인 전환하는 카메라 앵커.
- **필드 스펙**:
  ```json
  "micro_walk_zone_anchors": {
    "zone_name": "종로 관철동 젊음의 거리",
    "anchor_center": [126.9842, 37.5698],
    "walk_radius_m": 200,
    "recommended_camera": {
      "pitch_deg": 25,
      "heading_deg": 180,
      "altitude_m": 1.6
    },
    "target_facade_theme": "commercial_street"
  }
  ```
- **필수 준수**: 관내 가장 유동인구가 많거나 특색 있는 대표 보행거리 1곳 고유 매핑.

---

## 🛠️ 작업 및 PR 전달 프로세스
1. **작업 대상**: `barobogi/pimang-sandbox` 250개 기존 PR 브랜치 (`add-<코드>`) 누적 커밋
2. **검증 게이트**: CI 7-Gate 자동 검증 통과 후 PR 갱신
3. **배포 순서**: 준비 완료 시 종로구(`11110`) 파일럿 PR 우선 제출 후 250개 전역 순차 전개!
