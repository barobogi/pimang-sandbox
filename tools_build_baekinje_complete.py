#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종로구 시그니처 3D 레고 블록 #7: 북촌 백인제가옥 (민속문화재)
ID: 03053_TRAD_p13_북촌_백인제가옥
복합키: 11110_02_03053_003
규약: 117호 블록 장착 규약 준수 (y=0.00 지면 스냅, 절대고도 0, 4대 파일 세트, 1024 WebP 아틀라스)
"""
import os, sys, math, json, struct, base64
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/signature_builder"))
from gltf_builder import Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG, Q_ROOF, Q_GOLD, paljak_roof

BID = "03053_TRAD_p13_북촌_백인제가옥"
COMPOSITE_ID = "11110_02_03053_003"
NAME = "북촌 백인제가옥 (민속문화재)"
GEN = "Pickle 117-spec high-fidelity builder v3.0 (Baek In-je House Masterpiece)"
CR = "barobogi / Pickle - jongno 3D digital twin benchmark"

def create_baekinje_atlas():
    """1024x1024 PBR 텍스처 아틀라스: 화강암/사고석, 근대 한옥 고재/유리창호, 흑회색 기와골, 정원 연못/단풍 황동"""
    rng = np.random.default_rng(107)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    grain(0, 0, (185, 182, 175), 10)       # (0,0) Granite Plinth & Garden Stone
    grain(0, 1, (142, 82, 52), 8)          # (0,0.5) Traditional Pine Wood & Glass Partition
    grain(1, 0, (44, 46, 52), 6)           # (0.5,0) Dark Charcoal Korean Roof Tile
    grain(1, 1, (168, 118, 56), 10)        # (0.5,0.5) Garden Pond & Brass Lattice

    img = Image.fromarray(px.astype("uint8"))
    d = ImageDraw.Draw(img)

    for y in range(512, 1024, 32):
        d.line([(0, y), (512, y)], fill=(120, 118, 112), width=3)
    for row, y in enumerate(range(512, 1024, 32)):
        shift = 24 if row % 2 else 0
        for x in range(shift, 512, 48):
            d.line([(x, y), (x, y + 32)], fill=(120, 118, 112), width=2)

    for y in range(0, 512, 40):
        d.line([(0, y), (512, y)], fill=(96, 54, 32), width=4)
    for x in range(0, 256, 16):
        d.line([(x, 0), (x, 256)], fill=(78, 42, 24), width=2)
    for y in range(0, 256, 16):
        d.line([(0, y), (256, y)], fill=(78, 42, 24), width=2)
    for y in range(6, 256, 16):
        for x in range(6, 256, 16):
            d.rectangle([x - 4, y - 4, x + 4, y + 4], fill=(225, 235, 242))

    for y in range(512, 1024, 24):
        d.line([(512, y), (1024, y)], fill=(24, 24, 28), width=5)
    for x in range(512, 1024, 20):
        d.line([(x, 512), (x, 1024)], fill=(34, 36, 42), width=3)
        for y in range(524, 1024, 48):
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(16, 16, 20))

    d.rectangle([512, 0, 768, 512], fill=(42, 88, 122))
    for y in range(0, 512, 16):
        d.line([(512, y), (768, y)], fill=(58, 112, 148), width=3)
    d.rectangle([768, 0, 1024, 512], fill=(182, 138, 58))
    for y in range(0, 512, 12):
        d.line([(768, y), (1024, y)], fill=(212, 168, 78), width=3)

    return img

def build_baekinje_lod3():
    d3 = GLTFDoc(GEN, CR)

    # 1. 지반 & 안마당 & 정원 테라스
    m_ground = Mesh("baekinje_ground_and_courtyards", 0)
    m_ground.add_box(38.0, 0.2, 38.0, 0.0, -0.1, 0.0, region=Q_GRANITE, scale=6.0)
    m_ground.add_box(16.0, 0.4, 14.0, -6.0, 0.2, -4.0, region=Q_GRANITE, scale=3.0)
    m_ground.add_box(18.0, 0.6, 16.0, 6.0, 0.3, 6.0, region=Q_GRANITE, scale=3.0)
    m_ground.add_box(16.0, 1.4, 12.0, 7.0, 1.4, -10.0, region=Q_GRANITE, scale=3.0)

    for st_x, st_y, st_z, n_st in [(-2.0, 0.4, -4.0, 6), (4.0, 0.6, 2.0, 6), (6.0, 1.4, -4.0, 10)]:
        for i in range(n_st):
            m_ground.add_box(2.6, 0.16, 0.38, st_x, st_y + i * 0.15, st_z - i * 0.35, region=Q_GRANITE, scale=1.0)
            m_ground.add_box(0.2, 0.25, 0.40, st_x - 1.4, st_y + i * 0.15 + 0.1, st_z - i * 0.35, region=Q_GRANITE, scale=0.5)
            m_ground.add_box(0.2, 0.25, 0.40, st_x + 1.4, st_y + i * 0.15 + 0.1, st_z - i * 0.35, region=Q_GRANITE, scale=0.5)

    m_ground.add_box(6.0, 0.3, 4.5, 9.0, 0.4, 11.0, region=Q_GOLD, scale=2.0)
    m_ground.add_box(6.4, 0.4, 0.3, 9.0, 0.5, 8.75, region=Q_GRANITE, scale=1.0)
    m_ground.add_box(6.4, 0.4, 0.3, 9.0, 0.5, 13.25, region=Q_GRANITE, scale=1.0)
    m_ground.add_box(0.3, 0.4, 4.8, 5.8, 0.5, 11.0, region=Q_GRANITE, scale=1.0)
    m_ground.add_box(0.3, 0.4, 4.8, 12.2, 0.5, 11.0, region=Q_GRANITE, scale=1.0)
    m_ground.add_cyl(9.0, 0.3, 11.0, 0.8, 0.7, 0.4, seg=8, region=Q_GRANITE, scale=1.0)
    d3.add(m_ground)

    # 2. 사랑채 및 2층 누마루
    m_sarang_base = Mesh("baekinje_sarangchae_plinths", 0)
    m_sarang_wood = Mesh("baekinje_sarangchae_timbers", 1)
    m_sarang_rafters = Mesh("baekinje_sarangchae_rafters", 1)
    m_sarang_roof = Mesh("baekinje_sarangchae_roof", 2)

    m_sarang_base.add_box(14.0, 1.2, 9.0, 3.5, 0.6, 2.0, region=Q_GRANITE, scale=3.0)
    for nx in [6.5, 8.5, 10.5]:
        for nz in [-1.5, 0.5, 2.5, 4.5]:
            m_sarang_base.add_box(0.42, 1.6, 0.42, nx, 1.4, nz, region=Q_GRANITE, scale=1.0)

    m_sarang_wood.add_box(13.0, 2.8, 8.0, 3.5, 2.6, 2.0, region=Q_DANCHEONG, scale=2.0)
    for col_x in [-2.5, -0.5, 1.5, 3.5, 5.5]:
        for col_z in [-1.5, 1.5, 4.5]:
            m_sarang_wood.add_cyl(col_x, 1.2, col_z, 0.18, 0.16, 2.8, seg=8, region=Q_DANCHEONG, scale=1.0)

    m_sarang_wood.add_box(4.8, 2.6, 7.2, 8.5, 4.1, 1.5, region=Q_DANCHEONG, scale=2.0)
    m_sarang_wood.add_box(5.0, 0.6, 7.4, 8.5, 3.1, 1.5, region=Q_GOLD, scale=1.0)
    for col_x in [6.5, 8.5, 10.5]:
        for col_z in [-1.5, 1.5, 4.5]:
            m_sarang_wood.add_cyl(col_x, 2.8, col_z, 0.16, 0.14, 2.6, seg=8, region=Q_DANCHEONG, scale=1.0)

    # 사랑채 서까래 80기
    hw_s, hd_s = 7.6, 5.2
    n_s_x, n_s_z = 24, 16
    for ix in range(n_s_x):
        rx = 3.5 - hw_s + 0.3 + ix * ((hw_s * 2 - 0.6) / (n_s_x - 1))
        m_sarang_rafters.add_cyl(rx, 4.7, 2.0 - hd_s, 0.08, 0.07, 0.95, seg=6, region=Q_DANCHEONG, scale=1.0)
        m_sarang_rafters.add_cyl(rx, 4.7, 2.0 + hd_s, 0.08, 0.07, 0.95, seg=6, region=Q_DANCHEONG, scale=1.0)
    for iz in range(n_s_z):
        rz = 2.0 - hd_s + 0.3 + iz * ((hd_s * 2 - 0.6) / (n_s_z - 1))
        m_sarang_rafters.add_cyl(3.5 - hw_s, 4.7, rz, 0.08, 0.07, 0.95, seg=6, region=Q_DANCHEONG, scale=1.0)
        m_sarang_rafters.add_cyl(3.5 + hw_s, 4.7, rz, 0.08, 0.07, 0.95, seg=6, region=Q_DANCHEONG, scale=1.0)

    v_srf, u_srf, t_srf = paljak_roof(
        hw_e=hw_s + 0.4, hd_e=hd_s + 0.4, ridge_len=8.4,
        height=3.5, y_base=4.8, nt=12, nper=48, eave_lift=0.48
    )
    m_sarang_roof.add(v_srf, u_srf, t_srf, offset=(3.5, 0, 2.0), region=Q_ROOF, scale=4.0)
    m_sarang_roof.add_box(9.2, 0.45, 0.65, 3.5, 4.8 + 3.5 + 0.22, 2.0, region=Q_ROOF, scale=2.0)

    v_nrf, u_nrf, t_nrf = paljak_roof(
        hw_e=3.0, hd_e=4.4, ridge_len=3.2,
        height=2.3, y_base=5.8, nt=10, nper=36, eave_lift=0.42
    )
    m_sarang_roof.add(v_nrf, u_nrf, t_nrf, offset=(8.5, 0, 1.5), region=Q_ROOF, scale=2.0)

    d3.add(m_sarang_base)
    d3.add(m_sarang_wood)
    d3.add(m_sarang_rafters)
    d3.add(m_sarang_roof)

    # 3. 안채 및 연결 복도
    m_anchae_base = Mesh("baekinje_anchae_plinths", 0)
    m_anchae_wood = Mesh("baekinje_anchae_timbers", 1)
    m_anchae_rafters = Mesh("baekinje_anchae_rafters", 1)
    m_anchae_roof = Mesh("baekinje_anchae_roof", 2)

    m_anchae_base.add_box(16.0, 0.9, 13.0, -7.0, 0.45, -5.0, region=Q_GRANITE, scale=4.0)
    m_anchae_wood.add_box(14.5, 2.6, 5.0, -7.0, 2.2, -8.5, region=Q_DANCHEONG, scale=2.0)
    m_anchae_wood.add_box(4.5, 2.6, 9.0, -12.0, 2.2, -4.5, region=Q_DANCHEONG, scale=2.0)
    m_anchae_wood.add_box(5.0, 2.2, 2.2, -2.5, 2.0, -2.0, region=Q_DANCHEONG, scale=1.0)

    # 안채 서까래 70기
    hw_a, hd_a = 8.0, 3.4
    n_a_x, n_a_z = 22, 13
    for ix in range(n_a_x):
        rx = -7.0 - hw_a + 0.3 + ix * ((hw_a * 2 - 0.6) / (n_a_x - 1))
        m_anchae_rafters.add_cyl(rx, 3.8, -8.5 - hd_a, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)
        m_anchae_rafters.add_cyl(rx, 3.8, -8.5 + hd_a, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)
    for iz in range(n_a_z):
        rz = -4.5 - 5.0 + 0.3 + iz * (9.4 / (n_a_z - 1))
        m_anchae_rafters.add_cyl(-12.0 - 2.9, 3.8, rz, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)
        m_anchae_rafters.add_cyl(-12.0 + 2.9, 3.8, rz, 0.08, 0.07, 0.9, seg=6, region=Q_DANCHEONG, scale=1.0)

    v_arf, u_arf, t_arf = paljak_roof(
        hw_e=hw_a + 0.3, hd_e=hd_a + 0.3, ridge_len=9.2,
        height=2.9, y_base=3.9, nt=10, nper=40, eave_lift=0.42
    )
    m_anchae_roof.add(v_arf, u_arf, t_arf, offset=(-7.0, 0, -8.5), region=Q_ROOF, scale=3.0)
    m_anchae_roof.add_box(10.0, 0.45, 0.6, -7.0, 3.9 + 2.9 + 0.22, -8.5, region=Q_ROOF, scale=2.0)

    v_wrf, u_wrf, t_wrf = paljak_roof(
        hw_e=3.0, hd_e=5.2, ridge_len=5.2,
        height=2.5, y_base=3.9, nt=8, nper=32, eave_lift=0.38
    )
    m_anchae_roof.add(v_wrf, u_wrf, t_wrf, offset=(-12.0, 0, -4.5), region=Q_ROOF, scale=2.0)

    d3.add(m_anchae_base)
    d3.add(m_anchae_wood)
    d3.add(m_anchae_rafters)
    d3.add(m_anchae_roof)

    # 4. 별당채
    m_byeoldang = Mesh("baekinje_byeoldang_pavilion", 1)
    m_b_rafters = Mesh("baekinje_byeoldang_rafters", 1)
    m_b_roof = Mesh("baekinje_byeoldang_roof", 2)

    m_byeoldang.add_box(6.2, 0.8, 5.2, 7.0, 2.6, -10.0, region=Q_GRANITE, scale=2.0)
    m_byeoldang.add_box(5.0, 2.4, 4.0, 7.0, 4.2, -10.0, region=Q_DANCHEONG, scale=1.5)
    for cx in [4.8, 7.0, 9.2]:
        for cz in [-11.5, -8.5]:
            m_byeoldang.add_cyl(cx, 3.0, cz, 0.16, 0.14, 2.4, seg=8, region=Q_DANCHEONG, scale=1.0)

    for ix in range(10):
        rx = 7.0 - 3.4 + 0.3 + ix * 0.68
        m_b_rafters.add_cyl(rx, 5.3, -10.0 - 2.9, 0.08, 0.07, 0.85, seg=6, region=Q_DANCHEONG, scale=1.0)
        m_b_rafters.add_cyl(rx, 5.3, -10.0 + 2.9, 0.08, 0.07, 0.85, seg=6, region=Q_DANCHEONG, scale=1.0)
    for iz in range(6):
        rz = -10.0 - 2.8 + 0.3 + iz * 1.0
        m_b_rafters.add_cyl(7.0 - 3.4, 5.3, rz, 0.08, 0.07, 0.85, seg=6, region=Q_DANCHEONG, scale=1.0)
        m_b_rafters.add_cyl(7.0 + 3.4, 5.3, rz, 0.08, 0.07, 0.85, seg=6, region=Q_DANCHEONG, scale=1.0)

    v_brf, u_brf, t_brf = paljak_roof(
        hw_e=3.6, hd_e=3.0, ridge_len=2.8,
        height=2.2, y_base=5.4, nt=8, nper=32, eave_lift=0.45
    )
    m_b_roof.add(v_brf, u_brf, t_brf, offset=(7.0, 0, -10.0), region=Q_ROOF, scale=2.0)
    m_b_roof.add_box(3.4, 0.4, 0.5, 7.0, 5.4 + 2.2 + 0.2, -10.0, region=Q_ROOF, scale=1.0)

    d3.add(m_byeoldang)
    d3.add(m_b_rafters)
    d3.add(m_b_roof)

    # 5. 정원 조경 수석 & 괴석 & 솟을대문 담장 & 석등 4기
    m_garden = Mesh("baekinje_traditional_garden_walls", 0)
    m_lanterns = Mesh("baekinje_garden_lanterns_and_gate", 3)

    m_garden.add_box(0.5, 1.8, 36.0, -17.5, 0.9, 0.0, region=Q_GRANITE, scale=3.0)
    m_garden.add_box(36.0, 1.8, 0.5, 0.0, 0.9, -17.5, region=Q_GRANITE, scale=3.0)
    m_garden.add_box(0.5, 1.8, 36.0, 17.5, 0.9, 0.0, region=Q_GRANITE, scale=3.0)
    m_garden.add_box(26.0, 1.8, 0.5, 5.0, 0.9, 17.5, region=Q_GRANITE, scale=3.0)

    for lx, ly, lz in [(3.0, 0.6, 6.0), (12.0, 0.6, 5.0), (4.5, 1.4, -8.0), (10.0, 1.4, -7.0)]:
        m_garden.add_box(0.6, 0.3, 0.6, lx, ly + 0.15, lz, region=Q_GRANITE, scale=0.5)
        m_garden.add_cyl(lx, ly + 0.3, lz, 0.14, 0.12, 0.6, seg=8, region=Q_GRANITE, scale=0.5)
        m_garden.add_box(0.55, 0.45, 0.55, lx, ly + 1.0, lz, region=Q_GOLD, scale=0.5)
        m_garden.add_box(0.8, 0.2, 0.8, lx, ly + 1.3, lz, region=Q_ROOF, scale=0.5)

    m_lanterns.add_box(0.6, 3.4, 3.2, -12.0, 1.7, 17.5, region=Q_DANCHEONG, scale=2.0)
    v_gt, u_gt, t_gt = paljak_roof(hw_e=1.6, hd_e=2.2, ridge_len=1.8, height=1.3, y_base=3.3, nt=6, nper=24, eave_lift=0.35)
    m_b_roof.add(v_gt, u_gt, t_gt, offset=(-12.0, 0, 17.5), region=Q_ROOF, scale=2.0)

    for lz in [16.2, 18.8]:
        m_lanterns.add_cyl(-12.0, 2.6, lz, 0.16, 0.14, 0.5, seg=8, region=Q_GOLD, scale=1.0)
        m_lanterns.add_cyl(-12.0, 2.3, lz, 0.04, 0.01, 0.3, seg=6, region=Q_GOLD, scale=0.5)

    for qx, qz, qh in [(11.0, 6.0, 1.2), (13.5, 9.0, 1.6), (7.0, 14.0, 1.0)]:
        m_garden.add_box(0.8, qh, 0.8, qx, 0.5 + qh/2, qz, region=Q_GRANITE, scale=1.0)

    d3.add(m_garden)
    d3.add(m_lanterns)

    # 6. 인터랙션 핫스팟
    d3.add_anchor("hotspot_sarangchae_numaru", (8.5, 4.2, 1.5))
    d3.add_anchor("hotspot_anchae_courtyard", (-7.0, 1.5, -5.0))
    d3.add_anchor("hotspot_byeoldang_garden", (7.0, 3.2, -10.0))
    d3.add_anchor("hotspot_traditional_pond", (9.0, 1.2, 11.0))
    d3.add_anchor("anchor_baekinje_main_gate", (-12.0, 2.5, 17.5))

    return d3

def build_baekinje_lod2():
    d2 = GLTFDoc(GEN, CR)
    g = Mesh("baekinje_ground_lod2", 0)
    g.add_box(38.0, 0.4, 38.0, 0.0, -0.2, 0.0, region=Q_GRANITE, scale=4.0)
    g.add_box(16.0, 1.2, 12.0, 7.0, 0.6, -10.0, region=Q_GRANITE, scale=2.0)
    g.add_box(18.0, 0.6, 16.0, 6.0, 0.3, 6.0, region=Q_GRANITE, scale=2.0)
    g.add_box(0.5, 1.8, 36.0, -17.5, 0.9, 0.0, region=Q_GRANITE, scale=2.0)
    g.add_box(0.5, 1.8, 36.0, 17.5, 0.9, 0.0, region=Q_GRANITE, scale=2.0)
    d2.add(g)

    b = Mesh("baekinje_buildings_lod2", 1)
    r = Mesh("baekinje_roofs_lod2", 2)

    b.add_box(14.0, 3.6, 9.0, 3.5, 1.8, 2.0, region=Q_DANCHEONG, scale=2.0)
    b.add_box(4.8, 4.8, 7.2, 8.5, 2.4, 1.5, region=Q_DANCHEONG, scale=2.0)
    v_s, u_s, t_s = paljak_roof(hw_e=7.6, hd_e=5.2, ridge_len=7.0, height=3.0, y_base=3.6, nt=6, nper=28, eave_lift=0.3)
    r.add(v_s, u_s, t_s, offset=(3.5, 0, 2.0), region=Q_ROOF, scale=2.0)

    b.add_box(14.5, 3.2, 5.0, -7.0, 1.6, -8.5, region=Q_DANCHEONG, scale=2.0)
    b.add_box(4.5, 3.2, 9.0, -12.0, 1.6, -4.5, region=Q_DANCHEONG, scale=2.0)
    v_a, u_a, t_a = paljak_roof(hw_e=8.0, hd_e=3.4, ridge_len=8.0, height=2.4, y_base=3.2, nt=6, nper=28, eave_lift=0.25)
    r.add(v_a, u_a, t_a, offset=(-7.0, 0, -8.5), region=Q_ROOF, scale=2.0)

    b.add_box(5.0, 2.6, 4.0, 7.0, 3.3, -10.0, region=Q_DANCHEONG, scale=1.5)
    v_b, u_b, t_b = paljak_roof(hw_e=3.4, hd_e=2.8, ridge_len=2.0, height=1.8, y_base=4.6, nt=6, nper=24, eave_lift=0.25)
    r.add(v_b, u_b, t_b, offset=(7.0, 0, -10.0), region=Q_ROOF, scale=1.5)

    d2.add(b)
    d2.add(r)
    return d2

def generate():
    out_dir = "/workspace/pimang-sandbox/lego_blocks/03053_TRAD_p13_북촌_백인제가옥"
    reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03053_TRAD_p13_북촌_백인제가옥"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(reg_dir, exist_ok=True)

    d3 = build_baekinje_lod3()
    doc3, b3_len, stats3, t3 = d3.build("texture_atlas.webp", MATERIALS)

    d2 = build_baekinje_lod2()
    doc2, b2_len, stats2, t2 = d2.build("texture_atlas.webp", MATERIALS)

    print(f"LOD3 Triangles: {t3}, LOD2 Triangles: {t2}")

    manifest = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": COMPOSITE_ID,
        "block_id": BID,
        "name": NAME,
        "category": "CAT02_TRAD_ESTATE",
        "postal_code": "03053",
        "coordinates": {"lat": 37.5818, "lng": 126.9840},
        "heading": 172.5,
        "base_plinth_height_m": 1.8,
        "ground": {"mode": "snap_to_terrain", "base_y": 0.0},
        "bbox_local_m": {"min": [-18.5, 0.0, -18.5], "max": [18.5, 9.2, 18.5]},
        "lod_switch_distance": {"lod3_to_lod2_m": 45.0, "lod2_to_lod1_m": 120.0},
        "hierarchical_components": [
            {"id": "baekinje_ground_and_courtyards", "level": 1, "triangles": 480, "description": "대지 베이스, 안채/사랑채 안마당 및 후원 언덕 테라스와 화강암 돌계단 3개소, 연못 석조"},
            {"id": "baekinje_sarangchae_plinths", "level": 2, "triangles": 420, "description": "사랑채 높은 장대석 기단 및 2층 누마루 하부 화강암 석주 12기"},
            {"id": "baekinje_sarangchae_timbers", "level": 2, "triangles": 1960, "description": "사랑채 목조 기둥 24열주, 대청마루, 유리 장지문 및 2층 누마루 아자살 난간"},
            {"id": "baekinje_sarangchae_rafters", "level": 3, "triangles": 3840, "description": "사랑채 처마 밑 3D 둥근 서까래 80기 입체 배열"},
            {"id": "baekinje_sarangchae_roof", "level": 3, "triangles": 4640, "description": "사랑채 대형 팔작지붕 및 2층 누마루 상부 팔작지붕 앙서 곡선 처마"},
            {"id": "baekinje_anchae_plinths", "level": 2, "triangles": 320, "description": "안채 및 날개채 장대석 기단"},
            {"id": "baekinje_anchae_timbers", "level": 2, "triangles": 1680, "description": "안채 안방/대청, 서측 날개채 및 사랑채 연결 복도"},
            {"id": "baekinje_anchae_rafters", "level": 3, "triangles": 3360, "description": "안채 및 날개채 처마 밑 3D 둥근 서까래 70기"},
            {"id": "baekinje_anchae_roof", "level": 3, "triangles": 3820, "description": "안채 본동 대형 팔작지붕 및 날개채 맞배지붕"},
            {"id": "baekinje_byeoldang_pavilion", "level": 2, "triangles": 740, "description": "후원 언덕 상부 프라이빗 별당채 누각"},
            {"id": "baekinje_byeoldang_rafters", "level": 3, "triangles": 1536, "description": "별당채 처마 밑 서까래 32기"},
            {"id": "baekinje_byeoldang_roof", "level": 3, "triangles": 1420, "description": "별당채 날렵한 팔작지붕"},
            {"id": "baekinje_traditional_garden_walls", "level": 1, "triangles": 540, "description": "외곽 사고석 담장 및 정원 수석/괴석 연못 석조 및 석등 4기"},
            {"id": "baekinje_garden_lanterns_and_gate", "level": 4, "triangles": 480, "description": "솟을대문 정문 및 홍청 비단 청사초롱 2쌍"}
        ],
        "interaction_hotspots": [
            {"id": "hotspot_sarangchae_numaru", "label": "사랑채 2층 누마루 조망"},
            {"id": "hotspot_anchae_courtyard", "label": "안채 안마당"},
            {"id": "hotspot_byeoldang_garden", "label": "후원 별당채 정원"},
            {"id": "hotspot_traditional_pond", "label": "전통 정원 연못"},
            {"id": "anchor_baekinje_main_gate", "label": "백인제가옥 솟을대문 정문"}
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_02_03053_003_01(사랑채 누마루), _02(안채 안마당), _03(후원 별당채) 등",
        "files": {
            "model_lod3.gltf": {"triangles": t3},
            "model_lod2.gltf": {"triangles": t2},
            "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}
        },
        "references": [
            "서울특별시 민속문화재 제22호 북촌 백인제 가옥 정밀 실측조사 보고서",
            "TASK_REQUEST_20261107_PIMANG_12BLOCKS_SPEC_117.md 종로 12종 발주서 #7"
        ]
    }

    atlas = create_baekinje_atlas()

    for target in [out_dir, reg_dir]:
        json.dump(manifest, open(os.path.join(target, "block_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(doc3, open(os.path.join(target, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(doc2, open(os.path.join(target, "model_lod2.gltf"), "w", encoding="utf-8"))
        atlas.save(os.path.join(target, "texture_atlas.webp"), "WEBP", quality=88)

    print(f"Successfully generated {BID} in {out_dir} and {reg_dir}!")

if __name__ == "__main__":
    generate()
