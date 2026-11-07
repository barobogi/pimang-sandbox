#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종로구 시그니처 3D 레고 블록 #6: 북촌 가회동 31번지 조망 뷰
ID: 03053_TRAD_p12_북촌_가회동31번지
복합키: 11110_02_03053_002
규약: 117호 블록 장착 규약 준수 (y=0.00 지면 스냅, 절대고도 0, 4대 파일 세트, 1024 WebP 아틀라스)
"""
import os, sys, math, json, struct, base64
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/signature_builder"))
from gltf_builder import Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG, Q_ROOF, Q_GOLD, paljak_roof

BID = "03053_TRAD_p12_북촌_가회동31번지"
COMPOSITE_ID = "11110_02_03053_002"
NAME = "북촌 가회동 31번지 조망 뷰"
GEN = "Pickle 117-spec high-fidelity builder v3.0 (Gahoe-dong 31 Masterpiece)"
CR = "barobogi / Pickle - jongno 3D digital twin benchmark"

def create_gahoe31_atlas():
    """1024x1024 PBR 텍스처 아틀라스: 화강암/사고석, 전통 고재/창호, 흑회색 기와골, 청사초롱/황동"""
    rng = np.random.default_rng(106)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    grain(0, 0, (188, 185, 178), 10)       # (0,0) Granite & Sagoseok
    grain(0, 1, (138, 85, 54), 8)          # (0,0.5) Traditional Pine Wood & Lattice
    grain(1, 0, (46, 48, 54), 6)           # (0.5,0) Dark Charcoal Korean Roof Tile
    grain(1, 1, (192, 142, 62), 10)        # (0.5,0.5) Silk Lantern & Brass

    img = Image.fromarray(px.astype("uint8"))
    d = ImageDraw.Draw(img)

    # 1. 사고석 돌담 및 박석 줄눈 패턴
    for y in range(512, 1024, 32):
        d.line([(0, y), (512, y)], fill=(122, 120, 114), width=3)
    for row, y in enumerate(range(512, 1024, 32)):
        shift = 24 if row % 2 else 0
        for x in range(shift, 512, 48):
            d.line([(x, y), (x, y + 32)], fill=(122, 120, 114), width=2)

    # 2. 전통 목조 기둥 및 세살창 격자
    for y in range(0, 512, 40):
        d.line([(0, y), (512, y)], fill=(92, 52, 32), width=4)
    for x in range(0, 256, 16):
        d.line([(x, 0), (x, 256)], fill=(76, 44, 25), width=2)
    for y in range(0, 256, 16):
        d.line([(0, y), (256, y)], fill=(76, 44, 25), width=2)
    for y in range(8, 256, 16):
        for x in range(8, 256, 16):
            d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(236, 232, 218))

    # 3. 한와 기와골 패턴
    for y in range(512, 1024, 24):
        d.line([(512, y), (1024, y)], fill=(26, 26, 30), width=5)
    for x in range(512, 1024, 20):
        d.line([(x, 512), (x, 1024)], fill=(36, 38, 44), width=3)
        for y in range(524, 1024, 48):
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(18, 18, 22))

    # 4. 청사초롱 홍청 비단 & 황동 장식
    d.rectangle([512, 0, 768, 256], fill=(188, 38, 48))
    for y in range(0, 256, 8):
        d.line([(512, y), (768, y)], fill=(212, 52, 62), width=2)
    d.rectangle([512, 256, 768, 512], fill=(28, 64, 148))
    for y in range(256, 512, 8):
        d.line([(512, y), (768, y)], fill=(42, 82, 178), width=2)
    for y in range(0, 512, 6):
        c = 202 + (y * 5) % 35
        d.line([(768, y), (1024, y)], fill=(c, int(c * 0.8), int(c * 0.35)), width=3)

    return img

def add_quad(mesh, p0, p1, p2, p3, region, scale=1.0):
    verts = [p0, p1, p2, p3]
    uvs = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    tris = [0, 1, 2, 0, 2, 3]
    mesh.add(verts, uvs, tris, region=region, scale=scale)

def add_gable_roof(mesh, hw_e, hd_e, height, y_base, cx, cz, ry=0.0, nt=8, nper=32):
    for side in (-1, 1):
        for it in range(nt):
            t0 = it / nt
            t1 = (it + 1) / nt
            y0 = y_base + height * (0.30 * t0 + 0.70 * (t0 ** 2.7))
            y1 = y_base + height * (0.30 * t1 + 0.70 * (t1 ** 2.7))
            z0 = side * hd_e * (1.0 - t0)
            z1 = side * hd_e * (1.0 - t1)
            for ix in range(nper):
                s0 = ix / nper
                s1 = (ix + 1) / nper
                x0 = -hw_e + 2 * hw_e * s0
                x1 = -hw_e + 2 * hw_e * s1
                lift0 = 0.35 * (1.0 - t0) * ((abs(s0 - 0.5) * 2) ** 2)
                lift1 = 0.35 * (1.0 - t1) * ((abs(s1 - 0.5) * 2) ** 2)

                pts = [
                    (x0, y0 + lift0, z0),
                    (x1, y1 + lift1, z0),
                    (x1, y1 + lift1, z1),
                    (x0, y1 + lift0, z1),
                ]
                rot_pts = []
                c, s = math.cos(ry), math.sin(ry)
                for px, py, pz in pts:
                    rx = px * c + pz * s + cx
                    rz = -px * s + pz * c + cz
                    rot_pts.append((rx, py, rz))

                v = [rot_pts[0], rot_pts[1], rot_pts[2], rot_pts[3]]
                u = [(s0 * 4.0, t0 * 2.0), (s1 * 4.0, t0 * 2.0), (s1 * 4.0, t1 * 2.0), (s0 * 4.0, t1 * 2.0)]
                t = [0, 1, 2, 0, 2, 3] if side == -1 else [0, 2, 1, 0, 3, 2]
                mesh.add(v, u, t, region=Q_ROOF, scale=2.0)
    mesh.add_box(hw_e * 2.1, 0.45, 0.65, cx, y_base + height + 0.22, cz, ry=ry, region=Q_ROOF, scale=4.0)

def build_gahoe31_lod3():
    d3 = GLTFDoc(GEN, CR)

    # 1. 가회동 31번지 경사지 골목길 & 조망 테라스 (Alley & Viewpoint Terrace)
    # Z축: -20m(언덕 정상 조망점, Y=3.2m) -> +20m(언덕 하단 진입로, Y=0.0m)
    m_ground = Mesh("gahoe31_sloped_alley_pavement", 0)
    for iz in range(20):
        z0 = -20.0 + iz * 2.0
        z1 = z0 + 2.0
        # 내리막 경사
        y0 = 3.2 * (1.0 - iz / 20.0)
        y1 = 3.2 * (1.0 - (iz + 1) / 20.0)
        add_quad(
            m_ground,
            (-2.2, y0, z0), (2.2, y0, z0),
            (2.2, y1, z1), (-2.2, y1, z1),
            region=Q_GRANITE, scale=3.0
        )
    # 지반 하부 기단 블록 (y=0.0 접지 보장)
    m_ground.add_box(38.0, 0.2, 42.0, 0.0, -0.1, 0.0, region=Q_GRANITE, scale=8.0)

    # 가회동 31번지 조망 뷰 테라스 데크 (Z=-20m ~ -17m)
    m_ground.add_box(4.6, 0.35, 3.2, 0.0, 3.2, -18.5, region=Q_GRANITE, scale=2.0)
    # 화강암 돌계단 2개 구간 (Z=-10m 부근 8단 계단, Z=+6m 부근 6단 계단)
    for z_st, y_st, n_step in [(-10.0, 2.2, 8), (6.0, 0.9, 6)]:
        for step in range(n_step):
            sy = y_st - step * 0.14
            sz = z_st + step * 0.35
            m_ground.add_box(3.8, 0.16, 0.40, 0.0, sy, sz, region=Q_GRANITE, scale=2.0)
            m_ground.add_box(0.25, 0.30, 0.45, -2.0, sy + 0.1, sz, region=Q_GRANITE, scale=1.0)
            m_ground.add_box(0.25, 0.30, 0.45, 2.0, sy + 0.1, sz, region=Q_GRANITE, scale=1.0)
    # 자연석 배수로 구거 (양측 X=±2.3m)
    m_ground.add_box(0.4, 0.25, 40.0, -2.4, 1.55, 0.0, region=Q_GRANITE, scale=4.0)
    m_ground.add_box(0.4, 0.25, 40.0, 2.4, 1.55, 0.0, region=Q_GRANITE, scale=4.0)
    d3.add(m_ground)

    # 2. 사고석 돌담 및 솟을대문 (Sagoseok Masonry Walls & Gates)
    m_walls = Mesh("gahoe31_sagoseok_walls", 0)
    m_wall_roofs = Mesh("gahoe31_wall_tile_caps", 2)
    # 8개 섹션 단차 돌담
    for iz in range(8):
        z_c = -17.0 + iz * 4.8
        y_b = 3.2 * (1.0 - (z_c + 20.0) / 40.0)
        # 동측 담장
        m_walls.add_box(0.45, 1.7, 4.6, 2.65, y_b + 0.85, z_c, region=Q_GRANITE, scale=3.0)
        m_wall_roofs.add_box(0.65, 0.22, 4.7, 2.65, y_b + 1.75, z_c, region=Q_ROOF, scale=2.0)
        # 서측 담장
        m_walls.add_box(0.45, 1.7, 4.6, -2.65, y_b + 0.85, z_c, region=Q_GRANITE, scale=3.0)
        m_wall_roofs.add_box(0.65, 0.22, 4.7, -2.65, y_b + 1.75, z_c, region=Q_ROOF, scale=2.0)
    d3.add(m_walls)
    d3.add(m_wall_roofs)

    # 3. 가회동 31번지 밀집 한옥 8채 루프탑 파노라마 (4 East, 4 West)
    m_plinths = Mesh("gahoe31_hanok_plinths", 0)
    m_timbers = Mesh("gahoe31_wood_columns_and_windows", 1)
    m_rafters = Mesh("gahoe31_eave_rafters_3d", 1)         # 입체 서까래 160기
    m_roofs = Mesh("gahoe31_rooftop_panorama_roofs", 2)    # 8채 한와 루프탑
    m_ornaments = Mesh("gahoe31_lanterns_and_gates", 3)

    hanok_specs = [
        # East row: 가회동 31번지 동측 4채 (경사지 계단식)
        {"id": "E1", "type": "paljak", "cx": 8.5,  "cz": -15.0, "yb": 2.6, "w": 9.5, "d": 7.5, "h": 4.8, "ridge": 5.5, "soseul": True},
        {"id": "E2", "type": "gable",  "cx": 8.0,  "cz": -5.0,  "yb": 1.8, "w": 8.5, "d": 7.0, "h": 4.5, "ridge": 6.5, "soseul": False},
        {"id": "E3", "type": "paljak", "cx": 8.8,  "cz": 5.0,   "yb": 1.0, "w": 9.0, "d": 8.0, "h": 4.9, "ridge": 5.0, "soseul": False},
        {"id": "E4", "type": "gable",  "cx": 8.2,  "cz": 15.0,  "yb": 0.2, "w": 8.6, "d": 7.2, "h": 4.4, "ridge": 6.2, "soseul": False},
        # West row: 가회동 31번지 서측 4채
        {"id": "W1", "type": "gable",  "cx": -8.0, "cz": -15.0, "yb": 2.6, "w": 8.5, "d": 7.0, "h": 4.5, "ridge": 6.5, "soseul": False},
        {"id": "W2", "type": "paljak", "cx": -9.0, "cz": -5.0,  "yb": 1.8, "w": 10.5, "d": 8.0, "h": 5.1, "ridge": 6.0, "soseul": True},
        {"id": "W3", "type": "gable",  "cx": -8.2, "cz": 5.0,   "yb": 1.0, "w": 8.8, "d": 7.5, "h": 4.6, "ridge": 6.8, "soseul": False},
        {"id": "W4", "type": "paljak", "cx": -8.8, "cz": 15.0,  "yb": 0.2, "w": 9.2, "d": 7.8, "h": 4.7, "ridge": 5.4, "soseul": False},
    ]

    for h in hanok_specs:
        cx, cz, yb = h["cx"], h["cz"], h["yb"]
        w, d, ht = h["w"], h["d"], h["h"]
        # 기단
        m_plinths.add_box(w + 1.2, 0.7, d + 1.2, cx, yb + 0.35, cz, region=Q_GRANITE, scale=4.0)

        # 목조 벽체 및 기둥 & 창호
        m_timbers.add_box(w, ht * 0.55, d, cx, yb + 0.7 + ht * 0.275, cz, region=Q_DANCHEONG, scale=2.0)
        for px in [-w/2 + 0.2, -w/6, w/6, w/2 - 0.2]:
            for pz in [-d/2 + 0.2, d/2 - 0.2]:
                m_timbers.add_cyl(cx + px, yb + 0.7, cz + pz, 0.16, 0.15, ht * 0.55, seg=8, region=Q_DANCHEONG, scale=2.0)

        # 처마 밑 3D 둥근 서까래 (각 채당 20기, 8채 총 160기!)
        n_raf_x = 8
        n_raf_z = 6
        raf_y = yb + 0.7 + ht * 0.55 - 0.15
        hw_e = w / 2.0 + 0.9
        hd_e = d / 2.0 + 0.9
        for ix in range(n_raf_x):
            rx = cx - hw_e + 0.3 + ix * ((hw_e * 2 - 0.6) / (n_raf_x - 1))
            m_rafters.add_cyl(rx, raf_y, cz - hd_e, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)
            m_rafters.add_cyl(rx, raf_y, cz + hd_e, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)
        for iz in range(n_raf_z):
            rz = cz - hd_e + 0.3 + iz * ((hd_e * 2 - 0.6) / (n_raf_z - 1))
            m_rafters.add_cyl(cx - hw_e, raf_y, rz, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)
            m_rafters.add_cyl(cx + hw_e, raf_y, rz, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)

        # 지붕 생성 (오공간 처마 곡률)
        rf_y = yb + 0.7 + ht * 0.55
        if h["type"] == "paljak":
            v_pal, u_pal, t_pal = paljak_roof(
                hw_e=hw_e, hd_e=hd_e, ridge_len=h["ridge"],
                height=ht * 0.48, y_base=rf_y, nt=10, nper=40,
                eave_lift=0.45
            )
            m_roofs.add(v_pal, u_pal, t_pal, offset=(cx, 0, cz), region=Q_ROOF, scale=4.0)
            m_roofs.add_box(h["ridge"] + 0.6, 0.45, 0.6, cx, rf_y + ht * 0.48 + 0.25, cz, region=Q_ROOF, scale=2.0)
        else:
            add_gable_roof(
                m_roofs, hw_e=hw_e, hd_e=hd_e, height=ht * 0.46, y_base=rf_y,
                cx=cx, cz=cz, nt=8, nper=32
            )

        # 솟을대문 및 청사초롱
        if h["soseul"]:
            gate_x = 2.8 if cx > 0 else -2.8
            gate_z = cz
            gate_y = yb + 0.2
            m_timbers.add_box(0.5, 3.2, 1.8, gate_x, gate_y + 1.6, gate_z, region=Q_DANCHEONG, scale=2.0)
            v_g, u_g, t_g = paljak_roof(
                hw_e=1.4, hd_e=1.6, ridge_len=1.2, height=1.1,
                y_base=gate_y + 3.1, nt=6, nper=24, eave_lift=0.3
            )
            m_roofs.add(v_g, u_g, t_g, offset=(gate_x, 0, gate_z), region=Q_ROOF, scale=2.0)
            for l_off in (-0.9, 0.9):
                lx = gate_x
                ly = gate_y + 2.5
                lz = gate_z + l_off
                m_ornaments.add_cyl(lx, ly, lz, 0.16, 0.14, 0.48, seg=8, region=Q_GOLD, scale=1.0)
                m_ornaments.add_cyl(lx, ly - 0.28, lz, 0.04, 0.01, 0.32, seg=6, region=Q_GOLD, scale=0.5)

    d3.add(m_plinths)
    d3.add(m_timbers)
    d3.add(m_rafters)
    d3.add(m_roofs)
    d3.add(m_ornaments)

    # 4. 전통 와편 굴뚝 4기
    m_cultural = Mesh("gahoe31_traditional_chimneys", 0)
    chimney_locs = [(13.5, 2.6, -17.0), (13.0, 0.2, 17.0), (-14.0, 2.6, -17.0), (-13.5, 0.2, 17.0)]
    for ch_x, ch_y, ch_z in chimney_locs:
        m_cultural.add_box(0.9, 2.2, 0.9, ch_x, ch_y + 1.1, ch_z, region=Q_GRANITE, scale=2.0)
        m_cultural.add_box(1.2, 0.3, 1.2, ch_x, ch_y + 2.3, ch_z, region=Q_ROOF, scale=1.0)
    d3.add(m_cultural)

    # 5. 앵커 및 핫스팟 노드 (Anchors & Hotspots)
    d3.add_anchor("hotspot_gahoe31_viewpoint", (0.0, 3.4, -18.5))
    d3.add_anchor("hotspot_rooftop_panorama", (0.0, 4.2, 0.0))
    d3.add_anchor("hotspot_sloped_stairs", (0.0, 1.6, -10.0))
    d3.add_anchor("anchor_n_seoul_tower_view", (0.0, 5.5, 24.0)) # 남쪽 원경 앵커
    d3.add_anchor("night_light_lantern_01", (2.8, 4.8, -15.9))
    d3.add_anchor("night_light_lantern_02", (2.8, 4.8, -14.1))
    d3.add_anchor("night_light_lantern_03", (-2.8, 3.8, -5.9))
    d3.add_anchor("night_light_lantern_04", (-2.8, 3.8, -4.1))

    return d3

def build_gahoe31_lod2():
    d2 = GLTFDoc(GEN, CR)
    g = Mesh("gahoe31_ground_lod2", 0)
    g.add_box(38.0, 0.4, 42.0, 0.0, -0.2, 0.0, region=Q_GRANITE, scale=4.0)
    for iz in range(10):
        z0 = -20.0 + iz * 4.0
        z1 = z0 + 4.0
        y0 = 3.2 * (1.0 - iz / 10.0)
        y1 = 3.2 * (1.0 - (iz + 1) / 10.0)
        add_quad(g, (-2.2, y0, z0), (2.2, y0, z0), (2.2, y1, z1), (-2.2, y1, z1), region=Q_GRANITE, scale=2.0)
    d2.add(g)

    w = Mesh("gahoe31_walls_lod2", 0)
    w.add_box(0.5, 2.0, 38.0, 2.65, 2.0, 0.0, region=Q_GRANITE, scale=4.0)
    w.add_box(0.5, 2.0, 38.0, -2.65, 2.0, 0.0, region=Q_GRANITE, scale=4.0)
    d2.add(w)

    h_mass = Mesh("gahoe31_buildings_lod2", 1)
    h_roof = Mesh("gahoe31_roofs_lod2", 2)
    hanok_specs = [
        {"cx": 8.5,  "cz": -15.0, "yb": 2.6, "w": 9.5, "d": 7.5, "h": 4.8},
        {"cx": 8.0,  "cz": -5.0,  "yb": 1.8, "w": 8.5, "d": 7.0, "h": 4.5},
        {"cx": 8.8,  "cz": 5.0,   "yb": 1.0, "w": 9.0, "d": 8.0, "h": 4.9},
        {"cx": 8.2,  "cz": 15.0,  "yb": 0.2, "w": 8.6, "d": 7.2, "h": 4.4},
        {"cx": -8.0, "cz": -15.0, "yb": 2.6, "w": 8.5, "d": 7.0, "h": 4.5},
        {"cx": -9.0, "cz": -5.0,  "yb": 1.8, "w": 10.5, "d": 8.0, "h": 5.1},
        {"cx": -8.2, "cz": 5.0,   "yb": 1.0, "w": 8.8, "d": 7.5, "h": 4.6},
        {"cx": -8.8, "cz": 15.0,  "yb": 0.2, "w": 9.2, "d": 7.8, "h": 4.7},
    ]
    for h in hanok_specs:
        cx, cz, yb = h["cx"], h["cz"], h["yb"]
        w, d, ht = h["w"], h["d"], h["h"]
        h_mass.add_box(w, ht * 0.6, d, cx, yb + ht * 0.3, cz, region=Q_DANCHEONG, scale=2.0)
        h_mass.add_box(w + 0.8, 0.5, d + 0.8, cx, yb + 0.25, cz, region=Q_GRANITE, scale=2.0)
        hw_e, hd_e = w / 2.0 + 0.7, d / 2.0 + 0.7
        rf_y = yb + ht * 0.6
        v_pal, u_pal, t_pal = paljak_roof(hw_e=hw_e, hd_e=hd_e, ridge_len=4.0, height=ht * 0.42, y_base=rf_y, nt=4, nper=16, eave_lift=0.25)
        h_roof.add(v_pal, u_pal, t_pal, offset=(cx, 0, cz), region=Q_ROOF, scale=2.0)
    d2.add(h_mass)
    d2.add(h_roof)

    return d2

def generate():
    out_dir = "/workspace/pimang-sandbox/lego_blocks/03053_TRAD_p12_북촌_가회동31번지"
    reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03053_TRAD_p12_북촌_가회동31번지"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(reg_dir, exist_ok=True)

    print("Building LOD3...")
    d3 = build_gahoe31_lod3()
    doc3, b3_len, stats3, t3 = d3.build("texture_atlas.webp", MATERIALS)

    print("Building LOD2...")
    d2 = build_gahoe31_lod2()
    doc2, b2_len, stats2, t2 = d2.build("texture_atlas.webp", MATERIALS)

    print(f"LOD3 Triangles: {t3}, LOD2 Triangles: {t2}")

    manifest = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": COMPOSITE_ID,
        "block_id": BID,
        "name": NAME,
        "category": "CAT02_TRAD_ALLEY",
        "postal_code": "03053",
        "coordinates": {"lat": 37.5828, "lng": 126.9854},
        "heading": 174.0,
        "base_plinth_height_m": 3.2,
        "ground": {"mode": "snap_to_terrain", "base_y": 0.0},
        "bbox_local_m": {"min": [-19.0, 0.0, -21.0], "max": [19.0, 8.5, 21.0]},
        "lod_switch_distance": {"lod3_to_lod2_m": 45.0, "lod2_to_lod1_m": 120.0},
        "hierarchical_components": [
            {"id": "gahoe31_sloped_alley_pavement", "level": 1, "triangles": 420, "description": "가회동 31번지 조망 뷰 테라스 데크 및 2개 구간 실측 화강암 돌계단"},
            {"id": "gahoe31_sagoseok_walls", "level": 1, "triangles": 520, "description": "골목길 양측 8개 섹션 사고석 돌담 및 2단 기와 갓"},
            {"id": "gahoe31_hanok_plinths", "level": 2, "triangles": 480, "description": "한옥 8채 계단식 맞춤 화강암 장대석 기단"},
            {"id": "gahoe31_wood_columns_and_windows", "level": 2, "triangles": 2480, "description": "전통 목조 기둥 64열주 및 세살창/아자창 창호살 파사드"},
            {"id": "gahoe31_eave_rafters_3d", "level": 3, "triangles": 7680, "description": "처마선 둘레 3D 둥근 서까래 160기 입체 배열"},
            {"id": "gahoe31_rooftop_panorama_roofs", "level": 3, "triangles": 6240, "description": "오공간 상승 처마 곡률 적용 한옥 8채 루프탑 파노라마 기와 패키지"},
            {"id": "gahoe31_lanterns_and_gates", "level": 4, "triangles": 720, "description": "솟을대문 처마 밑 홍청 비단 청사초롱 4쌍 및 황동 문고리"},
            {"id": "gahoe31_traditional_chimneys", "level": 4, "triangles": 240, "description": "전통 와편 굴뚝 4기 및 연가 지붕 갓"}
        ],
        "interaction_hotspots": [
            {"id": "hotspot_gahoe31_viewpoint", "label": "가회동 31번지 언덕 조망점"},
            {"id": "hotspot_rooftop_panorama", "label": "한옥 루프탑 파노라마 뷰"},
            {"id": "hotspot_sloped_stairs", "label": "경사지 골목 돌계단"},
            {"id": "anchor_n_seoul_tower_view", "label": "남산서울타워 원경 조망 앵커"}
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_02_03053_002_01(조망데크), _02(루프탑 세트), _03(남산타워 앵커) 등 무한 분해",
        "files": {
            "model_lod3.gltf": {"triangles": t3},
            "model_lod2.gltf": {"triangles": t2},
            "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}
        },
        "references": [
            "북촌 5경·6경 가회동 31번지 골목길 조망 실측 자료 — 서울시 역사문화재과",
            "TASK_REQUEST_20261107_PIMANG_12BLOCKS_SPEC_117.md 종로 12종 발주서 #6"
        ]
    }

    atlas = create_gahoe31_atlas()

    for target in [out_dir, reg_dir]:
        json.dump(manifest, open(os.path.join(target, "block_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(doc3, open(os.path.join(target, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(doc2, open(os.path.join(target, "model_lod2.gltf"), "w", encoding="utf-8"))
        atlas.save(os.path.join(target, "texture_atlas.webp"), "WEBP", quality=88)

    print(f"Successfully generated {BID} in {out_dir} and {reg_dir}!")

if __name__ == "__main__":
    generate()
