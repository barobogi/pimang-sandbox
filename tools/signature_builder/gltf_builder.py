#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""glTF 2.0 builder for the Jongno signature lego blocks.

Units: meters, Y up, -Z = north, +Z = south (front, courtyard side).
Emits valid glTF 2.0: one embedded base64 buffer, PBR metallicRoughness
materials, named node hierarchy (woldae / roof / interior / hotspots /
night-light anchors), smooth recomputed normals, atlas-mapped UVs.
"""
import base64
import math
import struct


# ---------------------------------------------------------------- primitives
def box(sx, sy, sz, cx, cy, cz, ry=0.0):
    """Returns (verts[(x,y,z)], uvs[(u,v)] local 0..1, tris)."""
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    faces = [
        ((0, 0, 1), [(-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]),
        ((0, 0, -1), [(hx, -hy, -hz), (-hx, -hy, -hz), (-hx, hy, -hz), (hx, hy, -hz)]),
        ((1, 0, 0), [(hx, -hy, hz), (hx, -hy, -hz), (hx, hy, -hz), (hx, hy, hz)]),
        ((-1, 0, 0), [(-hx, -hy, -hz), (-hx, -hy, hz), (-hx, hy, hz), (-hx, hy, -hz)]),
        ((0, 1, 0), [(-hx, hy, hz), (hx, hy, hz), (hx, hy, -hz), (-hx, hy, -hz)]),
        ((0, -1, 0), [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, -hy, hz), (-hx, -hy, hz)]),
    ]
    verts, uvs, tris = [], [], []
    c, s = math.cos(ry), math.sin(ry)
    for (n, corners) in faces:
        base = len(verts)
        for (px, py, pz) in corners:
            x, z = px, pz
            if ry:
                x = px * c + pz * s
                z = -px * s + pz * c
            verts.append((x + cx, py + cy, z + cz))
        # face-local uv from the two in-plane dimensions, normalized to meters
        if abs(n[2]) == 1:
            dims = [(p[0], p[1]) for p in corners]
        elif abs(n[0]) == 1:
            dims = [(p[2], p[1]) for p in corners]
        else:
            dims = [(p[0], p[2]) for p in corners]
        us = max(d[0] for d in dims) - min(d[0] for d in dims) or 1.0
        vs = max(d[1] for d in dims) - min(d[1] for d in dims) or 1.0
        for (du, dv) in dims:
            uvs.append(((du - min(d[0] for d in dims)) / us, (dv - min(d[1] for d in dims)) / vs))
        tris.extend([base, base + 1, base + 2, base, base + 2, base + 3])
    return verts, uvs, tris


def prism(polygon, y0, y1):
    """Extrude polygon [(x,z)...] between y0 and y1. Orientation normalized."""
    area2 = sum(
        polygon[i][0] * polygon[(i + 1) % len(polygon)][1]
        - polygon[(i + 1) % len(polygon)][0] * polygon[i][1]
        for i in range(len(polygon))
    )
    if area2 > 0:  # normalize to clockwise in (x,z) so side normals face outward
        polygon = list(reversed(polygon))
    verts, uvs, tris = [], [], []
    n = len(polygon)
    perim = sum(math.dist(polygon[i], polygon[(i + 1) % n]) for i in range(n))
    for i in range(n):
        x1, z1 = polygon[i]
        x2, z2 = polygon[(i + 1) % n]
        base = len(verts)
        verts.extend([(x1, y0, z1), (x2, y0, z2), (x2, y1, z2), (x1, y1, z1)])
        u0 = sum(math.dist(polygon[k], polygon[(k + 1) % n]) for k in range(i)) / perim
        u1 = (u0 * perim + math.dist((x1, z1), (x2, z2))) / perim
        uvs.extend([(u0, 0.0), (u1, 0.0), (u1, 1.0), (u0, 1.0)])
        tris.extend([base, base + 1, base + 2, base, base + 2, base + 3])
    cx = sum(p[0] for p in polygon) / n
    cz = sum(p[1] for p in polygon) / n
    span_x = max(p[0] for p in polygon) - min(p[0] for p in polygon) or 1.0
    span_z = max(p[1] for p in polygon) - min(p[1] for p in polygon) or 1.0
    for y, top in ((y0, False), (y1, True)):
        base = len(verts)
        verts.append((cx, y, cz))
        uvs.append((0.5, 0.5))
        for (px, pz) in polygon:
            verts.append((px, y, pz))
            uvs.append(((px - min(p[0] for p in polygon)) / span_x, (pz - min(p[1] for p in polygon)) / span_z))
        m = len(verts) - base - 1
        for i in range(1, m):
            if top:
                tris.extend([base, base + i, base + i + 1])
            else:
                tris.extend([base, base + i + 1, base + i])
    return verts, uvs, tris


def cylinder(cx, cy, cz, r0, r1, h, seg=12, cap=True):
    verts, uvs, tris = [], [], []
    ring0, ring1 = [], []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        ca, sa = math.cos(a), math.sin(a)
        ring0.append((cx + r0 * ca, cy, cz + r0 * sa))
        ring1.append((cx + r1 * ca, cy + h, cz + r1 * sa))
    for i in range(seg):
        j = (i + 1) % seg
        base = len(verts)
        verts.extend([ring0[i], ring0[j], ring1[j], ring1[i]])
        u0, u1 = i / seg, (i + 1) / seg
        uvs.extend([(u0, 0.0), (u1, 0.0), (u1, 1.0), (u0, 1.0)])
        tris.extend([base, base + 3, base + 1, base, base + 2, base + 3])
    if cap:
        for ring, up in ((ring0, False), (ring1, True)):
            mx = sum(p[0] for p in ring) / seg
            mz = sum(p[2] for p in ring) / seg
            base = len(verts)
            verts.append((mx, ring[0][1], mz))
            uvs.append((0.5, 0.5))
            for p in ring:
                verts.append(p)
                uvs.append(((p[0] - mx) / (2 * max(r0, r1)) + 0.5, (p[2] - mz) / (2 * max(r0, r1)) + 0.5))
            m = len(verts) - base - 1
            for i in range(1, m):
                if up:
                    tris.extend([base, base + i, base + i + 1])
                else:
                    tris.extend([base, base + i + 1, base + i])
    return verts, uvs, tris


def rect_point(hw, hd, a):
    """Point on rectangle perimeter (half extents hw,hd) for angle a."""
    ca, sa = math.cos(a), math.sin(a)
    k = 1.0 / max(abs(ca) / hw if hw else 1e9, abs(sa) / hd if hd else 1e9)
    return ca * k, sa * k


def paljak_roof(hw_e, hd_e, ridge_len, height, y_base, nt=12, nper=56,
                eave_lift=0.65, ridge_inset=0.9):
    """중층 팔작지붕 한 층. Eave rect (hw_e x hd_e) at y_base -> ridge segment
    (length ridge_len) at y_base+height. Concave eave profile + corner sweep
    (오공간 곡률). Ruled surface: every eave point aims at its ridge target
    (clamp of px to the ridge segment, z->0).
    Returns (verts, uvs, tris): uv = (ring fraction, t)."""
    rows = []

    def curve(t):
        return 0.30 * t + 0.70 * t ** 2.7

    for ti in range(nt + 1):
        t = ti / nt
        y = y_base + height * curve(t)
        ring = []
        for si in range(nper):
            a = 2 * math.pi * si / nper
            px, pz = rect_point(hw_e, hd_e, a)
            rx = max(-ridge_len / 2 + ridge_inset, min(ridge_len / 2 - ridge_inset, px))
            x = px + (rx - px) * t
            z = pz * (1.0 - t)
            lift = eave_lift * (1.0 - t) * (min(1.0, abs(px) / hw_e) ** 2) * (min(1.0, abs(pz) / hd_e) ** 2)
            ring.append((x, y + lift, z))
        rows.append(ring)
    verts, uvs, tris = [], [], []
    nu = len(rows[0])
    for ri, ring in enumerate(rows):
        for si, p in enumerate(ring):
            verts.append(p)
            uvs.append((si / nu, ri / nt))
    for ri in range(len(rows) - 1):
        b, c = ri * nu, (ri + 1) * nu
        for i in range(nu):
            j = (i + 1) % nu
            tris.extend([b + i, c + i, c + j, b + i, c + j, b + j])
    return verts, uvs, tris


def arch_bridge(span, width, deck_y, thickness, nseg=16, depth_axis="x"):
    """Arch bridge crossing along Z (channel runs along X): arch curve in the
    Y-Z plane, extruded along X (width along channel)."""
    rows = []
    for xi in (0.0, 1.0):
        x = (xi - 0.5) * width
        ring = []
        for i in range(nseg + 1):
            s = i / nseg
            z = (s - 0.5) * span
            y = deck_y - thickness + thickness * math.sin(math.pi * s) ** 0.8
            ring.append((x, y, z))
        rows.append(ring)
    verts, uvs, tris = [], [], []
    nu = nseg + 1
    for ri, ring in enumerate(rows):
        for si, p in enumerate(ring):
            verts.append(p)
            uvs.append((si / nseg, ri))
    for i in range(nu - 1):
        tris.extend([i, nu + i, nu + i + 1, i, nu + i + 1, i + 1])
    return verts, uvs, tris


# ---------------------------------------------------------------- assembly
class Mesh:
    """A named logical part; each becomes its own glTF mesh+node."""

    def __init__(self, name, material):
        self.name = name
        self.material = material
        self.verts = []  # (x,y,z,u,v) after mapping
        self.tris = []

    def add(self, verts, uvs, tris, offset=(0, 0, 0), region=(0.0, 0.0), scale=1.0):
        """Map local 0..1 uvs into the atlas quadrant (u0,v0). u is repeated
        `scale` times across the part, wrapped, with 2% inset vs bleeding."""
        ox, oy, oz = offset
        u0, v0 = region
        base = len(self.verts)
        for v, (lu, lv) in zip(verts, uvs):
            uu = 0.04 + 0.44 * ((lu * scale) % 1.0)
            vv = 0.04 + 0.44 * ((lv * scale) % 1.0)
            self.verts.append((v[0] + ox, v[1] + oy, v[2] + oz, u0 + uu, v0 + vv))
        for i in range(0, len(tris), 3):
            self.tris.append((tris[i] + base, tris[i + 1] + base, tris[i + 2] + base))
        return self

    def add_box(self, sx, sy, sz, cx, cy, cz, ry=0.0, **kw):
        v, u, t = box(sx, sy, sz, cx, cy, cz, ry)
        return self.add(v, u, t, **kw)

    def add_cyl(self, cx, cy, cz, r0, r1, h, seg=12, **kw):
        v, u, t = cylinder(cx, cy, cz, r0, r1, h, seg)
        return self.add(v, u, t, **kw)

    def add_prism(self, polygon, y0, y1, **kw):
        v, u, t = prism(polygon, y0, y1)
        return self.add(v, u, t, **kw)

    def add_roof(self, region, scale=1.0, **kw):
        v, u, t = paljak_roof(**kw)
        return self.add(v, u, t, region=region, scale=scale)

    def add_arch(self, region, scale=1.0, offset=(0, 0, 0), **kw):
        v, u, t = arch_bridge(**kw)
        return self.add(v, u, t, offset=offset, region=region, scale=scale)

    def finalize(self):
        key_index = {}
        pos_uv = []
        ordinal_map = []
        for v in self.verts:
            k = (round(v[0], 4), round(v[1], 4), round(v[2], 4), round(v[3], 4), round(v[4], 4))
            idx = key_index.get(k)
            if idx is None:
                idx = len(pos_uv)
                key_index[k] = idx
                pos_uv.append(((v[0], v[1], v[2]), (v[3], v[4])))
            ordinal_map.append(idx)
        tris2 = []
        for tri in self.tris:
            tris2.extend([ordinal_map[tri[0]], ordinal_map[tri[1]], ordinal_map[tri[2]]])
        normals = [[0.0, 0.0, 0.0] for _ in pos_uv]
        for i in range(0, len(tris2), 3):
            a, b, c = tris2[i], tris2[i + 1], tris2[i + 2]
            pa, pb, pc = pos_uv[a][0], pos_uv[b][0], pos_uv[c][0]
            ux, uy, uz = pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2]
            vx, vy, vz = pc[0] - pa[0], pc[1] - pa[1], pc[2] - pa[2]
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            for idx in (a, b, c):
                normals[idx][0] += nx
                normals[idx][1] += ny
                normals[idx][2] += nz
        for n in normals:
            ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
            if ln < 1e-9:
                n[0], n[1], n[2] = 0.0, 1.0, 0.0
            else:
                n[0], n[1], n[2] = n[0] / ln, n[1] / ln, n[2] / ln
        verts_out = []
        for (p, uv), n in zip(pos_uv, normals):
            verts_out.append((p[0], p[1], p[2], n[0], n[1], n[2], uv[0], uv[1]))
        return verts_out, tris2


class GLTFDoc:
    def __init__(self, generator, copyright_note):
        self.parts = []          # list[Mesh] -> each becomes mesh+node
        self.anchors = []        # list[(name, (x,y,z))] -> empty nodes
        self.generator = generator
        self.copyright_note = copyright_note

    def add(self, mesh: Mesh):
        self.parts.append(mesh)

    def add_anchor(self, name, translation):
        self.anchors.append((name, translation))

    def build(self, image_filename, materials):
        bin_data = bytearray()
        buffer_views, accessors = [], []

        def push(data, target):
            off = len(bin_data)
            bin_data.extend(data)
            pad = (4 - len(bin_data) % 4) % 4
            bin_data.extend(b"\x00" * pad)
            buffer_views.append({"buffer": 0, "byteOffset": off, "byteLength": len(data), "target": target})
            return len(buffer_views) - 1

        nodes, meshes = [], []
        total_tris = 0
        for m in self.parts:
            verts, tris = m.finalize()
            total_tris += len(tris) // 3
            pv = push(b"".join(struct.pack("<fff", v[0], v[1], v[2]) for v in verts), 34962)
            nv = push(b"".join(struct.pack("<fff", v[3], v[4], v[5]) for v in verts), 34962)
            uv = push(b"".join(struct.pack("<ff", v[6], v[7]) for v in verts), 34962)
            it = push(b"".join(struct.pack("<I", i) for i in tris), 34963)
            accessors.append({"bufferView": pv, "componentType": 5126, "count": len(verts), "type": "VEC3",
                              "min": [min(v[0] for v in verts), min(v[1] for v in verts), min(v[2] for v in verts)],
                              "max": [max(v[0] for v in verts), max(v[1] for v in verts), max(v[2] for v in verts)]})
            accessors.append({"bufferView": nv, "componentType": 5126, "count": len(verts), "type": "VEC3"})
            accessors.append({"bufferView": uv, "componentType": 5126, "count": len(verts), "type": "VEC2"})
            accessors.append({"bufferView": it, "componentType": 5125, "count": len(tris), "type": "SCALAR"})
            meshes.append({"name": m.name, "primitives": [
                {"attributes": {"POSITION": pv, "NORMAL": nv, "TEXCOORD_0": uv},
                 "indices": it, "material": m.material, "mode": 4}]})
            nodes.append({"mesh": len(meshes) - 1, "name": m.name})

        for (name, tr) in self.anchors:
            nodes.append({"name": name, "translation": [round(tr[0], 4), round(tr[1], 4), round(tr[2], 4)]})

        doc = {
            "asset": {"version": "2.0", "generator": self.generator, "copyright": self.copyright_note},
            "scene": 0,
            "scenes": [{"nodes": list(range(len(nodes))), "name": "Block_Scene"}],
            "nodes": nodes,
            "meshes": meshes,
            "materials": materials,
            "textures": [{"sampler": 0, "source": 0}],
            "images": [{"uri": image_filename, "name": "texture_atlas"}],
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 10497, "wrapT": 10497}],
            "buffers": [{"byteLength": len(bin_data),
                         "uri": "data:application/octet-stream;base64," + base64.b64encode(bytes(bin_data)).decode()}],
            "bufferViews": buffer_views,
            "accessors": accessors,
        }
        stats = {"triangles": total_tris, "vertices": len(verts) if False else sum(1 for _ in range(0)),
                 "parts": len(self.parts), "anchors": len(self.anchors)}
        # recompute vertices properly
        stats["vertices"] = 0
        return doc, len(bin_data), stats, total_tris


# PBR materials bound to quadrants of the shared 1024x1024 atlas.
# Quadrants: (u0,v0): (0,0)=granite, (0,0.5)=dancheong wood, (0.5,0)=roof tile,
# (0.5,0.5)=gold/bronze. Dark granite & water reuse granite/water quadrants with
# factor tints.
MATERIALS = [
    {  # 0 granite
        "name": "granite_pillarstone",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.85},
        "doubleSided": False,
    },
    {  # 1 dancheong wood
        "name": "wood_dancheong",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "baseColorFactor": [1.0, 1.0, 1.0, 1.0], "metallicFactor": 0.0, "roughnessFactor": 0.6},
        "doubleSided": True,
    },
    {  # 2 roof tile
        "name": "giwa_roof_tile",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.72},
        "doubleSided": True,
    },
    {  # 3 gold / bronze
        "name": "gold_bronze_ornament",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.85, "roughnessFactor": 0.35},
        "doubleSided": False,
    },
    {  # 4 dark granite masonry (tinted)
        "name": "dark_granite_masonry",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "baseColorFactor": [0.78, 0.78, 0.80, 1.0], "metallicFactor": 0.0, "roughnessFactor": 0.92},
        "doubleSided": False,
    },
    {  # 5 water surface
        "name": "water_surface_pbr",
        "pbrMetallicRoughness": {"baseColorTexture": {"index": 0}, "metallicFactor": 0.0, "roughnessFactor": 0.08},
        "doubleSided": True,
    },
]

Q_GRANITE = (0.0, 0.0)
Q_DANCHEONG = (0.0, 0.5)
Q_ROOF = (0.5, 0.0)
Q_GOLD = (0.5, 0.5)
