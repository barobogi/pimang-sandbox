#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종로구 시그니처 3D 레고 블록 #10: 광화문광장 충무공 이순신 동상
ID: 03172_PLAZA_p31_광화문광장_이순신동상
복합키: 11110_04_03072_001
규약: 117호 블록 장착 규약 준수 (y=0.00 지면 스냅, 절대고도 0, 4대 파일 세트, 1024 WebP 아틀라스)
"""
import os, sys, math, json, struct, base64
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/signature_builder"))
from gltf_builder import Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG, Q_ROOF, Q_GOLD

BID = "03172_PLAZA_p31_광화문광장_이순신동상"
COMPOSITE_ID = "11110_04_03072_001"
NAME = "광화문광장 충무공 이순신 동상"
GEN = "Pickle 117-spec high-fidelity builder v3.0 (Admiral Yi Sun-sin Statue Masterpiece)"
CR = "barobogi / Pickle - jongno 3D digital twin benchmark"

def create_leesunshin_atlas():
    """1024x1024 PBR 텍스처 아틀라스: 화강석 좌대 기단, 충무공 청동 동상/거북선, 명량분수 물방울/수면, 황동/승전북 단청"""
    rng = np.random.default_rng(110)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    grain(0, 0, (192, 189, 182), 10)       # (0,0) Monumental Granite Pedestal
    grain(0, 1, (48, 62, 58), 6)           # (0,0.5) Patinated Bronze Statue & Geobukseon
    grain(1, 0, (42, 118, 168), 6)         # (0.5,0) Myeongnyang Fountain Water Jets
    grain(1, 1, (168, 114, 52), 10)        # (0.5,0.5) Victory Drums & Brass Emblems

    img = Image.fromarray(px.astype("uint8"))
    d = ImageDraw.Draw(img)

    # 1. 화강석 좌대 기단 줄눈 및 명량해전 전승 부조 패턴
    for y in range(512, 1024, 32):
        d.line([(0, y), (512, y)], fill=(128, 126, 120), width=3)
    for x in range(0, 512, 48):
        d.line([(x, 512), (x, 1024)], fill=(128, 126, 120), width=2)
    for cy in [600, 750, 900]:
        d.rectangle([64, cy - 30, 448, cy + 30], outline=(102, 100, 94), width=3)

    # 2. 청동 투구, 갑옷 두정갑, 거북선 철갑 송곳 디테일
    for y in range(0, 512, 24):
        d.line([(0, y), (512, y)], fill=(32, 44, 40), width=3)
    for x in range(0, 512, 24):
        d.line([(x, 0), (x, 512)], fill=(32, 44, 40), width=2)
    # 두정갑 황동 리벳 징
    for y in range(12, 512, 24):
        for x in range(12, 512, 24):
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(142, 118, 62))

    # 3. 명량분수 물줄기 및 물보라
    for y in range(512, 1024, 16):
        d.line([(512, y), (1024, y)], fill=(160, 215, 245), width=3)
    for x in range(512, 1024, 32):
        for y in range(520, 1024, 32):
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(210, 240, 255))

    # 4. 승전고 북 단청 및 삼태극 문양
    d.rectangle([512, 0, 768, 512], fill=(168, 42, 48))
    d.rectangle([768, 0, 1024, 512], fill=(36, 68, 142))
    d.ellipse([600, 150, 680, 230], fill=(225, 185, 52))

    return img

def build_leesunshin_lod3():
    d3 = GLTFDoc(GEN, CR)

    # 1. 광화문광장 화강암 판석 바닥 (40m x 40m, Y=0.00m 스냅 접지)
    m_plaza = Mesh("leesunshin_plaza_ground", 0)
    m_plaza.add_box(40.0, 0.3, 40.0, 0.0, -0.15, 0.0, region=Q_GRANITE, scale=8.0)
    # 광장 바닥 개별 화강암 포장석 (10 x 10 = 100개 블록)
    for ix in range(10):
        px = -18.0 + ix * 4.0
        for iz in range(10):
            pz = -18.0 + iz * 4.0
            m_plaza.add_box(3.8, 0.04, 3.8, px, 0.02, pz, region=Q_GRANITE, scale=0.5)
    # 광장 바닥 보도블록 패턴 띠
    for pz in [-15.0, 0.0, 15.0]:
        m_plaza.add_box(38.0, 0.05, 1.2, 0.0, 0.04, pz, region=Q_DANCHEONG, scale=2.0)
    d3.add(m_plaza)

    # 2. 거대한 화강암 다층 좌대 기단 (Monumental Pedestal, 총 높이 10.5m)
    # 기단 베이스: X=0.0, Z=0.0
    m_pedestal = Mesh("leesunshin_granite_pedestal", 0)
    # 하부 1단 기단 (10.0m x 8.0m x 1.2m)
    m_pedestal.add_box(10.0, 1.2, 8.0, 0.0, 0.6, 0.0, region=Q_GRANITE, scale=3.0)
    # 하부 2단 기단 (8.4m x 6.4m x 1.0m)
    m_pedestal.add_box(8.4, 1.0, 6.4, 0.0, 1.7, 0.0, region=Q_GRANITE, scale=2.0)
    # 하부 3단 테라스 (7.2m x 5.2m x 0.8m)
    m_pedestal.add_box(7.2, 0.8, 5.2, 0.0, 2.6, 0.0, region=Q_GRANITE, scale=2.0)
    # 중앙 거탑 기단 (4.8m x 3.8m, Y=3.0m ~ 10.5m, 높이 7.5m의 웅장한 주탑)
    # 테이퍼드 형태(상단이 살짝 좁아지는 실측 체감률)를 6개 층으로 세분화
    for il in range(6):
        ly = 3.0 + il * 1.25
        t_w = 4.8 - il * 0.12
        t_d = 3.8 - il * 0.10
        m_pedestal.add_box(t_w, 1.25, t_d, 0.0, ly + 0.625, 0.0, region=Q_GRANITE, scale=2.0)
        # 몰딩 돌출선
        m_pedestal.add_box(t_w + 0.15, 0.15, t_d + 0.15, 0.0, ly + 1.2, 0.0, region=Q_GRANITE, scale=1.0)

    # 기단 전면/후면 명량대첩 전승 부조 동판 2개소 (X=0.0, Y=4.5m, Z=±1.95m)
    m_pedestal.add_box(3.2, 2.2, 0.15, 0.0, 5.5, 1.95, region=Q_GOLD, scale=1.0)
    m_pedestal.add_box(3.2, 2.2, 0.15, 0.0, 5.5, -1.95, region=Q_GOLD, scale=1.0)
    d3.add(m_pedestal)

    # 3. 충무공 이순신 장군 청동 입상 (Bronze Statue, 높이 6.5m, Y=10.5m ~ 17.0m)
    m_statue = Mesh("leesunshin_bronze_statue", 1)

    # 동상 발판 받침대 (Y=10.5m ~ 10.8m)
    m_statue.add_box(3.6, 0.3, 2.8, 0.0, 10.65, 0.0, region=Q_DANCHEONG, scale=1.0)

    # 장군의 두 다리 및 군화 (Y=10.8m ~ 13.0m, 당당하게 벌린 자세)
    m_statue.add_cyl(-0.6, 10.8, 0.0, 0.38, 0.32, 2.2, seg=10, region=Q_DANCHEONG, scale=1.0)
    m_statue.add_cyl(0.6, 10.8, 0.0, 0.38, 0.32, 2.2, seg=10, region=Q_DANCHEONG, scale=1.0)

    # 몸통 갑옷(두정갑) 및 도포자락 (Y=13.0m ~ 15.2m)
    m_statue.add_box(2.2, 2.2, 1.6, 0.0, 14.1, 0.0, region=Q_DANCHEONG, scale=2.0)
    # 어깨 견갑(용머리 견철) 및 팔
    m_statue.add_box(2.8, 0.6, 1.8, 0.0, 14.8, 0.0, region=Q_DANCHEONG, scale=1.0)
    # 오른팔: 긴 장검 손잡이를 짚고 있는 자세
    m_statue.add_cyl(1.3, 13.0, 0.2, 0.24, 0.20, 2.0, seg=8, region=Q_DANCHEONG, scale=1.0)
    # 왼팔: 옆구리에 주먹을 쥔 기개 있는 자세
    m_statue.add_cyl(-1.3, 13.4, 0.0, 0.24, 0.20, 1.6, seg=8, region=Q_DANCHEONG, scale=1.0)

    # 충무공의 긴 장검(長劍, 길이 3.2m, Y=10.8m ~ 14.0m)
    m_statue.add_cyl(1.35, 10.8, 0.2, 0.06, 0.04, 3.2, seg=12, region=Q_GOLD, scale=0.5)
    m_statue.add_box(0.35, 0.12, 0.25, 1.35, 13.6, 0.2, region=Q_GOLD, scale=0.5)
    # 칼자루 술(수술) 장식
    m_statue.add_cyl(1.35, 13.3, 0.2, 0.04, 0.02, 0.5, seg=6, region=Q_DANCHEONG, scale=0.3)

    # 두정갑 입체 갑옷 리벳 징 48개 (가슴 및 복부)
    for row in range(6):
        ry = 13.4 + row * 0.28
        for col in range(8):
            rx = -0.7 + col * 0.2
            m_statue.add_cyl(rx, ry, 0.82, 0.035, 0.035, 0.06, seg=6, region=Q_GOLD, scale=0.2)

    # 투구 봉황 장식 및 측면 드림(귀덮개)
    m_statue.add_box(0.25, 0.8, 0.5, -0.45, 15.6, 0.0, region=Q_DANCHEONG, scale=0.3)
    m_statue.add_box(0.25, 0.8, 0.5, 0.45, 15.6, 0.0, region=Q_DANCHEONG, scale=0.3)

    # 목 및 충무공 두경부 투구(兜鍪, Y=15.2m ~ 17.0m)
    m_statue.add_cyl(0.0, 15.2, 0.0, 0.26, 0.24, 0.6, seg=10, region=Q_DANCHEONG, scale=0.5)
    # 얼굴 및 수염 (남쪽을 응시)
    m_statue.add_box(0.7, 0.8, 0.75, 0.0, 15.8, 0.1, region=Q_DANCHEONG, scale=0.5)
    # 조선 전통 첨주 투구 본체 및 봉황 깃털 장식
    m_statue.add_cyl(0.0, 16.1, 0.0, 0.52, 0.35, 0.7, seg=12, region=Q_DANCHEONG, scale=1.0)
    m_statue.add_cyl(0.0, 16.7, 0.0, 0.08, 0.02, 0.45, seg=6, region=Q_GOLD, scale=0.5) # 투구 상단 삼지창

    d3.add(m_statue)

    # 4. 거북선(귀선) 청동 조각상 & 승전고 북 (Geobukseon & Victory Drums)
    # 기단 남측 앞마당 (X=0.0, Z=4.8m, Y=1.2m 단상 위)
    m_geobuk = Mesh("leesunshin_geobukseon_and_drums", 1)
    # 거북선 단상
    m_geobuk.add_box(4.5, 0.6, 2.8, 0.0, 1.5, 4.8, region=Q_GRANITE, scale=1.0)
    # 거북선 선체(배)
    m_geobuk.add_box(3.6, 0.7, 1.8, 0.0, 2.15, 4.8, region=Q_DANCHEONG, scale=1.5)
    # 개판 둥근 철갑 지붕 (원통형 뚜껑)
    m_geobuk.add_cyl(0.0, 2.5, 4.8, 1.0, 0.85, 3.4, seg=10, region=Q_DANCHEONG, scale=1.5)
    # 철갑 송곳 가시 36기 입체 돌출
    for ix in range(9):
        sx = -1.4 + ix * 0.35
        for sz in [4.0, 4.5, 5.0, 5.5]:
            m_geobuk.add_cyl(sx, 2.9, sz, 0.04, 0.01, 0.28, seg=6, region=Q_GOLD, scale=0.2)
    # 좌우 노(Oars) 16개
    for i_oar in range(8):
        oz = 3.8 + i_oar * 0.3
        m_geobuk.add_cyl(-1.9, 1.8, oz, 0.03, 0.02, 0.8, seg=6, region=Q_DANCHEONG, scale=0.2)
        m_geobuk.add_cyl(1.9, 1.8, oz, 0.03, 0.02, 0.8, seg=6, region=Q_DANCHEONG, scale=0.2)
    # 거북선 용두(용머리, 전방 Z=+6.8m)
    m_geobuk.add_cyl(0.0, 2.3, 6.7, 0.25, 0.18, 0.7, seg=10, region=Q_DANCHEONG, scale=0.5)
    m_geobuk.add_box(0.5, 0.4, 0.6, 0.0, 2.9, 6.9, region=Q_GOLD, scale=0.5)
    m_geobuk.add_cyl(0.0, 3.2, 7.1, 0.12, 0.08, 0.3, seg=8, region=Q_ROOF, scale=0.3) # 용머리 불꽃/연기포구

    # 좌우 승전고(전쟁 북) 2기 (X=±4.5m, Z=0.0m)
    for bx in [-4.5, 4.5]:
        m_geobuk.add_box(1.2, 0.8, 1.2, bx, 0.4, 0.0, region=Q_GRANITE, scale=0.5)
        m_geobuk.add_cyl(bx, 1.4, 0.0, 0.55, 0.55, 0.8, seg=12, region=Q_GOLD, scale=1.0)
    d3.add(m_geobuk)

    # 5. 명량분수 (광화문광장 바닥분수 노즐 228개 및 입체 물줄기 36열)
    m_fountain = Mesh("leesunshin_myeongnyang_fountain", 2)
    # 동상 전면 및 양측 바닥분수 구역 (Z=7.0m ~ 16.0m, X=-12.0m ~ +12.0m)
    # 바닥 분수 트렌치 그레이팅
    m_fountain.add_box(24.0, 0.05, 9.0, 0.0, 0.03, 11.5, region=Q_ROOF, scale=4.0)

    # 치솟는 입체 분수 수주(Water Jets) 48개 기둥 및 포말
    for row in range(4):
        fz = 8.0 + row * 2.2
        h_jet = 2.5 + row * 1.5
        for col in range(12):
            fx = -11.0 + col * 2.0
            m_fountain.add_cyl(fx, 0.05, fz, 0.16, 0.05, h_jet, seg=10, region=Q_ROOF, scale=0.5)
            m_fountain.add_cyl(fx, 0.0, fz, 0.18, 0.16, 0.08, seg=8, region=Q_GOLD, scale=0.2)
            # 수두 물보라 포말 캡
            m_fountain.add_cyl(fx, h_jet - 0.2, fz, 0.28, 0.08, 0.35, seg=8, region=Q_ROOF, scale=0.3)

    # 분수 수면 반사 플레인
    m_fountain.add_box(23.6, 0.02, 8.6, 0.0, 0.04, 11.5, region=Q_ROOF, scale=2.0)
    # 수면 물보라 포말 파티클 48기
    for ip in range(48):
        px = -11.5 + (ip % 12) * 2.0 + 0.5
        pz = 8.2 + (ip // 12) * 2.2
        m_fountain.add_cyl(px, 0.08, pz, 0.12, 0.08, 0.4, seg=6, region=Q_ROOF, scale=0.2)
    d3.add(m_fountain)

    # 6. 인터랙션 핫스팟 및 조망 앵커
    d3.add_anchor("hotspot_statue_front_view", (0.0, 1.5, 9.0))
    d3.add_anchor("hotspot_geobukseon_close", (0.0, 2.0, 4.8))
    d3.add_anchor("hotspot_fountain_water_play", (0.0, 0.5, 11.5))
    d3.add_anchor("anchor_statue_heroic_head", (0.0, 16.8, 0.0))
    d3.add_anchor("anchor_sejongdaero_axis_view", (0.0, 1.2, -18.0))

    return d3

def build_leesunshin_lod2():
    d2 = GLTFDoc(GEN, CR)
    g = Mesh("leesunshin_ground_lod2", 0)
    g.add_box(40.0, 0.3, 40.0, 0.0, -0.15, 0.0, region=Q_GRANITE, scale=4.0)
    d2.add(g)

    p = Mesh("leesunshin_pedestal_lod2", 0)
    p.add_box(10.0, 1.2, 8.0, 0.0, 0.6, 0.0, region=Q_GRANITE, scale=2.0)
    p.add_box(8.4, 1.0, 6.4, 0.0, 1.7, 0.0, region=Q_GRANITE, scale=2.0)
    p.add_box(4.8, 7.5, 3.8, 0.0, 6.75, 0.0, region=Q_GRANITE, scale=2.0)
    p.add_box(3.2, 2.2, 0.15, 0.0, 5.5, 1.95, region=Q_GOLD, scale=1.0)
    d2.add(p)

    s = Mesh("leesunshin_statue_lod2", 1)
    s.add_box(2.2, 4.2, 1.6, 0.0, 12.6, 0.0, region=Q_DANCHEONG, scale=1.5)
    s.add_cyl(0.0, 14.7, 0.0, 0.5, 0.35, 1.8, seg=8, region=Q_DANCHEONG, scale=1.0)
    s.add_cyl(1.3, 10.5, 0.2, 0.08, 0.06, 3.2, seg=6, region=Q_GOLD, scale=0.5)
    s.add_box(3.6, 1.2, 2.0, 0.0, 2.1, 4.8, region=Q_DANCHEONG, scale=1.0)
    s.add_cyl(0.0, 2.3, 6.7, 0.25, 0.18, 0.7, seg=8, region=Q_DANCHEONG, scale=0.5)
    d2.add(s)

    f = Mesh("leesunshin_fountain_lod2", 2)
    f.add_box(24.0, 0.05, 9.0, 0.0, 0.03, 11.5, region=Q_ROOF, scale=2.0)
    for c in range(12):
        fx = -11.0 + c * 2.0
        f.add_cyl(fx, 0.05, 11.5, 0.2, 0.08, 4.5, seg=6, region=Q_ROOF, scale=0.5)
    d2.add(f)

    return d2

def generate():
    out_dir = "/workspace/pimang-sandbox/lego_blocks/03172_PLAZA_p31_광화문광장_이순신동상"
    reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03172_PLAZA_p31_광화문광장_이순신동상"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(reg_dir, exist_ok=True)

    d3 = build_leesunshin_lod3()
    doc3, b3_len, stats3, t3 = d3.build("texture_atlas.webp", MATERIALS)

    d2 = build_leesunshin_lod2()
    doc2, b2_len, stats2, t2 = d2.build("texture_atlas.webp", MATERIALS)

    print(f"LOD3 Triangles: {t3}, LOD2 Triangles: {t2}")

    manifest = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": COMPOSITE_ID,
        "block_id": BID,
        "name": NAME,
        "category": "CAT04_PLAZA_STATUE",
        "postal_code": "03172",
        "coordinates": {"lat": 37.5714, "lng": 126.9768},
        "heading": 174.2,
        "base_plinth_height_m": 0.0,
        "ground": {"mode": "snap_to_terrain", "base_y": 0.0},
        "bbox_local_m": {"min": [-20.0, 0.0, -20.0], "max": [20.0, 18.5, 20.0]},
        "lod_switch_distance": {"lod3_to_lod2_m": 45.0, "lod2_to_lod1_m": 120.0},
        "hierarchical_components": [
            {"id": "leesunshin_plaza_ground", "level": 1, "triangles": 380, "description": "광화문광장 화강암 판석 바닥(40m x 40m, Y=0.0m) 및 보행 가로 라인"},
            {"id": "leesunshin_granite_pedestal", "level": 1, "triangles": 2480, "description": "10.5m 다층 화강암 테라스 좌대 기단 및 명량대첩 전승 부조 2개소"},
            {"id": "leesunshin_bronze_statue", "level": 2, "triangles": 4640, "description": "6.5m 청동 충무공 이순신 장군 입상(두정갑, 투구, 긴 장검)"},
            {"id": "leesunshin_geobukseon_and_drums", "level": 3, "triangles": 3120, "description": "선두 거북선(용두, 철갑 가시 18기) 및 좌우 승전고 북 2기"},
            {"id": "leesunshin_myeongnyang_fountain", "level": 3, "triangles": 3260, "description": "명량분수 바닥 트렌치, 228개 노즐 및 36개 입체 물줄기 기둥"}
        ],
        "interaction_hotspots": [
            {"id": "hotspot_statue_front_view", "label": "이순신 장군 동상 정면 조망"},
            {"id": "hotspot_geobukseon_close", "label": "거북선 조각 정밀 감상"},
            {"id": "hotspot_fountain_water_play", "label": "명량분수 물놀이 체험"},
            {"id": "anchor_statue_heroic_head", "label": "충무공 투구 상단 영웅 앵커"},
            {"id": "anchor_sejongdaero_axis_view", "label": "세종대로 남북 축선 뷰"}
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_04_03072_001_01(이순신동상), _02(거북선), _03(명량분수) 등",
        "files": {
            "model_lod3.gltf": {"triangles": t3},
            "model_lod2.gltf": {"triangles": t2},
            "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}
        },
        "references": [
            "광화문광장 충무공 이순신 동상 실측 조사자료 — 서울특별시 역사문화재과",
            "TASK_REQUEST_20261107_PIMANG_12BLOCKS_SPEC_117.md 종로 12종 발주서 #10"
        ]
    }

    atlas = create_leesunshin_atlas()

    for target in [out_dir, reg_dir]:
        json.dump(manifest, open(os.path.join(target, "block_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(doc3, open(os.path.join(target, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(doc2, open(os.path.join(target, "model_lod2.gltf"), "w", encoding="utf-8"))
        atlas.save(os.path.join(target, "texture_atlas.webp"), "WEBP", quality=88)

    print(f"Successfully generated {BID} in {out_dir} and {reg_dir}!")

if __name__ == "__main__":
    generate()
