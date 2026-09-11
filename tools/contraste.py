#!/usr/bin/env python3
"""Verifica contraste WCAG (AA) dos principais pares de cor do design system."""

def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexs):
    h = hexs.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

PAIRS = [
    ("Texto corpo sobre paper", "#0e2f2f", "#f6f4ee", 4.5),
    ("Texto secundário (stone) sobre paper", "#5c6b66", "#f6f4ee", 4.5),
    ("Terciário (stone-2) sobre paper", "#7a8580", "#f6f4ee", 3.0),
    ("Texto claro sobre ink", "#eef1ec", "#0e2f2f", 4.5),
    ("Claro esmaecido sobre ink", "#a9bdb5", "#0e2f2f", 3.0),
    ("Clay (destaque) sobre ink", "#c8683c", "#0e2f2f", 3.0),
    ("Branco sobre moss (badge)", "#ffffff", "#3f6b4a", 4.5),
    ("Branco sobre clay (botão)", "#ffffff", "#c8683c", 3.0),
    ("Selo confirmado moss sobre paper", "#3f6b4a", "#f6f4ee", 3.0),
    ("Selo parcial gold sobre paper", "#8a6714", "#f6f4ee", 4.5),
    ("Alerta clay-escuro sobre paper", "#9a4a25", "#f6f4ee", 4.5),
]

def main():
    print(f"{'PAR':46} {'RÁCIO':>7}  {'ALVO':>5}  RESULTADO")
    print("-" * 78)
    fails = 0
    for nome, fg, bg, alvo in PAIRS:
        r = ratio(fg, bg)
        ok = r >= alvo
        if not ok:
            fails += 1
        print(f"{nome:46} {r:6.2f}:1  {alvo:>4}:1  {'OK' if ok else 'FALHA'}")
    print("-" * 78)
    print("TODOS PASSAM (AA)" if fails == 0 else f"{fails} PAR(ES) ABAIXO DO ALVO")
    return 1 if fails else 0

if __name__ == "__main__":
    raise SystemExit(main())
