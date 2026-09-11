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
    ("Texto corpo (ink) sobre paper", "#1a2a21", "#fbf7ee", 4.5),
    ("Texto corpo (ink) sobre cream", "#1a2a21", "#fcf8f0", 4.5),
    ("Secundário (stone) sobre cream", "#55645b", "#fcf8f0", 4.5),
    ("Terciário (stone-2) sobre cream", "#79877e", "#fcf8f0", 3.0),
    ("Botão lime: lime-ink sobre lime", "#14351f", "#c6f24e", 4.5),
    ("Branco sobre velvet (botão/pill)", "#ffffff", "#7a1e2b", 4.5),
    ("Claro (on-forest) sobre forest", "#eef3ea", "#123c2c", 4.5),
    ("Claro esmaecido sobre forest", "#a7c0b2", "#123c2c", 3.0),
    ("Lima sobre forest (menu/realce)", "#c6f24e", "#123c2c", 3.0),
    ("Eyebrow velvet sobre paper", "#7a1e2b", "#fbf7ee", 4.5),
    ("Selo confirmado (moss) sobre cream", "#2f6b45", "#fcf8f0", 3.0),
    ("Selo parcial (gold) sobre cream", "#8a6714", "#fcf8f0", 4.5),
    ("Alerta/status velvet sobre cream", "#7a1e2b", "#fcf8f0", 4.5),
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
