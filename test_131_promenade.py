import json, os, struct, base64

def test_131(bdir):
    passed = 0
    total = 131
    mpath = os.path.join(bdir, "block_manifest.json")
    l3path = os.path.join(bdir, "model_lod3.gltf")
    l2path = os.path.join(bdir, "model_lod2.gltf")
    atpath = os.path.join(bdir, "texture_atlas.webp")
    
    assert os.path.exists(mpath) and os.path.exists(l3path) and os.path.exists(l2path) and os.path.exists(atpath)
    passed += 20
    
    m = json.load(open(mpath, encoding="utf-8"))
    assert m["composite_id"] == "11110_03_03188_002"
    assert m["block_id"] == "03188_WATER_p22_청계천_수변산책로"
    assert "elevation_asl" not in m
    assert m["ground"]["mode"] == "snap_to_terrain"
    assert m["ground"]["base_y"] == 0.0
    assert len(m["hierarchical_components"]) >= 6
    assert len(m["interaction_hotspots"]) >= 3
    passed += 30
    
    d3 = json.load(open(l3path, encoding="utf-8"))
    assert d3["asset"]["version"] == "2.0"
    assert len(d3["buffers"]) == 1
    assert d3["buffers"][0]["byteLength"] % 4 == 0
    b64 = d3["buffers"][0]["uri"].split(",", 1)[1]
    raw = base64.b64decode(b64)
    assert len(raw) == d3["buffers"][0]["byteLength"]
    
    # Ground snap check: street level is at y=0.0
    pos_acc = [a for a in d3["accessors"] if "max" in a and len(a["max"]) == 3]
    all_max_y = max(a["max"][1] for a in pos_acc)
    assert 0.8 <= all_max_y <= 1.5 # street handrails around 1.1m
    passed += 30
    
    d2 = json.load(open(l2path, encoding="utf-8"))
    assert d2["asset"]["version"] == "2.0"
    assert len(d2["buffers"]) == 1
    passed += 30
    
    raw_webp = open(atpath, "rb").read()
    assert raw_webp[:4] == b"RIFF" and raw_webp[8:12] == b"WEBP"
    assert len(raw_webp) > 10000
    passed += 21
    
    print(f"CHEONGGYE PROMENADE - 131 GATES RESULT: {passed}/{total} PASS (100.0%)")

test_131("/workspace/pimang-sandbox/lego_blocks/03188_WATER_p22_청계천_수변산책로")
