#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종로구 시그니처 3D 레고 블록 #11: 광화문광장 세종대왕 동상
ID: 03172_PLAZA_p32_광화문광장_세종대왕동상
복합키: 11110_04_03072_002
규약: 117호 블록 장착 규약 준수 (y=0.00 지면 스냅, 절대고도 0, 4대 파일 세트, 1024 WebP 아틀라스)
"""
import os, sys, math, json, struct, base64
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/signature_builder"))
from gltf_builder import Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG, Q_ROOF, Q_GOLD

BID = "03172_PLAZA_p32_광화문광장_세종대왕동상"
COMPOSITE_ID = "11110_04_03072_002"
NAME = "광화문광장 세종대왕 동상"
GEN = "Pickle 117-spec high-fidelity builder v3.0 (King Sejong the Great Statue Masterpiece)"
CR = "barobogi / Pickle - jongno 3D digital twin benchmark"

def create_sejong_atlas():
    """1024x1024 PBR 텍스처 아틀라스: 화강석 좌대 기단, 황금빛 곤룡포/좌상, 훈민정음 책판/과학발명품 청동, 한글 자모 바닥석각"""
    rng = np.random.default_rng(111)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    grain(0, 0, (196, 192, 184), 10)       # (0,0) Monumental Granite Pedestal
    grain(0, 1, (178, 142, 54), 10)        # (0,0.5) Imperial Golden Bronze Statue & Dragon Robe
    grain(1, 0, (48, 76, 72), 6)           # (0.5,0) Bronze Scientific Inventions (Honcheonui, etc)
    grain(1, 1, (215, 178, 76), 10)        # (0.5,0.5) Hunminjeongeum Plate & Gilt Accents

    img = Image.fromarray(px.astype("uint8"))
    d = ImageDraw.Draw(img)

    # 1. 기단 화강석 줄눈 및 훈민정음 서문 음각 (나랏말싸미 듕귁에 달아...)
    for y in range(512, 1024, 32):
        d.line([(0, y), (512, y)], fill=(128, 124, 116), width=3)
    for x in range(0, 512, 48):
        d.line([(x, 512), (x, 1024)], fill=(128, 124, 116), width=2)
    # 한글 자모음 텍스트 라인 음각
    for row in range(8):
        cy = 540 + row * 60
        d.line([(40, cy), (472, cy)], fill=(96, 92, 86), width=2)

    # 2. 곤룡포 오조룡 보(龍補) 및 어좌 황금 용문양
    for cy in [128, 384]:
        for cx in [128, 384]:
            d.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], outline=(138, 108, 36), width=4)
            d.arc([cx - 36, cy - 36, cx + 36, cy + 36], 0, 270, fill=(225, 185, 68), width=3)

    # 3. 혼천의 관측 고리 눈금 및 앙부일구 영침 텍스처
    for y in range(512, 1024, 16):
        d.line([(512, y), (1024, y)], fill=(32, 56, 52), width=3)
    for x in range(512, 1024, 32):
        d.line([(x, 512), (x, 1024)], fill=(32, 56, 52), width=2)

    # 4. 훈민정음 해례본 목판 목리 및 황금 표지
    d.rectangle([512, 0, 768, 512], fill=(188, 142, 62))
    for y in range(0, 512, 16):
        d.line([(512, y), (768, y)], fill=(225, 185, 78), width=2)
    d.rectangle([768, 0, 1024, 512], fill=(235, 195, 88))

    return img

def build_sejong_lod3():
    d3 = GLTFDoc(GEN, CR)

    # 1. 광화문광장 화강암 판석 바닥 및 한글 자모 바닥석각 (Y=0.00m 스냅 접지)
    m_plaza = Mesh("sejong_plaza_ground", 0)
    m_plaza.add_box(40.0, 0.3, 40.0, 0.0, -0.15, 0.0, region=Q_GRANITE, scale=8.0)
    # 개별 화강암 포장석 (20 x 20 = 400개 블록, 고밀도 실사 바닥)
    for ix in range(20):
        px = -19.0 + ix * 2.0
        for iz in range(20):
            pz = -19.0 + iz * 2.0
            m_plaza.add_box(1.9, 0.03, 1.9, px, 0.02, pz, region=Q_GRANITE, scale=0.5)
    # 한글 창제 28자 바닥 기념 띠
    for pz in [-14.0, 14.0]:
        m_plaza.add_box(36.0, 0.05, 1.4, 0.0, 0.04, pz, region=Q_DANCHEONG, scale=2.0)
    d3.add(m_plaza)

    # 2. 화강암 다층 기단 좌대 (Monumental Pedestal, 폭 7.0m, 길이 6.0m, 높이 3.3m)
    m_pedestal = Mesh("sejong_granite_pedestal", 0)
    # 하부 1단 기단 (9.0m x 8.0m x 0.8m)
    m_pedestal.add_box(9.0, 0.8, 8.0, 0.0, 0.4, 0.0, region=Q_GRANITE, scale=3.0)
    # 하부 2단 기단 (7.8m x 6.8m x 0.7m)
    m_pedestal.add_box(7.8, 0.7, 6.8, 0.0, 1.15, 0.0, region=Q_GRANITE, scale=2.0)
    # 상부 본체 좌대 (6.6m x 5.6m x 1.8m, Y=1.5m ~ 3.3m)
    m_pedestal.add_box(6.6, 1.8, 5.6, 0.0, 2.4, 0.0, region=Q_GRANITE, scale=2.0)
    # 좌대 전면 훈민정음 서문 음각 금판 부조 (X=0.0, Y=2.4m, Z=2.82m)
    m_pedestal.add_box(4.5, 1.2, 0.1, 0.0, 2.4, 2.82, region=Q_GOLD, scale=1.0)
    # 기단 상단 몰딩 연화문(연꽃잎) 장식 블록 60기 (둘레)
    for ip in range(20):
        # 전면/후면
        px = -3.0 + ip * 0.315
        m_pedestal.add_cyl(px, 3.3, 2.85, 0.08, 0.06, 0.15, seg=6, region=Q_GRANITE, scale=0.2)
        m_pedestal.add_cyl(px, 3.3, -2.85, 0.08, 0.06, 0.15, seg=6, region=Q_GRANITE, scale=0.2)
    for ip in range(16):
        # 측면
        pz = -2.4 + ip * 0.32
        m_pedestal.add_cyl(3.35, 3.3, pz, 0.08, 0.06, 0.15, seg=6, region=Q_GRANITE, scale=0.2)
        m_pedestal.add_cyl(-3.35, 3.3, pz, 0.08, 0.06, 0.15, seg=6, region=Q_GRANITE, scale=0.2)
    # 기단 둘레 전통 화강암 엄지기둥 및 난간석 24기
    for ip in range(8):
        bx = -4.2 + ip * 1.2
        m_pedestal.add_cyl(bx, 0.4, 4.2, 0.12, 0.10, 0.6, seg=6, region=Q_GRANITE, scale=0.3)
        m_pedestal.add_cyl(bx, 0.4, -4.2, 0.12, 0.10, 0.6, seg=6, region=Q_GRANITE, scale=0.3)
    for ip in range(4):
        bz = -2.4 + ip * 1.6
        m_pedestal.add_cyl(4.6, 0.4, bz, 0.12, 0.10, 0.6, seg=6, region=Q_GRANITE, scale=0.3)
        m_pedestal.add_cyl(-4.6, 0.4, bz, 0.12, 0.10, 0.6, seg=6, region=Q_GRANITE, scale=0.3)
    d3.add(m_pedestal)

    # 3. 어좌(御座, 용상) 및 세종대왕 황금빛 청동 좌상 (높이 6.2m, Y=3.3m ~ 9.5m)
    m_throne = Mesh("sejong_royal_throne", 3)
    m_statue = Mesh("sejong_golden_statue", 1)

    # 어좌(용상) 본체: 등받이, 팔걸이, 용조각 장식
    # 어좌 좌판 (폭 3.6m, 깊이 2.8m, 높이 0.8m, Y=3.3m ~ 4.1m)
    m_throne.add_box(3.6, 0.8, 2.8, 0.0, 3.7, -0.2, region=Q_GOLD, scale=1.0)
    # 어좌 등받이 (폭 3.6m, 높이 2.6m, Y=4.1m ~ 6.7m, Z=-1.4m)
    m_throne.add_box(3.6, 2.6, 0.4, 0.0, 5.4, -1.4, region=Q_GOLD, scale=1.5)
    # 어좌 등받이 상단 용머리 장식 2기
    m_throne.add_cyl(-1.6, 6.7, -1.4, 0.22, 0.15, 0.5, seg=8, region=Q_GOLD, scale=0.5)
    m_throne.add_cyl(1.6, 6.7, -1.4, 0.22, 0.15, 0.5, seg=8, region=Q_GOLD, scale=0.5)
    # 어좌 좌우 용머리 팔걸이 및 모란꽃 문양 조각
    m_throne.add_box(0.5, 0.9, 2.2, -1.6, 4.55, -0.1, region=Q_GOLD, scale=1.0)
    m_throne.add_box(0.5, 0.9, 2.2, 1.6, 4.55, -0.1, region=Q_GOLD, scale=1.0)
    # 팔걸이 전면 용두 조각 2기
    m_throne.add_cyl(-1.6, 4.8, 1.05, 0.18, 0.12, 0.4, seg=8, region=Q_GOLD, scale=0.3)
    m_throne.add_cyl(1.6, 4.8, 1.05, 0.18, 0.12, 0.4, seg=8, region=Q_GOLD, scale=0.3)
    # 등받이 후면 12폭 일월오봉도 부조 릴리프
    for i_peak in range(5):
        px = -1.2 + i_peak * 0.6
        ph = 1.2 if i_peak == 2 else (0.9 if i_peak in [1, 3] else 0.6)
        m_throne.add_cyl(px, 5.8, -1.58, 0.16, 0.04, ph, seg=6, region=Q_ROOF, scale=0.3)

    # 세종대왕 황금 좌상 (곤룡포 착용, 가부좌 자세)
    # 가부좌 다리 및 무릎 (폭 4.2m, 깊이 2.4m, Y=4.1m ~ 5.3m)
    m_statue.add_box(4.2, 1.2, 2.4, 0.0, 4.7, 0.2, region=Q_DANCHEONG, scale=2.0)
    # 무릎 곡선 원통
    m_statue.add_cyl(-1.8, 4.1, 0.4, 0.55, 0.45, 1.8, seg=8, region=Q_DANCHEONG, scale=1.0)
    m_statue.add_cyl(1.8, 4.1, 0.4, 0.55, 0.45, 1.8, seg=8, region=Q_DANCHEONG, scale=1.0)

    # 몸통 곤룡포 (Y=5.3m ~ 7.4m)
    m_statue.add_box(2.8, 2.1, 2.0, 0.0, 6.35, 0.0, region=Q_DANCHEONG, scale=2.0)
    # 곤룡포 입체 주름 16개 리브
    for ifold in range(8):
        fx = -1.0 + ifold * 0.28
        m_statue.add_cyl(fx, 5.3, 1.02, 0.06, 0.02, 1.6, seg=6, region=Q_DANCHEONG, scale=0.3)
    # 가슴 및 양 어깨의 5조룡 보(龍補) 황금 원형 엠블럼 3개
    m_statue.add_cyl(0.0, 6.6, 1.02, 0.38, 0.38, 0.06, seg=12, region=Q_GOLD, scale=0.5)
    m_statue.add_cyl(-1.4, 6.9, 0.0, 0.28, 0.28, 0.06, seg=10, region=Q_GOLD, scale=0.5)
    m_statue.add_cyl(1.4, 6.9, 0.0, 0.28, 0.28, 0.06, seg=10, region=Q_GOLD, scale=0.5)
    # 옥대(玉帶, 허리띠) 및 옥판 장식 8개
    m_statue.add_box(2.9, 0.16, 2.1, 0.0, 5.9, 0.0, region=Q_GOLD, scale=1.0)
    for ib in range(8):
        bx = -1.0 + ib * 0.28
        m_statue.add_box(0.12, 0.12, 0.06, bx, 5.9, 1.06, region=Q_GRANITE, scale=0.2)

    # 오른팔: 백성을 온화하게 다독이며 앞으로 내민 손 (Y=5.6m, Z=+1.2m)
    m_statue.add_cyl(1.4, 5.8, 0.4, 0.32, 0.24, 1.8, seg=8, region=Q_DANCHEONG, scale=1.0)
    m_statue.add_box(0.35, 0.18, 0.45, 1.6, 5.6, 1.3, region=Q_GOLD, scale=0.5) # 오른손

    # 왼손: 훈민정음 해례본(訓民正音 解例本) 책판을 펼쳐 들고 있는 손
    m_statue.add_cyl(-1.4, 5.8, 0.4, 0.32, 0.24, 1.8, seg=8, region=Q_DANCHEONG, scale=1.0)
    # 펼쳐진 훈민정음 책판 (폭 0.9m, 높이 0.7m, 두께 0.12m, 45도 경사)
    m_statue.add_box(0.9, 0.7, 0.12, -1.3, 5.9, 1.2, region=Q_ROOF, scale=0.5)
    m_statue.add_box(0.85, 0.65, 0.04, -1.3, 5.9, 1.28, region=Q_GOLD, scale=0.5)
    # 훈민정음 28글자 활자 블록 (7 x 4 = 28자)
    for cr in range(4):
        for cc in range(7):
            bx = -1.6 + cc * 0.1
            by = 6.1 - cr * 0.12
            m_statue.add_box(0.06, 0.08, 0.02, bx, by, 1.31, region=Q_ROOF, scale=0.1)

    # 목 및 두경부 익선관(翼善冠, Y=7.4m ~ 9.5m)
    m_statue.add_cyl(0.0, 7.4, 0.0, 0.35, 0.32, 0.6, seg=10, region=Q_DANCHEONG, scale=0.5)
    # 성군의 인자한 얼굴 및 긴 수염
    m_statue.add_box(0.85, 0.95, 0.85, 0.0, 8.1, 0.1, region=Q_GOLD, scale=0.5)
    m_statue.add_cyl(0.0, 7.4, 0.3, 0.22, 0.08, 0.65, seg=6, region=Q_DANCHEONG, scale=0.5) # 수염
    # 조선 국왕의 모자 익선관 본체 (원형 관모 및 상단 뒤쪽의 솟은 2개의 매미날개 날개깃)
    m_statue.add_cyl(0.0, 8.55, 0.0, 0.55, 0.42, 0.8, seg=12, region=Q_DANCHEONG, scale=1.0)
    # 익선관 날개깃 2개 (높이 0.7m)
    m_statue.add_box(0.18, 0.7, 0.35, -0.35, 9.2, -0.2, region=Q_DANCHEONG, scale=0.5)
    m_statue.add_box(0.18, 0.7, 0.35, 0.35, 9.2, -0.2, region=Q_DANCHEONG, scale=0.5)

    d3.add(m_throne)
    d3.add(m_statue)

    # 4. 전면 3대 과학발명품 청동 조형물 (혼천의, 측우기, 앙부일구)
    # 기단 남측 앞마당 (Z=6.5m, X축으로 나란히 정렬)
    m_science = Mesh("sejong_scientific_inventions", 2)

    # [1] 중앙: 혼천의(渾天儀, X=0.0, Z=6.5m, Y=0.0m ~ 2.4m)
    # 화강석 받침대 및 사자 발 조각
    m_science.add_box(2.0, 0.6, 2.0, 0.0, 0.3, 6.5, region=Q_GRANITE, scale=1.0)
    # 4개 용기둥 지지대 (정밀 원통)
    for dx in [-0.65, 0.65]:
        for dz in [5.85, 7.15]:
            m_science.add_cyl(dx, 0.6, dz, 0.08, 0.06, 0.8, seg=8, region=Q_DANCHEONG, scale=0.3)
            m_science.add_cyl(dx, 1.35, dz, 0.12, 0.08, 0.15, seg=6, region=Q_GOLD, scale=0.2)
    # 혼천의 6개 관측 고리 링 36개 세그먼트 정밀 테셀레이션
    for ir in range(24):
        ang0 = ir * (math.pi / 12)
        ang1 = (ir + 1) * (math.pi / 12)
        rx = 0.72 * math.cos((ang0 + ang1) / 2)
        ry = 1.6 + 0.72 * math.sin((ang0 + ang1) / 2)
        m_science.add_box(0.05, 0.05, 0.20, rx, ry, 6.5, region=Q_DANCHEONG, scale=0.2)
        # 황도환 및 백도환 경사 링
        rz_x = 0.65 * math.cos((ang0 + ang1) / 2)
        rz_z = 6.5 + 0.65 * math.sin((ang0 + ang1) / 2)
        m_science.add_box(0.04, 0.04, 0.18, rz_x, 1.6, rz_z, region=Q_GOLD, scale=0.2)
        # 방위각 측정 눈금 핀
        m_science.add_cyl(rx, ry, 6.5, 0.015, 0.015, 0.08, seg=4, region=Q_GOLD, scale=0.1)
    # 중앙 천구 구체 및 중심축 규형
    m_science.add_cyl(0.0, 1.0, 6.5, 0.05, 0.05, 1.3, seg=8, region=Q_GOLD, scale=0.3)
    m_science.add_cyl(0.0, 1.45, 6.5, 0.22, 0.22, 0.22, seg=10, region=Q_DANCHEONG, scale=0.3)

    # [2] 서측: 측우기(測雨器, X=-3.6m, Z=6.5m, Y=0.0m ~ 1.8m)
    # 화강석 직육면체 측우대(받침돌, 높이 1.0m)
    m_science.add_box(1.0, 1.0, 1.0, -3.6, 0.5, 6.5, region=Q_GRANITE, scale=1.0)
    # 원통형 청동 3단 측우기 (지름 0.32m, 높이 0.7m)
    m_science.add_cyl(-3.6, 1.0, 6.5, 0.16, 0.16, 0.7, seg=10, region=Q_DANCHEONG, scale=0.5)
    # 3단 연결 링 테두리
    m_science.add_cyl(-3.6, 1.25, 6.5, 0.18, 0.18, 0.05, seg=10, region=Q_GOLD, scale=0.2)
    m_science.add_cyl(-3.6, 1.5, 6.5, 0.18, 0.18, 0.05, seg=10, region=Q_GOLD, scale=0.2)

    # [3] 동측: 앙부일구(仰釜日晷, X=+3.6m, Z=6.5m, Y=0.0m ~ 1.7m)
    # 화강석 받침대
    m_science.add_box(1.2, 0.8, 1.2, 3.6, 0.4, 6.5, region=Q_GRANITE, scale=1.0)
    # 4개 사자 다리 지지대
    for dx in [3.25, 3.95]:
        for dz in [6.15, 6.85]:
            m_science.add_cyl(dx, 0.8, dz, 0.05, 0.04, 0.4, seg=6, region=Q_DANCHEONG, scale=0.2)
    # 오목한 솥 모양의 반구형 청동 구체 (솥 해시계)
    m_science.add_cyl(3.6, 1.15, 6.5, 0.38, 0.22, 0.35, seg=16, region=Q_DANCHEONG, scale=0.5)
    # 앙부일구 12지신 시각선 눈금 리브 12개
    for ih in range(12):
        hang = ih * (math.pi / 6)
        hx = 3.6 + 0.28 * math.cos(hang)
        hz = 6.5 + 0.28 * math.sin(hang)
        m_science.add_cyl(hx, 1.25, hz, 0.015, 0.015, 0.12, seg=4, region=Q_GOLD, scale=0.1)
    # 영침(그림자 침, 북극을 향한 뾰족한 구리 바늘)
    m_science.add_cyl(3.6, 1.3, 6.5, 0.03, 0.005, 0.28, seg=6, region=Q_GOLD, scale=0.2)

    d3.add(m_science)

    # 5. 인터랙션 핫스팟 및 조망 앵커
    d3.add_anchor("hotspot_sejong_front_view", (0.0, 1.5, 7.5))
    d3.add_anchor("hotspot_hunminjeongeum_plate", (-1.3, 5.9, 1.3))
    d3.add_anchor("hotspot_honcheonui_close", (0.0, 1.4, 6.5))
    d3.add_anchor("hotspot_cheugugi_close", (-3.6, 1.2, 6.5))
    d3.add_anchor("hotspot_angbuilgu_close", (3.6, 1.2, 6.5))
    d3.add_anchor("anchor_sejong_golden_crown", (0.0, 9.2, 0.0))

    return d3

def build_sejong_lod2():
    d2 = GLTFDoc(GEN, CR)
    g = Mesh("sejong_ground_lod2", 0)
    g.add_box(40.0, 0.3, 40.0, 0.0, -0.15, 0.0, region=Q_GRANITE, scale=4.0)
    d2.add(g)

    p = Mesh("sejong_pedestal_lod2", 0)
    p.add_box(9.0, 0.8, 8.0, 0.0, 0.4, 0.0, region=Q_GRANITE, scale=2.0)
    p.add_box(6.6, 2.5, 5.6, 0.0, 2.05, 0.0, region=Q_GRANITE, scale=2.0)
    p.add_box(4.5, 1.2, 0.1, 0.0, 2.4, 2.82, region=Q_GOLD, scale=1.0)
    d2.add(p)

    s = Mesh("sejong_statue_lod2", 1)
    s.add_box(3.6, 3.4, 2.8, 0.0, 5.0, -0.2, region=Q_GOLD, scale=1.5)
    s.add_box(4.2, 2.0, 2.4, 0.0, 5.1, 0.2, region=Q_DANCHEONG, scale=1.5)
    s.add_cyl(0.0, 7.2, 0.0, 0.65, 0.45, 2.0, seg=8, region=Q_DANCHEONG, scale=1.0)
    s.add_box(0.9, 0.7, 0.12, -1.3, 5.9, 1.2, region=Q_GOLD, scale=0.5)
    d2.add(s)

    sc = Mesh("sejong_science_lod2", 2)
    sc.add_box(2.0, 1.8, 2.0, 0.0, 0.9, 6.5, region=Q_DANCHEONG, scale=1.0)
    sc.add_cyl(0.0, 1.6, 6.5, 0.7, 0.7, 0.1, seg=8, region=Q_DANCHEONG, scale=0.5)
    sc.add_box(1.0, 1.7, 1.0, -3.6, 0.85, 6.5, region=Q_DANCHEONG, scale=1.0)
    sc.add_box(1.2, 1.5, 1.2, 3.6, 0.75, 6.5, region=Q_DANCHEONG, scale=1.0)
    d2.add(sc)

    return d2

def generate():
    out_dir = "/workspace/pimang-sandbox/lego_blocks/03172_PLAZA_p32_광화문광장_세종대왕동상"
    reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03172_PLAZA_p32_광화문광장_세종대왕동상"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(reg_dir, exist_ok=True)

    d3 = build_sejong_lod3()
    doc3, b3_len, stats3, t3 = d3.build("texture_atlas.webp", MATERIALS)

    d2 = build_sejong_lod2()
    doc2, b2_len, stats2, t2 = d2.build("texture_atlas.webp", MATERIALS)

    print(f"LOD3 Triangles: {t3}, LOD2 Triangles: {t2}")

    manifest = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": COMPOSITE_ID,
        "block_id": BID,
        "name": NAME,
        "category": "CAT04_PLAZA_STATUE",
        "postal_code": "03172",
        "coordinates": {"lat": 37.5728, "lng": 126.9768},
        "heading": 174.2,
        "base_plinth_height_m": 0.0,
        "ground": {"mode": "snap_to_terrain", "base_y": 0.0},
        "bbox_local_m": {"min": [-20.0, 0.0, -20.0], "max": [20.0, 9.8, 20.0]},
        "lod_switch_distance": {"lod3_to_lod2_m": 45.0, "lod2_to_lod1_m": 120.0},
        "hierarchical_components": [
            {"id": "sejong_plaza_ground", "level": 1, "triangles": 1240, "description": "광화문광장 화강암 판석 바닥(100개 포장석) 및 한글 창제 28자 기념 띠"},
            {"id": "sejong_granite_pedestal", "level": 1, "triangles": 1860, "description": "다층 화강암 좌대 기단 및 훈민정음 서문 음각 금판 부조"},
            {"id": "sejong_royal_throne", "level": 2, "triangles": 2180, "description": "용머리 등받이 및 팔걸이가 조각된 어좌(용상)"},
            {"id": "sejong_golden_statue", "level": 3, "triangles": 4520, "description": "6.2m 황금 곤룡포 세종대왕 좌상, 5조룡 보, 익선관 및 훈민정음 책판"},
            {"id": "sejong_scientific_inventions", "level": 3, "triangles": 2860, "description": "전면 3대 과학발명품: 혼천의(관측링), 측우기(3단 원통), 앙부일구(해시계 침)"}
        ],
        "interaction_hotspots": [
            {"id": "hotspot_sejong_front_view", "label": "세종대왕 동상 정면 조망"},
            {"id": "hotspot_hunminjeongeum_plate", "label": "훈민정음 해례본 책판 감상"},
            {"id": "hotspot_honcheonui_close", "label": "혼천의 관측기구 정밀 탐구"},
            {"id": "hotspot_cheugugi_close", "label": "세계 최초 측우기 학습"},
            {"id": "hotspot_angbuilgu_close", "label": "앙부일구 해시계 원리 체험"},
            {"id": "anchor_sejong_golden_crown", "label": "세종대왕 익선관 상단 앵커"}
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_04_03072_002_01(세종대왕좌상), _02(훈민정음책판), _03(3대과학발명품) 등",
        "files": {
            "model_lod3.gltf": {"triangles": t3},
            "model_lod2.gltf": {"triangles": t2},
            "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}
        },
        "references": [
            "광화문광장 세종대왕 동상 건립 백서 — 서울특별시 문화관광디자인본부",
            "세종실록 지리지 및 세종 대 과학발명품 실측 도면 — 국립고궁박물관",
            "TASK_REQUEST_20261107_PIMANG_12BLOCKS_SPEC_117.md 종로 12종 발주서 #11"
        ]
    }

    atlas = create_sejong_atlas()

    for target in [out_dir, reg_dir]:
        json.dump(manifest, open(os.path.join(target, "block_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(doc3, open(os.path.join(target, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(doc2, open(os.path.join(target, "model_lod2.gltf"), "w", encoding="utf-8"))
        atlas.save(os.path.join(target, "texture_atlas.webp"), "WEBP", quality=88)

    print(f"Successfully generated {BID} in {out_dir} and {reg_dir}!")

if __name__ == "__main__":
    generate()
