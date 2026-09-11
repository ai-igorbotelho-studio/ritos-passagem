# Ritos do Mundo Real

Site estático leve — pesquisa + visualização + instrumento de decisão sobre ritos de
passagem e rituais coletivos do mundo. HTML + CSS + JavaScript vanilla, **sem framework e
sem build**. Um único `data/ritos.json` alimenta todas as páginas.

## Estrutura

```
index.html                      HOME (hero + mapa, números, clusters, filtro)
clusters/<slug>/index.html      6 páginas de cluster (mesma template, renderizadas por JS)
biblioteca/index.html           Biblioteca de conhecimento
sobre/index.html                Método, selos de confiança, ética, créditos do mapa
assets/css/site.css             Design system (paleta fixa, tipografia)
assets/js/app.js                Motor: carrega o JSON, plota pins, tabelas e filtros
assets/fonts/*.woff2            Gloock · Instrument Sans · Mulish (self-hosted, OFL)
assets/map/equal-earth.svg      Mapa-múndi em projeção Equal Earth (gerado, domínio público)
data/ritos.json                 Dataset de 42 ritos (fonte única de verdade)
data/biblioteca.json            Fontes multimídia por cluster
tools/                          Scripts Python de geração e auditoria (não vão ao ar)
_headers _redirects robots.txt sitemap.xml favicon.svg og.jpg
```

## Rodar localmente

Como o site usa `fetch()` para carregar os JSON e o SVG do mapa, sirva por HTTP
(não abra o arquivo direto):

```bash
python3 -m http.server 8099
# abra http://localhost:8099/
```

## Ferramentas (Python, opcionais)

```bash
python3 tools/validar_dados.py     # valida enums, campos e imprime contagens
python3 tools/contraste.py         # contraste WCAG AA de todos os pares de cor
python3 tools/checar_meta.py       # higiene de <head> em cada HTML
python3 tools/gerar_mapa.py        # regenera assets/map/equal-earth.svg a partir de tools/world.geojson
```

`tools/world.geojson` é o Natural Earth 110m (domínio público), usado apenas como
entrada do gerador do mapa.

## Tipografia

- **Gloock** — títulos (display serif de alto contraste)
- **Instrument Sans** — subtítulos, interface, pílulas e rótulos
- **Mulish** — corpo de texto (peso leve)

## Selos de confiança

Todo número de "participantes/ano" carrega um selo: ✅ confirmado (fonte oficial),
⚠️ parcial (ordem de grandeza), ❓ estimativa (sem dado público). A cor nunca aparece
sozinha — sempre com texto.

## Deploy — Cloudflare Pages

- Framework preset: **None**
- Build command: *(vazio)*
- Output directory: `/`
- Deploy automático a cada push em `main`. Sem Node em produção.

Cabeçalhos de segurança e cache em `_headers`; normalização de barra final em `_redirects`.
