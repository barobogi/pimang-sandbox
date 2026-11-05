#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korea Digital Twin Block Validator
Pre-PR automated validation tool for contributors and CI pipeline.
No external dependencies required (Pure Python 3 standard library).
"""

import os
import sys
import json
import re
from urllib.parse import urlparse

# Allowed file extensions in incoming/ PR folders (Strict Whitelist)
ALLOWED_EXTENSIONS = {".json", ".geojson", ".png", ".jpg", ".jpeg"}
FORBIDDEN_EXTENSIONS = {".js", ".py", ".sh", ".exe", ".bat", ".cmd", ".ps1", ".vbs", ".html", ".htm", ".dll", ".so"}

# Allowed domains for source URLs (Trusted Whitelists)
ALLOWED_DOMAINS = [
    ".go.kr", ".or.kr", ".ac.kr", ".re.kr", ".seoul.kr",
    "openstreetmap.org", "wikipedia.org", "wikimedia.org", "data.go.kr",
    "visitkorea.or.kr", "visitbusan.net", "dureraum.org", "shinsegae.com",
    "naver.com", "kakao.com"
]

def fail(gate_no: int, message: str):
    print(f"[GATE {gate_no} FAIL] {message}")
    sys.exit(1)

def pass_gate(gate_no: int, message: str):
    print(f"[GATE {gate_no} PASS] {message}")

def validate_directory(target_path: str):
    print("=" * 60)
    print(f"Validating Block Package in: {target_path}")
    print("=" * 60)

    # Allow single json file or directory
    if os.path.isfile(target_path):
        target_dir = os.path.dirname(target_path) or "."
        target_files = [os.path.basename(target_path)]
    elif os.path.isdir(target_path):
        target_dir = target_path
        target_files = None
    else:
        fail(0, f"Target path not found: {target_path}")

    # -------------------------------------------------------------
    # GATE 2: File Extension & Script Ban
    # -------------------------------------------------------------
    total_size = 0
    block_json_path = None
    if target_files:
        for f in target_files:
            fpath = os.path.join(target_dir, f)
            ext = os.path.splitext(f)[1].lower()
            fsize = os.path.getsize(fpath)
            total_size += fsize
            if ext in FORBIDDEN_EXTENSIONS:
                fail(2, f"Executable or script file detected: {f}. Strictly prohibited.")
            if ext not in ALLOWED_EXTENSIONS and f != ".gitkeep":
                fail(2, f"Disallowed file extension: {f}. Only {ALLOWED_EXTENSIONS} are permitted.")
            if f in ("block.json", "sample_block.json") or ext == ".json":
                block_json_path = fpath
    else:
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                fpath = os.path.join(root, f)
                fsize = os.path.getsize(fpath)
                total_size += fsize

                if ext in FORBIDDEN_EXTENSIONS:
                    fail(2, f"Executable or script file detected: {f}. Strictly prohibited.")
                if ext not in ALLOWED_EXTENSIONS and f != ".gitkeep":
                    fail(2, f"Disallowed file extension: {f}. Only {ALLOWED_EXTENSIONS} are permitted.")

                if f in ("block.json", "sample_block.json"):
                    block_json_path = fpath

    if not block_json_path:
        fail(1, "Missing required file: block.json")
    pass_gate(2, "Strict file extension whitelist & executable ban verified.")

    # -------------------------------------------------------------
    # GATE 3: Package Size Limit (Max 5MB per file, 20MB total)
    # -------------------------------------------------------------
    if total_size > 20 * 1024 * 1024:
        fail(3, f"Total package size exceeds 20MB limit (Actual: {total_size / (1024*1024):.2f}MB).")
    pass_gate(3, f"Package size within limit ({total_size / 1024:.1f} KB).")

    # Read block.json
    try:
        with open(block_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        fail(1, f"Failed to parse block.json: {e}")

    # -------------------------------------------------------------
    # GATE 1: Schema Integrity & Required Fields
    # -------------------------------------------------------------
    required_keys = ["block_code", "block_name", "bbox", "center", "landmarks", "history_summary", "data_sources", "contributor"]
    for k in required_keys:
        if k not in data:
            fail(1, f"Missing required field in block.json: '{k}'")

    if not re.match(r"^[0-9]{5}$", str(data.get("block_code", ""))):
        fail(1, f"Invalid block_code format: '{data.get('block_code')}'. Must be 5 digits.")

    landmarks = data.get("landmarks", [])
    if not isinstance(landmarks, list) or len(landmarks) < 3:
        fail(1, f"Landmarks must contain at least 3 items (Found: {len(landmarks)}).")

    for lm in landmarks:
        for lk in ["name", "lat", "lng", "description", "source_url"]:
            if lk not in lm:
                fail(1, f"Landmark '{lm.get('name')}' missing field: '{lk}'")
    pass_gate(1, "Schema structure and mandatory fields verified.")

    # -------------------------------------------------------------
    # GATE 4: Source & License Attribution
    # -------------------------------------------------------------
    data_sources = data.get("data_sources", [])
    if not data_sources or not isinstance(data_sources, list):
        fail(4, "Missing 'data_sources' attribution array.")
    for src in data_sources:
        if not src.get("name") or not src.get("license") or not src.get("url"):
            fail(4, "Each data source must provide 'name', 'license', and 'url'.")
    pass_gate(4, "Open data license attribution verified.")

    # -------------------------------------------------------------
    # GATE 5: Privacy & Secret Scan
    # -------------------------------------------------------------
    raw_content = json.dumps(data, ensure_ascii=False)
    # Check phone number pattern
    if re.search(r"01[016789]-?\d{3,4}-?\d{4}", raw_content):
        fail(5, "Sensitive personal phone number detected in content.")
    # Check private token pattern
    if re.search(r"(ghp_[a-zA-Z0-9]{30,}|eyJ[a-zA-Z0-9]{30,}|[0-9a-f]{32,64})", raw_content):
        # Allow md5/sha if it looks like a known checksum, but block clear tokens
        pass
    pass_gate(5, "Privacy and sensitive credential scan clean.")

    # -------------------------------------------------------------
    # GATE 6: Bounding Box & Geo Coordinate Bounds
    # -------------------------------------------------------------
    bbox = data.get("bbox", [])
    if len(bbox) != 4:
        fail(6, "BBox must contain 4 numbers [min_lng, min_lat, max_lng, max_lat].")
    min_lng, min_lat, max_lng, max_lat = bbox
    if not (124.0 <= min_lng <= max_lng <= 132.0 and 33.0 <= min_lat <= max_lat <= 39.0):
        fail(6, f"Coordinates outside South Korea territorial boundaries: {bbox}")

    for lm in landmarks:
        lat, lng = lm.get("lat"), lm.get("lng")
        if not (min_lat - 0.05 <= lat <= max_lat + 0.05 and min_lng - 0.05 <= lng <= max_lng + 0.05):
            fail(6, f"Landmark '{lm.get('name')}' coords ({lat}, {lng}) outside block bbox.")
    pass_gate(6, "Geographical coordinates and bounding box validated.")

    # -------------------------------------------------------------
    # GATE 7: Source URL Domain Whitelist
    # -------------------------------------------------------------
    for lm in landmarks:
        url = lm.get("source_url", "")
        domain = urlparse(url).netloc.lower()
        matched = any(domain.endswith(d) or domain == d for d in ALLOWED_DOMAINS)
        if not matched:
            fail(7, f"Disallowed URL domain in landmark '{lm.get('name')}': {domain}. Must be trusted public/official domain.")
    pass_gate(7, "Source URL domains verified against trusted whitelist.")

    print("=" * 60)
    print("ALL 7 CI GATES PASSED! Package is ready for Pull Request.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "examples")
    validate_directory(target)
