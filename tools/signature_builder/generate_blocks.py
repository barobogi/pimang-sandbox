#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""종로구 시그니처 3D 레고 블록 2종 생성기 (Task B 선도 블록)
1. 03045_HERO_p01_경복궁_근정전
2. 03188_WATER_p21_청계천_단면음각_수로
지시서: TASK_REQUEST_20261107_JONGNO_LEGO_PRIORITY12.md
축: 미터, Y상, -Z 북, +Z 남(정면/마당 방향). 블록2는 X=흐름방향.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gltf_builder import (Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG,
                          Q_ROOF, Q_GOLD)

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
GEN = "Pimang signature-block generator v1.0 (jongno Task B)"
CR = "barobogi / Pimang - jongno 3D digital twin benchmark"

Q_WATER = (0.5, 0.0)     # stream atlas: bottom-right
Q_PEBBLE = (0.5, 0.5)    # stream atlas: top-right
Q_MASONRY = (0.0, 0.5)   # stream atlas: top-left

MATS_PALACE = MATERIALS[:5]
MATS_STREAM = [
    {  # 0 pavement granite
        "name": "paving_granite_walkway",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.88},
    },
    {  # 1 stone masonry retaining wall
        "name": "retaining_wall_masonry",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.92},
        "doubleSided": False,
    },
    {  # 2 water surface
        "name": "cheonggyecheon_water_pbr",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.08},
        "doubleSided": True,
    },
    {  # 3 crossing stones / bridge deck
        "name": "stepping_stone_bridge_deck",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.78},
        "doubleSided": True,
    },
]


