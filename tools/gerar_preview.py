#!/usr/bin/env python3
"""Monta um preview single-file (SPA) a partir dos assets reais do site.

Reúne CSS (com fontes embutidas em data URI), data/ritos.json, data/biblioteca.json,
o mapa SVG e o app.js (em modo embutido) num único HTML autossuficiente — para
visualização/Artifact. Não faz parte do site publicado.

Uso: python3 tools/gerar_preview.py [saida.html]
"""
import base64
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "preview.html")


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def data_uri(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return "data:font/woff2;base64," + base64.b64encode(f.read()).decode()


def main():
    css = read("assets/css/site.css")
    # embute as fontes como data URIs (o Artifact não hospeda os woff2)
    for fname in ["gloock-latin", "gloock-latin-ext", "instrumentsans-latin",
                  "instrumentsans-latin-ext", "mulish-latin", "mulish-latin-ext"]:
        css = css.replace('url("../fonts/%s.woff2")' % fname,
                          'url("%s")' % data_uri("assets/fonts/%s.woff2" % fname))

    ritos = read("data/ritos.json")
    biblio = read("data/biblioteca.json")
    mapsvg = read("assets/map/equal-earth.svg")
    appjs = read("assets/js/app.js")

    def main_of(path):
        html = read(path)
        m = re.search(r'<main id="conteudo">(.*?)</main>', html, re.S)
        return m.group(1).strip()

    home = main_of("index.html")
    cluster = main_of("clusters/pais-e-filhos/index.html")
    biblioteca = main_of("biblioteca/index.html")
    sobre = main_of("sobre/index.html")

    # reescreve links internos do "sobre" (multipage -> âncoras internas neutras)
    sobre = re.sub(r'href="\.\./sobre/#\w+"', 'href="#/sobre"', sobre)
    sobre = re.sub(r'href="\.\./clusters/[^"]+"', 'href="#/cluster/pais-e-filhos"', sobre)
    sobre = re.sub(r'href="\.\./biblioteca/"', 'href="#/biblioteca"', sobre)
    sobre = re.sub(r'href="\.\./"', 'href="#/"', sobre)

    templates = {"home": home, "cluster": cluster, "biblioteca": biblioteca, "sobre": sobre}

    header = (
        '<header class="site-head">'
        '<a class="brand" href="#/"><span class="dot" aria-hidden="true"></span>Ritos do Mundo Real</a>'
        '<nav class="nav" aria-label="Principal">'
        '<a data-nav="home" href="#/">Início</a>'
        '<a data-nav="cluster" href="#/cluster/pais-e-filhos">Clusters</a>'
        '<a data-nav="biblioteca" href="#/biblioteca">Biblioteca</a>'
        '<a data-nav="sobre" href="#/sobre">Sobre &amp; Método</a>'
        '</nav></header>'
    )
    footer = (
        '<footer class="site-foot">'
        '<div class="col"><b>Ritos do Mundo Real</b><small>Preview interativo · dados com selo de confiança · PT-BR.</small></div>'
        '<div class="cols">'
        '<div class="col"><b>Navegar</b><a href="#/">Início</a><a href="#/biblioteca">Biblioteca</a><a href="#/sobre">Sobre &amp; Método</a></div>'
        '<div class="col"><b>Ética</b><a href="#/sobre">Ritos fechados &amp; FPIC</a><a href="#/sobre">Selos de confiança</a></div>'
        '</div></footer>'
    )

    router = '''
(function(){
  var TPL = __TPL__;
  var app = document.getElementById("app");
  function setNav(page){
    document.querySelectorAll(".nav a[data-nav]").forEach(function(a){
      if(a.getAttribute("data-nav")===page) a.setAttribute("aria-current","page"); else a.removeAttribute("aria-current");
    });
  }
  function parse(){
    var h = location.hash || "#/";
    var m;
    if((m=h.match(/^#\\/cluster\\/([a-z-]+)(?:\\/([^\\/?#]+))?/))) return {page:"cluster", slug:m[1], id:m[2]};
    if(h.indexOf("#/biblioteca")===0) return {page:"biblioteca"};
    if(h.indexOf("#/sobre")===0) return {page:"sobre"};
    if(h==="#/"||h===""||h==="#") return {page:"home"};
    return null; // âncora interna (#mapa, #etica, id de rito) — não roteia
  }
  function render(){
    var r = parse();
    if(!r) return; // deixa o browser tratar âncoras internas
    document.body.setAttribute("data-page", r.page);
    if(r.slug) document.body.setAttribute("data-slug", r.slug);
    app.innerHTML = TPL[r.page];
    setNav(r.page);
    window.scrollTo(0,0);
    if(r.page==="home"){ RMR.loadRitos().then(function(d){ RMR.initHome(d); }); }
    else if(r.page==="cluster"){ RMR.loadRitos().then(function(d){ RMR.initCluster(d, r.slug); if(r.id){ setTimeout(function(){ var el=document.getElementById(r.id); if(el){ el.scrollIntoView({block:"center"}); el.classList.add("flash"); } }, 120); } }); }
    else if(r.page==="biblioteca"){ RMR.initBiblioteca(); }
    else { RMR.revealStagger && RMR.revealStagger(); }
  }
  window.addEventListener("hashchange", render);
  document.addEventListener("DOMContentLoaded", render);
  render();
})();
'''
    router = router.replace("__TPL__", json.dumps(templates, ensure_ascii=False))

    # modo Artifact: emite só o conteúdo (o Artifact embrulha head/body)
    artifact = "--artifact" in sys.argv

    body = []
    body.append('<a class="skip-link" href="#/">Pular para o conteúdo</a>')
    body.append('<div class="frame"><div class="sheet">')
    body.append(header)
    body.append('<main id="app"></main>')
    body.append(footer)
    body.append("</div></div>")
    body.append("<script>window.__RITOS__=" + ritos + ";window.__BIBLIO__=" + biblio + ";")
    body.append("window.__MAPSVG__=" + json.dumps(mapsvg) + ";</script>")
    body.append("<script>\n" + appjs + "\n</script>")
    body.append("<script>\n" + router + "\n</script>")

    html = []
    if artifact:
        html.append("<title>Ritos do Mundo Real</title>")
        html.append("<style>\n" + css + "\n</style>")
        html.extend(body)
    else:
        html.append("<!DOCTYPE html><html lang=\"pt-BR\"><head><meta charset=\"UTF-8\">")
        html.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
        html.append("<title>Ritos do Mundo Real — preview</title>")
        html.append("<style>\n" + css + "\n</style>")
        html.append("</head><body>")
        html.extend(body)
        html.append("</body></html>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print("preview escrito: %s (%.0f KB)" % (OUT, os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
