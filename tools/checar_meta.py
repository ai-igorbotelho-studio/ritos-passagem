#!/usr/bin/env python3
"""Higiene de <head> em cada HTML: lang, title, description, viewport, canonical, og:image, favicon.
Uso: python3 tools/checar_meta.py  (varre a árvore) """
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHECKS = [
    ("lang pt-BR", re.compile(r'<html[^>]+lang="pt-BR"', re.I)),
    ("<title>", re.compile(r"<title>[^<]{10,}</title>", re.I)),
    ("meta description", re.compile(r'name="description"[^>]+content="[^"]{40,}"', re.I)),
    ("viewport", re.compile(r'name="viewport"', re.I)),
    ("canonical", re.compile(r'rel="canonical"', re.I)),
    ("og:title", re.compile(r'property="og:title"', re.I)),
    ("og:image", re.compile(r'property="og:image"', re.I)),
    ("favicon", re.compile(r'rel="icon"', re.I)),
    ("charset", re.compile(r'charset="UTF-8"', re.I)),
]

def main():
    htmls = []
    for dp, _, fs in os.walk(ROOT):
        if "/.git" in dp:
            continue
        for f in fs:
            if f.endswith(".html"):
                htmls.append(os.path.join(dp, f))
    htmls.sort()
    fails = 0
    for path in htmls:
        with open(path) as fh:
            html = fh.read()
        rel = os.path.relpath(path, ROOT)
        missing = [name for name, rx in CHECKS if not rx.search(html)]
        if missing:
            fails += 1
            print(f"[FALHA] {rel}: falta {', '.join(missing)}")
        else:
            print(f"[  OK ] {rel}")
    print("-" * 60)
    print("Higiene de meta: TUDO OK" if fails == 0 else f"{fails} arquivo(s) com pendências")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
