#!/usr/bin/env python3
"""Valida data/ritos.json: enums, campos obrigatórios, coordenadas e imprime contagens."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = {"muito_popular", "conhecido", "exotico"}
ACESSO = {"aberto", "aberto_com_guia", "restrito", "fechado"}
CONF = {"confirmado", "parcial", "estimativa"}
CLUSTERS = {"pais-e-filhos", "maes-e-filhas", "casais", "avos-e-netos",
            "coletivos-e-peregrinacoes", "natureza-animais-e-plantas"}
REQ = ["id", "nome", "povo_ou_tradicao", "pais", "lat", "lon", "clusters",
       "descricao", "epoca", "memoravel", "status", "espiritual",
       "participantes_ano", "acesso_visitante"]

def main():
    with open(os.path.join(ROOT, "data", "ritos.json")) as f:
        ritos = json.load(f)
    errs = []
    ids = set()
    for r in ritos:
        rid = r.get("id", "?")
        for k in REQ:
            if k not in r:
                errs.append(f"{rid}: falta campo '{k}'")
        if rid in ids:
            errs.append(f"{rid}: id duplicado")
        ids.add(rid)
        if r.get("status") not in STATUS:
            errs.append(f"{rid}: status inválido '{r.get('status')}'")
        if r.get("acesso_visitante") not in ACESSO:
            errs.append(f"{rid}: acesso inválido '{r.get('acesso_visitante')}'")
        pa = r.get("participantes_ano", {})
        if pa.get("confianca") not in CONF:
            errs.append(f"{rid}: confianca inválida '{pa.get('confianca')}'")
        for c in r.get("clusters", []):
            if c not in CLUSTERS:
                errs.append(f"{rid}: cluster desconhecido '{c}'")
        if not (-90 <= r.get("lat", 999) <= 90) or not (-180 <= r.get("lon", 999) <= 180):
            errs.append(f"{rid}: lat/lon fora de faixa")
        if not isinstance(r.get("espiritual"), bool):
            errs.append(f"{rid}: 'espiritual' deve ser booleano")

    # contagens
    paises = {r["pais"] for r in ritos}
    por_cluster = {c: sum(1 for r in ritos if c in r["clusters"]) for c in CLUSTERS}
    com_video = sum(1 for r in ritos if r.get("video"))
    conf_dist = {}
    for r in ritos:
        c = r["participantes_ano"]["confianca"]
        conf_dist[c] = conf_dist.get(c, 0) + 1

    print(f"ritos: {len(ritos)} | países: {len(paises)} | com vídeo: {com_video} | sem vídeo: {len(ritos)-com_video}")
    print("por cluster:", por_cluster)
    print("confiança:", conf_dist)
    if errs:
        print("\nERROS:")
        for e in errs:
            print("  -", e)
        return 1
    print("\nOK — dados válidos.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
