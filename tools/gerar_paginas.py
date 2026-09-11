#!/usr/bin/env python3
"""Gera TODAS as páginas (home, hub 'Rituais pelo mundo', clusters, biblioteca, sobre)
com o mesmo chrome: header + megamenu (páginas e subpáginas) + rodapé com subpáginas +
bloco do autor. Sem emojis — apenas ícones SVG minimalistas.
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

# ---- ícones SVG (currentColor, sem emoji) ----
BRAND = ('<span class="mark" aria-hidden="true"><svg viewBox="0 0 24 24">'
         '<path d="M5 21V11a7 7 0 0 1 14 0v10" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round"/>'
         '<path d="M12 21v-6.4" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round"/></svg></span>')
IC_CHECK = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.4 8.7l3 3L12.8 4.7" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IC_ALERT = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.4l6.1 10.6H1.9z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M8 6.3v3.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="8" cy="11.5" r=".95" fill="currentColor"/></svg>'
IC_HELP = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.3" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6.1 6.3a1.95 1.95 0 1 1 2.7 1.8c-.6.3-.95.75-.95 1.4v.25" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><circle cx="8" cy="11.6" r=".9" fill="currentColor"/></svg>'
IC_DOT = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="4" fill="currentColor"/></svg>'
IC_MAIL = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><rect x="1.7" y="3.5" width="12.6" height="9" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M2.3 4.5 8 8.7l5.7-4.2" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'
IC_GLOBE = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.3" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M1.8 8h12.4M8 1.7c3 2.4 3 10.2 0 12.6M8 1.7c-3 2.4-3 10.2 0 12.6" fill="none" stroke="currentColor" stroke-width="1.15"/></svg>'
IC_LINK = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M9 3.2h3.8V7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M12.6 3.4 7.4 8.6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M11.8 9.5V12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5.2a1 1 0 0 1 1-1h2.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'


def T(s, base):
    return s.replace("~B~", base)


def head(base, title, desc, canon):
    return T('''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>~TITLE~</title>
  <meta name="description" content="~DESC~">
  <link rel="canonical" href="https://ritos.exemplo/~CANON~">
  <meta property="og:type" content="website">
  <meta property="og:title" content="~TITLE~">
  <meta property="og:description" content="~DESC~">
  <meta property="og:image" content="https://ritos.exemplo/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="~B~favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://images.unsplash.com" crossorigin>
  <link rel="preload" href="~B~assets/fonts/gloock-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="~B~assets/fonts/mulish-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="~B~assets/css/site.css">
</head>''', base).replace("~TITLE~", title).replace("~DESC~", desc).replace("~CANON~", canon)


def header(base, is_home):
    cta = ('<a class="btn btn--lime" href="#rituais">Explorar rituais</a>' if is_home
           else '<a class="btn btn--lime" href="https://calendly.com/ferttil/meet" target="_blank" rel="noopener">Agendar conversa</a>')
    subs = "".join('<a href="~B~clusters/%s/">%s</a>' % (s, n) for s, n, _ in CLUSTERS)
    return T('''      <header class="site-head">
        <a class="brand" href="~B~">''' + BRAND + '''Ritos do Mundo Real</a>
        <div class="head-actions">
          ''' + cta + '''
          <button class="menu-btn" id="menu-toggle" aria-expanded="false" aria-controls="menu-overlay">
            <span class="bars" aria-hidden="true"><i></i><i></i><i></i></span> Menu
          </button>
        </div>
      </header>

      <div class="menu-overlay" id="menu-overlay" role="dialog" aria-modal="true" aria-label="Menu de navegação">
        <div class="menu-top">
          <a class="brand" href="~B~">''' + BRAND + '''Ritos do Mundo Real</a>
          <button class="menu-close" id="menu-close" aria-label="Fechar menu">✕</button>
        </div>
        <div class="menu-body">
          <nav class="megamenu" aria-label="Páginas e subpáginas">
            <a class="mm-page" href="~B~">Início</a>
            <div class="mm-block">
              <a class="mm-page" href="~B~clusters/">Rituais pelo mundo</a>
              <div class="mm-subs">''' + subs + '''</div>
            </div>
            <a class="mm-page" href="~B~biblioteca/">Biblioteca</a>
            <a class="mm-page" href="~B~sobre/">Sobre &amp; Método</a>
          </nav>
          <aside class="mm-aside">
            <p class="eyebrow" style="color:var(--lime)">Comece por aqui</p>
            <p style="color:var(--on-forest-dim)">Filtre rituais por quem participa, pelo sentimento que tratam e pelo que muda para quem passa — no instrumento de decisão.</p>
            <a class="btn btn--lime" href="~B~#instrumento">Instrumento de decisão</a>
            <a class="btn btn--ghost" style="color:#fff" href="https://calendly.com/ferttil/meet" target="_blank" rel="noopener">Agendar uma conversa</a>
          </aside>
        </div>
      </div>''', base).replace('<button class="menu-close" id="menu-close" aria-label="Fechar menu">✕</button>',
                               '<button class="menu-close" id="menu-close" aria-label="Fechar menu"><svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg></button>')


def footer(base):
    subs = "".join('<a href="~B~clusters/%s/">%s</a>' % (s, n) for s, n, _ in CLUSTERS)
    return T('''      <footer class="site-foot">
        <div class="col"><b>Ritos do Mundo Real</b><small>Pesquisa + visualização + instrumento de decisão.<br>Dados com selo de confiança · PT-BR.</small></div>
        <div class="cols">
          <div class="col"><b>Páginas</b><a href="~B~">Início</a><a href="~B~clusters/">Rituais pelo mundo</a><a href="~B~biblioteca/">Biblioteca</a><a href="~B~sobre/">Sobre &amp; Método</a></div>
          <div class="col"><b>Rituais pelo mundo</b>''' + subs + '''</div>
          <div class="col"><b>Ética</b><a href="~B~sobre/#etica">Rituais fechados &amp; FPIC</a><a href="~B~sobre/#selos">Selos de confiança</a></div>
        </div>
      </footer>

      <section class="author" aria-label="Sobre esta ferramenta">
        <div class="author__band">
          <p class="eyebrow">Sobre esta ferramenta</p>
          <p>Essa ferramenta é independente, um projeto autônomo e parte de uma jornada de <strong style="color:#fff">Transição</strong>. Pesquisa, planejamento, análise, modelagem, criação e publicação — co-criados conectando fontes abertas, usando inteligência artificial e validação rigorosa.</p>
        </div>
        <div class="author__card">
          <div class="author__who">
            <div class="author__photo" data-mono="IB"><img id="author-photo" src="~B~assets/img/igor-botelho.jpg" alt="Igor Botelho" loading="lazy"></div>
            <div>
              <h3 class="author__name">Igor Botelho</h3>
              <p class="author__loc">Waiheke Island, Auckland · Nova Zelândia</p>
              <div class="author__links">
                <a href="mailto:igor@ferttil.com">''' + IC_MAIL + ''' igor@ferttil.com</a>
                <a href="https://www.igorbotelho.com" target="_blank" rel="noopener">''' + IC_GLOBE + ''' www.igorbotelho.com</a>
                <a href="https://linkedin.com/in/bernardesigor" target="_blank" rel="noopener">''' + IC_LINK + ''' linkedin.com/in/bernardesigor</a>
              </div>
            </div>
          </div>
          <div class="author__cta">
            <a class="btn btn--forest" href="https://calendly.com/ferttil/meet" target="_blank" rel="noopener">Agendar uma conversa →</a>
            <a class="btn btn--soft" href="mailto:igor@ferttil.com">Enviar um e-mail</a>
          </div>
        </div>
        <p class="author__note">Agendamento via Calendly · calendly.com/ferttil/meet</p>
      </section>''', base)


def page(base, title, desc, canon, body, data_attrs, is_home=False):
    return (head(base, title, desc, canon) + "\n"
            + '<body data-page="' + data_attrs + '">\n'
            + '  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>\n'
            + '  <div class="frame">\n    <div class="sheet">\n\n'
            + header(base, is_home) + "\n\n"
            + '      <main id="conteudo">\n' + body + '\n      </main>\n\n'
            + footer(base) + "\n\n"
            + '    </div>\n  </div>\n  <script src="' + base + 'assets/js/app.js"></script>\n</body>\n</html>\n')


# ---------- HOME ----------
def home_body():
    return T('''        <section class="hero">
          <div>
            <p class="eyebrow">Rituais de passagem · mundo real</p>
            <h1 class="hero__title">É tempo de viver o mundo real, com <em>pessoas reais</em>.</h1>
            <p class="hero__sub">Rituais memoráveis e experiências irreproduzíveis, reunidos numa base consultável, visual e honesta — organizada por quem participa.</p>
            <div class="hero__cta">
              <a class="btn btn--lime" href="#rituais">Explorar rituais</a>
              <a class="btn btn--soft" href="#instrumento">Instrumento de decisão</a>
            </div>
          </div>
          <div class="hero__media">
            <div class="pframe pframe--hover pframe--duo kb">
              <img src="~B~assets/img/hero-himba.jpg" data-fallback="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1000&q=70" alt="Mulher Himba com o toucado de ocre (erembe), Namíbia" loading="eager" width="1000" height="1100">
              <span class="notch notch--tr" aria-hidden="true"></span>
            </div>
            <span class="pill pill--lime hero__badge">Eco · exótico · contemporâneo</span>
            <div class="hero__float">
              <div class="k">Todo dado com selo</div>
              <div class="v"><span class="seal seal--conf">''' + IC_CHECK + ''' confirmado</span> · <span class="seal seal--parcial">''' + IC_ALERT + ''' parcial</span> · <span class="seal seal--estimativa">''' + IC_HELP + ''' estimativa</span></div>
            </div>
          </div>
        </section>

        <p id="data-error" class="wrap" role="alert" hidden style="color:var(--velvet);padding-top:1rem"></p>

        <section class="section wrap" aria-label="Panorama">
          <div class="stats">
            <div class="stat reveal"><b id="stat-ritos">—</b><span>rituais catalogados</span></div>
            <div class="stat reveal"><b id="stat-clusters">—</b><span>clusters de participação</span></div>
            <div class="stat reveal"><b id="stat-paises">—</b><span>países</span></div>
            <div class="stat stat--velvet reveal"><b id="stat-continentes">—</b><span>continentes</span></div>
            <div class="stats__note">
              <span class="pill pill--moss">''' + IC_CHECK + ''' Todo dado numérico traz um selo de confiança — nunca apresentamos estimativa como fato.</span>
            </div>
          </div>
        </section>

        <section class="section--tight wrap">
          <div class="banner banner--transicao reveal" data-parallax>
            <div class="parallax-layer" style="background-image:url('~B~assets/img/transicao.jpg')" aria-hidden="true"></div>
            <div class="banner__body">
              <p class="eyebrow" style="color:var(--lime)">Uma travessia</p>
              <h2>Todo rito é um limiar: um antes, uma margem e um depois.</h2>
              <p>Separação, passagem e reagregação — a gramática que van Gennep descreveu em 1909 e que atravessa cada cultura desta base.</p>
            </div>
          </div>
        </section>

        <section class="section wrap" id="rituais" aria-labelledby="rituais-h">
          <p class="eyebrow">Navegue por quem participa</p>
          <h2 id="rituais-h" class="h-sec">Rituais pelo mundo</h2>
          <p class="lede" style="margin-bottom:1.6rem">Em vez de listar por país ou religião, organizamos os rituais por quem os atravessa junto — pais e filhos, mães e filhas, casais, avós e netos, a multidão em peregrinação, ou a natureza que conduz a passagem.</p>
          <div class="cluster-grid" id="cluster-grid"></div>
        </section>

        <section class="section wrap" aria-labelledby="dest-h">
          <div class="carousel" data-carousel>
            <div class="carousel__head">
              <div><p class="eyebrow">Destaques</p><h2 id="dest-h" class="h-sec">Experiências memoráveis</h2></div>
              <div class="carousel__nav">
                <button class="cbtn" data-car-prev aria-label="Anterior"><svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3l-5 5 5 5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
                <button class="cbtn" data-car-next aria-label="Próximo"><svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
              </div>
            </div>
            <div class="carousel__track" id="featured-track" tabindex="0" aria-label="Rituais em destaque"></div>
          </div>
        </section>

        <section class="section--tight wrap">
          <div class="banner banner--natureza reveal" data-parallax>
            <div class="parallax-layer" style="background-image:url('~B~assets/img/natureza.jpg')" aria-hidden="true"></div>
            <div class="banner__body">
              <p class="eyebrow" style="color:var(--lime)">Natureza, animais e plantas</p>
              <h2>Às vezes, quem conduz a passagem é o mundo não humano.</h2>
              <p>Um boi, uma águia, um rio, uma rã, o inhame que amadurece — a natureza dita o calendário e o ser humano pede licença.</p>
            </div>
          </div>
        </section>

        <section class="section wrap" aria-labelledby="mapa-h">
          <div class="mapbanner reveal">
            <div class="map-holder" id="map-banner" aria-label="Mapa-múndi com os rituais plotados por cluster"></div>
            <div>
              <p class="eyebrow">O mundo em áreas iguais</p>
              <h2 id="mapa-h">Sobre o mapa</h2>
              <p>A projeção é a <strong style="color:#fff">Equal Earth</strong> (Šavrič, Patterson &amp; Jenny, 2018), de áreas iguais: cada país aparece no tamanho que realmente tem, ao contrário de Mercator, que infla o Norte. O contorno usa dados de domínio público; os pinos são calculados a partir da latitude e longitude de cada rito.</p>
              <div class="map-legend">
                <span class="pill">''' + IC_DOT + ''' cor por cluster</span>
                <span class="pill">clique num pino para abrir o rito</span>
              </div>
              <p style="margin-top:1rem"><a class="btn btn--lime" href="~B~sobre/#mapa">Ler a nota de validação →</a></p>
            </div>
          </div>
        </section>

        <section class="section wrap" id="instrumento" aria-labelledby="filtro-h">
          <div class="tool">
            <p class="eyebrow">Instrumento de decisão</p>
            <h2 id="filtro-h" class="h-sec">Qual experiência vale viver, quando e com que cuidado?</h2>
            <p class="lede">Filtre por quem participa, pelo sentimento que o rito trata, pelo que muda para quem passa, pela época, popularidade e acesso. Tudo vem da base — com selo de confiança e alerta ético quando houver.</p>
            <div class="filters">
              <div class="field"><label for="f-quem">Quem participa</label><select id="f-quem"><option value="">Todos</option></select></div>
              <div class="field"><label for="f-sentimento">Que sentimento trata</label><select id="f-sentimento"><option value="">Todos</option></select></div>
              <div class="field"><label for="f-muda">O que muda para quem passa</label><select id="f-muda"><option value="">Todos</option></select></div>
              <div class="field"><label for="f-mes">Época (mês)</label><select id="f-mes"><option value="">Qualquer mês</option></select></div>
              <div class="field"><label for="f-status">Status</label><select id="f-status"><option value="">Todos</option><option value="muito_popular">Muito popular</option><option value="conhecido">Conhecido</option><option value="exotico">Exótico</option></select></div>
              <div class="field"><label for="f-acesso">Acesso a visitante</label><select id="f-acesso"><option value="">Todos</option><option value="aberto">Aberto</option><option value="aberto_com_guia">Com guia</option><option value="restrito">Restrito (familiar)</option><option value="fechado">Fechado</option></select></div>
            </div>
            <div class="tool__actions">
              <button class="btn btn--velvet" id="f-clear" type="button">Limpar filtros</button>
              <span class="tool__count" id="f-count"></span>
            </div>
            <div class="results" id="f-results" aria-live="polite"></div>
          </div>
        </section>

        <section class="section wrap" aria-labelledby="acc-h">
          <p class="eyebrow">Perguntas frequentes</p>
          <h2 id="acc-h" class="h-sec">O essencial, em poucas linhas</h2>
          <div class="accordion" style="margin-top:1.4rem" data-accordion>
            <div class="acc-item"><button class="acc-head" aria-expanded="false"><span>O que são ritos?</span><span class="ico" aria-hidden="true">+</span></button><div class="acc-body"><div class="acc-body-inner"><p>São cerimônias que marcam a passagem de uma fase da vida para outra — nascer, virar adulto, casar, reencontrar os mortos. O antropólogo Arnold van Gennep (1909) mostrou que quase todas seguem três tempos: <strong>separação</strong> do que se era, uma <strong>margem</strong> (o limiar) e a <strong>reagregação</strong> num novo lugar social. São o corpo, o tempo e a comunidade que tornam cada rito irreproduzível.</p></div></div></div>
            <div class="acc-item"><button class="acc-head" aria-expanded="false"><span>Por que “do Mundo Real”?</span><span class="ico" aria-hidden="true">+</span></button><div class="acc-body"><div class="acc-body-inner"><p>Sem telas, sem prompts, sem wi-fi, você vai ver que o tempo e a qualidade no Planeta Terra são reenergizantes. Estes rituais só acontecem uma vez, num corpo que não ensaia e diante de pessoas reais — o oposto do que se reproduz num feed.</p></div></div></div>
            <div class="acc-item"><button class="acc-head" aria-expanded="false"><span>Como sei que os dados são confiáveis?</span><span class="ico" aria-hidden="true">+</span></button><div class="acc-body"><div class="acc-body-inner"><p>Todo número traz um selo: <span class="seal seal--conf">''' + IC_CHECK + ''' confirmado</span> (fonte oficial), <span class="seal seal--parcial">''' + IC_ALERT + ''' parcial</span> (ordem de grandeza) e <span class="seal seal--estimativa">''' + IC_HELP + ''' estimativa</span> (sem dado público). A cor nunca aparece sozinha; vem sempre com texto. Nunca apresentamos estimativa como fato.</p></div></div></div>
            <div class="acc-item"><button class="acc-head" aria-expanded="false"><span>Posso assistir a qualquer ritual?</span><span class="ico" aria-hidden="true">+</span></button><div class="acc-body"><div class="acc-body-inner"><p>Não. Alguns são <strong>fechados</strong> (Sun Dance, Vision Quest, Ulwaluko, Festa da Moça Nova sem convite, o Hajj em Meca): listamos como conhecimento, sem indexar operadores nem vídeos comerciais, em respeito ao consentimento livre, prévio e informado. O campo “acesso” diz de cada um: aberto, com guia, restrito ou fechado.</p></div></div></div>
            <div class="acc-item"><button class="acc-head" aria-expanded="false"><span>Como escolho uma experiência para viver?</span><span class="ico" aria-hidden="true">+</span></button><div class="acc-body"><div class="acc-body-inner"><p>Use o <a href="#instrumento">Instrumento de decisão</a>: filtre por quem participa, pelo sentimento que o rito trata, pelo que muda para quem passa, pela época, popularidade e acesso. Cada resultado traz o selo de confiança e, quando houver, o alerta ético.</p></div></div></div>
            <div class="acc-item"><button class="acc-head" aria-expanded="false"><span>Isto é uma agência de viagens?</span><span class="ico" aria-hidden="true">+</span></button><div class="acc-body"><div class="acc-body-inner"><p>Não. É um projeto independente de pesquisa e curadoria. Quando o assunto é ir até lá, defendemos turismo com cuidado: operador comunitário, remuneração direta, sem encenação fora de época — e alertamos sobre turismo-espetáculo, bem-estar animal e overtourism, com fonte e sem tomar partido.</p></div></div></div>
          </div>
        </section>''', "")  # base "" para a home


def build_home():
    html = page("", "Ritos do Mundo Real — rituais de passagem do mundo, com selo de confiança",
                "Uma base consultável, visual e honesta de rituais de passagem do mundo — organizada por quem participa, com selos de confiança e cuidado ético.",
                "", home_body(), "home", is_home=True)
    with open(os.path.join(ROOT, "index.html"), "w") as f:
        f.write(html)
    print("home: ok")


# ---------- RITUAIS (hub) ----------
def build_rituais():
    body = '''        <section class="section wrap">
          <p class="eyebrow">Páginas · Rituais pelo mundo</p>
          <h1 class="h-sec">Rituais pelo mundo</h1>
          <p class="lede">Seis clusters, um mesmo limiar. Escolha por quem atravessa a passagem junto — cada cluster reúne rituais de todos os continentes, com tabela filtrável, curiosidades, turismo no entorno e o que os torna memoráveis.</p>
        </section>
        <section class="section--tight wrap" id="rituais">
          <div class="cluster-grid" id="cluster-grid"></div>
          <p id="data-error" role="alert" hidden style="color:var(--velvet)"></p>
        </section>
        <section class="section wrap" aria-labelledby="mapa-h">
          <div class="mapbanner reveal">
            <div class="map-holder" id="map-banner" aria-label="Mapa-múndi com todos os rituais"></div>
            <div>
              <p class="eyebrow">O mundo em áreas iguais</p>
              <h2 id="mapa-h">Todos no mapa</h2>
              <p>Cada pino é um ritual, com a cor do seu cluster. Clique para abrir. A projeção Equal Earth mostra cada país no tamanho real.</p>
              <p style="margin-top:1rem"><a class="btn btn--lime" href="../sobre/#mapa">Sobre o mapa →</a></p>
            </div>
          </div>
        </section>'''
    html = page("../", "Rituais pelo mundo — Ritos do Mundo Real",
                "Os seis clusters de rituais de passagem, organizados por quem participa.",
                "clusters/", body, "rituais")
    os.makedirs(os.path.join(ROOT, "clusters"), exist_ok=True)
    with open(os.path.join(ROOT, "clusters", "index.html"), "w") as f:
        f.write(html)
    print("rituais (hub): ok")


# ---------- CLUSTER ----------
def cluster_body():
    return '''        <section class="section wrap">
          <div class="cluster-head">
            <div>
              <p class="eyebrow"><a href="../" style="color:var(--velvet);text-decoration:none">Rituais pelo mundo</a> · quem participa</p>
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
        html = head("../../", nome + " — Ritos do Mundo Real", desc, "clusters/" + slug + "/")
        html += '\n<body data-page="cluster" data-slug="' + slug + '">\n'
        html += '  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>\n'
        html += '  <div class="frame">\n    <div class="sheet">\n\n'
        html += header("../../", False) + "\n\n"
        html += '      <main id="conteudo">\n' + cluster_body() + '\n      </main>\n\n'
        html += footer("../../") + "\n\n"
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
            <div class="about-card"><div class="seal-key"><span class="seal seal--conf">''' + IC_CHECK + ''' Confirmado</span><p>Fonte oficial ou estatística. É o único selo que tratamos como fato.</p></div></div>
            <div class="about-card"><div class="seal-key"><span class="seal seal--parcial">''' + IC_ALERT + ''' Parcial</span><p>Ordem de grandeza plausível a partir de fontes secundárias.</p></div></div>
            <div class="about-card"><div class="seal-key"><span class="seal seal--estimativa">''' + IC_HELP + ''' Estimativa</span><p>Sem dado público. Mostramos como “ordem de grandeza”, jamais como certeza.</p></div></div>
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
          <blockquote class="quote">Nota de validação: a afirmação de que a projeção teria sido “lançada pela ONU” <strong>não se confirma</strong> — ela foi criada por três cartógrafos (Esri, US National Park Service e Monash University). O defensável é dizer que é “usada em mapas da ONU”.<cite>Validação de dados do projeto</cite></blockquote>
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
    build_home()
    build_rituais()
    build_clusters()
    build_biblioteca()
    build_sobre()