# ------------------------------------------------------------------ 블록 1
def build_geunjeongjeon():
    doc = GLTFDoc(GEN, CR)

    g = Mesh("woldae_2tier_granite", 0)          # 2단 월대 + 돌난간
    g.add_prism([(-26, -16), (26, -16), (26, 16), (-26, 16)], 0.0, 1.2,
                region=Q_GRANITE, scale=8.0)
    g.add_prism([(-22, -13), (22, -13), (22, 13), (-22, 13)], 1.2, 2.4,
                region=Q_GRANITE, scale=8.0)
    for (ax, az, bx, bz) in [(-22, -13, 22, -13), (-22, 13, 22, 13),
                             (-22, -13, -22, 13), (22, -13, 22, 13)]:
        n = int(max(abs(bx - ax), abs(bz - az)) / 2.2)
        for i in range(n + 1):
            t = i / n
            px, pz = ax + (bx - ax) * t, az + (bz - az) * t
            g.add_box(0.16, 1.0, 0.16, px, 2.9, pz, region=Q_GRANITE, scale=3.0)
        lenx, lenz = abs(bx - ax), abs(bz - az)
        g.add_box(lenx or 0.16, 0.12, lenz or 0.16,
                  (ax + bx) / 2, 3.42, (az + bz) / 2, region=Q_GRANITE, scale=4.0)
        g.add_box(lenx or 0.12, 0.10, lenz or 0.12,
                  (ax + bx) / 2, 3.02, (az + bz) / 2, region=Q_GRANITE, scale=4.0)
    doc.add(g)

    s = Mesh("sasinsu_sibijisin_stone_statues", 4)   # 사신수/십이지신 석수 12기
    spots = [(-18, -12.4), (-8, -12.4), (0, -12.4), (8, -12.4), (18, -12.4),
             (-21.4, 0), (21.4, 0), (-18, 12.4), (-8, 12.4), (8, 12.4),
             (18, 12.4), (0, 12.4)]
    for k, (sx, sz) in enumerate(spots):
        s.add_box(1.0, 0.9, 1.0, sx, 2.85, sz, region=Q_GRANITE, scale=2.0)
        s.add_cyl(sx, 3.3, sz, 0.34, 0.28, 0.85, seg=8, region=Q_GRANITE, scale=2.0)
        s.add_box(0.5, 0.45, 0.5, sx, 4.3, sz, ry=k * 0.26, region=Q_GRANITE, scale=2.0)
    doc.add(s)

    hall = Mesh("geunjeongjeon_hall_columns_walls", 1)   # 정전 본체 (7칸 x 4)
    hall.add_box(33.5, 0.5, 20.5, 0, 2.65, -2.0, region=Q_GRANITE, scale=6.0)
    for i in range(7):
        for j in range(4):
            hall.add_cyl(-16.8 + i * 5.6, 2.9, -9.5 + j * 5.0, 0.42, 0.40, 5.2,
                         seg=10, region=Q_DANCHEONG, scale=2.0)
    hall.add_box(31.5, 4.4, 0.3, 0, 5.1, -9.6, region=Q_DANCHEONG, scale=1.4)
    hall.add_box(0.3, 4.4, 17.5, -16.6, 5.1, -2.0, region=Q_DANCHEONG, scale=1.4)
    hall.add_box(0.3, 4.4, 17.5, 16.6, 5.1, -2.0, region=Q_DANCHEONG, scale=1.4)
    for i in range(6):                                    # 전면 판자문 6칸
        hall.add_box(4.9, 4.4, 0.18, -14.0 + i * 5.6, 5.1, 5.7, region=Q_DANCHEONG, scale=1.4)
    hall.add_box(34.5, 0.55, 0.55, 0, 8.15, 8.8, region=Q_DANCHEONG, scale=1.6)
    hall.add_box(34.5, 0.55, 0.55, 0, 8.15, -12.8, region=Q_DANCHEONG, scale=1.6)
    doc.add(hall)

    roof = Mesh("paljak_roof_two_tier_curved_eaves", 2)   # 중층 팔작지붕
    roof.add_roof(Q_ROOF, hw_e=20.5, hd_e=13.5, ridge_len=21.0, height=4.8,
                  y_base=8.45, eave_lift=0.9)
    roof.add_roof(Q_ROOF, hw_e=11.6, hd_e=4.6, ridge_len=16.0, height=4.0,
                  y_base=13.1, eave_lift=0.75)
    roof.add_box(17.0, 0.75, 0.85, 0, 17.35, 0.0, region=Q_DANCHEONG, scale=2.0)
    roof.add_box(22.2, 0.7, 1.0, 0, 13.25, 0.0, region=Q_DANCHEONG, scale=2.0)
    for sx in (-10.6, 10.6):                              # 잡상/치미
        roof.add_box(1.15, 2.3, 1.15, sx, 14.4, 0.0, region=Q_GOLD, scale=2.0)
    for sx in (-8.2, 8.2):
        roof.add_box(0.95, 1.7, 0.95, sx, 18.25, 0.0, region=Q_GOLD, scale=2.0)
    doc.add(roof)

    interior = Mesh("throne_ilwolobongdo_ceiling_dragon", 3)  # 어좌 + 일월오봉도
    interior.add_box(2.9, 1.15, 1.6, 0.0, 3.47, -6.2, region=Q_GRANITE, scale=2.0)
    interior.add_box(1.5, 0.35, 1.0, 0.0, 4.22, -6.0, region=Q_GOLD, scale=2.0)
    interior.add_box(2.5, 3.1, 0.28, 0.0, 5.95, -7.0, region=Q_GOLD, scale=1.4)
    for k in range(5):                                    # 일월오봉도 5폭 병풍
        interior.add_box(1.75, 3.3, 0.12, -3.4 + k * 1.7, 6.05, -9.15,
                         ry=(k - 2) * 0.10, region=Q_DANCHEONG, scale=1.1)
    interior.add_cyl(0.0, 10.2, -6.2, 0.05, 0.34, 1.15, seg=8, region=Q_GOLD, scale=1.5)
    doc.add(interior)

    pum = Mesh("pumgyeseok_rank_stones_courtyard", 0)      # 품계석 박석 2열
    for row_sign in (-1, 1):
        for i in range(14):
            pum.add_box(0.52, 0.12, 1.7, -8.1 + i * 1.25, 0.06, 18.2 + row_sign * 2.3,
                        ry=(-1 if i % 2 else 1) * 0.05, region=Q_GRANITE, scale=2.2)
    doc.add(pum)

    deumu = Mesh("deumu_bronze_water_cauldrons", 3)        # 드므 2기
    for sx in (-20.5, 20.5):
        deumu.add_cyl(sx, 0.0, 19.5, 1.05, 0.92, 1.25, seg=14, region=Q_GOLD, scale=2.0)
    doc.add(deumu)

    haenggak = Mesh("haenggak_corridor_boundary", 1)        # 사방 행각 바운더리
    for (ax, az, bx, bz) in [(-34, 31.5, 34, 31.5), (-34, 31.5, -34, -2.5),
                             (34, 31.5, 34, -2.5)]:
        lenx, lenz = abs(bx - ax), abs(bz - az)
        haenggak.add_box(lenx or 0.4, 3.0, lenz or 0.4,
                         (ax + bx) / 2, 1.5, (az + bz) / 2, region=Q_DANCHEONG, scale=1.2)
        haenggak.add_box((lenx + 1.1) if lenx else 1.3, 0.35,
                         (lenz + 1.1) if lenz else 1.3,
                         (ax + bx) / 2, 3.2, (az + bz) / 2, region=Q_ROOF, scale=1.6)
    doc.add(haenggak)

    for (nm, tr) in [
        ("night_light_spotlight_NE_3000K", (26.0, 3.4, -22.0)),
        ("night_light_spotlight_NW_3000K", (-26.0, 3.4, -22.0)),
        ("night_light_spotlight_SE_3000K", (26.0, 3.4, 26.0)),
        ("night_light_spotlight_SW_3000K", (-26.0, 3.4, 26.0)),
        ("anchor_ceiling_dragon_chiljo", (0.0, 11.6, -6.2)),
        ("hotspot_ilwolobongdo", (0.0, 6.1, -9.0)),
        ("hotspot_deumu_SE", (-20.5, 1.3, 19.5)),
        ("hotspot_deumu_SW", (20.5, 1.3, 19.5)),
        ("hotspot_pumgyeseok_row", (0.0, 0.5, 18.2)),
        ("hotspot_sasinsu_statues", (0.0, 3.5, -12.4)),
    ]:
        doc.add_anchor(nm, tr)
    return doc


