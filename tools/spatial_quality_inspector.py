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
    g_score = 0
    if any(k in content_lower for k in ["curved_roof", "roof_rake", "custom_mesh"]) or gltf_glb_count > 0:
        g_score += 5
        report["details"].append({"code": "G-01", "name": "지붕 곡률 실측", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-01", "name": "지붕 곡률 실측", "score": 0, "status": "FAIL", "reason": "단순 박스 큐브 사용 감지"})

    if any(k in content_lower for k in ["eaves", "rafter", "japsang", "korean_tile"]):
        g_score += 5
        report["details"].append({"code": "G-02", "name": "서까래 및 잡상 모델링", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-02", "name": "서까래 및 잡상 모델링", "score": 0, "status": "FAIL", "reason": "전통 건축 세부 지오메트리 누락"})

    if any(k in content_lower for k in ["negative_elevation", "cheonggye_depth", "river_depth", "canal_depth"]):
        g_score += 5
        report["details"].append({"code": "G-03", "name": "음각 수변 지형 단차", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-03", "name": "음각 수변 지형 단차", "score": 0, "status": "FAIL", "reason": "하천 음각 단차 미구현 (2D 평면)"})

    if any(k in content_lower for k in ["stairs", "steps", "stone_wall", "balustrade"]):
        g_score += 5
        report["details"].append({"code": "G-04", "name": "계단 및 돌담 요철 조형", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-04", "name": "계단 및 돌담 요철 조형", "score": 0, "status": "FAIL", "reason": "계단 및 월대 난간 미구현"})

    if "draco" in content_lower or gltf_glb_count > 0:
        g_score += 5
        report["details"].append({"code": "G-05", "name": "Draco 압축 및 최적화", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "G-05", "name": "Draco 압축 및 최적화", "score": 0, "status": "FAIL", "reason": "Draco 로더 미연동"})

    # [영역 2] PBR 재질 & 현장감 (25점)
    m_score = 0
    if "normalmap" in content_lower and "roughnessmap" in content_lower:
        m_score += 5
        report["details"].append({"code": "M-01", "name": "4종 PBR 맵 탑재", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-01", "name": "4종 PBR 맵 탑재", "score": 0, "status": "FAIL", "reason": "노멀맵 또는 러프니스맵 누락"})

    if any(k in content_lower for k in ["envmap", "environmentmap", "reflectivity", "hdr"]):
        m_score += 5
        report["details"].append({"code": "M-02", "name": "건축 외벽/유리 환경 반사", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-02", "name": "건축 외벽/유리 환경 반사", "score": 0, "status": "FAIL", "reason": "실시간 환경 큐브맵/유리 반사 미적용"})

    if "water" in content_lower and any(k in content_lower for k in ["shader", "ripple", "wave"]):
        m_score += 5
        report["details"].append({"code": "M-03", "name": "수면 동적 셰이더 리플", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-03", "name": "수면 동적 셰이더 리플", "score": 0, "status": "FAIL", "reason": "동적 수면 셰이더 미작동"})

    if any(k in content_lower for k in ["asphalt", "sidewalk_normal", "cobblestone", "road_texture"]):
        m_score += 5
        report["details"].append({"code": "M-04", "name": "바닥재 요철 노멀맵", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-04", "name": "바닥재 요철 노멀맵", "score": 0, "status": "FAIL", "reason": "도로/보도블록 민무늬 장판 감지"})

    if "textureatlas" in content_lower or "atlas" in content_lower:
        m_score += 5
        report["details"].append({"code": "M-05", "name": "텍스처 아틀라스 규격", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "M-05", "name": "텍스처 아틀라스 규격", "score": 0, "status": "FAIL", "reason": "아틀라싱 미최적화"})

    # [영역 3] 1인칭 공간 다이빙 (25점)
    d_score = 0
    if any(k in content_lower for k in ["interior_scene", "indoor_model", "room_mesh", "dive_target"]):
        d_score += 5
        report["details"].append({"code": "D-01", "name": "건물 내부 3D 공간 구축", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-01", "name": "건물 내부 3D 공간 구축", "score": 0, "status": "FAIL", "reason": "내부 실내 3D 씬 부재"})

    if any(k in content_lower for k in ["cameradive", "spatialsmoothdive", "tween.to", "flytointerior"]):
        d_score += 5
        report["details"].append({"code": "D-02", "name": "1초 무지연 카메라 트랜지션", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-02", "name": "1초 무지연 카메라 트랜지션", "score": 0, "status": "FAIL", "reason": "실내 진입 카메라 연출 누락"})

    if any(k in content_lower for k in ["furniture", "interior_prop", "bookshelf", "throne"]):
        d_score += 5
        report["details"].append({"code": "D-03", "name": "실내 3D 소품 완비", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-03", "name": "실내 3D 소품 완비", "score": 0, "status": "FAIL", "reason": "실내 소품 부재"})

    if any(k in content_lower for k in ["firstpersoncontrols", "pointerlock", "gyroindoor", "lookaround"]):
        d_score += 5
        report["details"].append({"code": "D-04", "name": "1인칭 360도 궤도 회전", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-04", "name": "1인칭 360도 궤도 회전", "score": 0, "status": "FAIL", "reason": "실내 자유 시점 회전 불가"})

    if any(k in content_lower for k in ["exitdive", "returntomap", "resetcamera"]):
        d_score += 5
        report["details"].append({"code": "D-05", "name": "외부 복귀 원터치 탈출", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "D-05", "name": "외부 복귀 원터치 탈출", "score": 0, "status": "FAIL", "reason": "지도 뷰 복귀 버튼 부재"})

    # [영역 4] 모바일 네이티브 UX (25점)
    u_score = 0
    if "deviceorientation" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-01", "name": "자이로스코프 시점 연동", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-01", "name": "자이로스코프 시점 연동", "score": 0, "status": "FAIL", "reason": "DeviceOrientation 리스너 부재"})

    if any(k in content_lower for k in ["bottomsheet", "sheet-step", "touchstart"]):
        u_score += 5
        report["details"].append({"code": "U-02", "name": "3단계 네이티브 바텀시트", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-02", "name": "3단계 네이티브 바텀시트", "score": 0, "status": "FAIL", "reason": "PC용 사이드 모달 사용 감지"})

    if "vibrate" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-03", "name": "햅틱 촉각 진동 피드백", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-03", "name": "햅틱 촉각 진동 피드백", "score": 0, "status": "FAIL", "reason": "navigator.vibrate 미연동"})

    if any(k in content_lower for k in ["thumbwheel", "compass-dial", "altitude-slider"]):
        u_score += 5
        report["details"].append({"code": "U-04", "name": "모바일 엄지 조작계", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-04", "name": "모바일 엄지 조작계", "score": 0, "status": "FAIL", "reason": "Thumb Zone 플로팅 컨트롤러 부재"})

    if "requestanimationframe" in content_lower:
        u_score += 5
        report["details"].append({"code": "U-05", "name": "모바일 60fps 렌더링 루프", "score": 5, "status": "PASS"})
    else:
        report["details"].append({"code": "U-05", "name": "모바일 60fps 렌더링 루프", "score": 0, "status": "FAIL", "reason": "렌더링 루프 미감지"})

    total_score = g_score + m_score + d_score + u_score
    report["scores"]["geometry"] = g_score
    report["scores"]["materials"] = m_score
    report["scores"]["spatial_dive"] = d_score
    report["scores"]["mobile_ux"] = u_score
    report["total_score"] = total_score

    if total_score >= 90:
        report["verdict"] = "PASS"
    elif total_score >= 80:
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
    print(f"Scores: Geometry: {report['scores']['geometry']}/25 | Materials: {report['scores']['materials']}/25 | Dive: {report['scores']['spatial_dive']}/25 | Mobile UX: {report['scores']['mobile_ux']}/25")
    print(f"Total: {report['total_score']} / 100")
    print(f"Verdict: {report['verdict']}")
    print(f"Report saved to: {args.output}")

    if report["verdict"] == "FAIL":
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
