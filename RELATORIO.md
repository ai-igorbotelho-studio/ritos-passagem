# Relatório de auditoria — Ritos do Mundo Real

Build validado localmente (servidor HTTP + Chromium/Playwright). Data: 2026-09-11.

## Métricas medidas (não estimadas)

| Item | Medida | Orçamento | Situação |
|---|---|---|---|
| HTML+CSS+JS por página (gzip) | 16–18 KB | < 120 KB | ✅ folgado |
| Mapa `equal-earth.svg` (raw / gzip) | 125 KB / 42 KB | ≤ 150 KB | ✅ |
| `ritos.json` (gzip) | 13 KB | — | ✅ |
| Fontes woff2 (6 subsets, total) | 135 KB | 2 famílias latin | ✅ self-hosted |
| Contraste WCAG | todos os pares AA | AA | ✅ (após ajuste do ocre) |
| Scroll horizontal 320→1440 px | 0 px em todas as páginas | 0 | ✅ |
| Erros de console (todas as páginas) | nenhum | 0 | ✅ |

Matriz de viewport testada: **320 / 375 / 390 / 768 / 1024 / 1440 px**.

## Dados

- **42 ritos** catalogados · **25 países** · **6 continentes** · **6 clusters**.
- Distribuição de confiança: 10 ✅ confirmado · 24 ⚠️ parcial · 8 ❓ estimativa.
- Vídeos: **40 com URL** (18 do briefing + 22 pesquisadas no YouTube) · **2 sem URL** por
  decisão ética (Vision Quest/Sun Dance e Kambô/Ayahuasca).
- Os contadores da HOME são **calculados a partir do JSON** em tempo de carregamento —
  nunca digitados à mão.

## NÃO VERIFICADO (declarado)

1. **Contagem de ritos vs. briefing.** O cabeçalho do briefing diz "32 ritos", mas as
   tabelas da seção 3 enumeram **42 itens distintos** (contando os "repetidos" Ukuli Bula
   e Naghol uma só vez, com dois clusters cada). Optei por catalogar **todos os 42** e
   **medir** os contadores a partir do JSON, em vez de forçar o número 32. Se a intenção
   for exatamente 32, é preciso decidir quais 10 remover.

2. **Vídeos.** As 22 URLs pendentes foram **pesquisadas no YouTube** (nunca inventadas) e
   gravadas no JSON, com o campo `video_fonte` indicando a origem. Prioridade a fontes
   reputáveis: BBC (Hajj), AFP (Día de Muertos, Boi-Bumbá), ITV News (Águia Dourada),
   HBO (Quinceañera), WION (Kumbh), notícia UNESCO (Songkran). As demais são registros/
   documentários de canais menores. **Pendência:** confirmar a permanência de cada link
   (vídeos do YouTube podem ser removidos) antes da publicação definitiva. **Vision
   Quest/Sun Dance** e **Kambô/Ayahuasca** seguem deliberadamente sem vídeo por decisão
   ética (rito fechado / não indexar conteúdo comercial).

3. **Coordenadas lat/lon.** Aproximadas pela cidade-âncora de cada rito (não pela aldeia
   exata). Verificadas contra 3 pontos conhecidos na projeção (Golfo da Guiné, Sul do
   Brasil, Tóquio) — o alinhamento pino↔mapa é consistente por construção (mesma fórmula
   Equal Earth em Python e JS).

4. **Números ⚠️ e ❓.** Apresentados como ordem de grandeza; **não** promovidos a ✅ sem
   fonte primária. Os ✅ trazem a fonte no próprio JSON (`participantes_ano.fonte`).

5. **Links da Biblioteca.** Publiquei URL apenas para domínios institucionais estáveis
   (UNESCO ICH, Oficina del Peregrino, GASTAT, ICEERS). Os demais itens aparecem como
   "link em verificação" — precisam de confirmação de URL antes de virar link ativo.

6. **Afirmação "ONU" sobre o mapa.** Registrada em `/sobre/#mapa` como **não confirmada**:
   a projeção Equal Earth foi criada por três cartógrafos (Esri, US National Park Service,
   Monash), não "lançada pela ONU". Texto usa a formulação defensável ("usada em mapas da
   ONU").

7. **Domínio.** Metatags `canonical`/`og:*` usam o placeholder `https://ritos.exemplo/`.
   Trocar pelo domínio real antes de publicar.

## Pendências antes do deploy público

- [ ] Trocar `ritos.exemplo` pelo domínio final (5 ocorrências por página + sitemap/robots).
- [x] ~~Buscar as 22 URLs de vídeo~~ — feito; falta confirmar a permanência de cada link.
- [ ] Confirmar URLs restantes da Biblioteca.
- [x] ~~Decidir 32 vs 42 ritos~~ — decidido: **42**.
- [ ] Publicar no Cloudflare Pages (**aguardando sua confirmação**, conforme o briefing).