# ------------------------------------------------------------------ 블록 2
def build_cheonggyecheon():
    doc = GLTFDoc(GEN, CR)
    L = 300.0

    ground = Mesh("city_ground_level_banks", 0)
    ground.add_box(L, 0.3, 34, 0, -0.15, 25.0, region=Q_GRANITE, scale=6.0)
    ground.add_box(L, 0.3, 34, 0, -0.15, -25.0, region=Q_GRANITE, scale=6.0)
    doc.add(ground)

    wall = Mesh("retaining_wall_stone_chute_neg2_5m", 1)   # 옹벽 석축 (-2.5m)
    wall.add_box(L, 2.5, 0.6, 0, -1.25, 8.4, region=Q_MASONRY, scale=3.0)
    wall.add_box(L, 2.5, 0.6, 0, -1.25, -8.4, region=Q_MASONRY, scale=3.0)
    doc.add(wall)

    bed = Mesh("channel_bed_du_shape", 1)                  # ㄷ자형 수로 바닥
    bed.add_box(L, 0.35, 17.4, 0, -2.52, 0.0, region=Q_MASONRY, scale=3.0)
    doc.add(bed)

    walk = Mesh("streamside_promenade_walkway", 0)         # 수변 산책로
    walk.add_box(L, 0.3, 2.6, 0, -1.35, 6.6, region=Q_GRANITE, scale=5.0)
    walk.add_box(L, 0.3, 2.6, 0, -1.35, -6.6, region=Q_GRANITE, scale=5.0)
    doc.add(walk)

    water = Mesh("water_surface_plane", 2)                 # 수면 플레인
    water.add_box(L - 6, 0.06, 12.4, 0, -1.92, 0.0, region=Q_WATER, scale=4.0)
    doc.add(water)

    steps = Mesh("jingyeomdari_stepping_stones", 3)        # 징검다리 2열 20기
    for row, rx in ((0, 64.0), (1, 65.6)):
        for k in range(10):
            steps.add_box(0.85, 0.3, 0.85, rx - 0.8 * row, -1.95, -4.5 + k * 1.0,
                          region=Q_PEBBLE, scale=1.5)
    doc.add(steps)

    bridges = Mesh("stone_arch_bridges_mojeongyo_gwangtonggyo", 0)
    parapets = Mesh("bridge_parapets_banisters", 1)
    for bx in (0.0, -90.0):                                # 모전교 / 광통교
        bridges.add_arch(Q_GRANITE, span=20.5, width=12.5, deck_y=1.75,
                         thickness=1.35, nseg=18, offset=(bx, 0, 0), scale=1.2)
        bridges.add_box(12.5, 0.55, 22.0, bx, 1.95, 0.0, region=Q_GRANITE, scale=4.0)
        parapets.add_box(12.5, 0.95, 0.35, bx, 2.7, 10.9, region=Q_MASONRY, scale=3.0)
        parapets.add_box(12.5, 0.95, 0.35, bx, 2.7, -10.9, region=Q_MASONRY, scale=3.0)
        bridges.add_box(13.5, 2.2, 2.6, bx, -3.6, 10.2, region=Q_MASONRY, scale=2.0)
        bridges.add_box(13.5, 2.2, 2.6, bx, -3.6, -10.2, region=Q_MASONRY, scale=2.0)
    doc.add(bridges)
    doc.add(parapets)

    for (nm, tr) in [
        ("anchor_bridge_mojeongyo", (0.0, 2.4, 0.0)),
        ("anchor_bridge_gwangtonggyo", (-90.0, 2.4, 0.0)),
        ("anchor_section_cheonggye_plaza_start", (150.0, 0.4, 0.0)),
        ("anchor_section_mujeon_midpoint", (0.0, 0.4, 0.0)),
        ("anchor_section_gwangtong_end", (-150.0, 0.4, 0.0)),
        ("hotspot_jingyeomdari", (64.8, -1.6, 0.5)),
        ("hotspot_baekcheon_fountain_wall", (120.0, -0.5, 8.0)),
    ]:
        doc.add_anchor(nm, tr)
    return doc


