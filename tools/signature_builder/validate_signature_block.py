#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""로컬 검증기: 블록 패키지 4대 파일 유효성 검증.
- block_manifest.json: 필수 필드 체크
- model_lod3/2.gltf: glTF 2.0 구조 검증 (JSON, buffer/accessor 경계, scene 그래프,
  material PBR, 이미지 참조, 노드 계층, 삼각수 집계)
- texture_atlas.webp: RIFF/WEBP 헤더 + 1024x1024 치수
"""
import base64
import json
import struct
import sys

REQUIRED = ["composite_id", "block_id", "name", "category", "postal_code",
            "coordinates", "lod_switch_distance", "hierarchical_components"]


def validate_gltf(path):
    errs, info = [], {}
    doc = json.load(open(path, encoding="utf-8"))
    if doc.get("asset", {}).get("version") != "2.0":
        errs.append("asset.version != 2.0")
    # buffer
    bufs = doc["buffers"]
    if len(bufs) != 1:
        errs.append("expect exactly 1 buffer")
    uri = bufs[0]["uri"]
    if not uri.startswith("data:application/octet-stream;base64,"):
        errs.append("buffer uri not base64 data URI")
    data = base64.b64decode(uri.split(",", 1)[1]) if uri.startswith("data:") else b""
    if len(data) < bufs[0]["byteLength"]:
        errs.append("buffer shorter than declared byteLength")
    if bufs[0]["byteLength"] % 4:
        errs.append("buffer byteLength not 4-aligned")
    # buffer views within buffer
    for i, bv in enumerate(doc.get("bufferViews", [])):
        if bv["byteOffset"] + bv["byteLength"] > bufs[0]["byteLength"]:
            errs.append(f"bufferView {i} out of bounds")
    # accessors
    comp_size = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
    ncomp = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}
    for i, ac in enumerate(doc.get("accessors", [])):
        bv = doc["bufferViews"][ac["bufferView"]]
        need = comp_size[ac["componentType"]] * ncomp[ac["type"]] * ac["count"]
        if need > bv["byteLength"]:
            errs.append(f"accessor {i} needs {need}B > view {bv['byteLength']}B")
    # meshes/primitives/materials
    tris = 0
    mat_ids = set()
    for m in doc.get("meshes", []):
        for p in m["primitives"]:
            if p.get("mode", 4) != 4:
                errs.append("non-triangles primitive")
            acc = doc["accessors"][p["indices"]]
            tris += acc["count"] // 3
            mat_ids.add(p["material"])
            for a in ("POSITION", "NORMAL", "TEXCOORD_0"):
                if a not in p["attributes"]:
                    errs.append(f"missing attribute {a}")
    for mid in mat_ids:
        mat = doc["materials"][mid]
        pbr = mat.get("pbrMetallicRoughness")
        if not pbr or "baseColorTexture" not in pbr:
            errs.append(f"material {mid} missing PBR baseColorTexture")
    # scene graph
    scene = doc["scenes"][doc["scene"]]
    nodes = doc["nodes"]
    if len(scene["nodes"]) < 2:
        errs.append("scene too flat (expect hierarchical nodes)")
    named = [n.get("name", "") for n in nodes]
    if len([n for n in named if n]) != len(nodes):
        errs.append("unnamed nodes present")
    info["nodes"] = len(nodes)
    info["anchors"] = len([n for n in nodes if "mesh" not in n])
    # images point at atlas
    for im in doc.get("images", []):
        if im["uri"] != "texture_atlas.webp":
            errs.append(f"unexpected image uri {im['uri']}")
    info["triangles"] = tris
    info["bytes"] = len(open(path, "rb").read())
    return errs, info


def validate_webp(path):
    errs, info = [], {}
    raw = open(path, "rb").read()
    if raw[:4] != b"RIFF" or raw[8:12] != b"WEBP":
        return ["not a WebP RIFF container"], info
    chunk = raw[12:16]
    if chunk == b"VP8X":
        w = 1 + int.from_bytes(raw[24:27], "little")
        h = 1 + int.from_bytes(raw[27:30], "little")
    elif chunk == b"VP8 ":
        w = struct.unpack("<H", raw[26:28])[0] & 0x3FFF
        h = struct.unpack("<H", raw[28:30])[0] & 0x3FFF
    elif chunk == b"VP8L":
        bits = struct.unpack("<I", raw[21:25])[0]
        w = (bits & 0x3FFF) + 1
        h = ((bits >> 14) & 0x3FFF) + 1
    else:
        return [f"unknown webp chunk {chunk}"], info
    info.update({"width": w, "height": h, "chunk": chunk.decode().strip(), "bytes": len(raw)})
    if (w, h) != (1024, 1024):
        errs.append(f"atlas is {w}x{h}, expect 1024x1024")
    return errs, info


def validate_manifest(path):
    errs, info = [], {}
    m = json.load(open(path, encoding="utf-8"))
    for k in REQUIRED:
        if k not in m:
            errs.append(f"missing required field {k}")
    info["composite_id"] = m.get("composite_id")
    info["components"] = len(m.get("hierarchical_components", []))
    return errs, info


def main():
    root = sys.argv[1]
    ok = True
    for sub in ("block_manifest.json", "model_lod3.gltf", "model_lod2.gltf", "texture_atlas.webp"):
        path = f"{root}/{sub}"
        if sub.endswith(".gltf"):
            errs, info = validate_gltf(path)
        elif sub.endswith(".webp"):
            errs, info = validate_webp(path)
        else:
            errs, info = validate_manifest(path)
        status = "PASS" if not errs else "FAIL"
        if errs:
            ok = False
        print(f"[{status}] {path} {info}")
        for e in errs:
            print("   -", e)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
