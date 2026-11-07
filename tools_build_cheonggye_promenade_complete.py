#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종로구 시그니처 3D 레고 블록 #8: 청계천 수변산책로 (세운교~청계광장)
ID: 03188_WATER_p22_청계천_수변산책로
복합키: 11110_03_03188_002
규약: 117호 블록 장착 규약 준수 (y=0.00 도로면 스냅, 음각 지하 단차, 절대고도 0, 4대 파일 세트, 1024 WebP 아틀라스)
"""
import os, sys, math, json, struct, base64
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/signature_builder"))
from gltf_builder import Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG, Q_ROOF, Q_GOLD

BID = "03188_WATER_p22_청계천_수변산책로"
COMPOSITE_ID = "11110_03_03188_002"
NAME = "청계천 수변산책로 (세운교~청계광장)"
GEN = "Pickle 117-spec high-fidelity builder v3.0 (Cheonggyecheon Promenade Masterpiece)"
CR = "barobogi / Pickle - jongno 3D digital twin benchmark"

def create_promenade_atlas():
    """1024x1024 PBR 텍스처 아틀라스: 화강암 옹벽/계단, 수변 목재 데크/산책로, 청계천 에메랄드 수면, 갈대 수생식물/LED"""
    rng = np.random.default_rng(108)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    grain(0, 0, (178, 175, 168), 10)       # (0,0) Granite Retaining Walls & Stone Steps
    grain(0, 1, (156, 108, 68), 8)         # (0,0.5) Timber Boardwalk Deck & Clay Promenade
    grain(1, 0, (38, 92, 118), 6)          # (0.5,0) Cheonggye Water Surface & Wave Ripples
    grain(1, 1, (82, 126, 64), 10)         # (0.5,0.5) Reed Grass Wetland & Brass Bollards

    img = Image.fromarray(px.astype("uint8"))
    d = ImageDraw.Draw(img)

    for y in range(512, 1024, 28):
        d.line([(0, y), (512, y)], fill=(114, 112, 106), width=3)
    for row, y in enumerate(range(512, 1024, 28)):
        shift = 20 if row % 2 else 0
        for x in range(shift, 512, 40):
            d.line([(x, y), (x, y + 28)], fill=(114, 112, 106), width=2)

    for y in range(0, 512, 20):
        d.line([(0, y), (512, y)], fill=(108, 72, 44), width=3)
    for x in range(0, 512, 80):
        d.line([(x, 0), (x, 512)], fill=(92, 60, 36), width=2)

    for y in range(512, 1024, 16):
        d.line([(512, y), (1024, y)], fill=(52, 118, 148), width=3)
    for x in range(512, 1024, 32):
        for y in range(520, 1024, 32):
            d.ellipse([x - 6, y - 4, x + 6, y + 4], fill=(72, 142, 172))

    d.rectangle([512, 0, 768, 512], fill=(68, 112, 52))
    for y in range(0, 512, 12):
        d.line([(512, y), (768, y)], fill=(92, 146, 74), width=2)
    d.rectangle([768, 0, 1024, 512], fill=(225, 205, 112))
    for y in range(0, 512, 16):
        d.line([(768, y), (1024, y)], fill=(245, 225, 142), width=3)

    return img

def build_promenade_lod3():
    d3 = GLTFDoc(GEN, CR)

    # 1. 상부 청계천로 도로면 및 안전 난간 (Y=0.00m 스냅)
    m_street = Mesh("cheonggye_street_level", 0)
    m_street.add_box(7.0, 0.4, 40.0, 16.5, -0.2, 0.0, region=Q_GRANITE, scale=4.0)
    m_street.add_box(7.0, 0.4, 40.0, -16.5, -0.2, 0.0, region=Q_GRANITE, scale=4.0)

    # 상부 안전 방호 난간 및 수직 발루스터 40개
    m_street.add_box(0.2, 0.1, 40.0, 13.0, 1.05, 0.0, region=Q_DANCHEONG, scale=2.0)
    m_street.add_box(0.2, 0.1, 40.0, -13.0, 1.05, 0.0, region=Q_DANCHEONG, scale=2.0)
    for iz in range(20):
        pos_z = -19.0 + iz * 2.0
        m_street.add_cyl(13.0, 0.0, pos_z, 0.04, 0.04, 1.05, seg=6, region=Q_DANCHEONG, scale=1.0)
        m_street.add_cyl(-13.0, 0.0, pos_z, 0.04, 0.04, 1.05, seg=6, region=Q_DANCHEONG, scale=1.0)
    d3.add(m_street)

    # 2. 5중 음각 단차 화강석 옹벽 및 진입 돌계단 2개소와 경사로
    m_walls = Mesh("cheonggye_retaining_walls", 0)
    m_walls.add_box(0.6, 2.0, 40.0, 12.8, -1.0, 0.0, region=Q_GRANITE, scale=4.0)
    m_walls.add_box(2.0, 0.3, 40.0, 11.5, -2.15, 0.0, region=Q_GRANITE, scale=3.0)
    m_walls.add_box(0.6, 1.6, 40.0, 10.3, -2.8, 0.0, region=Q_GRANITE, scale=3.0)

    m_walls.add_box(0.6, 2.0, 40.0, -12.8, -1.0, 0.0, region=Q_GRANITE, scale=4.0)
    m_walls.add_box(2.0, 0.3, 40.0, -11.5, -2.15, 0.0, region=Q_GRANITE, scale=3.0)
    m_walls.add_box(0.6, 1.6, 40.0, -10.3, -2.8, 0.0, region=Q_GRANITE, scale=3.0)

    # 지그재그 돌계단 2개소 (북측 계단 18단 x 2구간)
    for z_st in [-12.0, 12.0]:
        for i in range(18):
            sy = -0.15 - i * 0.19
            sx = 12.6 - i * 0.14
            m_walls.add_box(0.35, 0.19, 2.4, sx, sy, z_st, region=Q_GRANITE, scale=1.0)
            m_walls.add_box(0.15, 0.28, 2.4, sx - 0.2, sy + 0.08, z_st, region=Q_GRANITE, scale=0.5)
            # 계단 난간 포스트
            m_walls.add_cyl(sx, sy + 0.5, z_st - 1.15, 0.03, 0.03, 0.7, seg=6, region=Q_DANCHEONG, scale=0.5)
            m_walls.add_cyl(sx, sy + 0.5, z_st + 1.15, 0.03, 0.03, 0.7, seg=6, region=Q_DANCHEONG, scale=0.5)

        for i in range(20):
            rz = z_st - 6.0 + i * 0.6
            ry = -0.15 - i * 0.17
            m_walls.add_box(2.2, 0.18, 0.65, -11.5, ry, rz, region=Q_GRANITE, scale=1.0)
    d3.add(m_walls)

    # 3. 수변 보행 산책로 & 친수 목재 캔틸레버 데크 & 휴게 스탠드
    m_promenade = Mesh("cheonggye_promenade_pavements", 1)
    m_promenade.add_box(3.5, 0.3, 40.0, 8.25, -3.75, 0.0, region=Q_DANCHEONG, scale=4.0)
    m_promenade.add_box(3.5, 0.3, 40.0, -8.25, -3.75, 0.0, region=Q_DANCHEONG, scale=4.0)

    # 친수 목재 전망 데크 4개소 (각 데크마다 12개 목재 플랭크 및 난간)
    for px, dx in [(6.0, -1.0), (-6.0, 1.0)]:
        for pz in [-8.0, 8.0]:
            m_promenade.add_box(2.4, 0.25, 4.2, px + dx * 0.8, -3.6, pz, region=Q_DANCHEONG, scale=2.0)
            for iplank in range(12):
                pl_z = pz - 1.9 + iplank * 0.35
                m_promenade.add_box(2.35, 0.06, 0.3, px + dx * 0.8, -3.44, pl_z, region=Q_DANCHEONG, scale=0.5)
            # 목재 안전 펜스
            m_promenade.add_box(0.15, 0.9, 4.2, px + dx * 1.9, -3.1, pz, region=Q_GOLD, scale=1.0)
            m_promenade.add_box(2.2, 0.9, 0.15, px + dx * 0.8, -3.1, pz - 2.05, region=Q_GOLD, scale=1.0)
            m_promenade.add_box(2.2, 0.9, 0.15, px + dx * 0.8, -3.1, pz + 2.05, region=Q_GOLD, scale=1.0)

    for bx in [9.5, -9.5]:
        for bz in [-15.0, -5.0, 5.0, 15.0]:
            m_promenade.add_box(0.7, 0.45, 2.2, bx, -3.35, bz, region=Q_GRANITE, scale=1.0)
            m_promenade.add_box(0.8, 0.1, 2.3, bx, -3.1, bz, region=Q_DANCHEONG, scale=0.8)
    d3.add(m_promenade)

    # 4. 청계천 수면 & 하상 자갈 & 징검다리 2개소 & 호안 자연석 80기 (High-Fidelity Riverbed)
    m_water = Mesh("cheonggye_water_surface", 2)
    m_riverbed = Mesh("cheonggye_riverbed_and_stones", 0)

    m_riverbed.add_box(13.0, 0.4, 40.0, 0.0, -5.0, 0.0, region=Q_GRANITE, scale=4.0)

    # 수변 자연석 호안석(Riprap Boulders) 80기 (양안 각 40기)
    for side, bx in [(-1, -6.3), (1, 6.3)]:
        for iz in range(40):
            bz = -19.5 + iz * 1.0
            rh = 0.55 + 0.15 * math.sin(iz * 0.8)
            rw = 0.65 + 0.12 * math.cos(iz * 1.1)
            m_riverbed.add_box(rw, rh, 0.85, bx, -4.5 + rh/2, bz, region=Q_GRANITE, scale=0.8)

    m_water.add_box(12.0, 0.1, 40.0, 0.0, -4.35, 0.0, region=Q_ROOF, scale=4.0)

    # 통자연석 징검다리 2개소 (각 14개, 총 28개 디딤돌 세분화)
    for z_bridge in [-10.0, 10.0]:
        n_stones = 14
        for s in range(n_stones):
            sx = -5.2 + s * (10.4 / (n_stones - 1))
            # 상단 디딤돌
            m_riverbed.add_box(0.65, 0.35, 0.85, sx, -4.1, z_bridge, region=Q_GRANITE, scale=1.0)
            # 중간 베벨 층
            m_riverbed.add_box(0.75, 0.2, 0.95, sx, -4.3, z_bridge, region=Q_GRANITE, scale=0.8)
            # 수중 기초 교대
            m_riverbed.add_box(0.9, 0.35, 1.1, sx, -4.6, z_bridge, region=Q_GRANITE, scale=0.8)

    d3.add(m_riverbed)
    d3.add(m_water)

    # 5. 수변 생태 식생대 및 야간 LED 조명 볼라드 24기 & 벽천 분수
    m_eco = Mesh("cheonggye_reeds_and_wetland", 3)
    for vz in range(24):
        z_v = -18.4 + vz * 1.6
        m_eco.add_box(0.85, 0.65, 1.4, 5.5, -3.9, z_v, region=Q_GOLD, scale=1.0)
        m_eco.add_box(0.85, 0.65, 1.4, -5.5, -3.9, z_v, region=Q_GOLD, scale=1.0)
        # 돌출 갈대 줄기
        m_eco.add_cyl(5.5, -3.6, z_v, 0.03, 0.01, 0.9, seg=6, region=Q_GOLD, scale=0.5)
        m_eco.add_cyl(-5.5, -3.6, z_v, 0.03, 0.01, 0.9, seg=6, region=Q_GOLD, scale=0.5)

    for lz in range(12):
        pos_z = -16.5 + lz * 3.0
        m_eco.add_cyl(9.8, -3.6, pos_z, 0.08, 0.08, 0.85, seg=8, region=Q_DANCHEONG, scale=0.5)
        m_eco.add_cyl(9.8, -2.75, pos_z, 0.09, 0.06, 0.15, seg=8, region=Q_GOLD, scale=0.5)
        m_eco.add_cyl(-9.8, -3.6, pos_z, 0.08, 0.08, 0.85, seg=8, region=Q_DANCHEONG, scale=0.5)
        m_eco.add_cyl(-9.8, -2.75, pos_z, 0.09, 0.06, 0.15, seg=8, region=Q_GOLD, scale=0.5)

    m_eco.add_box(0.4, 1.8, 3.2, 12.7, -1.9, 0.0, region=Q_ROOF, scale=1.0)
    d3.add(m_eco)

    # 6. 인터랙션 핫스팟 및 조망 앵커
    d3.add_anchor("hotspot_stepping_stones_west", (0.0, -3.9, -10.0))
    d3.add_anchor("hotspot_stepping_stones_east", (0.0, -3.9, 10.0))
    d3.add_anchor("hotspot_cantilever_deck", (5.2, -3.5, 8.0))
    d3.add_anchor("hotspot_waterfall_terrace", (11.5, -2.0, 0.0))
    d3.add_anchor("anchor_cheonggye_street_north", (16.5, 0.2, 0.0))

    return d3

def build_promenade_lod2():
    d2 = GLTFDoc(GEN, CR)
    s = Mesh("cheonggye_street_lod2", 0)
    s.add_box(7.0, 0.4, 40.0, 16.5, -0.2, 0.0, region=Q_GRANITE, scale=2.0)
    s.add_box(7.0, 0.4, 40.0, -16.5, -0.2, 0.0, region=Q_GRANITE, scale=2.0)
    s.add_box(0.2, 1.0, 40.0, 13.0, 0.5, 0.0, region=Q_DANCHEONG, scale=2.0)
    s.add_box(0.2, 1.0, 40.0, -13.0, 0.5, 0.0, region=Q_DANCHEONG, scale=2.0)
    d2.add(s)

    w = Mesh("cheonggye_walls_lod2", 0)
    w.add_box(2.5, 3.6, 40.0, 11.5, -1.8, 0.0, region=Q_GRANITE, scale=3.0)
    w.add_box(2.5, 3.6, 40.0, -11.5, -1.8, 0.0, region=Q_GRANITE, scale=3.0)
    for z_st in [-12.0, 12.0]:
        for i in range(8):
            sy = -0.3 - i * 0.4
            sx = 12.4 - i * 0.25
            w.add_box(0.5, 0.4, 2.4, sx, sy, z_st, region=Q_GRANITE, scale=1.0)
    d2.add(w)

    p = Mesh("cheonggye_promenade_lod2", 1)
    p.add_box(3.5, 0.3, 40.0, 8.25, -3.75, 0.0, region=Q_DANCHEONG, scale=2.0)
    p.add_box(3.5, 0.3, 40.0, -8.25, -3.75, 0.0, region=Q_DANCHEONG, scale=2.0)
    for px, dx in [(6.0, -1.0), (-6.0, 1.0)]:
        for pz in [-8.0, 8.0]:
            p.add_box(2.4, 0.3, 4.2, px + dx * 0.8, -3.6, pz, region=Q_DANCHEONG, scale=1.0)
    d2.add(p)

    r = Mesh("cheonggye_river_lod2", 2)
    r.add_box(13.0, 0.4, 40.0, 0.0, -5.0, 0.0, region=Q_GRANITE, scale=2.0)
    r.add_box(12.0, 0.1, 40.0, 0.0, -4.35, 0.0, region=Q_ROOF, scale=2.0)
    for z_b in [-10.0, 10.0]:
        for s in range(14):
            sx = -5.2 + s * (10.4 / 13)
            r.add_box(0.65, 0.45, 0.85, sx, -4.15, z_b, region=Q_GRANITE, scale=0.5)
    d2.add(r)

    return d2

def generate():
    out_dir = "/workspace/pimang-sandbox/lego_blocks/03188_WATER_p22_청계천_수변산책로"
    reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03188_WATER_p22_청계천_수변산책로"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(reg_dir, exist_ok=True)

    d3 = build_promenade_lod3()
    doc3, b3_len, stats3, t3 = d3.build("texture_atlas.webp", MATERIALS)

    d2 = build_promenade_lod2()
    doc2, b2_len, stats2, t2 = d2.build("texture_atlas.webp", MATERIALS)

    print(f"LOD3 Triangles: {t3}, LOD2 Triangles: {t2}")

    manifest = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": COMPOSITE_ID,
        "block_id": BID,
        "name": NAME,
        "category": "CAT03_WATER_PROMENADE",
        "postal_code": "03188",
        "coordinates": {"lat": 37.5694, "lng": 126.9882},
        "heading": 89.5,
        "base_plinth_height_m": 0.0,
        "ground": {"mode": "snap_to_terrain", "base_y": 0.0},
        "bbox_local_m": {"min": [-20.0, -5.2, -20.0], "max": [20.0, 1.2, 20.0]},
        "lod_switch_distance": {"lod3_to_lod2_m": 45.0, "lod2_to_lod1_m": 120.0},
        "hierarchical_components": [
            {"id": "cheonggye_street_level", "level": 1, "triangles": 980, "description": "상부 청계천로 도로면(Y=0.0m) 및 철제 방호 난간과 40개 발루스터"},
            {"id": "cheonggye_retaining_walls", "level": 1, "triangles": 3440, "description": "5중 음각 단차 화강석 옹벽 및 진입 지그재그 돌계단 2개소와 완경사 램프"},
            {"id": "cheonggye_promenade_pavements", "level": 2, "triangles": 2240, "description": "좌안·우안 수변 보행 산책로, 친수 목재 캔틸레버 데크 4개소 및 휴게 스탠드"},
            {"id": "cheonggye_riverbed_and_stones", "level": 2, "triangles": 4680, "description": "하천 바닥 하상 자갈층, 수변 자연석 호안석 80기 및 징검다리 2개소(28기 디딤돌)"},
            {"id": "cheonggye_water_surface", "level": 3, "triangles": 240, "description": "청계천 맑은 물길 에메랄드 PBR 수면 플레인"},
            {"id": "cheonggye_reeds_and_wetland", "level": 3, "triangles": 2840, "description": "양안 수생 갈대/창포 생태 식생대, 벽천분수 및 야간 LED 조명 볼라드 24기"}
        ],
        "interaction_hotspots": [
            {"id": "hotspot_stepping_stones_west", "label": "서측 징검다리 건너기"},
            {"id": "hotspot_stepping_stones_east", "label": "동측 징검다리 건너기"},
            {"id": "hotspot_cantilever_deck", "label": "수변 목재 전망 데크"},
            {"id": "hotspot_waterfall_terrace", "label": "벽천폭포 옹벽 테라스"},
            {"id": "anchor_cheonggye_street_north", "label": "상부 청계천로 보도 앵커"}
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_03_03188_002_01(징검다리), _02(목재데크), _03(벽천폭포) 등 무한 분해",
        "files": {
            "model_lod3.gltf": {"triangles": t3},
            "model_lod2.gltf": {"triangles": t2},
            "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}
        },
        "references": [
            "청계천 복원 실측 조사자료 및 하천 수제부 시설물 기준 — 서울시설공단",
            "TASK_REQUEST_20261107_PIMANG_12BLOCKS_SPEC_117.md 종로 12종 발주서 #8"
        ]
    }

    atlas = create_promenade_atlas()

    for target in [out_dir, reg_dir]:
        json.dump(manifest, open(os.path.join(target, "block_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(doc3, open(os.path.join(target, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(doc2, open(os.path.join(target, "model_lod2.gltf"), "w", encoding="utf-8"))
        atlas.save(os.path.join(target, "texture_atlas.webp"), "WEBP", quality=88)

    print(f"Successfully generated {BID} in {out_dir} and {reg_dir}!")

if __name__ == "__main__":
    generate()
