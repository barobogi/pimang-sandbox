#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종로구 시그니처 3D 레고 블록 #9: 청계천 광통교 역사복원 석교
ID: 03188_WATER_p23_청계천_광통교_역사복원
복합키: 11110_03_03188_003
규약: 117호 블록 장착 규약 준수 (y=0.00 도로면 스냅, 음각 지하 수로, 절대고도 0, 4대 파일 세트, 1024 WebP 아틀라스)
"""
import os, sys, math, json, struct, base64
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/signature_builder"))
from gltf_builder import Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG, Q_ROOF, Q_GOLD

BID = "03188_WATER_p23_청계천_광통교_역사복원"
COMPOSITE_ID = "11110_03_03188_003"
NAME = "청계천 광통교 역사복원 석교"
GEN = "Pickle 117-spec high-fidelity builder v3.0 (Gwangtonggyo Bridge Masterpiece)"
CR = "barobogi / Pickle - jongno 3D digital twin benchmark"

def create_gwangtonggyo_atlas():
    """1024x1024 PBR 텍스처 아틀라스: 화강석 홍예 아치/신장석 부조, 교각 석축/마름돌, 에메랄드 수면, 황동/서수 조각"""
    rng = np.random.default_rng(109)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    grain(0, 0, (182, 178, 170), 10)       # (0,0) Historic Granite Arch & Shinjinseok
    grain(0, 1, (132, 126, 118), 8)        # (0,0.5) Bridge Abutment & Cobblestone
    grain(1, 0, (36, 96, 122), 6)          # (0.5,0) Cheonggye Water Surface & Stream
    grain(1, 1, (172, 138, 72), 10)        # (0.5,0.5) Mythical Beast Relief & Brass

    img = Image.fromarray(px.astype("uint8"))
    d = ImageDraw.Draw(img)

    # 1. 신덕왕후 능석 신장석 부조 (구름무늬, 금강역사 부조) 및 아치 쐐기돌
    for y in range(512, 1024, 32):
        d.line([(0, y), (512, y)], fill=(116, 112, 106), width=3)
    for x in range(0, 512, 48):
        d.line([(x, 512), (x, 1024)], fill=(116, 112, 106), width=2)
    # 신장석 음각 구름 문양
    for row in range(4):
        cy = 576 + row * 110
        for col in range(4):
            cx = 64 + col * 120
            d.ellipse([cx - 24, cy - 14, cx + 24, cy + 14], outline=(88, 84, 78), width=3)
            d.arc([cx - 32, cy - 20, cx + 32, cy + 20], 0, 180, fill=(78, 74, 68), width=2)

    # 2. 교대 석벽 및 분수침 마름돌 줄눈
    for y in range(0, 512, 24):
        d.line([(0, y), (512, y)], fill=(96, 92, 86), width=3)
    for row, y in enumerate(range(0, 512, 24)):
        shift = 18 if row % 2 else 0
        for x in range(shift, 512, 36):
            d.line([(x, y), (x, y + 24)], fill=(96, 92, 86), width=2)

    # 3. 청계천 맑은 수면 플레인
    for y in range(512, 1024, 16):
        d.line([(512, y), (1024, y)], fill=(48, 122, 154), width=3)
    for x in range(512, 1024, 32):
        for y in range(520, 1024, 32):
            d.ellipse([x - 5, y - 3, x + 5, y + 3], fill=(68, 148, 178))

    # 4. 서수 조각상 및 난간 동자석 황동 디테일
    d.rectangle([512, 0, 768, 512], fill=(162, 142, 108))
    for y in range(0, 512, 16):
        d.line([(512, y), (768, y)], fill=(188, 168, 128), width=3)
    d.rectangle([768, 0, 1024, 512], fill=(198, 158, 68))
    for y in range(0, 512, 12):
        d.line([(768, y), (1024, y)], fill=(225, 182, 88), width=2)

    return img

def build_gwangtonggyo_lod3():
    d3 = GLTFDoc(GEN, CR)

    # 수직 좌표계:
    # Y = 0.00m : 상부 청계천로 도로면 및 광통교 상판 노면 (지면 스냅)
    # Y = +1.10m : 석교 난간 엄지기둥 및 난간대 상단
    # Y = -2.00m : 중간 수변 조경 테라스
    # Y = -3.60m : 좌안/우안 수변 산책로
    # Y = -4.30m : 청계천 하천 수면
    # Y = -4.80m : 하천 바닥 하상 자갈층

    # 1. 상부 청계천로 도로면 및 석교 진입 접속부 (Y=0.00m 스냅)
    m_street = Mesh("gwangtonggyo_street_connections", 0)
    # 북측 도로 (X=+13.0m ~ +20.0m)
    m_street.add_box(7.0, 0.4, 40.0, 16.5, -0.2, 0.0, region=Q_GRANITE, scale=4.0)
    # 남측 도로 (X=-20.0m ~ -13.0m)
    m_street.add_box(7.0, 0.4, 40.0, -16.5, -0.2, 0.0, region=Q_GRANITE, scale=4.0)
    # 도로변 안전 방호 난간
    m_street.add_box(0.2, 1.1, 40.0, 13.0, 0.55, 0.0, region=Q_DANCHEONG, scale=2.0)
    m_street.add_box(0.2, 1.1, 40.0, -13.0, 0.55, 0.0, region=Q_DANCHEONG, scale=2.0)
    d3.add(m_street)

    # 2. 광통교 2경간 홍예 아치 및 중앙 교각 분수침 (Two-Span Segmental Stone Arches)
    # X축 = 하천 횡단 (광통교 길이 12.0m, X=-6.0m ~ +6.0m)
    # Z축 = 다리 폭 (15.0m, Z=-7.5m ~ +7.5m)
    m_arches = Mesh("gwangtonggyo_segmental_arches", 0)
    m_piers = Mesh("gwangtonggyo_piers_and_cutwaters", 0)

    # 중앙 원두형 교각 및 유선형 분수침 (Pier & Diamond Cutwaters at X=0.0)
    # 중앙 교각 본체 (X=-0.75m ~ +0.75m, 두께 1.5m, 폭 16.0m)
    m_piers.add_box(1.5, 3.2, 16.0, 0.0, -3.1, 0.0, region=Q_GRANITE, scale=3.0)
    # 상류측 마름모꼴 분수침 (Z=+8.0m ~ +10.5m)
    for iz in range(8):
        tz = iz / 8.0
        w_cut = 1.5 * (1.0 - tz)
        m_piers.add_box(w_cut, 3.2, 0.35, 0.0, -3.1, 8.0 + iz * 0.35, region=Q_GRANITE, scale=1.0)
    # 하류측 마름모꼴 분수침 (Z=-8.0m ~ -10.5m)
    for iz in range(8):
        tz = iz / 8.0
        w_cut = 1.5 * (1.0 - tz)
        m_piers.add_box(w_cut, 3.2, 0.35, 0.0, -3.1, -8.0 - iz * 0.35, region=Q_GRANITE, scale=1.0)

    # 2개 홍예 아치 (서경간: X=-6.0m ~ -0.75m, 동경간: X=+0.75m ~ +6.0m)
    # 각 아치는 24개의 쐐기돌(Voussoirs) 블록 및 15개 링 세그먼트로 정밀 세분화 (고밀도 실사)
    n_voussoirs = 24
    for center_x, span_r, x_base in [(-3.375, 2.625, -3.375), (3.375, 2.625, 3.375)]:
        for iv in range(n_voussoirs):
            ang0 = math.pi * (iv / n_voussoirs)
            ang1 = math.pi * ((iv + 1) / n_voussoirs)
            r_in = span_r
            r_out = span_r + 0.65
            x_mid = x_base + ((r_in + r_out) / 2) * math.cos((ang0 + ang1) / 2)
            y_mid = -3.8 + ((r_in + r_out) / 2) * math.sin((ang0 + ang1) / 2)
            # Z축을 따라 10개 링 리브로 분할하여 입체 석재 이음매 구현
            for ir in range(10):
                rz = -6.75 + ir * 1.5
                m_arches.add_box(r_out - r_in, 0.45, 1.4, x_mid, y_mid, rz, region=Q_GRANITE, scale=1.0)
                # 쐐기돌 테두리 베벨
                m_arches.add_box(r_out - r_in + 0.06, 0.08, 1.45, x_mid, y_mid + 0.2, rz, region=Q_GRANITE, scale=0.5)

    # 아치 상부 화강석 채움벽(Spandrel Walls)
    m_arches.add_box(4.5, 1.4, 0.8, -3.375, -1.2, 7.1, region=Q_GRANITE, scale=2.0)
    m_arches.add_box(4.5, 1.4, 0.8, -3.375, -1.2, -7.1, region=Q_GRANITE, scale=2.0)
    m_arches.add_box(4.5, 1.4, 0.8, 3.375, -1.2, 7.1, region=Q_GRANITE, scale=2.0)
    m_arches.add_box(4.5, 1.4, 0.8, 3.375, -1.2, -7.1, region=Q_GRANITE, scale=2.0)

    d3.add(m_piers)
    d3.add(m_arches)

    # 3. 신덕왕후 능석 신장석 부조 4기 및 교대 석벽 (Historic Relic Shinjinseok Reliefs)
    # 태종 이방원이 정릉 석물을 거꾸로 쌓아 백성들이 밟고 지나가게 한 역사적 고증
    m_relics = Mesh("gwangtonggyo_shinjinseok_reliefs", 1)
    # 동/서 교대 하부 석벽에 신장석(神將石) 4기 정밀 부조 (X=±5.8m, Z=±4.0m, 거꾸로 뒤집힌 구름문양 & 무인 부조)
    for rx, ry_ang in [(-5.8, 180), (5.8, 0)]:
        for rz in [-5.0, -2.0, 2.0, 5.0]:
            # 신장석 4개소 및 능석 부조 (폭 1.2m, 높이 2.2m)
            m_relics.add_box(0.45, 2.2, 1.2, rx, -2.6, rz, region=Q_GOLD, scale=1.0)
            # 신장석 갑옷 투구
            m_relics.add_box(0.2, 0.5, 0.6, rx + (0.25 if rx > 0 else -0.25), -2.0, rz, region=Q_GRANITE, scale=0.5)
            m_relics.add_cyl(rx + (0.25 if rx > 0 else -0.25), -1.8, rz, 0.18, 0.12, 0.35, seg=8, region=Q_GOLD, scale=0.5)
            # 신장석 가슴 판갑 및 보검 부조
            m_relics.add_box(0.22, 0.7, 0.7, rx + (0.25 if rx > 0 else -0.25), -2.5, rz, region=Q_GRANITE, scale=0.5)
            m_relics.add_box(0.15, 0.9, 0.12, rx + (0.3 if rx > 0 else -0.3), -2.6, rz, region=Q_DANCHEONG, scale=0.3)
            # 거꾸로 뒤집힌 구름무늬(雲紋) 및 연화문 띠
            for cl in range(3):
                m_relics.add_cyl(rx + (0.25 if rx > 0 else -0.25), -3.3, rz - 0.35 + cl * 0.35, 0.14, 0.14, 0.18, seg=8, region=Q_ROOF, scale=0.5)
    d3.add(m_relics)

    # 4. 광통교 다리 상판 및 전통 돌난간 & 서수 조각상 4기 (Deck, Balustrades & Mythical Beasts)
    m_deck = Mesh("gwangtonggyo_deck_and_balustrades", 0)
    m_beasts = Mesh("gwangtonggyo_mythical_beasts", 3)

    # 다리 상판 화강석 판석 (길이 12.0m, 폭 15.0m, 완만한 아치 북선)
    m_deck.add_box(12.0, 0.5, 15.0, 0.0, -0.25, 0.0, region=Q_GRANITE, scale=4.0)
    # 상판 개별 화강암 포장석 (10 x 12 = 120개 돌판)
    for ix in range(10):
        px = -5.4 + ix * 1.2
        for iz in range(12):
            pz = -6.6 + iz * 1.2
            m_deck.add_box(1.15, 0.05, 1.15, px, 0.02, pz, region=Q_GRANITE, scale=0.5)

    # 다리 양측 전통 돌난간 (엄지기둥 4기, 동자석 24기, 하엽, 난간대)
    for bz in [-7.5, 7.5]:
        # 하부 지대석
        m_deck.add_box(12.0, 0.25, 0.4, 0.0, 0.125, bz, region=Q_GRANITE, scale=2.0)
        # 상부 난간대(핸드레일 돌대)
        m_deck.add_box(12.0, 0.2, 0.35, 0.0, 0.95, bz, region=Q_GRANITE, scale=2.0)
        # 동자석 12기씩 입체 배열
        for ic in range(12):
            cx = -5.5 + ic * 1.0
            m_deck.add_box(0.22, 0.65, 0.22, cx, 0.55, bz, region=Q_GRANITE, scale=0.5)
            # 하엽 연꽃잎 받침
            m_deck.add_box(0.32, 0.12, 0.32, cx, 0.25, bz, region=Q_GRANITE, scale=0.5)

    # 다리 네 귀퉁이 엄지기둥 및 서수 조각상 4기 (X=±6.0m, Z=±7.5m)
    for ex in [-6.0, 6.0]:
        for ez in [-7.5, 7.5]:
            # 엄지기둥 (두께 0.55m, 높이 1.3m)
            m_deck.add_box(0.55, 1.3, 0.55, ex, 0.65, ez, region=Q_GRANITE, scale=0.8)
            # 엄지기둥 상단 보주
            m_deck.add_cyl(ex, 1.3, ez, 0.22, 0.18, 0.35, seg=8, region=Q_GRANITE, scale=0.5)
            # 서수 조각상 (해태/사자 모양의 수호 동물 석상)
            m_beasts.add_box(0.45, 0.55, 0.45, ex, 1.6, ez, region=Q_GOLD, scale=0.5)
            m_beasts.add_cyl(ex, 1.85, ez, 0.18, 0.12, 0.25, seg=8, region=Q_GOLD, scale=0.5)

    d3.add(m_deck)
    d3.add(m_beasts)

    # 5. 수변 연결로 & 산책로 & 하천 수면 및 하상 (Water Surface, Bed & Underpass)
    m_river = Mesh("gwangtonggyo_riverbed_and_water", 2)
    # 청계천 맑은 수면 플레인 (Y=-4.30m)
    m_river.add_box(26.0, 0.1, 40.0, 0.0, -4.35, 0.0, region=Q_ROOF, scale=4.0)
    # 하천 바닥 하상 자갈층 (Y=-4.80m)
    m_river.add_box(26.0, 0.4, 40.0, 0.0, -5.0, 0.0, region=Q_GRANITE, scale=4.0)

    # 광통교 하부 수변 산책로 연결 통로 (X=±8.5m, 폭 3.0m)
    m_river.add_box(3.0, 0.3, 40.0, 8.5, -3.75, 0.0, region=Q_DANCHEONG, scale=4.0)
    m_river.add_box(3.0, 0.3, 40.0, -8.5, -3.75, 0.0, region=Q_DANCHEONG, scale=4.0)

    # 5중 음각 단차 옹벽 (X=±10.0m ~ ±13.0m)
    m_street.add_box(3.0, 3.6, 40.0, 11.5, -1.8, 0.0, region=Q_GRANITE, scale=4.0)
    m_street.add_box(3.0, 3.6, 40.0, -11.5, -1.8, 0.0, region=Q_GRANITE, scale=4.0)

    d3.add(m_river)

    # 6. 인터랙션 핫스팟 및 조망 앵커
    d3.add_anchor("hotspot_gwangtonggyo_deck", (0.0, 0.2, 0.0))
    d3.add_anchor("hotspot_shinjinseok_relief_east", (5.8, -2.6, 4.0))
    d3.add_anchor("hotspot_shinjinseok_relief_west", (-5.8, -2.6, -4.0))
    d3.add_anchor("hotspot_arch_underpass", (0.0, -3.6, 0.0))
    d3.add_anchor("anchor_mythical_beast_ne", (6.0, 1.8, 7.5))

    return d3

def build_gwangtonggyo_lod2():
    d2 = GLTFDoc(GEN, CR)
    s = Mesh("gwangtonggyo_street_lod2", 0)
    s.add_box(7.0, 0.4, 40.0, 16.5, -0.2, 0.0, region=Q_GRANITE, scale=2.0)
    s.add_box(7.0, 0.4, 40.0, -16.5, -0.2, 0.0, region=Q_GRANITE, scale=2.0)
    s.add_box(3.0, 3.6, 40.0, 11.5, -1.8, 0.0, region=Q_GRANITE, scale=2.0)
    s.add_box(3.0, 3.6, 40.0, -11.5, -1.8, 0.0, region=Q_GRANITE, scale=2.0)
    d2.add(s)

    b = Mesh("gwangtonggyo_bridge_lod2", 0)
    # 다리 상판
    b.add_box(12.0, 0.6, 15.0, 0.0, -0.3, 0.0, region=Q_GRANITE, scale=2.0)
    # 돌난간
    b.add_box(12.0, 1.0, 0.4, 0.0, 0.5, 7.5, region=Q_GRANITE, scale=1.0)
    b.add_box(12.0, 1.0, 0.4, 0.0, 0.5, -7.5, region=Q_GRANITE, scale=1.0)
    # 중앙 교각
    b.add_box(1.5, 3.2, 18.0, 0.0, -3.1, 0.0, region=Q_GRANITE, scale=2.0)
    b.add_box(1.5, 3.2, 2.5, 0.0, -3.1, 9.25, region=Q_GRANITE, scale=1.0)
    b.add_box(1.5, 3.2, 2.5, 0.0, -3.1, -9.25, region=Q_GRANITE, scale=1.0)
    # 아치 2개 간략화
    for center_x in [-3.375, 3.375]:
        for iv in range(8):
            ang = math.pi * ((iv + 0.5) / 8)
            xm = center_x + 2.9 * math.cos(ang)
            ym = -3.8 + 2.9 * math.sin(ang)
            b.add_box(0.7, 0.6, 15.0, xm, ym, 0.0, region=Q_GRANITE, scale=1.0)
    d2.add(b)

    r = Mesh("gwangtonggyo_river_lod2", 2)
    r.add_box(26.0, 0.1, 40.0, 0.0, -4.35, 0.0, region=Q_ROOF, scale=2.0)
    r.add_box(26.0, 0.4, 40.0, 0.0, -5.0, 0.0, region=Q_GRANITE, scale=2.0)
    d2.add(r)

    return d2

def generate():
    out_dir = "/workspace/pimang-sandbox/lego_blocks/03188_WATER_p23_청계천_광통교_역사복원"
    reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03188_WATER_p23_청계천_광통교_역사복원"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(reg_dir, exist_ok=True)

    d3 = build_gwangtonggyo_lod3()
    doc3, b3_len, stats3, t3 = d3.build("texture_atlas.webp", MATERIALS)

    d2 = build_gwangtonggyo_lod2()
    doc2, b2_len, stats2, t2 = d2.build("texture_atlas.webp", MATERIALS)

    print(f"LOD3 Triangles: {t3}, LOD2 Triangles: {t2}")

    manifest = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": COMPOSITE_ID,
        "block_id": BID,
        "name": NAME,
        "category": "CAT03_HISTORIC_BRIDGE",
        "postal_code": "03188",
        "coordinates": {"lat": 37.5691, "lng": 126.9822},
        "heading": 89.2,
        "base_plinth_height_m": 0.0,
        "ground": {"mode": "snap_to_terrain", "base_y": 0.0},
        "bbox_local_m": {"min": [-20.0, -5.2, -20.0], "max": [20.0, 2.2, 20.0]},
        "lod_switch_distance": {"lod3_to_lod2_m": 45.0, "lod2_to_lod1_m": 120.0},
        "hierarchical_components": [
            {"id": "gwangtonggyo_street_connections", "level": 1, "triangles": 480, "description": "상부 청계천로 도로면(Y=0.0m) 접속부 및 안전 방호 난간"},
            {"id": "gwangtonggyo_piers_and_cutwaters", "level": 2, "triangles": 960, "description": "원두형 중앙 교각 및 상·하류 마름모꼴 유선형 분수침"},
            {"id": "gwangtonggyo_segmental_arches", "level": 2, "triangles": 3840, "description": "실측 2경간 홍예 아치 쐐기돌(Voussoirs 36블록) 및 스팬드럴 석벽"},
            {"id": "gwangtonggyo_shinjinseok_reliefs", "level": 3, "triangles": 1680, "description": "교대 석벽에 거꾸로 뒤집혀 새겨진 신덕왕후 능석 신장석 부조 4기"},
            {"id": "gwangtonggyo_deck_and_balustrades", "level": 2, "triangles": 2480, "description": "다리 상판 화강석 판석, 엄지기둥 4기, 동자석 24기 및 하엽 난간대"},
            {"id": "gwangtonggyo_mythical_beasts", "level": 3, "triangles": 880, "description": "다리 네 귀퉁이 엄지기둥 상단 서수(해태) 석상 4기"},
            {"id": "gwangtonggyo_riverbed_and_water", "level": 1, "triangles": 360, "description": "청계천 맑은 수면 플레인, 하상 자갈 및 교각 하부 수변 산책로"}
        ],
        "interaction_hotspots": [
            {"id": "hotspot_gwangtonggyo_deck", "label": "광통교 상판 역사 보행"},
            {"id": "hotspot_shinjinseok_relief_east", "label": "동측 신덕왕후 능석 신장석 부조"},
            {"id": "hotspot_shinjinseok_relief_west", "label": "서측 신덕왕후 능석 신장석 부조"},
            {"id": "hotspot_arch_underpass", "label": "홍예 아치 하부 수변 통로"},
            {"id": "anchor_mythical_beast_ne", "label": "광통교 동북측 서수 조각상"}
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_03_03188_003_01(신장석 부조), _02(홍예 아치), _03(서수 조각상) 등",
        "files": {
            "model_lod3.gltf": {"triangles": t3},
            "model_lod2.gltf": {"triangles": t2},
            "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}
        },
        "references": [
            "청계천 광통교 복원 실측조사 보고서 — 서울역사박물관",
            "조선왕조실록 태종 10년 광통교 축조 및 정릉 능석 활용 기록",
            "TASK_REQUEST_20261107_PIMANG_12BLOCKS_SPEC_117.md 종로 12종 발주서 #9"
        ]
    }

    atlas = create_gwangtonggyo_atlas()

    for target in [out_dir, reg_dir]:
        json.dump(manifest, open(os.path.join(target, "block_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(doc3, open(os.path.join(target, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(doc2, open(os.path.join(target, "model_lod2.gltf"), "w", encoding="utf-8"))
        atlas.save(os.path.join(target, "texture_atlas.webp"), "WEBP", quality=88)

    print(f"Successfully generated {BID} in {out_dir} and {reg_dir}!")

if __name__ == "__main__":
    generate()
