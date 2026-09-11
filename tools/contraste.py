#!/usr/bin/env python3
"""Verifica contraste WCAG (AA) dos principais pares de cor do design system v3."""
def _lin(c):
    c/=255.0
    return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def lum(h):
    h=h.lstrip("#");r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return 0.2126*_lin(r)+0.7152*_lin(g)+0.0722*_lin(b)
def ratio(a,b):
    la,lb=lum(a),lum(b);hi,lo=max(la,lb),min(la,lb);return (hi+0.05)/(lo+0.05)
PAIRS=[
 ("Texto corpo (ink) sobre paper","#2a231d","#f1ebe0",4.5),
 ("Texto corpo (ink) sobre cream","#2a231d","#f6f1e8",4.5),
 ("Secundário (muted) sobre paper","#6f655b","#f1ebe0",4.5),
 ("Terciário (faint) sobre paper","#877c6b","#f1ebe0",3.0),
 ("Coral (títulos/links) sobre paper","#bd3717","#f1ebe0",4.5),
 ("Coral sobre cream","#bd3717","#f6f1e8",4.5),
 ("Branco/cream sobre coral (botão)","#f6f1e8","#bd3717",4.5),
 ("Cream sobre ink (botão escuro)","#f6f1e8","#2a231d",4.5),
 ("Texto sobre banner (branco/overlay)","#ffffff","#2b2018",4.5),
 ("Selo parcial (coral) sobre cream","#bd3717","#f6f1e8",4.5),
 ("Selo estimativa (faint) sobre paper","#877c6b","#f1ebe0",3.0),
 ("Coral sobre sand (banner claro)","#bd3717","#e9e1d3",3.0),
]
def main():
    print(f"{'PAR':44} {'RÁCIO':>7}  {'ALVO':>5}  RESULTADO");print("-"*76)
    fails=0
    for n,fg,bg,al in PAIRS:
        r=ratio(fg,bg);ok=r>=al;fails+= 0 if ok else 1
        print(f"{n:44} {r:6.2f}:1  {al:>4}:1  {'OK' if ok else 'FALHA'}")
    print("-"*76);print("TODOS PASSAM (AA)" if not fails else f"{fails} PAR(ES) ABAIXO")
    return 1 if fails else 0
if __name__=="__main__":raise SystemExit(main())
