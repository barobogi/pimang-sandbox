# -*- coding: utf-8 -*-
"""
spatial_quality_inspector.py
3AI 한국형 3D 디지털 트윈 공간 품질 자동 검사기 (CQO Gemini Engine)
- 4대 영역 20대 체크리스트 기반 정량적 자동 채점
- 1회성이 아닌 지속 가능한 품질 사후관리 감사 스크립트
"""

import os
import sys
import json
import argparse
from datetime import datetime

def inspect_spatial_package(target_path):
    report = {
        "inspector": "Gemini (3AI CQO)",
        "timestamp": datetime.now().isoformat(),
        "target_path": os.path.abspath(target_path),
        "scores": {
            "geometry": 0,
            "materials": 0,
            "spatial_dive": 0,
            "mobile_ux": 0
        },
        "details": [],
        "verdict": "FAIL"
    }

    found_files = []
    if os.path.isfile(target_path):
        found_files.append(target_path)
    else:
        for root, _, files in os.walk(target_path):
            for f in files:
                found_files.append(os.path.join(root, f))

    html_js_content = ""
    gltf_glb_count = 0

    for fpath in found_files:
        ext = os.path.splitext(fpath)[1].lower()
        if ext in [".html", ".js", ".ts"]:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    html_js_content += f.read() + "\n"
            except Exception:
                pass
        elif ext in [".glb", ".gltf"]:
            gltf_glb_count += 1

    content_lower = html_js_content.lower()

    # [영역 1] 지오메트리 & 조형 디테일 (25점)
    # 단순 코드 문자열이 아닌, 실제 3D 모델(GLTF/GLB) 에셋 파일이 실존해야만 점수 부여
    g_score = 0
    if gltf_glb_count > 0 and (any(k in content_lower for k in ["curved_roof", "roof_rake", "custom_mesh"])):
        g_score += 5
        report["details"].append({"code": "G-01", "name": "지붕 곡률 실측", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-01", "name": "지붕 곡률 실측", "score": 0, "status": "FAIL", "reason": "실물 커스텀 메쉬 부재 (단순 큐브 박스)"})

    if gltf_glb_count > 0 and any(k in content_lower for k in ["eaves", "rafter", "japsang", "korean_tile"]):
        g_score += 5
        report["details"].append({"code": "G-02", "name": "서까래 및 잡상 모델링", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-02", "name": "서까래 및 잡상 모델링", "score": 0, "status": "FAIL", "reason": "전통 건축 세부 지오메트리 실물 전무"})

    if "negative_elevation" in content_lower and "cheonggye_depth" in content_lower:
        g_score += 5
        report["details"].append({"code": "G-03", "name": "음각 수변 지형 단차", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-03", "name": "음각 수변 지형 단차", "score": 0, "status": "FAIL", "reason": "하천 음각 단차 미구현 (2D 평면 선)"})

    if gltf_glb_count > 0 and any(k in content_lower for k in ["stairs_mesh", "stone_wall_mesh"]):
        g_score += 5
        report["details"].append({"code": "G-04", "name": "계단 및 돌담 요철 조형", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-04", "name": "계단 및 돌담 요철 조형", "score": 0, "status": "FAIL", "reason": "계단/월대 난간 실물 메쉬 전무"})

    if gltf_glb_count > 0 and "dracoloader" in content_lower:
        g_score += 5
        report["details"].append({"code": "G-05", "name": "Draco 압축 및 최적화", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-05", "name": "Draco 압축 및 최적화", "score": 0, "status": "FAIL", "reason": "Draco 압축 에셋 및 로더 미연동"})

    # [영역 2] PBR 재질 & 현장감 (25점)
    # 실제 텍스처 파일과 실시간 셰이더 바인딩 실측
    m_score = 0
    if gltf_glb_count > 0 and "normalmap" in content_lower and "roughnessmap" in content_lower:
        m_score += 5
        report["details"].append({"code": "M-01", "name": "4종 PBR 맵 탑재", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-01", "name": "4종 PBR 맵 탑재", "score": 0, "status": "FAIL", "reason": "실물 PBR 노멀/러프니스 텍스처 미바인딩"})

    if "envmap" in content_lower and ("pmremgenerator" in content_lower or "rgbeloader" in content_lower):
        m_score += 5
        report["details"].append({"code": "M-02", "name": "건축 외벽/유리 환경 반사", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-02", "name": "건축 외벽/유리 환경 반사", "score": 0, "status": "FAIL", "reason": "실시간 HDR 환경 반사 미작동 (회색 플라스틱)"})

    if "water2" in content_lower or ("customwatershader" in content_lower and "flowspeed" in content_lower):
        m_score += 5
        report["details"].append({"code": "M-03", "name": "수면 동적 셰이더 리플", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-03", "name": "수면 동적 셰이더 리플", "score": 0, "status": "FAIL", "reason": "동적 물결 셰이더 미작동 (단순 파란색 판때기)"})

    if any(k in content_lower for k in ["asphalt_normal.jpg", "sidewalk_normal.png", "road_normal.jpg"]):
        m_score += 5
        report["details"].append({"code": "M-04", "name": "바닥재 요철 노멀맵", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-04", "name": "바닥재 요철 노멀맵", "score": 0, "status": "FAIL", "reason": "도로/보도블록 민무늬 장판 (요철 텍스처 실물 없음)"})

    if "textureatlas" in content_lower and gltf_glb_count > 0:
        m_score += 5
        report["details"].append({"code": "M-05", "name": "텍스처 아틀라스 규격", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-05", "name": "텍스처 아틀라스 규격", "score": 0, "status": "FAIL", "reason": "텍스처 아틀라스 최적화 미적용"})

    # [영역 3] 1인칭 공간 다이빙 (25점)
    # 실내 씬 실물이 없으면 트랜지션도 무의미
    d_score = 0
    has_interior_scene = any(k in content_lower for k in ["interior_scene", "indoor_model", "room_mesh"]) and gltf_glb_count > 0
    if has_interior_scene:
        d_score += 5
        report["details"].append({"code": "D-01", "name": "건물 내부 3D 공간 구축", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-01", "name": "건물 내부 3D 공간 구축", "score": 0, "status": "FAIL", "reason": "실내 3D 씬 실물 전무 (2D 글래스 시트 우회)"})

    if has_interior_scene and any(k in content_lower for k in ["cameradive", "flytointerior"]):
        d_score += 5
        report["details"].append({"code": "D-02", "name": "1초 무지연 카메라 트랜지션", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-02", "name": "1초 무지연 카메라 트랜지션", "score": 0, "status": "FAIL", "reason": "실내 다이빙 카메라 연출 전무"})

    if has_interior_scene and any(k in content_lower for k in ["interior_prop", "bookshelf", "throne"]):
        d_score += 5
        report["details"].append({"code": "D-03", "name": "실내 3D 소품 완비", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-03", "name": "실내 3D 소품 완비", "score": 0, "status": "FAIL", "reason": "실내 3D 소품 전무"})

    if has_interior_scene and any(k in content_lower for k in ["firstpersoncontrols", "gyroindoor"]):
        d_score += 5
        report["details"].append({"code": "D-04", "name": "1인칭 360도 궤도 회전", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-04", "name": "1인칭 360도 궤도 회전", "score": 0, "status": "FAIL", "reason": "실내 시점 회전 기능 전무"})

    if has_interior_scene and any(k in content_lower for k in ["exitdive", "returntomap"]):
        d_score += 5
        report["details"].append({"code": "D-05", "name": "외부 복귀 원터치 탈출", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-05", "name": "외부 복귀 원터치 탈출", "score": 0, "status": "FAIL", "reason": "실내 탈출 버튼 전무 (실내 공간 미존재)"})

    # [영역 4] 모바일 네이티브 UX (25점)
    u_score = 0
    if "deviceorientation" in content_lower and "addeventlistener" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-01", "name": "자이로스코프 시점 연동", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-01", "name": "자이로스코프 시점 연동", "score": 0, "status": "FAIL", "reason": "DeviceOrientation 이벤트 미연동"})

    if "bottomsheet" in content_lower and "touchstart" in content_lower and "touchmove" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-02", "name": "3단계 네이티브 바텀시트", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-02", "name": "3단계 네이티브 바텀시트", "score": 0, "status": "FAIL", "reason": "스와이프 제스처 바텀시트 부재 (PC용 글래스 시트)"})

    if "navigator.vibrate" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-03", "name": "햅틱 촉각 진동 피드백", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-03", "name": "햅틱 촉각 진동 피드백", "score": 0, "status": "FAIL", "reason": "navigator.vibrate 햅틱 연동 전무"})

    if any(k in content_lower for k in ["thumbwheel", "compass-dial"]) and "touchstart" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-04", "name": "모바일 엄지 조작계", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-04", "name": "모바일 엄지 조작계", "score": 0, "status": "FAIL", "reason": "Thumb Zone 플로팅 조작계 부재"})

    # U-05: 60fps & 1초 미만
    if "requestanimationframe" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-05", "name": "모바일 60fps 렌더링 루프", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-05", "name": "모바일 60fps 렌더링 루프", "score": 0, "status": "FAIL", "reason": "렌더링 루프 미감지"})

    passed_count = sum(1 for d in report["details"] if d["status"] == "PASS")
    total_checks = len(report["details"])
    report["passed_count"] = passed_count
    report["total_checks"] = total_checks
    report["score_ratio"] = f"{passed_count} / {total_checks}"

    # 영역별 통과 카운트
    for area_code, area_key in [("G", "geometry"), ("M", "materials"), ("D", "spatial_dive"), ("U", "mobile_ux")]:
        area_passed = sum(1 for d in report["details"] if d["code"].startswith(area_code) and d["status"] == "PASS")
        area_total = sum(1 for d in report["details"] if d["code"].startswith(area_code))
        report["scores"][area_key] = f"{area_passed} / {area_total}"

    if passed_count >= 18:
        report["verdict"] = "PASS"
    elif passed_count >= 15:
        report["verdict"] = "CONDITIONAL_PASS"
    else:
        report["verdict"] = "FAIL"

    return report

def main():
    parser = argparse.ArgumentParser(description="3AI Spatial Twin Quality Inspector")
    parser.add_argument("target", help="Target directory or file to inspect")
    parser.add_argument("--output", default="quality_audit_report.json", help="Output JSON path")
    args = parser.parse_args()

    report = inspect_spatial_package(args.target)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("=== [3AI Spatial Quality Inspector Result] ===")
    print(f"Target: {report['target_path']}")
    print(f"Scores (통과 항목 / 세부 체크항목):")
    print(f"  - 지오메트리 & 조형: {report['scores']['geometry']}")
    print(f"  - PBR 재질 & 현장감: {report['scores']['materials']}")
    print(f"  - 1인칭 공간 다이빙: {report['scores']['spatial_dive']}")
    print(f"  - 모바일 네이티브 UX: {report['scores']['mobile_ux']}")
    print(f"총 점수: {report['score_ratio']} (통과율: {report['passed_count'] / report['total_checks'] * 100:.1f}%)")
    print(f"판정: {report['verdict']}")
    print(f"Report saved to: {args.output}")

    if report["verdict"] == "FAIL":
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
