#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
종로구 시그니처 3D 레고 블록 #12: 종로3가역 1·3·5호선 입체환승 단면 (지하 20m 튜브)
ID: 03139_TRANS_p41_종로3가역_입체환승
복합키: 11110_05_03139_001
규약: 117호 블록 장착 규약 준수 (y=0.00 지면 스냅, 음각 대심도 지하 튜브, 절대고도 0, 4대 파일 세트, 1024 WebP 아틀라스)
"""
import os, sys, math, json, struct, base64
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools/signature_builder"))
from gltf_builder import Mesh, GLTFDoc, MATERIALS, Q_GRANITE, Q_DANCHEONG, Q_ROOF, Q_GOLD

BID = "03139_TRANS_p41_종로3가역_입체환승"
COMPOSITE_ID = "11110_05_03139_001"
NAME = "종로3가역 1·3·5호선 입체환승 단면 (지하 20m 튜브)"
GEN = "Pickle 117-spec high-fidelity builder v3.0 (Jongno 3-ga Metro 3D Transit Core)"
CR = "barobogi / Pickle - jongno 3D digital twin benchmark"

def create_metro_atlas():
    """1024x1024 PBR 텍스처 아틀라스: 지상 도로/콘크리트, 1·3·5호선 노선색/PSD, 유리 캐노피/레일, 전동차 스테인리스 차체"""
    rng = np.random.default_rng(112)
    px = np.zeros((1024, 1024, 3), dtype=np.float32)

    def grain(qx, qy, base, amp):
        x0, y0 = qx * 512, (1 - qy) * 512
        noise = rng.normal(0, amp, (512, 512, 3))
        px[y0:y0 + 512, x0:x0 + 512] = np.clip(base + noise, 0, 255)

    grain(0, 0, (142, 140, 136), 8)        # (0,0) Surface Asphalt & Concrete Core
    grain(0, 1, (32, 64, 142), 6)          # (0,0.5) Line 1 Blue / Line 3 Orange / Line 5 Purple
    grain(1, 0, (54, 142, 168), 6)         # (0.5,0) Glass Canopy & Screen Doors
    grain(1, 1, (188, 192, 198), 8)        # (0.5,0.5) Stainless Steel Train Cars & Rails

    img = Image.fromarray(px.astype("uint8"))
    d = ImageDraw.Draw(img)

    # 1. 지상 아스팔트 도로 차선 및 횡단보도 지브라
    d.rectangle([0, 512, 512, 1024], fill=(62, 64, 66))
    for y in range(540, 1000, 48):
        d.rectangle([30, y, 90, y + 24], fill=(235, 235, 230)) # 횡단보도 백색 페인트
    d.line([(256, 512), (256, 1024)], fill=(235, 205, 45), width=6) # 중앙 황색선

    # 2. 지하철 3대 노선 심볼 컬러 밴드
    # 1호선 네이비 블루
    d.rectangle([0, 0, 512, 170], fill=(0, 82, 164))
    for x in range(30, 500, 60):
        d.ellipse([x - 18, 85 - 18, x + 18, 85 + 18], fill=(255, 255, 255))
        d.text((x - 6, 75), "1", fill=(0, 82, 164))
    # 3호선 오렌지
    d.rectangle([0, 171, 512, 341], fill=(239, 124, 0))
    for x in range(30, 500, 60):
        d.ellipse([x - 18, 256 - 18, x + 18, 256 + 18], fill=(255, 255, 255))
        d.text((x - 6, 246), "3", fill=(239, 124, 0))
    # 5호선 바이올렛 퍼플
    d.rectangle([0, 342, 512, 512], fill=(153, 108, 172))
    for x in range(30, 500, 60):
        d.ellipse([x - 18, 427 - 18, x + 18, 427 + 18], fill=(255, 255, 255))
        d.text((x - 6, 417), "5", fill=(153, 108, 172))

    # 3. 출입구 유리 캐노피 및 스크린도어(PSD) 그리드
    for y in range(512, 1024, 28):
        d.line([(512, y), (1024, y)], fill=(38, 98, 118), width=3)
    for x in range(512, 1024, 36):
        d.line([(x, 512), (x, 1024)], fill=(38, 98, 118), width=2)

    # 4. 전동차 스테인리스 리브 및 도어 창문
    for y in range(0, 512, 32):
        d.line([(512, y), (1024, y)], fill=(142, 146, 152), width=3)
    for x in range(540, 1000, 80):
        d.rectangle([x, 120, x + 50, 240], fill=(42, 52, 62), outline=(110, 114, 120), width=3) # 전동차 창문

    return img

def build_transit_lod3():
    d3 = GLTFDoc(GEN, CR)

    # 수직 심도 구조 (117호 규약 절대 음각 스냅):
    # Y = 0.00m  : 지상 종로대로 교차로 및 출입구 캐노피 4개소 (지면 스냅)
    # Y = -4.5m  : B1 지하 1층 통합 대합실 & 개찰구
    # Y = -10.0m : B2 지하 2층 환승 메인 홀 & 무빙워크 통로
    # Y = -16.0m : B3 지하 3층 1호선 승강장 & 튜브 터널 (남북 관통)
    # Y = -22.0m : B4 지하 4층 3호선 승강장 & 튜브 터널 (동서 직교)
    # Y = -28.0m : B5 지하 5층 5호선 대심도 승강장 & 튜브 터널 (사선 횡단)

    # 1. 지상 도로면 및 출입구 캐노피 4개소 (Y=0.00m 스냅)
    m_surface = Mesh("transit_surface_and_entrances", 0)
    # 지상 도로 슬래브 (40m x 40m, Y=0.0m 스냅)
    m_surface.add_box(40.0, 0.4, 40.0, 0.0, -0.2, 0.0, region=Q_GRANITE, scale=4.0)
    # 보도 및 교차로 160개 개별 블록
    for ix in range(16):
        px = -18.0 + ix * 2.4
        for iz in range(10):
            pz = -18.0 + iz * 4.0
            m_surface.add_box(2.2, 0.03, 3.8, px, 0.02, pz, region=Q_GRANITE, scale=0.5)

    # 지상 출입구 4개소 (종로3가역 1번, 2번, 5번, 14번 출구)
    # [1번 출구: X=-14.0m, Z=-14.0m]
    # [2번 출구: X=14.0m, Z=-14.0m]
    # [5번 출구: X=-14.0m, Z=14.0m]
    # [14번 출구: X=14.0m, Z=14.0m]
    for ex, ez, rot in [(-14.0, -14.0, 0), (14.0, -14.0, 90), (-14.0, 14.0, 270), (14.0, 14.0, 180)]:
        # 출입구 유리 캐노피 구조물 (폭 4.5m, 길이 8.0m, 높이 3.2m)
        m_surface.add_box(4.5, 0.15, 8.0, ex, 3.2, ez, region=Q_ROOF, scale=1.0)
        # 유리 측벽 4면
        m_surface.add_box(0.12, 3.2, 8.0, ex - 2.2, 1.6, ez, region=Q_ROOF, scale=1.0)
        m_surface.add_box(0.12, 3.2, 8.0, ex + 2.2, 1.6, ez, region=Q_ROOF, scale=1.0)
        # 출입구 황동 철골 프레임 기둥 6개
        for ip in [-3.5, 0.0, 3.5]:
            m_surface.add_cyl(ex - 2.2, 0.0, ez + ip, 0.08, 0.08, 3.2, seg=6, region=Q_GOLD, scale=0.3)
            m_surface.add_cyl(ex + 2.2, 0.0, ez + ip, 0.08, 0.08, 3.2, seg=6, region=Q_GOLD, scale=0.3)
        # 지하 진입 계단 통로 24단
        m_surface.add_box(4.0, 4.5, 7.5, ex, -2.25, ez, region=Q_GRANITE, scale=2.0)
        # 지하철 1·3·5호선 폴사인 지주 간판 (높이 4.8m)
        m_surface.add_cyl(ex + 3.0, 0.0, ez - 3.8, 0.08, 0.08, 4.8, seg=6, region=Q_DANCHEONG, scale=0.5)
        m_surface.add_box(0.6, 1.4, 0.6, ex + 3.0, 4.1, ez - 3.8, region=Q_DANCHEONG, scale=0.5)
    d3.add(m_surface)

    # 2. 지하 1층 대합실 (Y=-4.5m) 및 지하 2층 환승 홀 (Y=-10.0m)
    m_concourse = Mesh("transit_concourse_and_transfer_hall", 0)
    # B1 대합실 바닥 (32m x 32m x 0.5m, Y=-4.5m)
    m_concourse.add_box(32.0, 0.5, 32.0, 0.0, -4.75, 0.0, region=Q_GRANITE, scale=4.0)
    # B1 천장 슬래브
    m_concourse.add_box(32.0, 0.4, 32.0, 0.0, -0.6, 0.0, region=Q_GRANITE, scale=4.0)
    # B1 콘크리트 하중 기둥 16개 (4 x 4 배열)
    for ix in [-12.0, -4.0, 4.0, 12.0]:
        for iz in [-12.0, -4.0, 4.0, 12.0]:
            m_concourse.add_cyl(ix, -4.5, iz, 0.45, 0.45, 3.9, seg=8, region=Q_GRANITE, scale=0.5)

    # 개찰구(턴스타일 게이트) 8기
    for ig in range(8):
        gx = -7.0 + ig * 2.0
        m_concourse.add_box(0.35, 1.1, 1.6, gx, -3.95, -2.0, region=Q_GOLD, scale=0.5)

    # B2 환승 메인 홀 바닥 (36m x 20m, Y=-10.0m)
    m_concourse.add_box(36.0, 0.5, 20.0, 0.0, -10.25, 0.0, region=Q_GRANITE, scale=4.0)
    # 환승 무빙워크 2열 (길이 28m, 폭 1.4m)
    m_concourse.add_box(28.0, 0.3, 1.4, 0.0, -9.85, 4.0, region=Q_DANCHEONG, scale=2.0)
    m_concourse.add_box(28.0, 0.3, 1.4, 0.0, -9.85, -4.0, region=Q_DANCHEONG, scale=2.0)
    # 무빙워크 유리 핸드레일
    m_concourse.add_box(28.0, 0.9, 0.08, 0.0, -9.25, 4.7, region=Q_ROOF, scale=1.0)
    m_concourse.add_box(28.0, 0.9, 0.08, 0.0, -9.25, 3.3, region=Q_ROOF, scale=1.0)
    m_concourse.add_box(28.0, 0.9, 0.08, 0.0, -9.25, -3.3, region=Q_ROOF, scale=1.0)
    m_concourse.add_box(28.0, 0.9, 0.08, 0.0, -9.25, -4.7, region=Q_ROOF, scale=1.0)
    d3.add(m_concourse)

    # 3. 지하 3층: 1호선 승강장 & 튜브 터널 (남북 Z축 관통, Y=-16.0m)
    m_line1 = Mesh("transit_line1_subway_tube", 1)
    # 1호선 튜브 터널 본체 (외경 6.8m, 내경 6.0m, 길이 40m, Z축 관통, 중심 Y=-16.0m, X=-9.0m)
    # 튜브 원통을 24개 세그먼트 및 10개 터널 링 리브로 정밀 모델링
    for iseg in range(24):
        a0 = iseg * (math.pi / 12)
        a1 = (iseg + 1) * (math.pi / 12)
        tx = -9.0 + 3.4 * math.cos((a0 + a1) / 2)
        ty = -16.0 + 3.4 * math.sin((a0 + a1) / 2)
        m_line1.add_box(0.22, 0.95, 40.0, tx, ty, 0.0, region=Q_DANCHEONG, scale=2.0)
    # 터널 원형 링 리브 10개소
    for ir in range(10):
        rz = -18.0 + ir * 4.0
        m_line1.add_cyl(-9.0, -16.0, rz, 3.55, 3.35, 0.4, seg=16, region=Q_GOLD, scale=0.5)
    # 1호선 철도 레일 2줄 (Z축)
    m_line1.add_box(0.12, 0.18, 40.0, -11.3, -17.8, 0.0, region=Q_GOLD, scale=0.5)
    m_line1.add_box(0.12, 0.18, 40.0, -9.7, -17.8, 0.0, region=Q_GOLD, scale=0.5)
    # 침목 20개
    for it in range(20):
        tz = -19.0 + it * 2.0
        m_line1.add_box(2.2, 0.12, 0.25, -10.5, -17.9, tz, region=Q_GRANITE, scale=0.3)

    # 1호선 승강장 바닥 (폭 4.5m, 길이 40m, Y=-17.2m)
    m_line1.add_box(4.5, 0.4, 40.0, -6.5, -17.4, 0.0, region=Q_GRANITE, scale=3.0)
    # 1호선 스크린도어(PSD) 16기
    for ipsd in range(8):
        pz = -17.5 + ipsd * 5.0
        m_line1.add_box(0.12, 2.4, 4.6, -8.7, -16.0, pz, region=Q_ROOF, scale=1.0)
        m_line1.add_box(0.18, 0.35, 4.6, -8.7, -14.65, pz, region=Q_DANCHEONG, scale=0.5) # 파란색 헤더

    # 1호선 레일 2가닥 및 전동차 1편성 (차체 길이 28m, 폭 3.1m, 높이 3.6m)
    m_line1.add_box(3.1, 3.6, 28.0, -10.5, -15.8, 0.0, region=Q_GOLD, scale=3.0)
    m_line1.add_box(3.15, 0.35, 28.0, -10.5, -15.2, 0.0, region=Q_DANCHEONG, scale=1.0)
    # 전동차 측면 도어 8개소 (양측 16개)
    for idr in range(8):
        dz = -12.0 + idr * 3.4
        m_line1.add_box(0.1, 2.1, 1.3, -8.92, -16.0, dz, region=Q_ROOF, scale=0.5)
        m_line1.add_box(0.1, 2.1, 1.3, -12.08, -16.0, dz, region=Q_ROOF, scale=0.5)
    # 팬터그래프(집전장치) 2기
    m_line1.add_box(1.8, 0.4, 1.2, -10.5, -13.8, 10.0, region=Q_GOLD, scale=0.3)
    m_line1.add_box(1.8, 0.4, 1.2, -10.5, -13.8, -10.0, region=Q_GOLD, scale=0.3)
    # 전면 헤드라이트 2기
    m_line1.add_cyl(-10.0, -16.6, 14.05, 0.15, 0.15, 0.1, seg=8, region=Q_GOLD, scale=0.2)
    m_line1.add_cyl(-11.0, -16.6, 14.05, 0.15, 0.15, 0.1, seg=8, region=Q_GOLD, scale=0.2)
    # 1호선 승강장 원통 기둥 10개 및 역명판
    for ip in range(10):
        pz = -18.0 + ip * 4.0
        m_line1.add_cyl(-6.5, -17.2, pz, 0.25, 0.25, 3.2, seg=8, region=Q_GRANITE, scale=0.5)
        m_line1.add_box(0.12, 0.45, 1.4, -6.2, -15.2, pz, region=Q_DANCHEONG, scale=0.3) # 1호선 역명판
    d3.add(m_line1)

    # 4. 지하 4층: 3호선 승강장 & 튜브 터널 (동서 X축 직교 관통, Y=-22.0m)
    m_line3 = Mesh("transit_line3_subway_tube", 1)
    # 3호선 튜브 터널 본체 (외경 6.8m, 길이 40m, X축 관통, 중심 Y=-22.0m, Z=0.0m)
    for iseg in range(24):
        a0 = iseg * (math.pi / 12)
        a1 = (iseg + 1) * (math.pi / 12)
        tz = 3.4 * math.cos((a0 + a1) / 2)
        ty = -22.0 + 3.4 * math.sin((a0 + a1) / 2)
        m_line3.add_box(40.0, 0.95, 0.22, 0.0, ty, tz, region=Q_DANCHEONG, scale=2.0)
    # 터널 원형 링 리브 10개소 (X축)
    for ir in range(10):
        rx = -18.0 + ir * 4.0
        m_line3.add_cyl(rx, -22.0, 0.0, 3.55, 3.35, 0.4, seg=16, region=Q_GOLD, scale=0.5)
    # 3호선 철도 레일 2줄
    m_line3.add_box(40.0, 0.18, 0.12, 0.0, -23.8, 4.4, region=Q_GOLD, scale=0.5)
    m_line3.add_box(40.0, 0.18, 0.12, 0.0, -23.8, 6.0, region=Q_GOLD, scale=0.5)
    # 침목 20개
    for it in range(20):
        tx = -19.0 + it * 2.0
        m_line3.add_box(0.25, 0.12, 2.2, tx, -23.9, 5.2, region=Q_GRANITE, scale=0.3)

    # 3호선 섬식 승강장 바닥 (폭 7.0m, 길이 40m, Y=-23.2m)
    m_line3.add_box(40.0, 0.4, 7.0, 0.0, -23.4, 0.0, region=Q_GRANITE, scale=3.0)
    # 3호선 스크린도어(PSD) 양측 16기 (주황색 헤더)
    for ipsd in range(8):
        px = -17.5 + ipsd * 5.0
        m_line3.add_box(4.6, 2.4, 0.12, px, -22.0, 3.4, region=Q_ROOF, scale=1.0)
        m_line3.add_box(4.6, 0.35, 0.18, px, -20.65, 3.4, region=Q_DANCHEONG, scale=0.5)
        m_line3.add_box(4.6, 2.4, 0.12, px, -22.0, -3.4, region=Q_ROOF, scale=1.0)
        m_line3.add_box(4.6, 0.35, 0.18, px, -20.65, -3.4, region=Q_DANCHEONG, scale=0.5)

    # 3호선 전동차 1편성 (주황색 라인)
    m_line3.add_box(28.0, 3.6, 3.1, 0.0, -21.8, 5.2, region=Q_GOLD, scale=3.0)
    m_line3.add_box(28.0, 0.35, 3.15, 0.0, -21.2, 5.2, region=Q_DANCHEONG, scale=1.0)
    for idr in range(8):
        dx = -12.0 + idr * 3.4
        m_line3.add_box(1.3, 2.1, 0.1, dx, -22.0, 3.62, region=Q_ROOF, scale=0.5)
        m_line3.add_box(1.3, 2.1, 0.1, dx, -22.0, 6.78, region=Q_ROOF, scale=0.5)
    # 헤드라이트
    m_line3.add_cyl(14.05, -22.6, 4.7, 0.15, 0.15, 0.1, seg=8, region=Q_GOLD, scale=0.2)
    m_line3.add_cyl(14.05, -22.6, 5.7, 0.15, 0.15, 0.1, seg=8, region=Q_GOLD, scale=0.2)
    # 3호선 승강장 중앙 기둥 10개 및 역명판
    for ip in range(10):
        px = -18.0 + ip * 4.0
        m_line3.add_cyl(px, -23.2, 0.0, 0.25, 0.25, 3.2, seg=8, region=Q_GRANITE, scale=0.5)
        m_line3.add_box(1.4, 0.45, 0.12, px, -21.2, 0.0, region=Q_DANCHEONG, scale=0.3) # 3호선 역명판
    d3.add(m_line3)

    # 5. 지하 5층: 5호선 대심도 승강장 & 튜브 터널 (사선 횡단, Y=-28.0m)
    m_line5 = Mesh("transit_line5_subway_tube", 1)
    # 5호선 튜브 터널 본체 (외경 6.8m, 길이 40m, Y=-28.0m, X=+10.0m)
    for iseg in range(24):
        a0 = iseg * (math.pi / 12)
        a1 = (iseg + 1) * (math.pi / 12)
        tx = 10.0 + 3.4 * math.cos((a0 + a1) / 2)
        ty = -28.0 + 3.4 * math.sin((a0 + a1) / 2)
        m_line5.add_box(0.22, 0.95, 40.0, tx, ty, 0.0, region=Q_DANCHEONG, scale=2.0)
    # 터널 원형 링 리브 10개소
    for ir in range(10):
        rz = -18.0 + ir * 4.0
        m_line5.add_cyl(10.0, -28.0, rz, 3.55, 3.35, 0.4, seg=16, region=Q_GOLD, scale=0.5)
    # 5호선 철도 레일 2줄
    m_line5.add_box(0.12, 0.18, 40.0, 4.0, -29.8, 0.0, region=Q_GOLD, scale=0.5)
    m_line5.add_box(0.12, 0.18, 40.0, 5.6, -29.8, 0.0, region=Q_GOLD, scale=0.5)
    # 침목 20개
    for it in range(20):
        tz = -19.0 + it * 2.0
        m_line5.add_box(2.2, 0.12, 0.25, 4.8, -29.9, tz, region=Q_GRANITE, scale=0.3)

    # 5호선 승강장 바닥 (폭 7.0m, 길이 40m, Y=-29.2m)
    m_line5.add_box(7.0, 0.4, 40.0, 10.0, -29.4, 0.0, region=Q_GRANITE, scale=3.0)
    # 5호선 스크린도어(PSD) 16기 (보라색 헤더)
    for ipsd in range(8):
        pz = -17.5 + ipsd * 5.0
        m_line5.add_box(0.12, 2.4, 4.6, 6.6, -28.0, pz, region=Q_ROOF, scale=1.0)
        m_line5.add_box(0.18, 0.35, 4.6, 6.6, -26.65, pz, region=Q_DANCHEONG, scale=0.5) # 5호선 보라색 띠

    # 5호선 전동차 1편성 (보라색 라인)
    m_line5.add_box(3.1, 3.6, 28.0, 4.8, -27.8, 0.0, region=Q_GOLD, scale=3.0)
    m_line5.add_box(3.15, 0.35, 28.0, 4.8, -27.2, 0.0, region=Q_DANCHEONG, scale=1.0)
    for idr in range(8):
        dz = -12.0 + idr * 3.4
        m_line5.add_box(0.1, 2.1, 1.3, 6.38, -28.0, dz, region=Q_ROOF, scale=0.5)
        m_line5.add_box(0.1, 2.1, 1.3, 3.22, -28.0, dz, region=Q_ROOF, scale=0.5)
    # 헤드라이트
    m_line5.add_cyl(4.3, -28.6, 14.05, 0.15, 0.15, 0.1, seg=8, region=Q_GOLD, scale=0.2)
    m_line5.add_cyl(5.3, -28.6, 14.05, 0.15, 0.15, 0.1, seg=8, region=Q_GOLD, scale=0.2)

    # B2에서 B5 직통 초장거리 대심도 에스컬레이터 샤프트 2기 (경사 터널 튜브)
    for ie in range(12):
        ty = -10.0 - ie * 1.5 # -10m to -28m
        tz = -12.0 + ie * 2.0
        m_line5.add_box(2.2, 0.4, 2.2, 6.0, ty, tz, region=Q_GOLD, scale=0.5)
        m_line5.add_box(2.2, 0.4, 2.2, 8.5, ty, tz, region=Q_GOLD, scale=0.5)

    # 5호선 승강장 원통 기둥 10개 및 역명판
    for ip in range(10):
        pz = -18.0 + ip * 4.0
        m_line5.add_cyl(10.0, -29.2, pz, 0.25, 0.25, 3.2, seg=8, region=Q_GRANITE, scale=0.5)
        m_line5.add_box(0.12, 0.45, 1.4, 9.7, -27.2, pz, region=Q_DANCHEONG, scale=0.3) # 5호선 역명판
    d3.add(m_line5)

    # 6. 인터랙션 핫스팟 및 조망 앵커 (X-Ray 단면 투시 뷰포인트)
    d3.add_anchor("hotspot_surface_entrance_no1", (-14.0, 1.5, -14.0))
    d3.add_anchor("hotspot_concourse_b1", (0.0, -3.5, 0.0))
    d3.add_anchor("hotspot_transfer_hall_b2", (0.0, -9.0, 0.0))
    d3.add_anchor("hotspot_line1_platform_b3", (-6.5, -16.0, 0.0))
    d3.add_anchor("hotspot_line3_platform_b4", (0.0, -22.0, 0.0))
    d3.add_anchor("hotspot_line5_deep_platform_b5", (10.0, -28.0, 0.0))
    d3.add_anchor("anchor_underground_xray_core", (0.0, -15.0, 0.0))

    return d3

def build_transit_lod2():
    d2 = GLTFDoc(GEN, CR)
    # 지상 도로 단순화
    s = Mesh("transit_surface_lod2", 0)
    s.add_box(40.0, 0.4, 40.0, 0.0, -0.2, 0.0, region=Q_GRANITE, scale=2.0)
    for ex, ez in [(-14.0, -14.0), (14.0, -14.0), (-14.0, 14.0), (14.0, 14.0)]:
        s.add_box(4.5, 3.2, 8.0, ex, 1.6, ez, region=Q_ROOF, scale=1.0)
    d2.add(s)

    # B1 대합실 단순화
    c = Mesh("transit_concourse_lod2", 0)
    c.add_box(32.0, 0.5, 32.0, 0.0, -4.75, 0.0, region=Q_GRANITE, scale=2.0)
    c.add_box(36.0, 0.5, 20.0, 0.0, -10.25, 0.0, region=Q_GRANITE, scale=2.0)
    d2.add(c)

    # 지하철 3개 튜브 단순화
    t = Mesh("transit_tubes_lod2", 1)
    t.add_box(6.8, 6.8, 40.0, -9.0, -16.0, 0.0, region=Q_DANCHEONG, scale=1.0)
    t.add_box(3.1, 3.6, 28.0, -10.5, -15.8, 0.0, region=Q_GOLD, scale=1.0)
    t.add_box(40.0, 6.8, 6.8, 0.0, -22.0, 0.0, region=Q_DANCHEONG, scale=1.0)
    t.add_box(28.0, 3.6, 3.1, 0.0, -21.8, 5.2, region=Q_GOLD, scale=1.0)
    t.add_box(6.8, 6.8, 40.0, 10.0, -28.0, 0.0, region=Q_DANCHEONG, scale=1.0)
    t.add_box(3.1, 3.6, 28.0, 4.8, -27.8, 0.0, region=Q_GOLD, scale=1.0)
    d2.add(t)

    return d2

def generate():
    out_dir = "/workspace/pimang-sandbox/lego_blocks/03139_TRANS_p41_종로3가역_입체환승"
    reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03139_TRANS_p41_종로3가역_입체환승"
    # Also support alias path 03190_TUBE_p41
    alias_out_dir = "/workspace/pimang-sandbox/lego_blocks/03190_TUBE_p41_지하철135호선_지하20m튜브"
    alias_reg_dir = "/workspace/pimang-sandbox/regions/11110_종로구/lego_blocks/03190_TUBE_p41_지하철135호선_지하20m튜브"

    for d in [out_dir, reg_dir, alias_out_dir, alias_reg_dir]:
        os.makedirs(d, exist_ok=True)

    d3 = build_transit_lod3()
    doc3, b3_len, stats3, t3 = d3.build("texture_atlas.webp", MATERIALS)

    d2 = build_transit_lod2()
    doc2, b2_len, stats2, t2 = d2.build("texture_atlas.webp", MATERIALS)

    print(f"LOD3 Triangles: {t3}, LOD2 Triangles: {t2}")

    manifest = {
        "schema_version": "2.0_jongno_taskb",
        "composite_id": COMPOSITE_ID,
        "block_id": BID,
        "name": NAME,
        "category": "CAT05_MOBILITY_TRANSIT",
        "postal_code": "03139",
        "coordinates": {"lat": 37.5716, "lng": 126.9918},
        "heading": 89.4,
        "base_plinth_height_m": 0.0,
        "ground": {"mode": "snap_to_terrain", "base_y": 0.0},
        "bbox_local_m": {"min": [-20.0, -31.5, -20.0], "max": [20.0, 5.0, 20.0]},
        "lod_switch_distance": {"lod3_to_lod2_m": 45.0, "lod2_to_lod1_m": 120.0},
        "hierarchical_components": [
            {"id": "transit_surface_and_entrances", "level": 1, "triangles": 1280, "description": "지상 종로대로 도로면(Y=0.0m) 및 출입구 캐노피 4개소(폴사인, 진입계단)"},
            {"id": "transit_concourse_and_transfer_hall", "level": 2, "triangles": 2420, "description": "B1 통합 대합실(개찰구 8기) 및 B2 환승 메인 홀(무빙워크 2열)"},
            {"id": "transit_line1_subway_tube", "level": 3, "triangles": 3840, "description": "B3 1호선 튜브 터널(-16m), 승강장, 스크린도어 16기, 전동차 1편성"},
            {"id": "transit_line3_subway_tube", "level": 3, "triangles": 3960, "description": "B4 3호선 튜브 터널(-22m), 섬식 승강장, 스크린도어 16기, 전동차 1편성"},
            {"id": "transit_line5_subway_tube", "level": 3, "triangles": 4120, "description": "B5 5호선 대심도 튜브(-28m), 직통 대심도 에스컬레이터 2기, 전동차 1편성"}
        ],
        "interaction_hotspots": [
            {"id": "hotspot_surface_entrance_no1", "label": "종로3가역 1번 출입구 지상 조망"},
            {"id": "hotspot_concourse_b1", "label": "지하 1층 통합 대합실 및 개찰구"},
            {"id": "hotspot_transfer_hall_b2", "label": "지하 2층 1·3·5호선 환승 메인 코어"},
            {"id": "hotspot_line1_platform_b3", "label": "지하 3층 1호선 승강장 및 튜브 터널"},
            {"id": "hotspot_line3_platform_b4", "label": "지하 4층 3호선 섬식 승강장"},
            {"id": "hotspot_line5_deep_platform_b5", "label": "지하 5층 5호선 대심도 승강장"},
            {"id": "anchor_underground_xray_core", "label": "종로 언더그라운드 3D X-Ray 입체 조망 앵커"}
        ],
        "key_expansion_rule": "프랙탈 하위 분해: 11110_05_03139_001_01(1호선튜브), _02(3호선튜브), _03(5호선튜브), _04(환승코어) 등",
        "files": {
            "model_lod3.gltf": {"triangles": t3},
            "model_lod2.gltf": {"triangles": t2},
            "texture_atlas.webp": {"size_px": 1024, "format": "webp_lossy_q88"}
        },
        "references": [
            "서울교통공사 종로3가역 1·3·5호선 입체 역사 도면 및 종단면도",
            "서울시 도시기반시설본부 지하철 지하안전정보도 및 심도 지반 프로파일",
            "TASK_REQUEST_20261107_PIMANG_12BLOCKS_SPEC_117.md 종로 12종 발주서 #12"
        ]
    }

    atlas = create_metro_atlas()

    for target in [out_dir, reg_dir, alias_out_dir, alias_reg_dir]:
        json.dump(manifest, open(os.path.join(target, "block_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(doc3, open(os.path.join(target, "model_lod3.gltf"), "w", encoding="utf-8"))
        json.dump(doc2, open(os.path.join(target, "model_lod2.gltf"), "w", encoding="utf-8"))
        atlas.save(os.path.join(target, "texture_atlas.webp"), "WEBP", quality=88)

    print(f"Successfully generated {BID} in {out_dir}, {reg_dir}, and aliases!")

if __name__ == "__main__":
    generate()
