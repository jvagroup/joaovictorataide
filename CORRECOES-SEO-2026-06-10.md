# Correções SEO — joaovictorataide.com.br (10/06/2026)

## O que foi corrigido neste pacote

**1. sitemap.xml** — regenerado a partir dos arquivos reais. Antes: 20 URLs com erro de digitação (404 para o Google) e 19 artigos publicados ausentes. Agora: 46 URLs, todas existentes (homepage, /blog/, /maritimidade/ e 43 artigos canônicos).

**2. Homepage (index.html)** — os 11 cards de "Insights e artigos" tinham 9 links trocados e 1 link 404. Substituídos por 12 cards apontando para artigos reais, cobrindo todos os silos (holding, imóveis, médicos, agro, comex, marítimo, reforma, teses).

**3. blog/index.html** — listava ~40 artigos, sendo 14 links 404 (artigos planejados nunca publicados). Grid regenerado com os 43 artigos canônicos, todos com data-cat correto. Novo filtro "Comércio Exterior" adicionado.

**4. 113 links internos quebrados** dentro dos artigos — todos remapeados para os artigos existentes equivalentes.

**5. Canonicals** — 42 artigos tinham canonical sem ".html" (divergindo do sitemap e dos links internos = sinais conflitantes para o Google). Padronizados com .html. 1 artigo (itcmd-progressivo) não tinha canonical — inserido.

**6. Duplicatas** — 3 pares de artigos quase idênticos. Mantido 1 canônico de cada par; o outro virou stub de redirecionamento:
- hong-kong-basileia-... → convencoes-hong-kong-basileia-...
- riocomex-regime-tributario-rj-2026 → riocomex-regime-tributario-importacao-rj-2026
- holding-familiarnareforma-... → holding-reforma-tributaria-2026

**7. Arquivo deletado** — "Create tributos-reforma-itcmd-progressivo-lc-214-2025.html" (nome inválido com espaço, criado por engano no GitHub web; conteúdo duplicava o artigo de ITCMD).

**8. 25 stubs de redirecionamento** criados em /blog/ — páginas com meta-refresh + canonical para os URLs antigos que o Google indexou. Necessário porque o GitHub Pages **ignora o arquivo _redirects** (que é padrão Netlify/Cloudflare Pages). O _redirects foi mantido e corrigido (vários alvos dele apontavam para URLs com typo) para o caso de futura migração.

## Como publicar
1. Substitua TODO o conteúdo do repositório jvagroup/joaovictorataide pelos arquivos deste pacote (ou faça upload dos arquivos alterados mantendo os caminhos).
2. Delete manualmente no GitHub o arquivo "Create tributos-reforma-itcmd-progressivo-lc-214-2025.html" da pasta /blog/ (uploads não deletam arquivos).
3. No Google Search Console: Sitemaps → reenviar sitemap.xml.
4. Em 48–72h, verificar em Indexação → Páginas se os 404 caem.