# ------------------------------------------------------------ 텍스처 아틀라스
def make_atlas(kind):
    """1024x1024, 2x2 quadrant atlas. UV quadrant (u0,v0) maps to image
    (col*512, (1-row)*512) origin (image y is top-down)."""
    import numpy as np
    from PIL import Image, ImageDraw
    rng = np.random.default_rng(42 if kind == "palace" else 77)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    if kind == "palace":
        grain(0, 0, (188, 186, 180), 9)       # (0,0) granite
        px[512:1024, 512:1024] = (58, 58, 64)   # (0.5,0) roof tile base
        px[0:512, 512:1024] = (208, 172, 86)    # (0.5,0.5) gold base
        img = Image.fromarray(px.astype("uint8"))
        d = ImageDraw.Draw(img)
        # (0,0.5) dancheong wood: top-left
        for y in range(0, 512, 64):
            d.rectangle([0, y, 512, y + 54], fill=(148, 58, 44))
            d.rectangle([0, y + 54, 512, y + 64], fill=(72, 30, 26))
            d.rectangle([0, y + 18, 512, y + 24], fill=(42, 84, 78))
            d.rectangle([0, y + 36, 512, y + 40], fill=(58, 70, 130))
        # (0.5,0) roof tile: bottom-right
        for y in range(512, 1024, 26):
            d.line([(512, y), (1024, y)], fill=(30, 30, 34), width=4)
        for col in range(0, 512, 30):
            off = 13 if (col // 30) % 2 else 0
            d.line([(512 + col + off, 512), (512 + col + off, 1024)], fill=(38, 38, 44), width=3)
        # (0.5,0.5) gold: brushed horizontal grain
        for y in range(0, 512, 4):
            c = 196 + (y * 7) % 34
            d.line([(512, y), (1024, y)], fill=(c, int(c * 0.78), int(c * 0.30)))
    else:
        grain(0, 0, (176, 174, 169), 8)       # (0,0) pavement
        img = Image.fromarray(px.astype("uint8"))
        d = ImageDraw.Draw(img)
        for o in range(0, 513, 64):
            d.line([(o, 512), (o, 1024)], fill=(126, 124, 118), width=3)
            d.line([(0, 512 + o), (512, 512 + o)], fill=(126, 124, 118), width=3)
        # (0,0.5) masonry courses: top-left
        for y in range(0, 512, 42):
            d.rectangle([0, y, 512, y + 36], fill=(126, 124, 120))
            d.rectangle([0, y + 36, 512, y + 42], fill=(84, 82, 80))
        for y in range(0, 512, 42):
            for x in range(0, 513, 90):
                off = 22 if (y // 42) % 2 else 0
                d.line([((x + off) % 512, y), ((x + off) % 512, y + 36)], fill=(96, 94, 92), width=2)
        # (0.5,0) water: bottom-right
        for y in range(512, 1024):
            t = (y - 512) / 512.0
            d.line([(512, y), (1024, y)], fill=(int(24 + 26 * t), int(88 + 40 * t), int(120 + 50 * t)))
        for y in range(518, 1024, 22):
            for x in range(512 + ((y * 13) % 44), 1024, 60):
                d.line([(x, y), (x + 34, y + 2)], fill=(172, 212, 232), width=1)
        # (0.5,0.5) pebble/stepping: top-right
        d.rectangle([512, 0, 1024, 512], fill=(158, 155, 150))
        for i in range(140):
            x = 512 + (i * 97) % 480 + 12
            y = (i * 61) % 480 + 12
            r = 8 + (i * 17) % 14
            d.ellipse([x, y, x + r, y + r], fill=(120 + (i * 13) % 40,) * 3)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    results = []

    # ---- 블록 1: 경복궁 근정전
    d3 = build_geunjeongjeon()
    g3, _, _, t3 = d3.build("texture_atlas.webp", MATS_PALACE)
    g2 = GLTFDoc(GEN, CR)
    lod2 = Mesh("woldae_lod2", 0)
    lod2.add_prism([(-26, -16), (26, -16), (26, 16), (-26, 16)], 0.0, 2.4)
    g2.add(lod2)
    hall2 = Mesh("hall_mass_lod2", 1)
    hall2.add_box(33.5, 6.0, 20.5, 0, 5.4, -2.0)
    g2.add(hall2)
    roof2 = Mesh("roof_mass_lod2", 2)
    roof2.add_roof(Q_ROOF, hw_e=20.5, hd_e=13.5, ridge_len=21.0, height=5.4,
                   y_base=8.45, nt=5, nper=24, eave_lift=0.7)
    g2.add(roof2)
    ridge2 = Mesh("ridge_lod2", 3)
    ridge2.add_box(17.0, 0.8, 0.9, 0, 17.75, 0.0)
    g2.add(ridge2)
    g2doc, _, _, t2 = g2.build("texture_atlas.webp", MATS_PALACE)
    m1 = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": "11110_01_03045_001",
        "block_id": "03045_HERO_p01_경복궁_근정전",
        "name": "경복궁 근정전",
        "category": "CAT01_PALACE_ROYAL",
        "postal_code": "03045",
        "coordinates": [126.977017, 37.57861],
        "heading": 174.2,
        "elevation_asl": 34.5,
        "lod_switch_distance": 250,
        "axis_alignment": {
            "reference": "한양도성 축선(경복궁 중심축)",
            "heading_deg": 174.2,
            "bbox_4corners_wgs84_approx": {
                "NW": [126.97515, 37.57995], "NE": [126.97899, 37.57995],
                "SW": [126.97515, 37.57727], "SE": [126.97899, 37.57727],
            },
        },
        "hierarchical_components": [
            {"id": "woldae_2tier_granite", "desc": "2단 월대 + 4면 돌난간(기둥 136기)"},
            {"id": "sasinsu_sibijisin_stone_statues", "desc": "사신수/십이지신 석수 12기"},
            {"id": "geunjeongjeon_hall_columns_walls", "desc": "정전 본체 7칸x4 기둥 28기 + 판자문 + 창방/평방 도리"},
            {"id": "paljak_roof_two_tier_curved_eaves", "desc": "중층 팔작지붕 곡선 처마(오공간 곡률) + 마루 + 잡상/치미"},
            {"id": "throne_ilwolobongdo_ceiling_dragon", "desc": "실내 핵심 심볼: 왕의 어좌 + 일월오봉도 병풍 5폭 + 천장 칠조룡 앵커"},
            {"id": "pumgyeseok_rank_stones_courtyard", "desc": "정1품~종9품 품계석 박석 2열 28기"},
            {"id": "haenggak_corridor_boundary", "desc": "사방 행각(회랑) 바운더리 — 조정 공간 완결성"},
        ],
        "night_lighting_anchors": {
            "color_temp_k": 3000,
            "phase_link": "Phase 7/18 야간 개장 투광 연동",
            "spots": [
                {"id": "NE", "offset_m": [26.0, 3.4, -22.0]},
                {"id": "NW", "offset_m": [-26.0, 3.4, -22.0]},
                {"id": "SE", "offset_m": [26.0, 3.4, 26.0]},
                {"id": "SW", "offset_m": [-26.0, 3.4, 26.0]},
            ],
        },
        "interaction_hotspots": [
            {"id": "hotspot_ilwolobongdo", "label": "일월오봉도 병풍"},
            {"id": "hotspot_deumu_SE", "label": "드므(화재방지 청동솥) 남동"},
            {"id": "hotspot_deumu_SW", "label": "드므 남서"},
            {"id": "hotspot_sasinsu_statues", "label": "사신수/십이지신 석수"},
            {"id": "hotspot_pumgyeseok_row", "label": "품계석 박석"},
        ],
        "key_expansion_rule": "프랙탈 하위 분해: composite_id 뒤 _01, _02 … (예: 11110_01_03045_001_02 어좌 초정밀 세트)",
        "files": {"model_lod3.gltf": {"triangles": t3}, "model_lod2.gltf": {"triangles": t2},
                  "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}},
        "references": [
            "국보 제223호 경복궁 근정전 — 문화재청 국가문화재포털",
            "TASK_REQUEST_20261107_JONGNO_LEGO_PRIORITY12.md 1차 최우선 12대 #1",
        ],
    }
    results.append(("03045_HERO_p01_경복궁_근정전", g3, g2doc, m1, "palace", MATS_PALACE, t3, t2))

    # ---- 블록 2: 청계천 단면음각 수로
    d3c = build_cheonggyecheon()
    c3, _, _, ct3 = d3c.build("texture_atlas.webp", MATS_STREAM)
    d2c = GLTFDoc(GEN, CR)
    w = Mesh("walls_bed_lod2", 1)
    w.add_box(300, 2.6, 0.6, 0, -1.1, 8.3)
    w.add_box(300, 2.6, 0.6, 0, -1.1, -8.3)
    w.add_box(300, 0.3, 17.4, 0, -2.35, 0.0)
    d2c.add(w)
    grd2 = Mesh("ground_lod2", 0)
    grd2.add_box(300, 0.3, 34, 0, -0.15, 25.0)
    grd2.add_box(300, 0.3, 34, 0, -0.15, -25.0)
    d2c.add(grd2)
    wt2 = Mesh("water_lod2", 2)
    wt2.add_box(294, 0.06, 12.4, 0, -1.9, 0.0)
    d2c.add(wt2)
    br2 = Mesh("bridges_lod2", 3)
    for bx in (0.0, -90.0):
        br2.add_box(12.5, 1.2, 22.0, bx, 1.2, 0.0)
        br2.add_box(13.5, 2.2, 2.6, bx, 0.4, 10.2)
        br2.add_box(13.5, 2.2, 2.6, bx, 0.4, -10.2)
    d2c.add(br2)
    c2, _, _, ct2 = d2c.build("texture_atlas.webp", MATS_STREAM)
    m2 = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": "11110_03_03188_021",
        "block_id": "03188_WATER_p21_청계천_단면음각_수로",
        "name": "청계천 단면음각 수로",
        "category": "CAT03_NATURE_WATER",
        "postal_code": "03188",
        "coordinates": [126.97793, 37.5692],
        "heading": 262.0,
        "elevation_asl": 18.0,
        "depth_negative_elevation": -2.5,
        "section": "청계광장 ~ 모전교 ~ 광통교",
        "lod_switch_distance": 250,
        "water_shader_parameters": {
            "type": "pbr_planar_reflection",
            "base_roughness": 0.08,
            "metallic": 0.0,
            "normal_scale": 0.35,
            "uv_scroll_speed": [0.02, 0.05],
            "reflection_intensity": 0.85,
            "fresnel_power": 3.0,
            "tint_rgb": [0.32, 0.55, 0.62],
        },
        "bridges": [
            {"name": "모전교", "offset_along_flow_m": 0.0, "type": "arch_stone", "anchor": "anchor_bridge_mojeongyo"},
            {"name": "광통교", "offset_along_flow_m": -90.0, "type": "arch_stone", "anchor": "anchor_bridge_gwangtonggyo"},
        ],
        "hierarchical_components": [
            {"id": "retaining_wall_stone_chute_neg2_5m", "desc": "-2.5m ㄷ자형 음각 단면 + 양측 옹벽 석축"},
            {"id": "channel_bed_du_shape", "desc": "수로 바닥 석축 바닥판"},
            {"id": "streamside_promenade_walkway", "desc": "수변 산책로(양측, 수면 위 1.4m)"},
            {"id": "stone_arch_bridges_mojeongyo_gwangtonggyo", "desc": "모전교·광통교 아치 석교 + 수중 교각 기단"},
            {"id": "jingyeomdari_stepping_stones", "desc": "징검다리 2열 20기"},
            {"id": "water_surface_plane", "desc": "PBR 수면 반사 플레인"},
        ],
        "interaction_hotspots": [
            {"id": "hotspot_jingyeomdari", "label": "징검다리 건너기"},
            {"id": "hotspot_baekcheon_fountain_wall", "label": "벽천 폭포 분수대"},
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_03_03188_021_01(모전교 교각), _02(광통교 아치) 등 무한 분해",
        "files": {"model_lod3.gltf": {"triangles": ct3}, "model_lod2.gltf": {"triangles": ct2},
                  "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}},
        "references": [
            "서울시 청계천 복원(2005) 구간 자료 - 청계광장~광통교",
            "TASK_REQUEST_20261107_JONGNO_LEGO_PRIORITY12.md 1차 최우선 12대 #7",
        ],
    }
    results.append(("03188_WATER_p21_청계천_단면음각_수로", c3, c2, m2, "stream", MATS_STREAM, ct3, ct2))

    for (bid, lod3, lod2, manifest, kind, mats, t3n, t2n) in results:
        p = os.path.join(OUT, bid)
        os.makedirs(p, exist_ok=True)
        manifest["files"]["model_lod3.gltf"]["triangles"] = t3n
        manifest["files"]["model_lod2.gltf"]["triangles"] = t2n
        json.dump(manifest, open(os.path.join(p, "block_manifest.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        json.dump(lod3, open(os.path.join(p, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(lod2, open(os.path.join(p, "model_lod2.gltf"), "w", encoding="utf-8"))
        make_atlas(kind).save(os.path.join(p, "texture_atlas.webp"), "WEBP", quality=88)
        print(f"{bid}: lod3 {t3n} tris, lod2 {t2n} tris -> {p}")


if __name__ == "__main__":
    main()
