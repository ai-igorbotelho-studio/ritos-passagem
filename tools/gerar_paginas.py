#!/usr/bin/env python3
"""Gera as páginas internas (clusters, biblioteca, sobre) com o mesmo 'chrome'
(header + menu overlay + rodapé + bloco do autor) da home. index.html é mantida à mão.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLUSTERS = [
    ("pais-e-filhos", "Pais e filhos", "Rituais de pai, avô e filho — iniciação masculina, do salto do gado à leitura da Torá."),
    ("maes-e-filhas", "Mães e filhas", "Rituais de mãe, madrinha e tias com a filha — menarca e feminilidade, de Kinaaldá a quinceañera."),
    ("casais", "Casais", "Rituais de casamento e união de famílias — do fogo sagrado hindu ao chá servido aos sogros."),
    ("avos-e-netos", "Avós e netos", "Nascimento, nomeação e primeira comida — o que a geração mais velha oferece à mais nova."),
    ("coletivos-e-peregrinacoes", "Coletivos e peregrinações", "Multidão, cidade e fé — do Kumbh Mela ao Caminho de Santiago."),
    ("natureza-animais-e-plantas", "Natureza, animais e plantas", "Rituais mediados por bicho, planta, rio ou colheita — quando o mundo não humano conduz a passagem."),
]


def head(base, title, desc, canon):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://ritos.exemplo/{canon}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://ritos.exemplo/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://images.unsplash.com" crossorigin>
  <link rel="preload" href="{base}assets/fonts/gloock-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{base}assets/fonts/mulish-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{base}assets/css/site.css">
</head>'''


def chrome_header(base):
    return f'''      <header class="site-head">
        <a class="brand" href="{base}"><span class="mark" aria-hidden="true">✳</span>Ritos do Mundo Real</a>
        <div class="head-actions">
          <a class="btn btn--lime" href="https://calendly.com/ferttil/meet" target="_blank" rel="noopener">Agendar conversa</a>
          <button class="menu-btn" id="menu-toggle" aria-expanded="false" aria-controls="menu-overlay">
            <span class="bars" aria-hidden="true"><i></i><i></i><i></i></span> Menu
          </button>
        </div>
      </header>

      <div class="menu-overlay" id="menu-overlay" role="dialog" aria-modal="true" aria-label="Menu de navegação">
        <div class="menu-top">
          <a class="brand" href="{base}"><span class="mark" aria-hidden="true">✳</span>Ritos do Mundo Real</a>
          <button class="menu-close" id="menu-close" aria-label="Fechar menu">✕</button>
        </div>
        <div class="menu-body">
          <nav class="menu-nav" aria-label="Páginas">
            <a href="{base}">Início</a>
            <a href="{base}clusters/pais-e-filhos/">Rituais pelo mundo</a>
            <a href="{base}biblioteca/">Biblioteca</a>
            <a href="{base}sobre/">Sobre &amp; Método</a>
          </nav>
          <div class="menu-sub">
            <h3>Visualizar cada cluster</h3>
            <div class="rl">
              <a href="{base}clusters/pais-e-filhos/">Pais e filhos</a>
              <a href="{base}clusters/maes-e-filhas/">Mães e filhas</a>
              <a href="{base}clusters/casais/">Casais</a>
              <a href="{base}clusters/avos-e-netos/">Avós e netos</a>
              <a href="{base}clusters/coletivos-e-peregrinacoes/">Coletivos e peregrinações</a>
              <a href="{base}clusters/natureza-animais-e-plantas/">Natureza, animais e plantas</a>
            </div>
            <div class="menu-cta">
              <a class="btn btn--lime" href="https://calendly.com/ferttil/meet" target="_blank" rel="noopener">Agendar uma conversa →</a>
            </div>
          </div>
        </div>
      </div>'''


def chrome_footer(base):
    return f'''      <footer class="site-foot">
        <div class="col"><b>Ritos do Mundo Real</b><small>Pesquisa + visualização + instrumento de decisão.<br>Dados com selo de confiança · PT-BR.</small></div>
        <div class="cols">
          <div class="col"><b>Navegar</b><a href="{base}">Início</a><a href="{base}clusters/pais-e-filhos/">Rituais pelo mundo</a><a href="{base}biblioteca/">Biblioteca</a><a href="{base}sobre/">Sobre &amp; Método</a></div>
          <div class="col"><b>Ética</b><a href="{base}sobre/#etica">Rituais fechados &amp; FPIC</a><a href="{base}sobre/#selos">Selos de confiança</a></div>
        </div>
      </footer>

      <section class="author" aria-label="Sobre esta ferramenta">
        <div class="author__band">
          <p class="eyebrow">Sobre esta ferramenta</p>
          <p>Essa ferramenta é independente, um projeto autônomo e parte de uma jornada de <strong style="color:#fff">Transição</strong>. Pesquisa, planejamento, análise, modelagem, criação e publicação — co-criados conectando fontes abertas, usando inteligência artificial e validação rigorosa.</p>
        </div>
        <div class="author__card">
          <div class="author__who">
            <div class="author__photo" data-mono="IB"><img id="author-photo" src="{base}assets/img/igor-botelho.jpg" alt="Igor Botelho" loading="lazy"></div>
            <div>
              <h3 class="author__name">Igor Botelho</h3>
              <p class="author__loc">Waiheke Island, Auckland · Nova Zelândia</p>
              <div class="author__links">
                <a href="mailto:igor@ferttil.com">✉ igor@ferttil.com</a>
                <a href="https://www.igorbotelho.com" target="_blank" rel="noopener">◎ www.igorbotelho.com</a>
                <a href="https://linkedin.com/in/bernardesigor" target="_blank" rel="noopener">in linkedin.com/in/bernardesigor</a>
              </div>
            </div>
          </div>
          <div class="author__cta">
            <a class="btn btn--forest" href="https://calendly.com/ferttil/meet" target="_blank" rel="noopener">Agendar uma conversa →</a>
            <a class="btn btn--soft" href="mailto:igor@ferttil.com">Enviar um e-mail</a>
          </div>
        </div>
        <p class="author__note">Agendamento via Calendly · calendly.com/ferttil/meet</p>
      </section>'''


def page(base, title, desc, canon, body, data_attrs=""):
    return (head(base, title, desc, canon) + "\n"
            + f'<body data-page="{data_attrs}">\n'
            + '  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>\n'
            + '  <div class="frame">\n    <div class="sheet">\n\n'
            + chrome_header(base) + "\n\n"
            + '      <main id="conteudo">\n' + body + '\n      </main>\n\n'
            + chrome_footer(base) + "\n\n"
            + f'    </div>\n  </div>\n  <script src="{base}assets/js/app.js"></script>\n</body>\n</html>\n')


# ---------- CLUSTER ----------
def cluster_body():
    return '''        <section class="section wrap">
          <div class="cluster-head">
            <div>
              <p class="eyebrow">Rituais pelo mundo · quem participa</p>
              <h1 data-cluster-nome style="font-size:clamp(2rem,4.6vw,3.6rem)"></h1>
              <p class="lede" id="cluster-frase"></p>
              <p style="color:var(--stone);font-family:var(--font-ui);font-size:.9rem">A tabela abaixo é gerada a partir de <code>data/ritos.json</code>. Ordene por qualquer coluna. Cada número traz seu selo de confiança.</p>
            </div>
            <div class="minimap"><div id="cluster-map" aria-label="Mini-mapa com os rituais deste cluster"></div></div>
          </div>
          <p id="data-error" role="alert" hidden style="color:var(--velvet)"></p>
        </section>

        <section class="section--tight wrap" aria-label="Tabela de rituais do cluster">
          <div class="table-wrap">
            <table class="ritos">
              <thead id="ritos-head">
                <tr>
                  <th scope="col"><button data-key="nome" type="button">Rito <span class="arrow" aria-hidden="true">↕</span></button></th>
                  <th scope="col"><button data-key="local" type="button">Local <span class="arrow" aria-hidden="true">↕</span></button></th>
                  <th scope="col"><button data-key="epoca" type="button">Época <span class="arrow" aria-hidden="true">↕</span></button></th>
                  <th scope="col"><button data-key="status" type="button">Status <span class="arrow" aria-hidden="true">↕</span></button></th>
                  <th scope="col" class="center"><button data-key="espiritual" type="button">Espiritual <span class="arrow" aria-hidden="true">↕</span></button></th>
                  <th scope="col">Participantes/ano</th>
                  <th scope="col"><button data-key="acesso" type="button">Acesso <span class="arrow" aria-hidden="true">↕</span></button></th>
                  <th scope="col" class="center">Vídeo</th>
                </tr>
              </thead>
              <tbody id="ritos-body"></tbody>
            </table>
          </div>
        </section>

        <section class="section wrap prose" aria-labelledby="curio-h">
          <p class="eyebrow">Curiosidades</p>
          <h2 id="curio-h" class="h-sec">Para guardar</h2>
          <ul class="curio" id="curiosidades"></ul>
        </section>

        <section class="section wrap prose" aria-labelledby="entorno-h">
          <p class="eyebrow">Turismo nos arredores</p>
          <h2 id="entorno-h" class="h-sec">O que ver perto — e com que cuidado</h2>
          <div class="entorno" id="entorno"></div>
        </section>

        <section class="section wrap prose" aria-labelledby="mem-h">
          <p class="eyebrow">Por que é memorável</p>
          <h2 id="mem-h" class="h-sec">O irreproduzível</h2>
          <div id="memoravel"></div>
        </section>

        <section class="section--tight wrap">
          <nav class="cluster-nav" id="cluster-nav" aria-label="Outros clusters"></nav>
        </section>'''


def build_clusters():
    for slug, nome, desc in CLUSTERS:
        html = head("../../", f"{nome} — Ritos do Mundo Real", desc, f"clusters/{slug}/")
        html += f'\n<body data-page="cluster" data-slug="{slug}">\n'
        html += '  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>\n'
        html += '  <div class="frame">\n    <div class="sheet">\n\n'
        html += chrome_header("../../") + "\n\n"
        html += '      <main id="conteudo">\n' + cluster_body() + '\n      </main>\n\n'
        html += chrome_footer("../../") + "\n\n"
        html += '    </div>\n  </div>\n  <script src="../../assets/js/app.js"></script>\n</body>\n</html>\n'
        with open(os.path.join(ROOT, "clusters", slug, "index.html"), "w") as f:
            f.write(html)
    print("clusters:", len(CLUSTERS))


# ---------- BIBLIOTECA ----------
def build_biblioteca():
    body = '''        <section class="section wrap">
          <p class="eyebrow">Biblioteca de conhecimento</p>
          <h1 class="h-sec">As fontes por trás do projeto</h1>
          <p class="lede">Mais de 100 referências — livros, artigos, documentários, reportagens e datasets. Filtre pelos cartões abaixo. Onde a URL ainda não foi confirmada, indicamos <em>“link em verificação”</em> em vez de publicar um endereço incerto.</p>
        </section>
        <section class="section--tight wrap">
          <div class="lib-bar">
            <div class="grp"><span class="lbl">Tipo</span><div class="lib-filters" id="lib-tipos"></div></div>
            <div class="grp"><span class="lbl">Cluster</span><div class="lib-filters" id="lib-clusters"></div></div>
            <span class="lib-count" id="lib-count"></span>
          </div>
          <div id="lib-root"><div class="lib-items" id="lib-grid"></div></div>
        </section>'''
    html = page("../", "Biblioteca de conhecimento — Ritos do Mundo Real",
                "Mais de 100 referências sobre rituais de passagem, com subnavegação por filtros.",
                "biblioteca/", body, "biblioteca")
    with open(os.path.join(ROOT, "biblioteca", "index.html"), "w") as f:
        f.write(html)
    print("biblioteca: ok")


# ---------- SOBRE ----------
def build_sobre():
    body = '''        <section class="section wrap">
          <p class="eyebrow">Sobre &amp; método</p>
          <h1 class="h-sec">Honestidade sobre os dados vem antes de tudo</h1>
          <p class="lede">Este projeto organiza rituais de passagem e rituais coletivos do mundo numa base consultável, visual e honesta — para ajudar a decidir qual experiência vale viver, quando, e com que cuidado ético.</p>
        </section>

        <section class="section--tight wrap" id="selos">
          <p class="eyebrow">Selos de confiança</p>
          <h2 class="h-sec">Nunca apresentamos estimativa como fato</h2>
          <p class="lede" style="margin-bottom:1.4rem">Todo número de “participantes/ano” carrega um selo. A cor nunca aparece sozinha — vem sempre com texto.</p>
          <div class="about-grid">
            <div class="about-card"><div class="seal-key"><span class="seal seal--conf"><span class="ic">✅</span>Confirmado</span><p>Fonte oficial ou estatística. É o único selo que tratamos como fato.</p></div></div>
            <div class="about-card"><div class="seal-key"><span class="seal seal--parcial"><span class="ic">⚠️</span>Parcial</span><p>Ordem de grandeza plausível a partir de fontes secundárias.</p></div></div>
            <div class="about-card"><div class="seal-key"><span class="seal seal--estimativa"><span class="ic">❓</span>Estimativa</span><p>Sem dado público. Mostramos como “ordem de grandeza”, jamais como certeza.</p></div></div>
          </div>
        </section>

        <section class="section wrap prose" id="etica">
          <p class="eyebrow">Ética e sustentabilidade</p>
          <h2 class="h-sec">Cinco regras editoriais</h2>
          <div class="entorno" style="margin-top:1rem">
            <div class="item"><h4>1. Rituais fechados (FPIC)</h4><p class="meta">Sun Dance, Vision Quest, Ulwaluko, Festa da Moça Nova sem convite e o Hajj em Meca são listados como conhecimento, marcados como acesso fechado. Não indexamos vídeos comerciais nem operadores.</p></div>
            <div class="item"><h4>2. Turismo-espetáculo</h4><p class="meta">No Omo, na tucandeira “para turista” e na ayahuasca comercial, mostramos o alerta e sugerimos operador comunitário, remuneração direta e nada de encenação fora de época.</p></div>
            <div class="item"><h4>3. Bem-estar animal</h4><p class="meta">Jallikattu e a corrida de cavalos com jóqueis-crianças do Naadam entram com a controvérsia registrada e com fonte — sem tomar partido.</p></div>
            <div class="item"><h4>4. Overtourism</h4><p class="meta">Para Kumbh Mela, Caminho de Santiago e Yi Peng indicamos os meses e trechos de menor pressão.</p></div>
            <div class="item"><h4>5. Imagens e menores</h4><p class="meta">Nunca reproduzimos imagens de menores em rituais de nudez. Links apenas para fontes editoriais e institucionais.</p></div>
          </div>
        </section>

        <section class="section wrap prose" id="mapa">
          <p class="eyebrow">Créditos do mapa</p>
          <h2 class="h-sec">Sobre o mapa</h2>
          <p>A projeção é a <strong>Equal Earth</strong>, publicada em 2018 pelos cartógrafos Bojan Šavrič, Tom Patterson e Bernhard Jenny. É uma projeção de <strong>áreas iguais</strong>: cada país aparece no tamanho que realmente tem, ao contrário de Mercator, que infla o Norte. O contorno de países usa dados de domínio público (Natural Earth); os pinos são posicionados calculando a projeção Equal Earth a partir da latitude e longitude de cada rito.</p>
          <blockquote class="quote">⚠️ Nota de validação: a afirmação de que a projeção teria sido “lançada pela ONU” <strong>não se confirma</strong> — ela foi criada por três cartógrafos (Esri, US National Park Service e Monash University). O defensável é dizer que é “usada em mapas da ONU”.<cite>Validação de dados do projeto</cite></blockquote>
        </section>

        <section class="section--tight wrap prose">
          <p class="eyebrow">Como foi feito</p>
          <h2 class="h-sec">Método e stack</h2>
          <ul>
            <li>Site estático em HTML + CSS + JavaScript vanilla, <strong>sem framework e sem build</strong>. Um único <code>data/ritos.json</code> alimenta todas as páginas.</li>
            <li>Fontes self-hosted (OFL): <strong>Gloock</strong> (títulos), <strong>Instrument Sans</strong> (interface) e <strong>Mulish</strong> (corpo).</li>
            <li>Mapa gerado por script Python a partir de contornos de domínio público, projetado em Equal Earth; os pinos usam a mesma fórmula em JavaScript.</li>
            <li>Deploy em Cloudflare Pages a partir do GitHub, sem Node em produção.</li>
          </ul>
        </section>'''
    html = page("../", "Sobre & Método — Ritos do Mundo Real",
                "Método, selos de confiança, ética (FPIC) e créditos do mapa Equal Earth.",
                "sobre/", body, "sobre")
    with open(os.path.join(ROOT, "sobre", "index.html"), "w") as f:
        f.write(html)
    print("sobre: ok")


if __name__ == "__main__":
    build_clusters()
    build_biblioteca()
    build_sobre()
