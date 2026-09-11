#!/usr/bin/env python3
"""Gera assets/map/equal-earth.svg a partir de um GeoJSON de países (Natural Earth 110m),
usando a projeção Equal Earth (Šavrič, Patterson & Jenny, 2018).

Também imprime as constantes de projeção (SCALE, OX, OY, viewBox) para que o mesmo
posicionamento seja reproduzido em assets/js/app.js ao plotar os pins dos ritos.
"""
import json
import math
import os
import sys

A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
SQRT3 = math.sqrt(3)


def equal_earth(lon_deg, lat_deg):
    """Retorna (x, y) no espaço da projeção (unidades ~[-2.71,2.71] x [-1.31,1.31])."""
    lam = math.radians(lon_deg)
    phi = math.radians(lat_deg)
    th = math.asin((SQRT3 / 2.0) * math.sin(phi))
    den = 3.0 * (9 * A4 * th**8 + 7 * A3 * th**6 + 3 * A2 * th**2 + A1)
    x = (2.0 * SQRT3 * lam * math.cos(th)) / den
    y = A4 * th**9 + A3 * th**7 + A2 * th**3 + A1 * th
    return x, y


# extremos da projeção
X_MAX, _ = equal_earth(180, 0)
_, Y_MAX = equal_earth(0, 90)

SCALE = 200.0          # px por unidade de projeção
PAD = 12.0             # margem em px
OX = X_MAX * SCALE + PAD   # deslocamento horizontal (x=0 no centro)
OY = Y_MAX * SCALE + PAD   # deslocamento vertical
W = 2 * X_MAX * SCALE + 2 * PAD
H = 2 * Y_MAX * SCALE + 2 * PAD


def to_svg(lon, lat):
    x, y = equal_earth(lon, lat)
    sx = x * SCALE + OX
    sy = OY - y * SCALE  # y invertido (SVG cresce para baixo)
    return sx, sy


def ring_to_path(ring):
    pts = []
    for lon, lat in ring:
        sx, sy = to_svg(lon, lat)
        pts.append(f"{sx:.1f},{sy:.1f}")
    if len(pts) < 3:
        return ""
    return "M" + "L".join(pts) + "Z"


def geom_paths(geom):
    out = []
    t = geom["type"]
    if t == "Polygon":
        for ring in geom["coordinates"]:
            p = ring_to_path(ring)
            if p:
                out.append(p)
    elif t == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                p = ring_to_path(ring)
                if p:
                    out.append(p)
    return out


def graticule_border():
    """Contorno externo do mundo (meridianos ±180 + paralelos varridos)."""
    pts = []
    lat = -90
    while lat <= 90:
        pts.append(to_svg(180, lat)); lat += 2
    lon = 180
    while lon >= -180:
        pts.append(to_svg(lon, 90)); lon -= 2
    lat = 90
    while lat >= -90:
        pts.append(to_svg(-180, lat)); lat -= 2
    lon = -180
    while lon <= 180:
        pts.append(to_svg(lon, -90)); lon += 2
    d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    return d


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "tools", "world.geojson")
    with open(src) as f:
        gj = json.load(f)

    land_paths = []
    for feat in gj["features"]:
        name = feat.get("properties", {}).get("NAME") or feat.get("properties", {}).get("name", "")
        if name == "Antarctica":
            continue  # borda inferior distorcida; deixa de fora do traço de terras
        for p in geom_paths(feat["geometry"]):
            land_paths.append(p)

    border = graticule_border()

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
               f'preserveAspectRatio="xMidYMid meet" role="img" '
               f'aria-label="Mapa-múndi na projeção Equal Earth com os ritos plotados">')
    svg.append('<title>Ritos do mundo real — mapa Equal Earth</title>')
    # moldura do mundo
    svg.append(f'<path class="ee-border" d="{border}" fill="var(--map-sea, #eef1ec)" '
               f'stroke="var(--map-line, #0e2f2f)" stroke-width="1.1" stroke-linejoin="round"/>')
    # terras
    svg.append('<g class="ee-land" fill="var(--map-land, #d9e3df)" '
               'stroke="var(--map-line, #0e2f2f)" stroke-width="0.6" '
               'stroke-linejoin="round" stroke-linecap="round">')
    for p in land_paths:
        svg.append(f'<path d="{p}"/>')
    svg.append('</g>')
    # camada de pins preenchida por JS
    svg.append('<g class="ee-pins"></g>')
    svg.append('</svg>')

    out = os.path.join(root, "assets", "map", "equal-earth.svg")
    with open(out, "w") as f:
        f.write("\n".join(svg))

    size = os.path.getsize(out)
    print(f"SVG escrito: {out}  ({size/1024:.1f} KB, {len(land_paths)} paths de terra)")
    print("=== CONSTANTES DE PROJEÇÃO (copiar para app.js) ===")
    print(f"X_MAX={X_MAX:.6f}  Y_MAX={Y_MAX:.6f}")
    print(f"SCALE={SCALE}  OX={OX:.4f}  OY={OY:.4f}")
    print(f"viewBox W={W:.4f}  H={H:.4f}")
    # verificação: 3 pontos conhecidos
    print("=== VERIFICAÇÃO (lon,lat -> svgX,svgY) ===")
    for lon, lat, nome in [(0, 0, "Golfo da Guiné (0,0)"),
                            (-51.9, -23.4, "Sul do Brasil"),
                            (139.7, 35.7, "Tóquio")]:
        sx, sy = to_svg(lon, lat)
        print(f"  {nome}: ({sx:.1f}, {sy:.1f})")


if __name__ == "__main__":
    main()
