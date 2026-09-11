/* =========================================================================
   Ritos do Mundo Real — app.js (vanilla, sem build)
   Um único data/ritos.json alimenta HOME, páginas de cluster e filtros.
   ========================================================================= */
(function () {
  "use strict";

  /* ---- modo embutido (preview single-file / Artifact): dados inline + rotas por hash ---- */
  var EMBED = !!(window.__RITOS__);

  /* ---- base path (funciona em /, /clusters/x/, /biblioteca/, /sobre/) ---- */
  var BASE = (function () {
    var s = document.currentScript || (function () {
      var all = document.getElementsByTagName("script");
      return all[all.length - 1];
    })();
    return (s && s.src) ? s.src.replace(/assets\/js\/app\.js.*$/, "") : "";
  })();

  /* ---- geradores de link (multipage por padrão; hash em modo embutido) ---- */
  function hrefHome() { return EMBED ? "#/" : BASE; }
  function hrefCluster(slug, id) { return EMBED ? ("#/cluster/" + slug + (id ? "/" + id : "")) : (BASE + "clusters/" + slug + "/" + (id ? "#" + id : "")); }
  function hrefBiblioteca() { return EMBED ? "#/biblioteca" : (BASE + "biblioteca/"); }
  function hrefSobre(h) { return EMBED ? "#/sobre" : (BASE + "sobre/" + (h || "")); }

  /* ---- projeção Equal Earth (mesmas constantes de tools/gerar_mapa.py) ---- */
  var A1 = 1.340264, A2 = -0.081106, A3 = 0.000893, A4 = 0.003796, SQRT3 = Math.sqrt(3);
  var SCALE = 200, OX = 553.3260, OY = 275.4726;
  function project(lon, lat) {
    var lam = lon * Math.PI / 180, phi = lat * Math.PI / 180;
    var th = Math.asin((SQRT3 / 2) * Math.sin(phi));
    var den = 3 * (9 * A4 * Math.pow(th, 8) + 7 * A3 * Math.pow(th, 6) + 3 * A2 * th * th + A1);
    var x = (2 * SQRT3 * lam * Math.cos(th)) / den;
    var y = A4 * Math.pow(th, 9) + A3 * Math.pow(th, 7) + A2 * Math.pow(th, 3) + A1 * th;
    return { x: x * SCALE + OX, y: OY - y * SCALE };
  }

  /* ---- metadados de clusters (ordem = navegação) ---- */
  var CLUSTERS = [
    { slug: "pais-e-filhos", nome: "Pais e filhos", cor: "#b5502f",
      frase: "Pai, avô e filho; iniciação masculina.",
      curiosidades: [
        "A tucandeira é considerada 'mulher' pelos Sateré-Mawé — a formiga que ensina o homem a suportar.",
        "No Ukuli Bula, são as mulheres da família que pedem para ser chicoteadas, como prova pública de lealdade ao iniciado.",
        "No Bar Mitzvah, aos 13 anos o menino passa a responder sozinho pelos mandamentos: é o 'filho do dever'.",
        "No Ulwaluko xhosa, o retorno (umgidi) importa mais que o corte: é a aldeia inteira que reconhece o novo homem.",
        "No Naghol de Vanuatu, o pai salta ao lado do filho — e o comprimento do cipó é calculado para a cabeça tocar de leve a terra.",
        "No Shinbyu birmanês, o menino desfila vestido de príncipe antes de raspar a cabeça — reencenando o Buda antes da renúncia."
      ],
      memoravel: "O que se prova aqui é feito com o corpo e diante dos homens da linhagem. O salto sobre o gado, a luva de formigas, a reclusão na mata ou a leitura pública da Torá são todos irreversíveis no tempo: acontecem uma vez, num corpo que não pode ensaiar, sob o olhar de quem já passou pela prova. É a dor, o risco e a presença da comunidade que tornam a passagem impossível de reproduzir — não há atalho, não há repetição idêntica, e o novo estatuto (homem, adulto, responsável) só existe porque foi testemunhado.",
      quote: { t: "“A vida individual… é uma sucessão de etapas cujos finais e recomeços são semelhantes: nascimento, puberdade social, casamento, morte.”", a: "Arnold van Gennep, Os Ritos de Passagem (1909)" } },

    { slug: "maes-e-filhas", nome: "Mães e filhas", cor: "#c47a3d",
      frase: "Mãe, madrinha e tias; menarca e feminilidade.",
      curiosidades: [
        "No Kinaaldá navajo, o bolo de milho de quase 1 metro é assado a noite inteira na terra — e comê-lo é comungar com a menina.",
        "Na Sunrise Ceremony apache, durante quatro dias a menina 'é' a Mulher da Pintura Branca e pode curar quem a toca.",
        "Na Festa da Moça Nova ticuna, o cabelo é arrancado fio a fio ao amanhecer, encerrando meses de reclusão.",
        "No Dipo krobo, a prova final é sentar na pedra sagrada — que, diz-se, rejeita quem não está pura.",
        "No half-saree do sul da Índia, é a mãe quem veste na filha o meio-sári: um gesto que anuncia a maturidade à família inteira.",
        "Na quinceañera, o pai troca o sapato baixo pelo salto alto — a menina literalmente muda de altura diante de todos."
      ],
      memoravel: "Estas passagens giram em torno de um evento do corpo — a primeira menstruação — que só acontece uma vez e não escolhe data. Por isso o rito é convocado quando o corpo decide, não quando o calendário permite. Mãe, madrinha e tias transmitem, com as mãos, um saber que não cabe em texto: como correr para o sol, como sentar na pedra, como vestir o sári. O irreproduzível está nesse encontro entre um instante biológico único e uma linhagem de mulheres que se coloca ao redor para dizer, em coro: agora você é uma de nós.",
      quote: { t: "“Os atributos da liminaridade… são necessariamente ambíguos: a pessoa passa por um domínio que tem poucos dos atributos do estado passado ou futuro.”", a: "Victor Turner, O Processo Ritual (1969)" } },

    { slug: "casais", nome: "Casais", cor: "#9a6b3f",
      frase: "Casamento e união de duas famílias.",
      curiosidades: [
        "No Saptapadi hindu, cada um dos sete passos ao redor do fogo é um voto — e o casamento só é válido depois do sétimo.",
        "Na cerimônia do chá chinesa, o gesto decisivo é chamar os sogros de 'pai' e 'mãe' pela primeira vez.",
        "A expressão inglesa 'tying the knot' (atar o nó) vem literalmente do handfasting celta, em que as mãos são amarradas por fitas.",
        "Na coroação ortodoxa, os noivos usam coroas trocadas três vezes — são feitos rei e rainha de um novo lar.",
        "Na noite da henna, a mãe da noiva chora ritualmente a despedida antes de aplicar a tinta às mãos.",
        "No Rod Nam Sang tailandês, os anciãos derramam água de uma concha sobre as mãos unidas do casal, transmitindo bênção."
      ],
      memoravel: "O casamento é o rito de passagem mais universal e, ainda assim, o mais local: muda o sobrenome, a casa, a família e às vezes o próprio nome pelo qual se é chamado. O que não se reproduz é o instante em que duas linhagens, até então separadas, passam a se tratar como uma só — o fogo, a coroa, o nó, o chá servido de joelhos. São gestos pequenos que reorganizam quem pertence a quem. A festa pode durar três dias, mas o limiar é atravessado num segundo: antes, dois estranhos; depois, uma família.",
      quote: { t: "“A passagem de uma situação social a outra é assimilada a uma passagem territorial.”", a: "Arnold van Gennep, Os Ritos de Passagem (1909)" } },

    { slug: "avos-e-netos", nome: "Avós e netos", cor: "#7c6a4a",
      frase: "Nascimento, nomeação e primeira comida.",
      curiosidades: [
        "No Annaprashan bengali, o bebê escolhe entre livro, dinheiro, caneta e terra — e a família lê ali um destino.",
        "No Doljanchi coreano, o mesmo jogo de escolha (doljabi) marca o primeiro aniversário, sobre a mesa preparada pelos avós.",
        "No Shichi-Go-San japonês, a bala chitose-ame ('doce dos mil anos') é longa e fina de propósito: é um pedido de vida longa.",
        "No Primeiro Riso navajo, quem faz o bebê rir organiza a festa e distribui sal em nome dele — a criança aprende primeiro a dar.",
        "Na nomeação iorubá, mel, sal, kola e água tocam a boca do bebê: cada sabor é um voto sobre a vida que virá.",
        "No Famadihana de Madagascar, as gerações dançam com os ancestrais envoltos em seda nova antes de recolocá-los no túmulo."
      ],
      memoravel: "Aqui quem conduz a passagem raramente é o protagonista: o bebê não escolhe nascer, ser nomeado ou provar a primeira comida — são os avós que abrem o caminho. O irreproduzível é o gesto fundador: o primeiro nome dito em voz alta, a primeira colher de arroz, a primeira gargalhada. Cada um só acontece uma vez, e é sempre uma geração mais velha que o oferece à mais nova. No Famadihana, o mesmo eixo se inverte com ternura: são os vivos que cuidam dos mortos, fechando o círculo entre quem chega e quem já partiu.",
      quote: { t: "“É a própria sociedade que… faz e refaz os indivíduos, num ritmo de agregações e separações.”", a: "Comentário sobre van Gennep e Turner" } },

    { slug: "coletivos-e-peregrinacoes", nome: "Coletivos e peregrinações", cor: "#a85a48",
      frase: "Multidão, cidade e fé — festivais e caminhos.",
      curiosidades: [
        "O Kumbh Mela é a maior reunião humana do planeta: a contagem oficial de 2025 somou centenas de milhões de banhos.",
        "No Seijin no Hi, cidades inteiras do Japão se enchem, num único dia de janeiro, de jovens de furisode e hakama.",
        "No Caminho de Santiago, o rito não é a fé necessariamente, mas a chegada a pé — a Compostela só se ganha andando.",
        "No Thaipusam, devotos sobem os 272 degraus de Batu Caves com o kavadi preso à pele por ganchos.",
        "No Día de Muertos, a vigília acontece dentro do cemitério, à luz de velas, esperando os mortos voltarem.",
        "O Hajj reúne cerca de 1,8 milhão de peregrinos girando ao mesmo tempo ao redor da Kaaba."
      ],
      memoravel: "O que aqui é irreproduzível não é o corpo de um indivíduo, mas a multidão: a communitas de Turner, aquele estado em que hierarquias se dissolvem e milhões de estranhos viram, por alguns dias, um só corpo. Ninguém sozinho faz um Kumbh Mela ou um Hajj; a passagem é coletiva e passa pelo tamanho. Caminhar semanas até Santiago, banhar-se no Sangam, velar no cemitério em Oaxaca — em todos, o peregrino sai de casa uma pessoa e volta outra, tendo atravessado, junto com incontáveis desconhecidos, o mesmo limiar.",
      quote: { t: "“A communitas irrompe onde a estrutura social não está — na liminaridade, na marginalidade, na inferioridade.”", a: "Victor Turner, O Processo Ritual (1969)" } },

    { slug: "natureza-animais-e-plantas", nome: "Natureza, animais e plantas", cor: "#6f7a45",
      frase: "Rito mediado por bicho, planta, rio ou colheita.",
      curiosidades: [
        "No Naghol de Vanuatu, o salto está amarrado à colheita do inhame: bom salto, boa colheita.",
        "No Ukuli Bula, é o gado — não uma pessoa — que dá ou nega a passagem ao jovem que salta sobre o seu dorso.",
        "No Festival da Águia Dourada, meninos e meninas cazaques chamam do céu águias que caçam para eles.",
        "No Yi Peng, milhares de lanternas sobem ao mesmo tempo em Chiang Mai, levando embora o azar do ano.",
        "No Songkran, o gesto íntimo por trás da guerra de água é lavar as mãos dos avós, pedindo bênção.",
        "Na Festa do Boi-Bumbá, uma cidade inteira se divide entre vermelho e azul para reencenar a morte e a ressurreição de um boi."
      ],
      memoravel: "Nestes ritos, quem conduz a passagem é o mundo não humano: um boi, uma águia, o rio, a rã, a lanterna, o inhame que amadurece. O irreproduzível está no acoplamento entre o tempo humano e o tempo da natureza — só se salta quando o inhame está pronto, só se solta a lanterna na lua cheia certa, só se agarra o touro no Pongal da colheita. É uma passagem que não se pode adiantar nem adiar sem perder o sentido, porque depende de um calendário que não é o nosso. Aqui o ser humano não é o centro: é um participante que pede licença.",
      quote: { t: "“O rito de passagem não separa o homem da natureza; ao contrário, inscreve-o no ciclo que a governa.”", a: "Leitura contemporânea de van Gennep" } },

    { slug: "expansao-de-consciencia", nome: "Expansão de consciência", cor: "#6e4658",
      frase: "Jornadas com plantas de poder e enteógenos — cura, visão e o sagrado.",
      curiosidades: [
        "Para os Wixárika, o peyote (hikuri) não é uma droga: é uma divindade que se 'caça' no deserto de Wirikuta, a centenas de quilômetros de casa.",
        "A velada mazateca era usada para curar e encontrar pessoas desaparecidas — até um artigo na revista Life (1957) trazer o turismo que feriu María Sabina e sua comunidade.",
        "Na Native American Church, o peyote é sacramento legal apenas para membros de nações reconhecidas — e hoje vive uma crise de conservação.",
        "A iniciação Bwiti, no Gabão, usa doses altas de iboga para 'ver os ancestrais' — com risco cardíaco real e mortes documentadas.",
        "O cacto San Pedro (wachuma) aparece em relevos de Chavín de Huántar, no Peru, há cerca de 3.000 anos.",
        "No Brasil, o uso religioso da ayahuasca (Santo Daime, UDV) é regulamentado por lei."
      ],
      memoravel: "Aqui o limiar é atravessado por dentro: uma planta ou fungo — peyote, ayahuasca, iboga, cogumelo, San Pedro — abre, por uma noite, uma percepção que não se repete igual. O irreproduzível está no encontro entre a substância, o corpo de quem toma, os cantos de quem conduz e o tempo da vigília: a mesma dose, noutro contexto, é outra coisa. São tradições de cura e visão de povos originários, não recreação — e por isso carregam os cuidados mais sérios desta base: soberania indígena e consentimento (FPIC), contraindicações e riscos de saúde, conservação de plantas ameaçadas e o alerta contra o neo-extrativismo espiritual, que transforma o sagrado de um povo em produto de turismo.",
      quote: { t: "“A liminaridade… é um tempo e um lugar de retirada dos modos habituais de ação social — pode ser vista como um período de exame dos valores centrais da comunidade.”", a: "Victor Turner, O Processo Ritual (1969)" } },

    { slug: "iniciacao-espiritual", nome: "Iniciação espiritual", cor: "#4a6274",
      frase: "Entrar numa tradição sagrada — batismos, votos e consagrações.",
      curiosidades: [
        "No batismo cristão, a água encena morrer e renascer — 'sepultado com Cristo, ressuscitado com ele' — e muitas vezes traz um novo nome.",
        "O Amrit Sanchar sikh foi instituído em 1699 por Guru Gobind Singh, que criou o Khalsa e os 'cinco K'.",
        "Na diksha hindu, o guru sussurra um mantra pessoal ao discípulo, que passa a ter um novo nome espiritual.",
        "Na feitura de santo do Candomblé, o iaô fica recluso por meses e 'renasce' com o orixá assentado, recebendo novo nome.",
        "No Kanzo do Vodou haitiano, passar pelo fogo marca a entrada no sacerdócio.",
        "Na iniciação sufi (bay'ah), o discípulo aperta a mão do mestre e entra numa cadeia (silsila) que se diz remontar ao Profeta."
      ],
      memoravel: "Aqui o limiar não é a idade nem o casamento: é passar a pertencer a uma tradição. Quase sempre há três marcas juntas — um voto assumido diante de uma comunidade, uma transmissão de mestre para discípulo (um mantra, um sopro, uma imposição de mãos) e um renascimento simbólico que muitas vezes vem com um nome novo. O irreproduzível está nessa transmissão testemunhada: ela liga a pessoa a uma linhagem que a antecede e a sucederá. Vários desses ritos são fechados e cheios de segredo — Candomblé, Vodou, certas iniciações — e por isso pedem o mesmo cuidado do resto desta base: registrar como conhecimento, sem expor o que é reservado, sem exotizar religiões historicamente perseguidas.",
      quote: { t: "“O neófito da liminaridade… deve ser uma tábula rasa na qual se inscreve o conhecimento e a sabedoria do grupo.”", a: "Victor Turner, O Processo Ritual (1969)" } },
  ];

  /* fotos por cluster (Unsplash CDN — trocáveis) + tom pastel do card */
  var UP = "?auto=format&fit=crop&w=900&q=70";
  var CFOTO = {
    "pais-e-filhos": "https://images.unsplash.com/photo-1501785888041-af3ef285b470" + UP,
    "maes-e-filhas": "https://images.unsplash.com/photo-1490750967868-88aa4486c946" + UP,
    "casais": "https://images.unsplash.com/photo-1518495973542-4542c06a5843" + UP,
    "avos-e-netos": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e" + UP,
    "coletivos-e-peregrinacoes": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d" + UP,
    "natureza-animais-e-plantas": "https://images.unsplash.com/photo-1426604966848-d7adac402bff" + UP,
    "expansao-de-consciencia": "https://images.unsplash.com/photo-1502082553048-f009c37129b9" + UP,
    "iniciacao-espiritual": "https://images.unsplash.com/photo-1519681393784-d120267933ba" + UP
  };
  var CTINT = { "pais-e-filhos": "sage", "maes-e-filhas": "rose", "casais": "sand",
    "avos-e-netos": "sage", "coletivos-e-peregrinacoes": "rose", "natureza-animais-e-plantas": "sand",
    "expansao-de-consciencia": "rose", "iniciacao-espiritual": "sage" };

  var STATUS_LABEL = { muito_popular: "Muito popular", conhecido: "Conhecido", exotico: "Exótico" };
  var STATUS_CLASS = { muito_popular: "status-mp", conhecido: "status-c", exotico: "status-e" };
  var ACESSO_LABEL = { aberto: "Aberto", aberto_com_guia: "Com guia", restrito: "Restrito (familiar)", fechado: "Fechado" };
  var CONF = {
    confirmado: { ic: "", txt: "Confirmado", cls: "seal--conf" },
    parcial: { ic: "", txt: "Parcial", cls: "seal--parcial" },
    estimativa: { ic: "", txt: "Estimativa", cls: "seal--estimativa" }
  };

  function clusterBySlug(s) { for (var i = 0; i < CLUSTERS.length; i++) if (CLUSTERS[i].slug === s) return CLUSTERS[i]; return null; }
  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function ytId(url) { if (!url) return null; var m = url.match(/[?&]v=([^&]+)/); return m ? m[1] : null; }

  /* ---- ícones minimalistas (SVG inline, sem emoji) ---- */
  var ICONS = {
    check: '<path d="M3.4 8.7l3 3L12.8 4.7" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>',
    alert: '<path d="M8 2.4l6.1 10.6H1.9z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M8 6.3v3.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="8" cy="11.5" r=".95" fill="currentColor"/>',
    help: '<circle cx="8" cy="8" r="6.3" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6.1 6.3a1.95 1.95 0 1 1 2.7 1.8c-.6.3-.95.75-.95 1.4v.25" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><circle cx="8" cy="11.6" r=".9" fill="currentColor"/>',
    spirit: '<path d="M8 1.4c.55 3.65 2.4 5.5 6.05 6.05C10.4 8 8.55 9.85 8 13.5 7.45 9.85 5.6 8 1.95 7.45 5.6 6.9 7.45 5.05 8 1.4z" fill="currentColor"/>',
    play: '<path d="M5 3.4l8 4.6-8 4.6z" fill="currentColor"/>',
    dot: '<circle cx="8" cy="8" r="4" fill="currentColor"/>',
    mail: '<rect x="1.7" y="3.5" width="12.6" height="9" rx="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M2.3 4.5 8 8.7l5.7-4.2" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
    globe: '<circle cx="8" cy="8" r="6.3" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M1.8 8h12.4M8 1.7c3 2.4 3 10.2 0 12.6M8 1.7c-3 2.4-3 10.2 0 12.6" fill="none" stroke="currentColor" stroke-width="1.15"/>',
    link: '<path d="M9 3.2h3.8V7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M12.6 3.4 7.4 8.6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M11.8 9.5V12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5.2a1 1 0 0 1 1-1h2.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
  };
  function icon(name, cls) { return '<svg class="ic ' + (cls || "") + '" viewBox="0 0 16 16" aria-hidden="true" focusable="false">' + (ICONS[name] || "") + '</svg>'; }
  /* injeta os SVGs nos selos de confiança */
  CONF.confirmado.ic = icon("check");
  CONF.parcial.ic = icon("alert");
  CONF.estimativa.ic = icon("help");

  /* ---- fetch do dataset ---- */
  function loadRitos() {
    if (EMBED) return Promise.resolve(window.__RITOS__);
    return fetch(BASE + "data/ritos.json", { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    });
  }

  /* ---- carrega o SVG do mapa e injeta no container, depois plota pins ---- */
  var _mapCache = null;
  function loadMap(container, ritos, filterSlug) {
    if (!container) return;
    var doInject = function (txt) {
      container.innerHTML = txt;
      var svg = container.querySelector("svg");
      if (!svg) return;
      svg.classList.add("ee-map");
      svg.removeAttribute("width"); svg.removeAttribute("height");
      paintPins(svg, ritos, filterSlug);
    };
    if (EMBED && window.__MAPSVG__) { doInject(window.__MAPSVG__); return; }
    if (_mapCache) { doInject(_mapCache); return; }
    fetch(BASE + "assets/map/equal-earth.svg", { cache: "force-cache" })
      .then(function (r) { return r.text(); })
      .then(function (txt) { _mapCache = txt; doInject(txt); })
      .catch(function () { container.innerHTML = '<p style="color:var(--on-ink-dim);font-family:var(--font-subtitle);padding:1rem">Mapa indisponível offline.</p>'; });
  }

  /* ---- pins no mapa SVG ---- */
  function paintPins(svg, ritos, filterSlug) {
    var g = svg.querySelector(".ee-pins");
    if (!g) return;
    g.innerHTML = "";
    var NS = "http://www.w3.org/2000/svg";
    ritos.forEach(function (r) {
      if (filterSlug && r.clusters.indexOf(filterSlug) === -1) return;
      if (typeof r.lat !== "number" || typeof r.lon !== "number") return;
      var p = project(r.lon, r.lat);
      var cl = clusterBySlug(r.clusters[0]);
      var c = document.createElementNS(NS, "circle");
      c.setAttribute("cx", p.x.toFixed(1));
      c.setAttribute("cy", p.y.toFixed(1));
      c.setAttribute("r", "5");
      c.setAttribute("fill", cl ? cl.cor : "#3f6b4a");
      c.setAttribute("fill-opacity", "0.9");
      c.setAttribute("stroke", "#fff");
      c.setAttribute("stroke-width", "1");
      c.setAttribute("tabindex", "0");
      c.setAttribute("role", "link");
      var label = r.nome + " — " + r.pais;
      c.setAttribute("aria-label", label + " (abrir cluster)");
      var t = document.createElementNS(NS, "title");
      t.textContent = label;
      c.appendChild(t);
      var href = hrefCluster(r.clusters[0], r.id);
      function go() { window.location.href = href; }
      c.addEventListener("click", go);
      c.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
      g.appendChild(c);
    });
  }

  /* ==========================================================
     HOME
     ========================================================== */
  function initHome(ritos) {
    /* estatísticas medidas a partir do JSON */
    var paises = {}, continentes = {};
    var CONT = {
      "Etiópia": "África", "Nigéria": "África", "África do Sul": "África", "Quênia": "África", "Gana": "África", "Marrocos": "África", "Madagascar": "África", "Gabão": "África",
      "Brasil": "América do Sul", "Peru": "América do Sul",
      "Estados Unidos": "América do Norte", "México": "América do Norte",
      "Israel": "Ásia", "Índia": "Ásia", "Mianmar": "Ásia", "China": "Ásia", "Tailândia": "Ásia", "Japão": "Ásia", "Coreia do Sul": "Ásia", "Arábia Saudita": "Ásia", "Malásia": "Ásia", "Mongólia": "Ásia", "Turquia": "Ásia",
      "Reino Unido": "Europa", "Grécia": "Europa", "Espanha": "Europa",
      "Papua-Nova Guiné": "Oceania", "Vanuatu": "Oceania",
      "Haiti": "América do Norte"
    };
    ritos.forEach(function (r) { paises[r.pais] = 1; if (CONT[r.pais]) continentes[CONT[r.pais]] = 1; });
    setCount("stat-ritos", ritos.length);
    setCount("stat-clusters", CLUSTERS.length);
    setCount("stat-paises", Object.keys(paises).length);
    setCount("stat-continentes", Object.keys(continentes).length);

    renderClusterGrid(ritos);
    renderFeatured(ritos);
    loadMap(document.getElementById("map-banner"), ritos, null);
    initFilter(ritos);
    revealStagger();
  }

  /* grade de clusters (com foto) — usada na home e no hub "Rituais pelo mundo" */
  function renderClusterGrid(ritos) {
    var grid = document.getElementById("cluster-grid");
    if (!grid) return;
    grid.innerHTML = CLUSTERS.map(function (c) {
      var membros = ritos.filter(function (r) { return r.clusters.indexOf(c.slug) !== -1; });
      var ex = membros.slice(0, 3).map(function (r) { return r.nome.split(" (")[0]; }).join(" · ");
      return '<a class="ccard reveal" href="' + hrefCluster(c.slug) + '">' +
        '<div class="pframe"><img src="' + CFOTO[c.slug] + '" alt="" loading="lazy"></div>' +
        '<div class="ccard__body">' +
        '<span class="ccard__k">' + membros.length + ' rituais</span>' +
        '<h3>' + esc(c.nome) + '</h3>' +
        '<p>' + esc(c.frase) + '</p>' +
        '<span class="ccard__ex">' + esc(ex) + '</span>' +
        '<div class="ccard__foot"><span class="ccard__more">Ver o cluster <span aria-hidden="true">→</span></span></div>' +
        '</div></a>';
    }).join("");
  }

  /* hub "Rituais pelo mundo" (/clusters/) */
  function initRituais(ritos) {
    renderClusterGrid(ritos);
    loadMap(document.getElementById("map-banner"), ritos, null);
    revealStagger();
  }

  function renderFeatured(ritos) {
    var track = document.getElementById("featured-track");
    if (!track) return;
    /* destaques: muito populares com vídeo, um por cluster quando possível, no máx. 10 */
    var pick = [], seen = {};
    ritos.filter(function (r) { return r.status === "muito_popular" && r.video; }).forEach(function (r) {
      var k = r.clusters[0];
      if (!seen[k]) { seen[k] = 1; pick.push(r); }
    });
    ritos.filter(function (r) { return r.status === "muito_popular" && r.video && pick.indexOf(r) === -1; })
      .forEach(function (r) { if (pick.length < 10) pick.push(r); });
    track.innerHTML = pick.map(function (r) {
      var cl = clusterBySlug(r.clusters[0]);
      var conf = CONF[r.participantes_ano.confianca] || CONF.estimativa;
      return '<a class="car-card" href="' + hrefCluster(r.clusters[0], r.id) + '">' +
        '<div class="pframe"><img src="' + CFOTO[r.clusters[0]] + '" alt="" loading="lazy"></div>' +
        '<div class="car-card__body">' +
        '<h4>' + esc(r.nome) + '</h4>' +
        '<div class="meta">' + esc(r.pais) + " · " + esc(cl ? cl.nome : "") + '</div>' +
        '<div class="tags">' +
        '<span class="pill badge-status ' + STATUS_CLASS[r.status] + '">' + STATUS_LABEL[r.status] + '</span>' +
        '<span class="pill"><span class="seal ' + conf.cls + '"><span class="ic">' + conf.ic + '</span></span>' + esc(r.participantes_ano.valor.split(";")[0]).slice(0, 26) + '</span>' +
        '</div></div></a>';
    }).join("");
    initCarousels();
  }

  function initFilter(ritos) {
    var selQuem = document.getElementById("f-quem");
    var selSent = document.getElementById("f-sentimento");
    var selMuda = document.getElementById("f-muda");
    var selMes = document.getElementById("f-mes");
    var selStatus = document.getElementById("f-status");
    var selAcesso = document.getElementById("f-acesso");
    var out = document.getElementById("f-results");
    var count = document.getElementById("f-count");
    var clear = document.getElementById("f-clear");
    if (!out) return;

    /* preencher "quem participa" com clusters */
    CLUSTERS.forEach(function (c) { selQuem.appendChild(opt(c.slug, c.nome)); });
    /* sentimento e "o que muda": valores únicos vindos da base */
    uniq(ritos, "sentimento").forEach(function (v) { selSent.appendChild(opt(v, v)); });
    uniq(ritos, "muda").forEach(function (v) { selMuda.appendChild(opt(v, v)); });

    var MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
    MESES.forEach(function (m, i) { selMes.appendChild(opt(String(i + 1), m)); });

    function matchMes(rito, mesIdx) {
      if (!mesIdx) return true;
      var e = (rito.epoca || "").toLowerCase();
      var i = parseInt(mesIdx, 10) - 1;
      var full = MESES[i].toLowerCase();
      var abbr = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"][i];
      if (e.indexOf(full) !== -1 || e.indexOf(abbr) !== -1) return true;
      if (e.indexOf("ao longo do ano") !== -1 || e.indexOf("todo o ano") !== -1 || e.indexOf("datas ") !== -1) return true;
      return false;
    }

    function render() {
      var q = selQuem.value, se = selSent.value, mu = selMuda.value, m = selMes.value, st = selStatus.value, ac = selAcesso.value;
      var list = ritos.filter(function (r) {
        if (q && r.clusters.indexOf(q) === -1) return false;
        if (se && r.sentimento !== se) return false;
        if (mu && r.muda !== mu) return false;
        if (st && r.status !== st) return false;
        if (ac && r.acesso_visitante !== ac) return false;
        if (!matchMes(r, m)) return false;
        return true;
      });
      count.textContent = list.length + (list.length === 1 ? " rito" : " ritos");
      count.classList.remove("bump"); void count.offsetWidth; count.classList.add("bump");
      if (!list.length) { out.innerHTML = '<p class="results__empty">Nenhum rito com esses critérios. Tente afrouxar um filtro.</p>'; return; }
      var ARW = '<svg class="arw" viewBox="0 0 12 9" aria-hidden="true"><path d="M1 4.5h9M7 1l3.5 3.5L7 8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      out.innerHTML = list.map(function (r) {
        var conf = CONF[r.participantes_ano.confianca] || CONF.estimativa;
        var cl = clusterBySlug(r.clusters[0]);
        return '<article class="rcard">' +
          '<a class="rcard__hit" href="' + hrefCluster(r.clusters[0], r.id) + '" aria-label="Ver ' + esc(r.nome) + '">' +
            '<div class="rcard__media ' + STATUS_CLASS[r.status] + '">' +
              '<img src="' + CFOTO[r.clusters[0]] + '" alt="" loading="lazy">' +
              '<span class="rcard__status badge-status">' + STATUS_LABEL[r.status] + '</span>' +
              '<span class="rcard__cluster">' + esc(cl ? cl.nome : "") + '</span>' +
            '</div>' +
            '<div class="rcard__body">' +
              '<div class="rcard__loc">' + esc(r.pais) + (r.regiao ? " · " + esc(r.regiao) : "") + '</div>' +
              '<h4>' + esc(r.nome) + '</h4>' +
              '<div class="rcard__feel"><span>' + esc(r.sentimento) + '</span>' + ARW + '<em>' + esc(r.muda) + '</em></div>' +
              '<div class="rcard__foot">' +
                '<span class="seal ' + conf.cls + '">' + conf.ic + conf.txt + '</span>' +
                '<span class="rcard__go">Ver <span aria-hidden="true">→</span></span>' +
              '</div>' +
            '</div>' +
          '</a>' +
          '</article>';
      }).join("");
    }

    var selects = [selQuem, selSent, selMuda, selMes, selStatus, selAcesso];
    selects.forEach(function (s) { s.addEventListener("change", render); });
    clear.addEventListener("click", function () { selects.forEach(function (s) { s.value = ""; }); render(); });
    render();
  }

  /* ==========================================================
     PÁGINA DE CLUSTER
     ========================================================== */
  function initCluster(ritos, slug) {
    var c = clusterBySlug(slug);
    if (!c) return;
    document.querySelectorAll("[data-cluster-nome]").forEach(function (el) { el.textContent = c.nome; });
    var fraseEl = document.getElementById("cluster-frase"); if (fraseEl) fraseEl.textContent = c.frase;

    var membros = ritos.filter(function (r) { return r.clusters.indexOf(slug) !== -1; });

    /* minimapa */
    loadMap(document.getElementById("cluster-map"), membros, slug);

    /* lista interativa de rituais */
    renderRitoList(membros);

    /* curiosidades */
    var cur = document.getElementById("curiosidades");
    if (cur) cur.innerHTML = c.curiosidades.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("");

    /* turismo no entorno */
    var ent = document.getElementById("entorno");
    if (ent) {
      ent.innerHTML = membros.map(function (r) {
        return '<div class="item">' +
          '<h4>' + esc(r.nome) + '</h4>' +
          '<div class="meta"><strong>Arredores:</strong> ' + esc(r.turismo_entorno) + '</div>' +
          '<div class="meta"><strong>Melhor época:</strong> ' + esc(r.epoca) + ' · <strong>Acesso:</strong> ' + esc(ACESSO_LABEL[r.acesso_visitante]) + '</div>' +
          (r.alerta_etico ? '<div class="alerta">' + icon("alert") + ' ' + esc(r.alerta_etico) + '</div>' : '') +
          '</div>';
      }).join("");
    }

    /* por que é memorável */
    var mem = document.getElementById("memoravel");
    if (mem) mem.innerHTML = '<p>' + esc(c.memoravel) + '</p>' +
      '<blockquote class="quote">' + c.quote.t + '<cite>' + esc(c.quote.a) + '</cite></blockquote>';

    /* navegação prev/next */
    var idx = CLUSTERS.indexOf(c);
    var prev = CLUSTERS[(idx - 1 + CLUSTERS.length) % CLUSTERS.length];
    var next = CLUSTERS[(idx + 1) % CLUSTERS.length];
    var nav = document.getElementById("cluster-nav");
    if (nav) nav.innerHTML =
      '<a href="' + hrefCluster(prev.slug) + '">← ' + esc(prev.nome) + '</a>' +
      '<a href="' + hrefCluster(next.slug) + '">' + esc(next.nome) + ' →</a>';

    /* âncora #id: rolar, abrir o card e destacar */
    if (location.hash) {
      var el = document.getElementById(location.hash.slice(1));
      if (el) {
        el.scrollIntoView({ block: "center" });
        el.classList.add("flash");
        var head = el.querySelector && el.querySelector(".rito__head");
        if (head && !el.classList.contains("open")) head.click();
      }
    }
  }

  /* lista interativa de rituais (cards expansíveis) — substitui a tabela */
  function renderRitoList(membros) {
    var host = document.getElementById("ritos-list");
    if (!host) return;
    var barStatus = document.getElementById("rt-status");
    var barAcesso = document.getElementById("rt-acesso");
    var countEl = document.getElementById("rt-count");
    var fStatus = "", fAcesso = "";

    function chip(val, label) {
      var b = document.createElement("button");
      b.className = "chip"; b.type = "button"; b.textContent = label;
      b.setAttribute("aria-pressed", "false"); b.dataset.val = val;
      return b;
    }
    if (barStatus && !barStatus.childElementCount) {
      barStatus.appendChild(chip("", "Todos os status"));
      ["muito_popular", "conhecido", "exotico"].forEach(function (s) { if (membros.some(function (r) { return r.status === s; })) barStatus.appendChild(chip(s, STATUS_LABEL[s])); });
    }
    if (barAcesso && !barAcesso.childElementCount) {
      barAcesso.appendChild(chip("", "Todo acesso"));
      ["aberto", "aberto_com_guia", "restrito", "fechado"].forEach(function (a) { if (membros.some(function (r) { return r.acesso_visitante === a; })) barAcesso.appendChild(chip(a, ACESSO_LABEL[a])); });
    }

    function card(r) {
      var conf = CONF[r.participantes_ano.confianca] || CONF.estimativa;
      var vid = r.video ? '<a class="vlink" href="' + esc(r.video) + '" target="_blank" rel="noopener">' + icon("play") + ' ver vídeo<span class="sr-only"> (abre no YouTube)</span></a>' : '';
      return '<article class="rito reveal" id="' + esc(r.id) + '">' +
        '<button class="rito__head" aria-expanded="false"><span>' +
        '<span class="rito__k">' + esc(r.pais) + (r.regiao ? ' · ' + esc(r.regiao) : '') + '</span>' +
        '<h3>' + esc(r.nome) + '</h3>' +
        '<span class="rito__povo">' + esc(r.povo_ou_tradicao) + '</span></span>' +
        '<span class="rito__toggle" aria-hidden="true">+</span></button>' +
        '<div class="rito__meta">' +
        '<span class="pill badge-status ' + STATUS_CLASS[r.status] + '">' + STATUS_LABEL[r.status] + '</span>' +
        '<span class="pill">' + esc(ACESSO_LABEL[r.acesso_visitante]) + '</span>' +
        (r.espiritual ? '<span class="pill pill--velvet">' + icon("spirit") + ' espiritual</span>' : '') +
        '<span class="seal ' + conf.cls + '">' + conf.ic + ' ' + conf.txt + '</span>' +
        '<span class="rito__part">' + esc(r.participantes_ano.valor) + '</span>' +
        '</div>' +
        '<p class="rito__mem">' + esc(r.memoravel) + '</p>' +
        (vid ? '<div class="rito__actions">' + vid + '</div>' : '') +
        (r.alerta_etico ? '<div class="rito__alerta">' + icon("alert") + ' ' + esc(r.alerta_etico) + '</div>' : '') +
        '<div class="rito__more"><div class="rito__more-inner">' +
        '<div><h5>Quem participa</h5><p>' + esc(r.quem_participa) + '</p></div>' +
        '<div><h5>Época</h5><p>' + esc(r.epoca) + '</p></div>' +
        '<div style="grid-column:1/-1"><h5>Descrição</h5><p>' + esc(r.descricao) + '</p></div>' +
        '<div style="grid-column:1/-1"><h5>Por que acontece · sentimento</h5><p>' + esc(r.motivo) + ' — trata <strong>' + esc(r.sentimento) + '</strong>; quem passa <strong>' + esc(r.muda).toLowerCase() + '</strong>.</p></div>' +
        '</div></div>' +
        '</article>';
    }

    function wire() {
      host.querySelectorAll(".rito").forEach(function (el) {
        var head = el.querySelector(".rito__head");
        var more = el.querySelector(".rito__more");
        head.addEventListener("click", function () {
          var open = el.classList.toggle("open");
          head.setAttribute("aria-expanded", open ? "true" : "false");
          more.style.maxHeight = open ? more.scrollHeight + "px" : "0";
        });
      });
    }

    function paint() {
      var list = membros.filter(function (r) {
        if (fStatus && r.status !== fStatus) return false;
        if (fAcesso && r.acesso_visitante !== fAcesso) return false;
        return true;
      });
      if (countEl) countEl.textContent = list.length + (list.length === 1 ? " ritual" : " rituais");
      host.innerHTML = list.length ? list.map(card).join("") : '<p class="results__empty">Nenhum ritual com esses filtros.</p>';
      wire();
      revealStaggerScoped(host);
    }
    function bindBar(bar, setter) {
      if (!bar) return;
      bar.addEventListener("click", function (e) {
        var b = e.target.closest(".chip"); if (!b) return;
        bar.querySelectorAll(".chip").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true"); setter(b.dataset.val); paint();
      });
      bar.firstChild.setAttribute("aria-pressed", "true");
    }
    bindBar(barStatus, function (v) { fStatus = v; });
    bindBar(barAcesso, function (v) { fAcesso = v; });
    paint();
  }

  /* ==========================================================
     BIBLIOTECA
     ========================================================== */
  function initBiblioteca() {
    var host = document.getElementById("lib-root");
    if (!host) return;
    var src = EMBED ? Promise.resolve(window.__BIBLIO__) : fetch(BASE + "data/biblioteca.json", { cache: "no-cache" }).then(function (r) { return r.json(); });
    src.then(function (data) {
      var itens = data.itens, cnomes = data.clusters || {};
      var tipos = uniq(itens, "tipo");
      var cls = uniq(itens, "cluster");
      var fTipo = "", fCluster = "";
      var barTipo = document.getElementById("lib-tipos");
      var barCluster = document.getElementById("lib-clusters");
      var grid = document.getElementById("lib-grid");
      var countEl = document.getElementById("lib-count");

      function chip(val, label, group) {
        var b = document.createElement("button");
        b.className = "chip"; b.type = "button"; b.textContent = label;
        b.setAttribute("aria-pressed", "false");
        b.dataset.val = val; b.dataset.group = group;
        return b;
      }
      barTipo.appendChild(chip("", "Todos", "tipo"));
      tipos.forEach(function (t) { barTipo.appendChild(chip(t, t, "tipo")); });
      barCluster.appendChild(chip("", "Todos", "cluster"));
      cls.forEach(function (c) { barCluster.appendChild(chip(c, cnomes[c] || c, "cluster")); });

      function paint() {
        var list = itens.filter(function (it) {
          if (fTipo && it.tipo !== fTipo) return false;
          if (fCluster && it.cluster !== fCluster) return false;
          return true;
        });
        countEl.textContent = list.length + " de " + itens.length + " itens";
        grid.innerHTML = list.length ? list.map(function (it) { return libItem(it, cnomes); }).join("")
          : '<p class="results__empty">Nada com esses filtros.</p>';
        revealStaggerScoped(grid);
      }
      function wire(bar, setter, groupRef) {
        bar.addEventListener("click", function (e) {
          var b = e.target.closest(".chip"); if (!b) return;
          bar.querySelectorAll(".chip").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
          b.setAttribute("aria-pressed", "true");
          setter(b.dataset.val); paint();
        });
      }
      wire(barTipo, function (v) { fTipo = v; });
      wire(barCluster, function (v) { fCluster = v; });
      barTipo.firstChild.setAttribute("aria-pressed", "true");
      barCluster.firstChild.setAttribute("aria-pressed", "true");
      paint();
    }).catch(function () { host.innerHTML = '<p class="lede">Não foi possível carregar a biblioteca.</p>'; });
  }
  function libItem(it, cnomes) {
    var link = it.link
      ? '<a class="src" href="' + esc(it.link) + '" target="_blank" rel="noopener">Abrir fonte →</a>'
      : '<span class="nolink">Referência citada — link em verificação.</span>';
    var cl = (cnomes && cnomes[it.cluster]) || it.cluster;
    return '<article class="lib-item reveal">' +
      '<div class="toprow"><span class="pill">' + esc(it.tipo) + '</span><span class="lib-cluster">' + esc(cl) + '</span></div>' +
      '<h4>' + esc(it.titulo) + '</h4>' +
      '<div class="by">' + esc(it.autor) + (it.ano ? " · " + esc(it.ano) : "") + (it.idioma ? " · " + esc(it.idioma) : "") + '</div>' +
      (it.porque ? '<div class="why">' + esc(it.porque) + '</div>' : '') +
      link + '</article>';
  }

  /* ==========================================================
     COMPONENTES DE UI (menu, acordeão, carrossel)
     ========================================================== */
  function initMenu() {
    var toggle = document.getElementById("menu-toggle");
    var overlay = document.getElementById("menu-overlay");
    var close = document.getElementById("menu-close");
    if (!toggle || !overlay) return;
    function open() { overlay.classList.add("open"); toggle.setAttribute("aria-expanded", "true"); document.body.style.overflow = "hidden"; var f = overlay.querySelector("a,button"); if (f) f.focus(); }
    function shut() { overlay.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; toggle.focus(); }
    toggle.addEventListener("click", open);
    if (close) close.addEventListener("click", shut);
    overlay.addEventListener("click", function (e) { if (e.target === overlay) shut(); });
    overlay.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", shut); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && overlay.classList.contains("open")) shut(); });
  }

  function initAccordions() {
    document.querySelectorAll("[data-accordion] .acc-item").forEach(function (item) {
      var head = item.querySelector(".acc-head");
      var body = item.querySelector(".acc-body");
      if (!head || !body) return;
      head.addEventListener("click", function () {
        var open = item.classList.toggle("open");
        head.setAttribute("aria-expanded", open ? "true" : "false");
        body.style.maxHeight = open ? body.scrollHeight + "px" : "0";
      });
    });
  }

  function initCarousels() {
    document.querySelectorAll("[data-carousel]").forEach(function (car) {
      var track = car.querySelector(".carousel__track");
      var prev = car.querySelector("[data-car-prev]");
      var next = car.querySelector("[data-car-next]");
      if (!track || !prev || !next) return;
      function step() { var c = track.querySelector(":scope > *"); return c ? c.getBoundingClientRect().width + 18 : 300; }
      function upd() {
        prev.disabled = track.scrollLeft < 6;
        next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 6;
      }
      prev.onclick = function () { track.scrollBy({ left: -step(), behavior: "smooth" }); };
      next.onclick = function () { track.scrollBy({ left: step(), behavior: "smooth" }); };
      track.addEventListener("scroll", upd, { passive: true });
      setTimeout(upd, 60);
    });
  }

  function initAuthorPhoto() {
    var img = document.getElementById("author-photo");
    if (img) img.addEventListener("error", function () { img.remove(); });
  }

  /* imagens com fallback: se a foto local do usuário não existir, cai para o CDN */
  function initImgFallback() {
    document.querySelectorAll("img[data-fallback]").forEach(function (img) {
      img.addEventListener("error", function once() {
        img.removeEventListener("error", once);
        img.src = img.getAttribute("data-fallback");
      });
    });
  }

  function initUI() { initMenu(); initAccordions(); initCarousels(); initAuthorPhoto(); initImgFallback(); initParallax(); }

  /* ---- utilitários ---- */
  function setNum(id, n) { var el = document.getElementById(id); if (el) el.textContent = n; }
  var _countIO;
  function reduced() { return matchMedia("(prefers-reduced-motion: reduce)").matches; }
  function setCount(id, n) {
    var el = document.getElementById(id); if (!el) return;
    el.dataset.count = n;
    if (reduced() || !("IntersectionObserver" in window)) { el.textContent = n; return; }
    el.textContent = "0";
    if (!_countIO) _countIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { animateNum(e.target); _countIO.unobserve(e.target); } });
    }, { threshold: .4 });
    _countIO.observe(el);
  }
  function animateNum(el) {
    var n = +el.dataset.count, dur = 1200, t0 = 0;
    function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(e * n); if (p < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  function initParallax() {
    if (reduced() || window.innerWidth < 760) return;
    var layers = [].slice.call(document.querySelectorAll(".parallax-layer"));
    if (!layers.length) return;
    var ticking = false;
    function upd() {
      var vh = window.innerHeight;
      layers.forEach(function (el) {
        var host = el.parentElement, r = host.getBoundingClientRect();
        if (r.bottom < -120 || r.top > vh + 120) return;
        var off = ((r.top + r.height / 2) - vh / 2) / vh;
        el.style.transform = "translate3d(0," + (off * -42).toFixed(1) + "px,0)";
      });
      ticking = false;
    }
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    window.addEventListener("resize", upd);
    upd();
  }
  function opt(v, t) { var o = document.createElement("option"); o.value = v; o.textContent = t; return o; }
  function uniq(list, key) {
    var seen = {}, out = [];
    list.forEach(function (x) { var v = x[key]; if (v && !seen[v]) { seen[v] = 1; out.push(v); } });
    return out;
  }
  function revealStaggerScoped(root) {
    (root || document).querySelectorAll(".reveal").forEach(function (e) { e.classList.add("in"); });
  }
  function hexa(hex, a) {
    var h = hex.replace("#", ""); var r = parseInt(h.substr(0, 2), 16), g = parseInt(h.substr(2, 2), 16), b = parseInt(h.substr(4, 2), 16);
    return "rgba(" + r + "," + g + "," + b + "," + a + ")";
  }
  function revealStagger() {
    var els = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) {
      els.forEach(function (e) { e.classList.add("in"); }); return;
    }
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en, i) {
        if (en.isIntersecting) { var el = en.target; setTimeout(function () { el.classList.add("in"); }, (i % 6) * 60); io.unobserve(el); }
      });
    }, { threshold: .08, rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (e) { io.observe(e); });
    /* rede de segurança: nada fica invisível para sempre se o observer não disparar */
    setTimeout(function () { els.forEach(function (e) { e.classList.add("in"); }); }, 2600);
  }

  /* ---- boot ---- */
  function bootPage() {
    var page = document.body.getAttribute("data-page");
    if (page === "biblioteca") { initBiblioteca(); return; }
    if (page === "sobre") { return; }
    loadRitos().then(function (ritos) {
      if (page === "home") initHome(ritos);
      else if (page === "rituais") initRituais(ritos);
      else if (page === "cluster") initCluster(ritos, document.body.getAttribute("data-slug"));
    }).catch(function (e) {
      var err = document.getElementById("data-error");
      if (err) { err.hidden = false; err.textContent = "Não foi possível carregar os dados dos ritos (" + e.message + "). Sirva o site por HTTP (ex.: python3 -m http.server)."; }
    });
  }

  if (EMBED) {
    /* modo embutido: o roteador (preview single-file) controla a renderização */
    window.RMR = { initHome: initHome, initRituais: initRituais, initCluster: initCluster, initBiblioteca: initBiblioteca, loadRitos: loadRitos, revealStagger: revealStagger, initUI: initUI };
  } else {
    document.addEventListener("DOMContentLoaded", function () { initUI(); bootPage(); });
  }
})();
