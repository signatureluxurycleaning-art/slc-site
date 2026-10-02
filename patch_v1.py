# -*- coding: utf-8 -*-
"""Pacote v1 de melhorias do site (16/09/2026) — aplicado sobre site/.

O QUE ESTE SCRIPT FAZ (e por quê):
 1. PREÇO VISÍVEL NO CELULAR — o mockup de iPhone do hero (único lugar da home
    com preços) é display:none em telas ≤1024px; o primeiro preço que um
    visitante mobile via era o "From $750" do White Glove. Adiciona uma faixa
    de preços mobile no hero e preço em TODOS os cards de serviço da home.
 2. CTA vende o preço, não "o app": "Open Our App"/"Use Our App" viram
    "See Your Price & Book"/"See Prices & Book" nos botões de conversão.
 3. CONSISTÊNCIA: 6/7/8 serviços → 8; 18/18+/20+/22 cidades → 22; © 2025 →
    © 2026; e-mail do rodapé por extenso; topbar ganha "bonded".
 4. BEFORE/AFTER real: 3 pares de fotos wg_* (já no assets, dos trabalhos
    White Glove) viram uma faixa Antes/Depois na seção Our Work.
 5. REVIEWS DE CIDADE: depoimentos genéricos ("Jennifer M.") são trocados
    pelas reviews reais do Google que já estão na home.
 6. JAPONÊS no site (anúncios rodam para ja) + correções de contagem em
    TODAS as línguas.
 7. MEDIÇÃO: todo link para o app ganha ?src=site-... para o funil
    site→app ficar atribuível.
 8. 404 com a marca + robots.txt + .htaccess (ErrorDocument na IONOS).
 9. Badge "5.0 — Perfect Score" não cobre mais o "Welcome back!" do mockup.
10. (21/09) MEDIÇÃO EM TODAS AS PÁGINAS: evento de conversão nas páginas de
    serviço/legais (só existia na home e cidades — 13 cliques pagos, 0
    conversões), gclid/utm encaminhados do anúncio até o app, âncoras
    /#reviews e /#areas rolando na carga.
11. (21/09) FORMULÁRIO "personalized price by text" nas 8 páginas de serviço
    e na home: quem vem do anúncio deixa nome, celular e dados da casa e o
    dono responde por SMS com valor personalizado (o site NÃO mostra preço;
    o app segue exigindo cadastro antes do valor — decisão do dono).
12. (25/09) CIDADES DO NORTE: o Google Ads passou a mirar San Mateo, Foster
    City, Redwood Shores, Emerald Hills, Burlingame e Hillsborough, com
    sitelinks por cidade. Cria /locations/foster-city/ (não existia — os
    links "Foster City" caíam em /#areas), põe Redwood Shores na página de
    Redwood City, 22 → 23 cidades em todo o site (7 línguas) e sitemap.
13. (30/09) SEM O NOME DO DONO: "quando coloca Raphael, é homem, e muita gente
    fica com o pé atrás" — o formulário de cotação (home + 8 serviços) e a
    seção da primeira limpeza passam a dizer "the owner" / "one of the
    owners"; as reviews reais dos clientes que citam o nome ficam.
14. (30/09, tarde) NENHUM NOME, SEMPRE "OWNERS": "Não pode aparecer nem meu
    nome, nem o da Cristine, nem o da Viridiane. Em lugar nenhum. Fala donos.
    Sempre donos." — formulário e cards passam ao plural ("the owners will
    text you", "You Always Talk to the Owners", "One of the owners…"); nas
    reviews reais o nome vira [They]/[their] entre colchetes (edição sinalizada,
    sentido preservado), no card e no JSON-LD; comentário HTML sem nome. A
    verificação agora varre TODOS os arquivos de texto do site, sem exceção.

15. (02/10) CHATGPT / BING: o ChatGPT indicou a SLC para 2 clientes e o dono
    quer ser achado melhor. Os dados que os robôs leem estavam errados: o
    schema apontava para a Página ANTIGA do Facebook (perdida em ago/2026), as
    páginas de cidade tinham "YOUR_GOOGLE_CID" no lugar do link do Google, a
    contagem de reviews estava em 8/9 (são 12) e a home listava San Jose em
    primeiro e não tinha Atherton, Los Altos Hills, Woodside e San Carlos. E
    39% das visitas do robô de busca do ChatGPT davam 404 em endereços comuns
    (/pricing, /contact, /about, /faq, /book…) — _redirects leva cada um
    para o lugar certo. Os endereços das páginas de cidade NÃO mudam aqui
    (aguardam decisão do dono sobre Los Altos).

16. (02/10) LINK "LEAVE US A REVIEW" QUEBRADO: o place ID do Google no link
    de review da home e das 23 páginas de cidade tinha 26 caracteres (faltava
    um byte) e o Google respondia 404 — ninguém conseguia deixar review pelo
    site. O ID certo foi montado a partir do ID da ficha no Maps (o mesmo
    CID 10124342750083586343) e testado: abre "escrever review" da SLC.
    Só muda o href desses links; texto, títulos e schema ficam iguais.

Idempotente: rodar duas vezes dá no mesmo. Falha alto (exit 1) se qualquer
âncora esperada não existir ou existir em quantidade errada.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from patch_data import CHANGED_KEYS, STRONG_SWAP, PRICE_FIXES, NEW_KEYS, JA_DICT, REAL_REVIEWS

ROOT = Path(__file__).parent / "site"
ERRORS = []
CHANGES = []


def log(msg):
    CHANGES.append(msg)


def fail(msg):
    ERRORS.append(msg)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write(p: Path, s: str):
    p.write_text(s, encoding="utf-8")


def sub_count(text: str, old: str, new: str, expect, where: str):
    """Substitui old→new exigindo exatamente `expect` ocorrências (int ou (min,max))."""
    n = text.count(old)
    lo, hi = (expect, expect) if isinstance(expect, int) else expect
    if not (lo <= n <= hi):
        if old == new or n == 0 and text.count(new) > 0:
            return text  # já aplicado (idempotência)
        fail(f"{where}: esperava {expect}x o trecho {old[:60]!r}, achei {n}x")
        return text
    return text.replace(old, new)


# ═════════════════════════════ 1. translations.js ═══════════════════════════

def patch_translations():
    p = ROOT / "assets/translations.js"
    t = read(p)
    if '"ja"' in t or "ja: {" in t:
        log("translations.js: já contém ja — pulando inserções (idempotência)")
        return

    # blocos por idioma
    order = ["en", "zh", "hi", "tl", "vi", "ko"]
    idx = {lang: t.index(f"  {lang}: {{") for lang in order}
    end = t.index("\n};", idx["ko"])  # fecha o objeto TRANSLATIONS
    bounds = {lang: (idx[lang], idx[order[i + 1]] if i + 1 < len(order) else end)
              for i, lang in enumerate(order)}

    def edit_block(lang, fn):
        nonlocal t
        lo, hi = bounds[lang]
        block = t[lo:hi]
        block2 = fn(block)
        t = t[:lo] + block2 + t[hi:]
        delta = len(block2) - len(block)
        for l2 in order:
            a, b = bounds[l2]
            bounds[l2] = (a + delta if a > lo else a, b + delta if b >= hi else b)

    js = lambda v: v.replace("\\", "\\\\").replace('"', '\\"')

    for lang in order:
        def apply(block, lang=lang):
            to_add = dict(NEW_KEYS[lang])
            # chaves alteradas (se a língua não tiver a chave, ela é adicionada)
            for key, val in CHANGED_KEYS.get(lang, {}).items():
                pat = re.compile(r'(%s:\s*")(?:[^"\\]|\\.)*(")' % re.escape(key))
                if not pat.search(block):
                    to_add[key] = val
                    continue
                block = pat.sub(lambda m: m.group(1) + js(val) + m.group(2), block)
            # © 2025 → 2026 dentro de footer_copy
            block = re.sub(r'(footer_copy:\s*"[^"]*?)2025', r'\g<1>2026', block)
            # footer_desc: 20+ → 22 (formas por idioma)
            block = block.replace("20+ cities", "22 cities").replace("20多个城市", "22个城市")
            block = block.replace("20+ शहरों", "22 शहरों").replace("20+ lungsod", "22 lungsod")
            block = block.replace("hơn 20 thành phố", "22 thành phố").replace("20개 이상의 도시", "22개 도시")
            # <strong> dos botões compostos
            old_s, new_s = STRONG_SWAP[lang]
            block = block.replace(f"<strong>{old_s}</strong>", f"<strong>{new_s}</strong>")
            # preços defasados
            for key, (old_n, new_n) in PRICE_FIXES.items():
                block = re.sub(r'(%s:\s*"[^"]*?)%s' % (re.escape(key), old_n), r'\g<1>' + new_n, block)
            # chaves novas logo após a abertura do bloco ("  en: {\n")
            open_tok = f"  {lang}: {{\n"
            if open_tok not in block:
                fail(f"translations[{lang}]: abertura do bloco não encontrada")
                return block
            new_lines = "".join(f'    {k}: "{js(v)}",\n' for k, v in to_add.items())
            block = block.replace(open_tok, open_tok + new_lines, 1)
            return block
        edit_block(lang, apply)

    # dicionário japonês completo antes do fechamento do objeto.
    # O bloco ko fecha com "  }" SEM vírgula (é o último) — a inserção
    # começa com "," para manter o objeto válido.
    ja_lines = "".join(f'    {k}: "{js(v)}",\n' for k, v in JA_DICT.items())
    ja_block = ",\n\n  // ─────────────────────────────────────────────\n  ja: {\n" + ja_lines + "  }"
    end2 = t.index("\n};", idx["en"])
    t = t[:end2] + ja_block + t[end2:]

    t = sub_count(t, "const SUPPORTED_LANGS = ['en', 'zh', 'hi', 'tl', 'vi', 'ko'];",
                  "const SUPPORTED_LANGS = ['en', 'zh', 'hi', 'tl', 'vi', 'ko', 'ja'];", 1, "translations.js")
    write(p, t)
    log("translations.js: 6 línguas corrigidas + dicionário ja completo + SUPPORTED_LANGS")


# ═════════════════════════════ 2. index.html ═════════════════════════════════

HERO_PRICES_HTML = """        <div class="hero-prices" aria-label="Starting prices">
          <a class="hp-chip" href="https://app.signatureluxurycleaning.com/?src=site-hero">🧹 <span data-i18n="svc_regular">Regular</span>&nbsp;<strong>$170+</strong></a>
          <a class="hp-chip" href="https://app.signatureluxurycleaning.com/?src=site-hero">✨ <span data-i18n="svc_deep">Deep Clean</span>&nbsp;<strong>$270+</strong></a>
          <a class="hp-chip" href="https://app.signatureluxurycleaning.com/?src=site-hero">📦 <span data-i18n="svc_moveout">Move Out</span>&nbsp;<strong>$330+</strong></a>
          <div class="hp-note" data-i18n="hero_prices_note">Exact price for your home in the app — takes 60 seconds.</div>
        </div>
"""

HERO_PRICES_CSS = (
    ".hero-prices{display:none}"
    "@media(max-width:1024px){"
    ".hero-content{padding:3.5rem 2rem 3rem}"
    ".hero-title{font-size:clamp(2.3rem,8vw,3.2rem)}"
    ".hero-prices{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1.6rem}"
    ".hp-chip{display:inline-flex;align-items:center;gap:.35rem;background:rgba(255,255,255,.07);"
    "border:1px solid rgba(200,151,58,.45);color:#fff;font-size:.86rem;font-weight:500;"
    "padding:.5rem .85rem;border-radius:50px;white-space:nowrap}"
    ".hp-chip strong{color:var(--gold-light);font-weight:700}"
    ".hp-note{flex-basis:100%;color:rgba(255,255,255,.55);font-size:.75rem;margin-top:.15rem}"
    "}"
)

BA_HTML = """
      <div class="ba-strip">
        <h3 class="ba-title" data-i18n="ba_title">Before &amp; After — real jobs, documented by our own team</h3>
        <div class="ba-grid">
          <figure class="ba-pair">
            <div class="ba-imgs">
              <div class="ba-half"><img src="assets/img/wg_kitchen_stove_before.jpg" alt="Behind the stove before White Glove deep cleaning" loading="lazy" decoding="async"><span class="ba-tag">BEFORE</span></div>
              <div class="ba-half"><img src="assets/img/wg_kitchen_stove_after.jpg" alt="Behind the stove after White Glove deep cleaning" loading="lazy" decoding="async"><span class="ba-tag after">AFTER</span></div>
            </div>
            <figcaption data-i18n="ba_cap1">Behind the stove — White Glove Deep Clean</figcaption>
          </figure>
          <figure class="ba-pair">
            <div class="ba-imgs">
              <div class="ba-half"><img src="assets/img/wg_kitchen_fridge_before.jpg" alt="Under the refrigerator before deep cleaning" loading="lazy" decoding="async"><span class="ba-tag">BEFORE</span></div>
              <div class="ba-half"><img src="assets/img/wg_kitchen_fridge_after.jpg" alt="Under the refrigerator after deep cleaning" loading="lazy" decoding="async"><span class="ba-tag after">AFTER</span></div>
            </div>
            <figcaption data-i18n="ba_cap2">Under &amp; behind the refrigerator</figcaption>
          </figure>
          <figure class="ba-pair">
            <div class="ba-imgs">
              <div class="ba-half"><img src="assets/img/wg_bathroom_shower_before.jpg" alt="Shower and tile before restoration cleaning" loading="lazy" decoding="async"><span class="ba-tag">BEFORE</span></div>
              <div class="ba-half"><img src="assets/img/wg_bathroom_shower_after.jpg" alt="Shower and tile after restoration cleaning" loading="lazy" decoding="async"><span class="ba-tag after">AFTER</span></div>
            </div>
            <figcaption data-i18n="ba_cap3">Shower &amp; tile restoration</figcaption>
          </figure>
        </div>
      </div>
"""

BA_CSS = (
    "\n/* Before/After strip (v1 16/09/2026) */\n"
    ".ba-strip{margin-top:3rem}\n"
    ".ba-title{font-size:1.35rem;margin-bottom:1.25rem;color:var(--text-dark);text-align:center}\n"
    ".ba-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem}\n"
    ".ba-pair{margin:0;background:var(--white);border-radius:var(--radius-md);overflow:hidden;box-shadow:var(--shadow-sm)}\n"
    ".ba-imgs{display:grid;grid-template-columns:1fr 1fr;gap:2px}\n"
    ".ba-half{position:relative}\n"
    ".ba-half img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}\n"
    ".ba-tag{position:absolute;top:8px;left:8px;background:rgba(12,26,46,.85);color:#fff;font-size:.62rem;font-weight:700;letter-spacing:.08em;padding:.2rem .5rem;border-radius:4px}\n"
    ".ba-tag.after{background:var(--gold);color:var(--navy)}\n"
    ".ba-pair figcaption{font-size:.82rem;color:var(--text-body);padding:.7rem .9rem}\n"
    "@media(max-width:768px){.ba-grid{grid-template-columns:1fr}}\n"
)

CARD_PRICES = {
    'data-i18n="svc1_title"': 'From <strong>$170</strong>',
    'data-i18n="svc2_title"': 'From <strong>$270</strong>',
    'data-i18n="svc3_title"': 'From <strong>$330</strong>',
    'data-i18n="svc4_title"': '<strong>Custom Quote</strong>',
    'data-i18n="svc5_title"': 'From <strong>$155</strong>',
    '<h3>Office &amp; Commercial Cleaning</h3>': '<strong>Custom Quote</strong>',
    'data-i18n="svc6_title"': 'From <strong>$410</strong>',
}


def tag_app_links(text: str, src: str, where: str):
    """Acrescenta ?src=... a todos os links do app que ainda não têm query."""
    def rep(m):
        url = m.group(1)
        if "?" in url or "src=" in url:
            return m.group(0)
        if url.endswith("/download"):
            return f'href="{url}?src={src}"'
        if url.rstrip("/").endswith("signatureluxurycleaning.com"):
            base = url if url.endswith("/") else url + "/"
            return f'href="{base}?src={src}"'
        return f'href="{url}?src={src}"'
    out, n = re.subn(r'href="(https://app\.signatureluxurycleaning\.com[^"?]*)"', rep, text)
    if n:
        log(f"{where}: {n} link(s) do app marcados com ?src={src}")
    return out


def patch_index():
    p = ROOT / "index.html"
    t = read(p)
    if "hero-prices" in t:
        log("index.html: já patcheado — pulando (idempotência)")
        return

    # contagens / metadados
    t = sub_count(t, "Sunnyvale, Burlingame & 18 cities", "Sunnyvale, Burlingame & 22 cities", 1, "index meta")
    t = sub_count(t, "Serving 18 cities across Silicon Valley & Peninsula", "Serving 22 cities across Silicon Valley & Peninsula", 1, "index og")
    t = sub_count(t, "Cupertino and 18 cities across Silicon Valley & Peninsula",
                  "Cupertino and 22 cities across Silicon Valley & Peninsula", 1, "index schema desc")
    t = sub_count(t, "We serve 18 cities across the San Francisco Bay Area",
                  "We serve 22 cities across the San Francisco Bay Area", 1, "index schema faq")
    t = sub_count(t, "We serve 18 cities across the Bay Area:",
                  "We serve 22 cities across the Bay Area:", 1, "index faq details")
    t = sub_count(t, '<span class="number">18+</span>', '<span class="number">22</span>', 1, "index hero stat")
    t = sub_count(t, "We serve 18 cities across Silicon Valley & Peninsula — from Burlingame to San Jose.",
                  "We serve 22 cities across Silicon Valley & Peninsula — from Burlingame to San Jose.", 1, "index areas subtitle")

    # fallbacks EN no HTML (translations.js cobre depois do load)
    t = sub_count(t, "Signature Luxury Cleaning offers seven services across Silicon Valley: Regular Cleaning, Deep Cleaning, Move In/Out, Post-Construction, Airbnb Turnover, Office Cleaning, and Spring Cleaning.",
                  "Signature Luxury Cleaning offers eight services across Silicon Valley: Regular Cleaning, Deep Cleaning, Move In/Out, Post-Construction, Airbnb Turnover, Office Cleaning, Spring Cleaning, and the White Glove Deep Clean.", 1, "index aeo_services")
    t = sub_count(t, "Six professional cleaning services", "Eight professional cleaning services", 1, "index services_subtitle")
    t = sub_count(t, "Background-checked &amp; fully insured team", "Background-checked, bonded &amp; fully insured team", 2, "index topbar")
    t = t.replace("© 2025 Signature Luxury Cleaning", "© 2026 Signature Luxury Cleaning")

    # CTA fallbacks
    t = sub_count(t, '<strong data-i18n="hero_btn_strong">Open Our App</strong>',
                  '<strong data-i18n="hero_btn_strong">See Your Price &amp; Book</strong>', 1, "index hero btn")
    t = sub_count(t, '>📱 Use Our App</a>', '>📱 See Prices &amp; Book</a>', 2, "index nav_app")

    # faixa de preços mobile no hero — ANTES dos stats (preço é o que o
    # visitante frio quer ver primeiro; stats vêm depois)
    anchor = '        <div class="hero-stats">'
    t = sub_count(t, anchor, HERO_PRICES_HTML + anchor, 1, "index hero strip")

    # CSS crítico inline + preço nos cards
    t = sub_count(t, "  </style>", "    " + HERO_PRICES_CSS + "\n  </style>", 1, "index critical css")

    for anchor_h3, price in CARD_PRICES.items():
        i = t.find(anchor_h3)
        if i < 0:
            fail(f"index cards: âncora não achada: {anchor_h3[:50]}")
            continue
        j = t.find('<a href="https://app.signatureluxurycleaning.com', i)
        blockslice = t[i:j]
        if 'service-meta' in blockslice:
            continue  # WG já tem; idempotência
        meta = f'<div class="service-meta"><span class="service-price">{price}</span></div>\n            '
        t = t[:j] + meta + t[j:]

    # before/after na galeria
    gi = t.index('id="gallery"')
    gsec_end = t.index("</section>", gi)
    gallery_slice = t[gi:gsec_end]
    close_grid = gallery_slice.rindex("</div>\n      </div>")
    insert_at = gi + close_grid + len("</div>")
    t = t[:insert_at] + "\n" + BA_HTML + t[insert_at:]

    # e-mails por extenso
    t = re.sub(r'<a href="/cdn-cgi/l/email-protection#[^"]*">✉️ booking@\.\.\.</a>',
               '<a href="mailto:booking@signatureluxurycleaning.com">✉️ booking@signatureluxurycleaning.com</a>', t)
    t = re.sub(r'<a href="/cdn-cgi/l/email-protection"[^>]*data-cfemail="[^"]*">\[email&#160;protected\]</a>',
               '<a href="mailto:booking@signatureluxurycleaning.com">booking@signatureluxurycleaning.com</a>', t)

    # japonês nos DOIS seletores de idioma (dropdown desktop + linha mobile)
    ko_btn = '<button class="lang-btn" data-lang="ko">🇰🇷 한국어</button>'
    ja_btn = '<button class="lang-btn" data-lang="ja">🇯🇵 日本語</button>'
    t = sub_count(t, ko_btn, ko_btn + "\n        " + ja_btn, 2, "index lang selectors")

    # links do app com origem
    t = tag_app_links(t, "site-home", "index")

    write(p, t)
    log("index.html: contagens, CTA, faixa de preços mobile, preços nos cards, before/after, e-mail, ja, ?src")


# ═════════════════════ 3. style.css (badge + novas seções) ══════════════════

def patch_css():
    p = ROOT / "assets/style.css"
    t = read(p)
    if ".ba-strip" in t:
        log("style.css: já patcheado — pulando")
        return
    t = sub_count(t, ".mockup-badge.badge-rating {\n  top: 60px;\n  right: -30px;\n}",
                  ".mockup-badge.badge-rating {\n  top: 132px;\n  right: -30px;\n}", 1, "style badge")
    t += "\n/* v1 16/09/2026 — faixa de preços mobile no hero */\n" + HERO_PRICES_CSS + "\n" + BA_CSS
    write(p, t)
    log("style.css: badge 5.0 reposicionado + CSS da faixa de preços e do before/after")


# ═════════════════════ 4. páginas de cidade (22) ═════════════════════════════

def patch_cities():
    # cidades criadas depois do pacote v1 (passo 12) já nascem prontas e ficam
    # FORA da enumeração: o índice ci escolhe as reviews de cada página, e uma
    # pasta nova no meio da ordem alfabética trocaria as reviews de metade das
    # cidades a cada execução
    cities = sorted(c for c in (ROOT / "locations").iterdir() if c.is_dir() and c.name not in NEW_CITY_SLUGS)
    for ci, cdir in enumerate(cities):
        slug = cdir.name
        p = cdir / "index.html"
        t = read(p)

        t = t.replace("Background-checked &amp; fully insured team", "Background-checked, bonded &amp; fully insured team")
        t = t.replace("© 2025 Signature Luxury Cleaning", "© 2026 Signature Luxury Cleaning")
        t = t.replace("<strong>Open Our App</strong>", "<strong>See Your Price &amp; Book</strong>")

        # reviews reais no lugar dos depoimentos genéricos
        if "Read our Google reviews" in t:
            log(f"{slug}: bloco de reviews já é o card honesto do Google — mantido")
        else:
            picks = [REAL_REVIEWS[(ci + k) % len(REAL_REVIEWS)] for k in (0, 2, 4)]
            blocks = re.findall(r'<div class="review-card">.*?</div>\s*</div>', t, re.S)
            if len(blocks) >= 3:
                for (name, text), old in zip(picks, blocks[:3]):
                    new = ('<div class="review-card">\n          <div class="review-stars">★★★★★</div>\n'
                           f'          <p>"{text}"</p>\n'
                           f'          <div class="review-author">— {name}, Silicon Valley · Google review</div>\n        </div>')
                    t = t.replace(old, new, 1)
            else:
                fail(f"{slug}: bloco de reviews não encontrado ({len(blocks)})")

        t = tag_app_links(t, f"site-{slug}", slug)
        write(p, t)
    log("locations/: 22 cidades — bonded, © 2026, CTA, reviews reais, ?src")


# ═════════════════════ 5. páginas de serviço + legais ═══════════════════════

def patch_services_legal():
    for p in sorted(ROOT.glob("services/*/index.html")):
        slug = p.parent.name
        t = read(p)
        t = t.replace("© 2025 Signature Luxury Cleaning", "© 2026 Signature Luxury Cleaning")
        t = t.replace("Background-checked &amp; fully insured team", "Background-checked, bonded &amp; fully insured team")
        t = re.sub(r'<a href="/cdn-cgi/l/email-protection[^"]*"[^>]*>(?:<span[^>]*>)?\[email&#160;protected\](?:</span>)?</a>',
                   '<a href="mailto:booking@signatureluxurycleaning.com">booking@signatureluxurycleaning.com</a>', t)
        t = tag_app_links(t, f"site-svc-{slug}", f"services/{slug}")
        write(p, t)
    for rel in ["privacy-policy/index.html", "terms-and-conditions/index.html", "privacy.html"]:
        p = ROOT / rel
        if p.exists():
            t = read(p).replace("© 2025 Signature Luxury Cleaning", "© 2026 Signature Luxury Cleaning")
            write(p, t)
    log("services/ + legais: © 2026, bonded, e-mail, ?src")


# ═════════════ 5b. rótulos reais de conversão (Google Ads) ══════════════════
# Os eventos gtag do site apontavam para rótulos placeholder que o Google
# descarta. Ações criadas em 15/09/2026 (conta 314-199-1480, ambas Secondary):
#   • "Site - clique para o app"  → RBjKCM2TsfkcEODfpNg_
#   • "Site - clique ligar/SMS"   → KbSHCOeFsPkcEODfpNg_  (tel: e sms:)
CONV_LABELS = {
    "APP_OPEN_LABEL": "RBjKCM2TsfkcEODfpNg_",
    "PHONE_CLICK_LABEL": "KbSHCOeFsPkcEODfpNg_",
    "SMS_CLICK_LABEL": "KbSHCOeFsPkcEODfpNg_",
}


def patch_conversion_labels():
    n = 0
    for p in ROOT.rglob("*.html"):
        t = read(p)
        t2 = t
        for old, new in CONV_LABELS.items():
            t2 = t2.replace(f"AW-17096585184/{old}", f"AW-17096585184/{new}")
        if t2 != t:
            write(p, t2)
            n += 1
    log(f"rótulos de conversão reais aplicados em {n} página(s)")


# ═════════ 5c. medição em TODAS as páginas (21/09/2026) ═════════════════════
# Raio-X do Google Ads (Sep 1–20): 13 cliques pagos, 100% caindo nas páginas
# de serviço (/services/regular-cleaning/ e /services/deep-cleaning/) — e ZERO
# conversões "Site - clique para o app". Causa: o bloco de conversão só existia
# no index.html e nas 22 páginas de cidade; as páginas de serviço e legais não
# tinham NENHUM listener. Este passo:
#   (a) injeta o bloco de conversão (clique→app, tel:, sms:) em toda página
#       que ainda não o tem;
#   (b) em TODAS as páginas, encaminha gclid/gbraid/wbraid/utm_* do anúncio
#       para os links do app (guardados em sessionStorage para sobreviver à
#       navegação site→site), para o cadastro no app ficar google/cpc;
#   (c) corrige a âncora na carga (/#reviews, /#areas não rolavam: o scroll
#       inicial se perdia com o layout carregando).
CONV_LABEL_APP = "AW-17096585184/RBjKCM2TsfkcEODfpNg_"
CONV_LABEL_CONTACT = "AW-17096585184/KbSHCOeFsPkcEODfpNg_"

CONV_BLOCK = """
  <script>
    // slc-conv-v1 — Google Ads + GA4: clique para o app, ligar e SMS
    document.addEventListener('DOMContentLoaded', function() {
      function conv(label, ga4, extra) {
        if (typeof gtag !== 'function') return;
        gtag('event', 'conversion', { 'send_to': label });
        gtag('event', ga4, extra || {});
      }
      document.querySelectorAll('a[href*="app.signatureluxurycleaning.com"]').forEach(function(link) {
        link.addEventListener('click', function() {
          conv('%(app)s', 'open_app', { 'event_category': 'app', 'event_label': this.textContent.trim().slice(0, 50) });
        });
      });
      document.querySelectorAll('a[href^="tel:"]').forEach(function(link) {
        link.addEventListener('click', function() { conv('%(contact)s', 'phone_click', { 'event_category': 'contact' }); });
      });
      document.querySelectorAll('a[href^="sms:"]').forEach(function(link) {
        link.addEventListener('click', function() { conv('%(contact)s', 'sms_click', { 'event_category': 'contact' }); });
      });
    });
  </script>
""" % {"app": CONV_LABEL_APP, "contact": CONV_LABEL_CONTACT}

FORWARD_BLOCK = """
  <script>
    // slc-forward-v2 — leva gclid/utm do anúncio até o app e conserta a âncora na carga
    (function() {
      var KEYS = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
      var STORE = 'slc:click-params:v1';
      function readParams() {
        var out = {};
        try {
          var q = new URLSearchParams(location.search);
          KEYS.forEach(function(k) { var v = q.get(k); if (v) out[k] = v.slice(0, 200); });
          if (Object.keys(out).length) { sessionStorage.setItem(STORE, JSON.stringify(out)); return out; }
          var saved = sessionStorage.getItem(STORE);
          return saved ? JSON.parse(saved) : {};
        } catch (e) { return out; }
      }
      function forward() {
        var params = readParams();
        if (!Object.keys(params).length) return;
        document.querySelectorAll('a[href*="app.signatureluxurycleaning.com"]').forEach(function(a) {
          try {
            var u = new URL(a.getAttribute('href'), location.href);
            KEYS.forEach(function(k) { if (params[k] && !u.searchParams.has(k)) u.searchParams.set(k, params[k]); });
            a.setAttribute('href', u.toString());
          } catch (e) {}
        });
      }
      function fixHash() {
        if (!location.hash || location.hash.length < 2) return;
        var el = document.getElementById(location.hash.slice(1));
        if (!el) return;
        // 'instant' ignora o scroll-behavior:smooth do html — o scroll suave era
        // justamente o que se perdia com o layout ainda carregando.
        var go = function() { el.scrollIntoView({ block: 'start', behavior: 'instant' }); };
        setTimeout(go, 350);
        setTimeout(go, 1200);
      }
      if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', forward); else forward();
      window.addEventListener('load', fixHash);
    })();
  </script>
"""


def patch_measurement_everywhere():
    n_conv = n_fwd = 0
    for p in sorted(ROOT.rglob("*.html")):
        t = read(p)
        if "</body>" not in t:
            fail(f"{p}: sem </body>")
            continue
        t2 = t
        if "RBjKCM2TsfkcEODfpNg_" not in t2 and "slc-conv-v1" not in t2:
            t2 = t2.replace("</body>", CONV_BLOCK + "</body>", 1)
            n_conv += 1
        # versão antiga do bloco (v1, scroll suave) é removida antes de inserir a atual
        t2 = re.sub(r"\n  <script>\n    // slc-forward-v1 [\s\S]*?</script>\n", "\n", t2)
        if "slc-forward-v2" not in t2:
            t2 = t2.replace("</body>", FORWARD_BLOCK + "</body>", 1)
            n_fwd += 1
        if t2 != t:
            write(p, t2)
    log(f"medição: bloco de conversão em {n_conv} página(s) que não tinham; encaminhamento gclid/utm + âncora em {n_fwd} página(s)")


# ═════════ 5d. formulário "personalized price by text" (21/09/2026) ══════════
# Decisão do dono: o app continua pedindo cadastro antes do preço (filtra
# curiosos e concorrentes). Para quem vem do anúncio e não quer se cadastrar,
# as páginas de serviço e a home ganham um formulário: nome, celular e dados da
# casa → o Raphael responde por SMS com um valor personalizado. O cliente NÃO
# vê preço aqui. Envio vai direto ao Worker do app (POST /api/site/quote-request).
QUOTE_API = "https://slc-app-worker.booking-f8e.workers.dev/api/site/quote-request"
QUOTE_CONV_LABEL = "b8AICJ24ppMcEODfpNg_"  # Google Ads "Submit lead form" (AW-17096585184/b8AICJ24ppMcEODfpNg_), obtido 22/09/2026

# slug da página → (id do serviço no app, frequência sugerida)
QUOTE_SERVICE_BY_SLUG = {
    "regular-cleaning": ("regular", "biweekly"),
    "deep-cleaning": ("deep", "onetime"),
    "move-in-out-cleaning": ("moveinout", "onetime"),
    "post-construction-cleaning": ("postconstruction", "onetime"),
    "spring-cleaning": ("spring", "onetime"),
    "airbnb-cleaning": ("airbnb", "onetime"),
    "white-glove-deep-clean": ("whiteglove", "onetime"),
    "office-cleaning": ("office", "onetime"),
}

QUOTE_SECTION_HTML = """
  <!-- slc-quote-form v2: two ways to get a price — app (instant, automatic) or personalized text. No price shown here. -->
  <section class="section qf-section" id="quote-form" data-qf-version="2" data-default-service="%(service)s" data-default-frequency="%(frequency)s" data-app-href="%(app_href)s">
    <div class="qf-wrap">
      <div class="qf-intro">
        <div class="qf-eyebrow">Two ways to get your price</div>
        <h2 class="qf-title">Instant in the app, or personal by text</h2>
        <div class="qf-app">
          <div class="qf-app-badge">⚡ Fastest · fully automatic</div>
          <h3 class="qf-app-title">Do it all yourself in our app</h3>
          <ol class="qf-app-steps">
            <li><span class="qf-step-n">1</span><span><strong>See your exact price</strong> for your home in seconds</span></li>
            <li><span class="qf-step-n">2</span><span><strong>Pick the day and time</strong> that works for you</span></li>
            <li><span class="qf-step-n">3</span><span><strong>Book your visit</strong> — confirmed by text, no phone call needed</span></li>
          </ol>
          <a class="qf-app-btn" href="%(app_href)s" target="_blank" rel="noopener">📱 Open the App &amp; See My Price</a>
          <div class="qf-app-fine">No download · Secure · Takes about 2 minutes</div>
        </div>
        <ul class="qf-points">
          <li>Owner-operated · Bonded &amp; insured, background-checked team</li>
          <li>5.0★ on Google · Belmont to Los Gatos</li>
        </ul>
      </div>
      <form class="qf-form" id="qfForm" novalidate>
        <div class="qf-form-head">
          <div class="qf-form-kicker">Prefer a personal text?</div>
          <h3 class="qf-form-title">Get a personalized price by text</h3>
          <p class="qf-form-sub">Tell us about your home and Raphael, the owner, will text you a personalized price. No account needed.</p>
        </div>
        <div class="qf-grid">
          <label class="qf-field"><span>Your name</span><input name="name" type="text" autocomplete="name" required maxlength="120" placeholder="First and last name"></label>
          <label class="qf-field"><span>Mobile number</span><input name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20" placeholder="(650) 555-0123"></label>
          <label class="qf-field"><span>ZIP code</span><input name="zip" type="text" autocomplete="postal-code" inputmode="numeric" required pattern="[0-9]{5}" maxlength="5" placeholder="94301"></label>
          <label class="qf-field"><span>Home type</span><select name="propertyType"><option value="house">House</option><option value="apt">Apartment / condo</option></select></label>
          <label class="qf-field qf-half"><span>Bedrooms</span><select name="bedrooms"><option>1</option><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6</option><option value="7">7+</option></select></label>
          <label class="qf-field qf-half"><span>Bathrooms</span><select name="bathrooms"><option>1</option><option>1.5</option><option selected>2</option><option>2.5</option><option>3</option><option>3.5</option><option>4</option><option>4.5</option><option value="5">5+</option></select></label>
          <label class="qf-field"><span>Approx. square feet <em>(optional)</em></span><input name="sqft" type="text" inputmode="numeric" maxlength="6" placeholder="e.g. 2,400"></label>
          <label class="qf-field"><span>Service</span><select name="service">
            <option value="regular">Regular cleaning</option>
            <option value="deep">Deep cleaning</option>
            <option value="moveinout">Move-in / move-out</option>
            <option value="postconstruction">Post-construction</option>
            <option value="spring">Spring cleaning</option>
            <option value="airbnb">Airbnb turnover</option>
            <option value="whiteglove">White Glove deep clean</option>
            <option value="personalized">Personalized (you choose rooms)</option>
            <option value="office">Office cleaning</option>
          </select></label>
          <label class="qf-field"><span>How often</span><select name="frequency">
            <option value="onetime">One-time</option>
            <option value="weekly">Weekly</option>
            <option value="biweekly">Every 2 weeks</option>
            <option value="monthly">Monthly</option>
          </select></label>
          <label class="qf-field qf-full"><span>Anything we should know? <em>(optional)</em></span><textarea name="notes" rows="2" maxlength="1500" placeholder="Pets, preferred days, special requests…"></textarea></label>
        </div>
        <label class="qf-consent"><input type="checkbox" name="consent" required> <span>Text me my price at this number. One personal reply from Signature Luxury Cleaning; message &amp; data rates may apply. Reply STOP to opt out. <a href="/privacy-policy/" target="_blank" rel="noopener">Privacy</a></span></label>
        <div class="qf-hp" aria-hidden="true"><label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
        <button type="submit" class="qf-btn">💬 Text Me My Price</button>
        <div class="qf-error" role="alert" hidden></div>
        <div class="qf-fine">Owner-operated · We never share your number</div>
        <div class="qf-or"><span>or</span></div>
        <a class="qf-applink" href="%(app_href)s" target="_blank" rel="noopener">Skip the wait — see your price and book in the app →</a>
      </form>
      <div class="qf-success" id="qfSuccess" hidden>
        <div class="qf-success-icon">✅</div>
        <h3>Thanks, <span data-qf="firstName">there</span>!</h3>
        <p>Raphael will text <strong data-qf="phone"></strong> shortly with your personalized price.</p>
        <p class="qf-success-sub">Want it right now? <a href="%(app_href)s" target="_blank" rel="noopener">See your price and book in the app →</a></p>
      </div>
    </div>
  </section>
"""

QUOTE_CSS = (
    "\n/* slc-quote-v1 */"
    ".qf-section{background:var(--navy);padding:3.5rem 1rem;color:#fff}"
    ".qf-wrap{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:2.5rem;align-items:start}"
    ".qf-eyebrow{color:var(--gold-light);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;margin-bottom:.6rem}"
    ".qf-title{font-family:'Cormorant Garamond',serif;font-size:clamp(1.9rem,3.4vw,2.7rem);line-height:1.12;color:#fff;margin:0 0 .9rem}"
    ".qf-sub{color:rgba(255,255,255,.78);line-height:1.65;font-size:1rem;margin:0 0 1.2rem}"
    ".qf-points{list-style:none;padding:0;margin:0 0 1.4rem;display:grid;gap:.45rem}"
    ".qf-points li{color:rgba(255,255,255,.85);font-size:.92rem;padding-left:1.4rem;position:relative}"
    ".qf-points li:before{content:'✓';position:absolute;left:0;color:var(--gold-light);font-weight:700}"
    ".qf-applink{color:var(--gold-light);font-weight:600;text-decoration:none;font-size:.95rem;border-bottom:1px solid rgba(226,185,106,.45)}"
    ".qf-form{background:#fff;color:var(--text-dark);border-radius:16px;padding:1.5rem;box-shadow:0 18px 50px rgba(0,0,0,.28)}"
    ".qf-grid{display:grid;grid-template-columns:1fr 1fr;gap:.85rem 1rem}"
    ".qf-field{display:flex;flex-direction:column;gap:.3rem;font-size:.8rem;font-weight:600;color:var(--gray-700)}"
    ".qf-field em{font-weight:400;color:var(--gray-500);font-style:normal}"
    ".qf-field input,.qf-field select,.qf-field textarea{font:inherit;font-size:16px;font-weight:400;color:var(--text-dark);border:1px solid var(--gray-300);border-radius:10px;padding:.7rem .8rem;background:#fff;width:100%;min-width:0}"
    ".qf-field input:focus,.qf-field select:focus,.qf-field textarea:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 3px rgba(200,151,58,.18)}"
    ".qf-field.qf-invalid input,.qf-field.qf-invalid select{border-color:#c0392b}"
    ".qf-full{grid-column:1/-1}"
    ".qf-consent{display:flex;gap:.6rem;align-items:flex-start;margin:1rem 0 .9rem;font-size:.75rem;color:var(--gray-500);line-height:1.5}"
    ".qf-consent input{margin-top:.2rem;flex:none;width:16px;height:16px;accent-color:var(--gold)}"
    ".qf-consent a{color:var(--gold);text-decoration:none}"
    ".qf-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}"
    ".qf-btn{width:100%;border:0;cursor:pointer;background:linear-gradient(135deg,var(--gold),var(--gold-light));color:var(--navy);font-weight:700;font-size:1.05rem;padding:1rem 1.2rem;border-radius:50px;box-shadow:0 8px 24px rgba(200,151,58,.35);transition:transform .15s}"
    ".qf-btn:hover{transform:translateY(-1px)}.qf-btn[disabled]{opacity:.7;cursor:wait;transform:none}"
    ".qf-error{margin-top:.8rem;background:#fdf1ef;color:#8a2a1e;border:1px solid #f1c7c0;border-radius:10px;padding:.75rem .9rem;font-size:.88rem;line-height:1.5}"
    ".qf-error a{color:#8a2a1e;font-weight:700}"
    ".qf-fine{margin-top:.7rem;text-align:center;font-size:.72rem;color:var(--gray-500)}"
    ".qf-success{background:#fff;color:var(--text-dark);border-radius:16px;padding:2rem 1.5rem;text-align:center;box-shadow:0 18px 50px rgba(0,0,0,.28)}"
    ".qf-success-icon{font-size:2.4rem;margin-bottom:.4rem}"
    ".qf-success h3{font-family:'Cormorant Garamond',serif;font-size:1.9rem;margin:0 0 .5rem;color:var(--navy)}"
    ".qf-success p{color:var(--text-body);line-height:1.6;margin:0 0 .6rem}"
    ".qf-success-sub a{color:var(--gold);font-weight:600;text-decoration:none}"
    ".qf-app{background:rgba(255,255,255,.06);border:1px solid rgba(200,151,58,.45);border-radius:16px;padding:1.3rem 1.3rem 1.2rem;margin:.2rem 0 1.3rem;box-shadow:0 10px 30px rgba(0,0,0,.22)}"
    ".qf-app-badge{display:inline-block;background:linear-gradient(135deg,var(--gold),var(--gold-light));color:var(--navy);font-size:.72rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:.3rem .7rem;border-radius:50px;margin-bottom:.7rem}"
    ".qf-app-title{font-family:'Cormorant Garamond',serif;font-size:1.55rem;color:#fff;margin:0 0 .8rem;line-height:1.15}"
    ".qf-app-steps{list-style:none;margin:0 0 1rem;padding:0;display:grid;gap:.55rem}"
    ".qf-app-steps li{display:flex;gap:.7rem;align-items:flex-start;color:rgba(255,255,255,.88);font-size:.94rem;line-height:1.45}"
    ".qf-app-steps strong{color:#fff}"
    ".qf-step-n{flex:none;width:24px;height:24px;border-radius:50%;background:var(--gold);color:var(--navy);font-weight:700;font-size:.8rem;display:inline-flex;align-items:center;justify-content:center;margin-top:.05rem}"
    ".qf-app-btn{display:flex;align-items:center;justify-content:center;gap:.4rem;background:linear-gradient(135deg,var(--gold),var(--gold-light));color:var(--navy);font-weight:700;font-size:1rem;padding:.95rem 1.2rem;border-radius:50px;text-decoration:none;box-shadow:0 8px 24px rgba(200,151,58,.35);transition:transform .15s}"
    ".qf-app-btn:hover{transform:translateY(-1px)}"
    ".qf-app-fine{margin-top:.6rem;text-align:center;font-size:.74rem;color:rgba(255,255,255,.6)}"
    ".qf-form-head{margin-bottom:1rem}"
    ".qf-form-kicker{color:var(--gold);font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;margin-bottom:.3rem}"
    ".qf-form-title{font-family:'Cormorant Garamond',serif;font-size:1.6rem;color:var(--navy);margin:0 0 .35rem;line-height:1.15}"
    ".qf-form-sub{color:var(--text-body);font-size:.9rem;line-height:1.5;margin:0}"
    ".qf-or{display:flex;align-items:center;gap:.8rem;margin:1rem 0 .6rem;color:var(--gray-500);font-size:.75rem;text-transform:uppercase;letter-spacing:.1em}"
    ".qf-or:before,.qf-or:after{content:'';flex:1;height:1px;background:var(--gray-300)}"
    ".qf-form .qf-applink{display:block;text-align:center;color:var(--gold);border-bottom:0;font-size:.92rem}"
    "@media(max-width:860px){.qf-wrap{grid-template-columns:1fr;gap:1.6rem}.qf-section{padding:2.6rem 1rem}.qf-grid{grid-template-columns:1fr 1fr}.qf-grid .qf-field:not(.qf-half):not(.qf-full){grid-column:1/-1}.qf-form{padding:1.2rem}.qf-title{font-size:1.75rem}}"
)

QUOTE_JS = """
  <script>
    // slc-quote-v1 — envia o pedido de cotação ao Worker; nunca mostra preço aqui
    (function() {
      var API = '%(api)s';
      var CONV_LABEL = '%(label)s';
      var sec = document.getElementById('quote-form');
      var form = document.getElementById('qfForm');
      if (!sec || !form) return;
      var startedAt = Date.now();
      var byName = function(n) { return form.querySelector('[name="' + n + '"]'); };
      // pré-seleção pela página
      var svc = sec.getAttribute('data-default-service');
      var freq = sec.getAttribute('data-default-frequency');
      if (svc && byName('service').querySelector('option[value="' + svc + '"]')) byName('service').value = svc;
      if (freq) byName('frequency').value = freq;
      byName('service').addEventListener('change', function() {
        byName('frequency').value = this.value === 'regular' ? 'biweekly' : 'onetime';
      });
      // parâmetros do anúncio (mesma chave do encaminhamento gclid)
      function clickParams() {
        var out = {};
        try {
          var q = new URLSearchParams(location.search);
          var keys = ['gclid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
          keys.forEach(function(k) { var v = q.get(k); if (v) out[k] = v.slice(0, 200); });
          if (!Object.keys(out).length) {
            var saved = sessionStorage.getItem('slc:click-params:v1');
            if (saved) { var s = JSON.parse(saved); keys.forEach(function(k) { if (s[k]) out[k] = String(s[k]).slice(0, 200); }); }
          }
        } catch (e) {}
        return out;
      }
      function showError(html) {
        var box = form.querySelector('.qf-error');
        box.innerHTML = html;
        box.hidden = false;
      }
      function mark(name, bad) {
        var el = byName(name); if (!el) return;
        var field = el.closest('.qf-field'); if (field) field.classList.toggle('qf-invalid', !!bad);
      }
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        var box = form.querySelector('.qf-error'); box.hidden = true;
        var name = byName('name').value.trim();
        var phoneDigits = byName('phone').value.replace(/\\D/g, '');
        var zip = byName('zip').value.replace(/\\D/g, '');
        var consent = byName('consent').checked;
        var bad = [];
        if (name.length < 2) bad.push('name');
        if (!(phoneDigits.length === 10 || (phoneDigits.length === 11 && phoneDigits.charAt(0) === '1'))) bad.push('phone');
        if (!/^\\d{5}$/.test(zip)) bad.push('zip');
        ['name', 'phone', 'zip'].forEach(function(n) { mark(n, bad.indexOf(n) >= 0); });
        if (!consent) bad.push('consent');
        if (bad.length) {
          showError(bad.indexOf('consent') >= 0 && bad.length === 1
            ? 'Please check the box so we can text you back.'
            : 'Please check the highlighted fields — we need a name, a US mobile number and a 5-digit ZIP.');
          return;
        }
        var params = clickParams();
        var payload = {
          name: name,
          phone: byName('phone').value.trim(),
          zip: zip,
          propertyType: byName('propertyType').value,
          bedrooms: byName('bedrooms').value,
          bathrooms: byName('bathrooms').value,
          sqft: byName('sqft').value.replace(/[^0-9]/g, ''),
          service: byName('service').value,
          frequency: byName('frequency').value,
          notes: byName('notes').value.trim(),
          consent: true,
          website: byName('website').value,
          startedAt: startedAt,
          page: location.pathname,
          referrer: (function() { try { return document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) { return ''; } })()
        };
        if (!payload.sqft) delete payload.sqft;
        if (!payload.referrer) delete payload.referrer;
        Object.keys(params).forEach(function(k) { payload[k] = params[k]; });
        var btn = form.querySelector('.qf-btn');
        btn.disabled = true; btn.textContent = 'Sending…';
        var fallback = 'Something went wrong on our side. Text us directly at <a href="sms:+16506193504?&body=' + encodeURIComponent('Hi! I\\'d like a price for ' + byName('service').options[byName('service').selectedIndex].text.toLowerCase() + ' — ' + name) + '">(650) 619-3504</a> and we\\'ll reply with your price.';
        fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
          .then(function(r) { return r.json().then(function(j) { return { status: r.status, body: j }; }); })
          .then(function(res) {
            if (res.body && res.body.ok) {
              var ok = document.getElementById('qfSuccess');
              ok.querySelector('[data-qf="firstName"]').textContent = res.body.firstName || name.split(' ')[0];
              ok.querySelector('[data-qf="phone"]').textContent = res.body.phoneDisplay || byName('phone').value;
              form.hidden = true; ok.hidden = false;
              try { ok.scrollIntoView({ block: 'center', behavior: 'instant' }); } catch (e) {}
              if (typeof gtag === 'function') {
                gtag('event', 'generate_lead', { 'event_category': 'lead', 'event_label': 'site_quote_form', 'value': 1 });
                if (CONV_LABEL) gtag('event', 'conversion', { 'send_to': 'AW-17096585184/' + CONV_LABEL });
              }
              return;
            }
            btn.disabled = false; btn.textContent = '💬 Text Me My Price';
            if (res.status === 429) { showError('We already have your request — Raphael will text you shortly. If it\\'s urgent, call <a href="tel:+16506193504">(650) 619-3504</a>.'); return; }
            if (res.status === 400) {
              var f = res.body && res.body.field;
              if (f === 'phone' || f === 'zip' || f === 'name') { mark(f, true); showError('Please double-check your ' + (f === 'zip' ? 'ZIP code' : f === 'phone' ? 'mobile number' : 'name') + '.'); return; }
            }
            showError(fallback);
          })
          .catch(function() { btn.disabled = false; btn.textContent = '💬 Text Me My Price'; showError(fallback); });
      });
    })();
  </script>
"""


def _hero_end(text):
    """Índice logo após o </section> do hero (primeiro section com class="hero")."""
    i = text.find('<section class="hero')
    if i < 0:
        return -1
    j = text.find("</section>", i)
    return -1 if j < 0 else j + len("</section>")


def patch_quote_form():
    targets = [(ROOT / "services" / slug / "index.html", slug) for slug in QUOTE_SERVICE_BY_SLUG]
    targets.append((ROOT / "index.html", None))
    n = 0
    for p, slug in targets:
        if not p.exists():
            fail(f"{p}: não existe")
            continue
        t = read(p)
        # versão anterior da seção (v1, sem a vitrine do app) sai antes de entrar a atual
        if 'id="quote-form"' in t and 'data-qf-version="2"' not in t:
            t = re.sub(r"\n  <!-- slc-quote-(?:v1|form)[^\n]*\n  <section class=\"section qf-section\" id=\"quote-form\"[\s\S]*?</section>\n", "\n", t, count=1)
        if 'id="quote-form"' not in t:
            service, frequency = QUOTE_SERVICE_BY_SLUG.get(slug, ("regular", "biweekly"))
            src = f"site-quote-{slug}" if slug else "site-quote-home"
            app_href = f"https://app.signatureluxurycleaning.com/?src={src}"
            block = QUOTE_SECTION_HTML % {"service": service, "frequency": frequency, "app_href": app_href}
            at = _hero_end(t)
            if at < 0:
                fail(f"{p}: hero não encontrado para inserir o formulário")
                continue
            t = t[:at] + "\n" + block + t[at:]
            n += 1
        # o JS é reescrito a cada execução (rótulo do Ads, API): remove a versão
        # anterior pelo marcador e insere a atual antes do </body>
        js = QUOTE_JS % {"api": QUOTE_API, "label": QUOTE_CONV_LABEL}
        t = re.sub(r"\n  <script>\n    // slc-quote-v1 —[\s\S]*?\n  </script>\n", "\n", t, count=1)
        if "slc-quote-v1 —" not in t:
            t = t.replace("</body>", js + "</body>", 1)
        # remover + reinserir deixava UMA linha em branco a mais por execução
        # (o site do workflow e o zip publicado divergiam por linhas vazias):
        # fixa em duas linhas em branco antes do script
        t = re.sub(r"\n{3,}(  <script>\n    // slc-quote-v1 —)", "\n\n\n\\1", t, count=1)
        write(p, t)
    css_p = ROOT / "assets/style.css"
    css = read(css_p)
    # o bloco é uma linha só: remove a versão anterior (se houver) e reescreve —
    # assim uma correção no CSS chega ao site sem trocar o marcador
    css = re.sub(r"\n/\* slc-quote-v1 \*/[^\n]*\n", "\n", css)
    write(css_p, css.rstrip("\n") + "\n" + QUOTE_CSS + "\n")
    log(f"formulário de cotação por SMS inserido em {n} página(s) (8 serviços + home); CSS e JS no lugar")



# ═════════ 12. cidades do norte: Foster City + Redwood Shores (25/09/2026) ═══
# O Google Ads passou a mirar os ZIPs ricos do norte (San Mateo 94402/94403,
# Foster City 94404, Redwood Shores 94065, Burlingame/Hillsborough 94010,
# Emerald Hills 94062) e o dono pediu sitelinks por cidade. O site não tinha
# página de Foster City (os links "Foster City" de San Mateo e Belmont caíam
# em /#areas) e a página de Redwood City não citava Redwood Shores.
#   (a) /locations/foster-city/ nasce do molde de San Mateo (mesma estrutura,
#       medição e formulários), com dados próprios: bairros e marcos (Sea
#       Colony, Treasure Isle, Isle Cove, Marina Point, Edgewater; Leo J. Ryan
#       Park, lagoa, Sea Cloud Park, Edgewater Place), ZIP 94404, população do
#       Censo 2020 (33,805), valor típico de casa (Zillow ago/2026 ≈ $1.8M),
#       coordenadas, e 3 reviews reais diferentes das de San Mateo;
#   (b) Redwood City: Redwood Shores + Emerald Hills no badge, meta, bairros,
#       FAQ e ZIPs 94061/94062/94063/94065;
#   (c) links "Foster City" das páginas de cidade → página nova;
#   (d) home: pill na grade de áreas, schema areaServed, lista do SMS;
#       contagem 22 → 23 cidades no index e nas 7 línguas; FAQ "What areas
#       do you serve?" passa a citar o corredor da Península (antes citava
#       San Jose e Fremont);
#   (e) sitemap.xml: URL nova + lastmod das páginas tocadas.

NEW_CITY_SLUGS = ("foster-city",)
STEP12_DATE = "2026-09-25"
SITE_URL = "https://signatureluxurycleaning.com"

FC_LINK_RE = re.compile(r'<a href="/#areas"((?: class="[^"]*")?)>((?:<span class="nearby-icon">📍</span>)?(?:<span>)?Foster City<)')

AREAS_FAQ_SCHEMA = ("We serve 23 cities across the Peninsula and Silicon Valley, including Palo Alto, Menlo Park, "
                    "Atherton, Los Altos, San Mateo, Hillsborough, Burlingame, Foster City, Redwood City and Belmont.")
AREAS_FAQ_HTML = ("We serve 23 cities across the Peninsula and Silicon Valley: Palo Alto, Menlo Park, Atherton, "
                  "Los Altos, San Mateo, Hillsborough, Burlingame, Foster City, Redwood City, Belmont and more.")

TR_COUNT_SWAPS = [("22 cities", "23 cities"), ("22个城市", "23个城市"), ("22 शहरों", "23 शहरों"),
                  ("22 lungsod", "23 lungsod"), ("22 thành phố", "23 thành phố"), ("22개 도시", "23개 도시"),
                  ("22都市", "23都市")]


def once(text, old, new, where, expect=1):
    """Troca exigindo `expect` ocorrências; se `new` já está no texto, não mexe (idempotência)."""
    if new in text:
        return text
    return sub_count(text, old, new, expect, where)


def review_card(name, text):
    return ('<div class="review-card">\n          <div class="review-stars">★★★★★</div>\n'
            f'          <p>"{text}"</p>\n'
            f'          <div class="review-author">— {name}, Silicon Valley · Google review</div>\n        </div>')


def build_foster_city(sm):
    """Página de Foster City a partir da de San Mateo (que já tem o pacote v1 inteiro)."""
    w = "foster-city (molde San Mateo)"
    county = "\x00COUNTY\x00"
    t = sm.replace("San Mateo County", county)
    t = t.replace("San Mateo", "Foster City").replace("san-mateo", "foster-city")
    t = t.replace(county, "San Mateo County")
    pairs = [
        ('"postalCode": "94401"', '"postalCode": "94404"', 1),
        ('"latitude": 37.563,', '"latitude": 37.5514,', 2),
        ('"longitude": -122.3255', '"longitude": -122.2664', 2),
        ("Signature+Luxury+Cleaning+san+mateo+CA", "Signature+Luxury+Cleaning+foster+city+CA", 1),
        ("Serving Downtown, Baywood, Hillsdale, Beresford, Fiesta Gardens and surrounding areas.",
         "Serving Sea Colony, Treasure Isle, Isle Cove, Marina Point, Edgewater and surrounding areas.", 1),
        ("Median home value in Foster City is $1.9M.", "Median home value in Foster City is $1.8M.", 2),
        ("Yes! We serve all neighborhoods including Hillsdale, Foster City Park, Baywood and more. ZIP: 94401.",
         "Yes! We serve all neighborhoods including Sea Colony, Treasure Isle, Isle Cove and more. ZIP: 94404.", 2),
        ("We serve all neighborhoods in Foster City — including Downtown, Baywood, Hillsdale, Beresford, Fiesta Gardens.",
         "We serve all neighborhoods in Foster City — including Sea Colony, Treasure Isle, Isle Cove, Marina Point, Edgewater.", 1),
        ("work long hours in Peninsula", "work long hours on the Peninsula", 1),
        ("We also serve families in Burlingame, Foster City, Redwood City and across San Mateo County.",
         "We also serve families in San Mateo, Belmont, Redwood City and across San Mateo County.", 1),
        ('<a href="/locations/burlingame/" class="nearby-card"><span class="nearby-icon">📍</span><span>Burlingame</span></a>'
         '<a href="/#areas" class="nearby-card"><span class="nearby-icon">📍</span><span>Foster City</span></a>',
         '<a href="/locations/san-mateo/" class="nearby-card"><span class="nearby-icon">📍</span><span>San Mateo</span></a>'
         '<a href="/locations/belmont/" class="nearby-card"><span class="nearby-icon">📍</span><span>Belmont</span></a>', 1),
        ("Foster City's diverse housing means we bring the right approach to every home.",
         "Foster City's lagoon-front homes and waterside townhomes deserve steady, detail-oriented care.", 1),
        ('<span class="city-stat-number">105,661</span>', '<span class="city-stat-number">33,805</span>', 1),
        ('<span class="city-stat-number">$1.9M</span>', '<span class="city-stat-number">$1.8M</span>', 1),
        ('<span class="neighborhood-pill">Hillsdale</span><span class="neighborhood-pill">Foster City Park</span>'
         '<span class="neighborhood-pill">Baywood</span><span class="neighborhood-pill">Aragon</span>'
         '<span class="neighborhood-pill">Fiesta Gardens</span>',
         '<span class="neighborhood-pill">Sea Colony</span><span class="neighborhood-pill">Treasure Isle</span>'
         '<span class="neighborhood-pill">Isle Cove</span><span class="neighborhood-pill">Marina Point</span>'
         '<span class="neighborhood-pill">Edgewater</span>', 1),
        ('<ul class="landmarks-list"><li>Hillsdale Shopping Center</li><li>Central Park</li><li>Japanese Garden</li><li>Coyote Point</li></ul>',
         '<ul class="landmarks-list"><li>Leo J. Ryan Park</li><li>Foster City Lagoon</li><li>Sea Cloud Park</li><li>Edgewater Place</li></ul>', 1),
        ('<a href="/locations/burlingame/" class="nearby-link">Burlingame</a> <a href="/locations/belmont/" class="nearby-link">Belmont</a> '
         '<a href="/#areas" class="nearby-link">Foster City</a> ',
         '<a href="/locations/san-mateo/" class="nearby-link">San Mateo</a> <a href="/locations/belmont/" class="nearby-link">Belmont</a> '
         '<a href="/locations/redwood-city/" class="nearby-link">Redwood City</a> ', 1),
        ('<li><a href="/locations/burlingame/">Burlingame</a></li><li><a href="/#areas">Foster City</a></li>',
         '<li><a href="/locations/san-mateo/">San Mateo</a></li><li><a href="/locations/belmont/">Belmont</a></li>', 1),
    ]
    for old, new, n in pairs:
        t = sub_count(t, old, new, n, w)
    # 3 reviews reais diferentes das de San Mateo (lá: Mia, Danillo R., Alday C.)
    blocks = re.findall(r'<div class="review-card">.*?</div>\s*</div>', t, re.S)
    if len(blocks) != 3:
        fail(f"{w}: esperava 3 reviews no molde, achei {len(blocks)}")
    else:
        for (name, text), old in zip([REAL_REVIEWS[i] for i in (0, 2, 4)], blocks):
            t = t.replace(old, review_card(name, text), 1)
    return t


def patch_redwood_city(t):
    w = "redwood-city (passo 12)"
    t = once(t, 'content="Professional house cleaning in Redwood City, CA. Signature Luxury Cleaning serves',
             'content="Professional house cleaning in Redwood City, CA, including Redwood Shores and Emerald Hills. Signature Luxury Cleaning serves', w)
    t = once(t, "Serving Downtown, Emerald Hills, Farm Hill, Edgewood, Woodside Plaza and surrounding areas.",
             "Serving Redwood Shores, Emerald Hills, Downtown, Farm Hill, Edgewood, Woodside Plaza and surrounding areas.", w)
    t = once(t, "Yes! We serve all neighborhoods including Downtown Redwood City, Emerald Hills, Woodside Plaza and more. ZIP: 94061.",
             "Yes! We serve all neighborhoods including Redwood Shores, Emerald Hills, Downtown Redwood City, Woodside Plaza and more. "
             "ZIPs: 94061, 94062, 94063 and 94065.", w, 2)
    t = once(t, '<div class="hero-badge">📍 Serving Redwood City, San Mateo County</div>',
             '<div class="hero-badge">📍 Serving Redwood City, Redwood Shores &amp; Emerald Hills</div>', w)
    t = once(t, "We serve all neighborhoods in Redwood City — including Downtown, Emerald Hills, Farm Hill, Edgewood, Woodside Plaza.",
             "We serve all neighborhoods in Redwood City — including Redwood Shores, Emerald Hills, Downtown, Farm Hill, Edgewood, Woodside Plaza.", w)
    t = once(t, "Redwood City's revitalized downtown and Emerald Hills luxury homes create a unique mix.",
             "Redwood City's revitalized downtown, the waterfront homes of Redwood Shores and the hillside homes of Emerald Hills create a unique mix.", w)
    t = once(t, '<div class="neighborhoods-grid"><span class="neighborhood-pill">Downtown Redwood City</span>',
             '<div class="neighborhoods-grid"><span class="neighborhood-pill">Redwood Shores</span><span class="neighborhood-pill">Downtown Redwood City</span>', w)
    return t


def patch_home_step12(t):
    w = "index (passo 12)"
    pill_hb = '<a href="locations/hillsborough/" class="area-pill" title="House Cleaning Hillsborough CA">Hillsborough</a>\n'
    pill_fc = '          <a href="locations/foster-city/" class="area-pill" title="House Cleaning Foster City CA">Foster City</a>\n'
    t = once(t, pill_hb, pill_hb + pill_fc, w)
    t = once(t, '{"@type": "City", "name": "Hillsborough"}\n    ],',
             '{"@type": "City", "name": "Hillsborough"},\n      {"@type": "City", "name": "Foster City"}\n    ],', w)
    t = once(t, "'Burlingame','Hillsborough'];", "'Burlingame','Hillsborough','Foster City'];", w)
    t = sub_count(t, "22 cities", "23 cities", 7, w)
    t = sub_count(t, '<span class="number">22</span>', '<span class="number">23</span>', 1, w)
    t = sub_count(t, "All 22 service areas", "All 23 service areas", 1, w)
    t = once(t, "We serve 23 cities across the San Francisco Bay Area including San Jose, Palo Alto, Mountain View, Cupertino, Sunnyvale, and more.",
             AREAS_FAQ_SCHEMA, w)
    t = once(t, "We serve 23 cities across the Bay Area: San Jose, Palo Alto, Mountain View, Cupertino, Sunnyvale, Fremont, and more.",
             AREAS_FAQ_HTML, w)
    return t


def patch_sitemap_step12(t):
    fc_url = f"{SITE_URL}/locations/foster-city/"
    if fc_url not in t:
        m = re.search(r"  <url>\n    <loc>%s/locations/hillsborough/</loc>\n[\s\S]*?</url>\n" % re.escape(SITE_URL), t)
        if not m:
            fail("sitemap.xml: bloco de hillsborough não encontrado")
            return t
        block = (f"  <url>\n    <loc>{fc_url}</loc>\n    <lastmod>{STEP12_DATE}</lastmod>\n"
                 "    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n")
        t = t[:m.end()] + block + t[m.end():]
    for path in ("/", "/locations/redwood-city/", "/locations/san-mateo/", "/locations/belmont/"):
        t, n = re.subn(r"(<loc>%s</loc>\s*<lastmod>)[^<]*(</lastmod>)" % re.escape(SITE_URL + path),
                       r"\g<1>%s\g<2>" % STEP12_DATE, t)
        if n != 1:
            fail(f"sitemap.xml: esperava 1 entrada com lastmod para {path}, achei {n}")
    return t


def patch_step12():
    loc = ROOT / "locations"
    fc_p = loc / "foster-city" / "index.html"
    if fc_p.exists():
        log("foster-city: página já existe — mantida (idempotência)")
    else:
        fc_p.parent.mkdir(parents=True, exist_ok=True)
        write(fc_p, build_foster_city(read(loc / "san-mateo" / "index.html")))
        log("foster-city: página criada a partir do molde de San Mateo (dados próprios)")

    rc_p = loc / "redwood-city" / "index.html"
    write(rc_p, patch_redwood_city(read(rc_p)))

    n_links = 0
    for p in sorted(loc.glob("*/index.html")):
        t = read(p)
        t2 = FC_LINK_RE.sub(r'<a href="/locations/foster-city/"\1>\2', t)
        if t2 != t:
            n_links += len(FC_LINK_RE.findall(t))
            write(p, t2)

    idx_p = ROOT / "index.html"
    write(idx_p, patch_home_step12(read(idx_p)))

    tr_p = ROOT / "assets/translations.js"
    tr = read(tr_p)
    for old, new in TR_COUNT_SWAPS:
        tr = sub_count(tr, old, new, 3, "translations.js (22→23)")
    write(tr_p, tr)

    sm_p = ROOT / "sitemap.xml"
    write(sm_p, patch_sitemap_step12(read(sm_p)))
    log(f"passo 12: Foster City + Redwood Shores; {n_links} link(s) 'Foster City' → página nova; 23 cidades (7 línguas); sitemap")


# ═════════════ 13. (30/09) SEM O NOME DO DONO NO TEXTO PARA O CLIENTE ═════════
# "Tira meu nome, coloca só dono. Na hora que coloca Raphael, é homem, e muitas
# pessoas ficam com o pé atrás." Vale para tudo que o cliente lê antes de
# fechar: o formulário de cotação (9 páginas: home + 8 serviços) e a seção da
# primeira limpeza na home. As REVIEWS reais do Google que citam "Raphael" são
# palavras dos clientes — ficam. O app usa o mesmo texto (shared/firstVisitPromise.ts).

OWNER_NAME_SWAPS = [
    # (antes, depois, onde aparece)
    ("Tell us about your home and Raphael, the owner, will text you a personalized price.",
     "Tell us about your home and the owner will text you a personalized price.",
     "qf-form-sub"),
    ("<p>Raphael will text <strong data-qf=\"phone\"></strong> shortly with your personalized price.</p>",
     "<p>The owner will text <strong data-qf=\"phone\"></strong> shortly with your personalized price.</p>",
     "qf-success"),
    ("We already have your request — Raphael will text you shortly.",
     "We already have your request — the owner will text you shortly.",
     "erro 429"),
]
FIRST_VISIT_OLD = "For your first cleaning, Raphael or Veridiana is in your home in person, working alongside your two assistants."
FIRST_VISIT_NEW = "For your first cleaning, one of the owners is in your home in person, working alongside your two assistants."
REVIEW_NAME_RE = re.compile(r'(?:using Raphael cleaning service|Raphael and his team|Veridiana and her team)')


def quote_form_pages():
    return [ROOT / "index.html"] + sorted((ROOT / "services").glob("*/index.html"))


def patch_step13():
    n_pages = 0
    for p in quote_form_pages():
        t = read(p)
        if "qf-form-sub" not in t:
            continue  # página sem formulário (não deveria acontecer)
        t2 = t
        for old, new, where in OWNER_NAME_SWAPS:
            if old not in t2 and plural_owners(new) in t2:
                continue  # o passo 14 já levou este texto ao plural
            t2 = sub_count(t2, old, new, 1, f"{p.relative_to(ROOT)} ({where})")
        if p.name == "index.html" and p.parent == ROOT:
            t2 = sub_count(t2, FIRST_VISIT_OLD, FIRST_VISIT_NEW, 1, "index (first-visit)")
        if t2 != t:
            write(p, t2)
            n_pages += 1
    log(f"passo 13: nome do dono removido do formulário de cotação e da 1ª limpeza ({n_pages} página(s) alteradas; reviews reais mantidas)")


# ═════════════ 14. (30/09, tarde) NENHUM NOME — SEMPRE "OWNERS" ═══════════════
# "Não pode aparecer nem meu nome, nem o nome da Cristine, nem o nome da
# Viridiane. Em lugar nenhum. Fala donos. Sempre donos."

def plural_owners(s: str) -> str:
    """'the owner will text' → 'the owners will text' (só as frases do formulário)."""
    return s.replace("the owner will text", "the owners will text").replace("The owner will text", "The owners will text")


HOME_OWNERS_SWAPS = [
    ("<h4>You Always Talk to an Owner</h4>", "<h4>You Always Talk to the Owners</h4>"),
    ("<h4>An Owner on Your First Cleaning</h4>", "<h4>One of the Owners on Your First Cleaning</h4>"),
    ("<p>An owner works alongside your team on the first cleaning.",
     "<p>One of the owners works alongside your team on the first cleaning."),
    ('<h2 class="section-title">An owner is there for your first cleaning.</h2>',
     '<h2 class="section-title">One of the owners is there for your first cleaning.</h2>'),
]
# Reviews reais do Google: o trecho com o nome vira [They]/[their] — colchetes =
# edição sinalizada, sentido do cliente preservado. Cada trecho aparece 2x na
# home: no card visível e no JSON-LD (reviewBody).
REVIEW_SWAPS = [
    ("We have been using Raphael cleaning service for a while now",
     "We have been using [their] cleaning service for a while now"),
    ("Raphael and his team are so quick to respond", "[They] are so quick to respond"),
    ("Raphael and his team did an amazing deep clean", "[They] did an amazing deep clean"),
    ("Veridiana and her team are awesome!", "[They] are awesome!"),
]
COMMENT_SWAPS = [
    ("<!-- Checklist PDF link (once uploaded by Raphael) -->", "<!-- Checklist PDF link (once uploaded by the owners) -->"),
]
NAME_RE = re.compile(r"raphael|rafael|christine|cristine|veridiana|viridian", re.I)
TEXT_SUFFIXES = {".html", ".htm", ".js", ".css", ".xml", ".txt", ".json", ".webmanifest", ".md", ".svg"}


def patch_step14():
    n_pages = 0
    for p in quote_form_pages():
        t = read(p)
        if "qf-form-sub" not in t:
            continue
        t2 = t
        for old, new, where in OWNER_NAME_SWAPS:
            t2 = sub_count(t2, new, plural_owners(new), 1, f"{p.relative_to(ROOT)} ({where}, plural)")
        if p.name == "index.html" and p.parent == ROOT:
            for old, new in HOME_OWNERS_SWAPS:
                t2 = sub_count(t2, old, new, 1, "index (owners)")
            for old, new in REVIEW_SWAPS:
                t2 = sub_count(t2, old, new, 2, "index (review: card + JSON-LD)")
        if t2 != t:
            write(p, t2)
            n_pages += 1
    for p in sorted(ROOT.rglob("*.html")):
        t = read(p)
        t2 = t
        for old, new in COMMENT_SWAPS:
            if old in t2:
                t2 = t2.replace(old, new)
        if t2 != t:
            write(p, t2)
            n_pages += 1
    log(f"passo 14: 'the owners' no formulário e nos cards, nomes fora das reviews e dos comentários ({n_pages} alteração(ões) de página)")


# ═════════════════════ 15. (02/10) dados certos para ChatGPT/Bing ════════════

FB_OLD_TOKEN = 'www.facebook.com/signatureluxurycleaning"'
FB_NEW_TOKEN = 'www.facebook.com/signatureluxurycleaningca"'
GMAPS_PLACEHOLDER = "https://www.google.com/maps?cid=YOUR_GOOGLE_CID"
GMAPS_REAL = "https://www.google.com/maps?cid=10124342750083586343"  # CID conferido no Maps em 02/10
GMAPS_PLACE_OLD = "https://www.google.com/maps/place/?q=place_id:ChIJ4xtKfMPcIgInmQgTF-SAjA"  # não abria a ficha
YELP_URL = "https://www.yelp.com/biz/signature-luxury-cleaning-belmont"
REVIEW_COUNT = "12"  # Google, 30/09/2026: 12 reviews, todas 5★
AREA_ORDER = [
    "Los Altos", "Palo Alto", "Los Altos Hills", "Menlo Park", "Atherton", "Mountain View",
    "Woodside", "Cupertino", "Saratoga", "Los Gatos", "Sunnyvale", "Santa Clara", "Campbell",
    "San Jose", "Milpitas", "Fremont", "Redwood City", "San Carlos", "Belmont", "San Mateo",
    "Foster City", "Burlingame", "Hillsborough",
]
HOME_DESC_OLD = ("Silicon Valley & Peninsula's most trusted luxury residential cleaning service. "
                 "Serving Palo Alto, Burlingame, Mountain View, Sunnyvale, Santa Clara, Cupertino and "
                 "23 cities across Silicon Valley & Peninsula.")
HOME_DESC_NEW = ("Small, owner-operated house cleaning company serving Los Altos, Palo Alto and 23 cities "
                 "across Silicon Valley and the Peninsula. One of the owners leads the first cleaning in "
                 "every new home. Bonded & insured, 5.0 stars on Google.")
REDIRECTS = """# Endereços comuns que robôs e pessoas tentam (antes davam 404) — passo 15, 02/10/2026
/about           /#about        301
/about/          /#about        301
/about-us        /#about        301
/about-us/       /#about        301
/contact         /#quote-form   301
/contact/        /#quote-form   301
/contact-us      /#quote-form   301
/contact-us/     /#quote-form   301
/quote           /#quote-form   301
/quote/          /#quote-form   301
/pricing         /#services     301
/pricing/        /#services     301
/prices          /#services     301
/prices/         /#services     301
/services        /#services     301
/services/       /#services     301
/locations       /#areas        301
/locations/      /#areas        301
/service-areas   /#areas        301
/service-areas/  /#areas        301
/reviews         /#reviews      301
/reviews/        /#reviews      301
/testimonials    /#reviews      301
/testimonials/   /#reviews      301
/faq             /#faq          301
/faq/            /#faq          301
/gallery         /#gallery      301
/gallery/        /#gallery      301
/book            https://app.signatureluxurycleaning.com/?src=site-book   302
/book/           https://app.signatureluxurycleaning.com/?src=site-book   302
/booking         https://app.signatureluxurycleaning.com/?src=site-book   302
/booking/        https://app.signatureluxurycleaning.com/?src=site-book   302
"""


def _home_area_block():
    lines = ",\n".join('      {"@type": "City", "name": "%s"}' % c for c in AREA_ORDER)
    return '"areaServed": [\n' + lines + "\n    ],"


def patch_step15():
    n = 0
    for p in sorted(ROOT.rglob("*.html")):
        t = read(p)
        t2 = t.replace(FB_OLD_TOKEN, FB_NEW_TOKEN).replace(GMAPS_PLACEHOLDER, GMAPS_REAL).replace(GMAPS_PLACE_OLD, GMAPS_REAL)
        t2 = re.sub(r'"ratingCount": "(8|9)"', '"ratingCount": "%s"' % REVIEW_COUNT, t2)
        # Yelp no sameAs das páginas de cidade (o bloco termina com o Facebook)
        city_tail = '"https://www.facebook.com/signatureluxurycleaningca"\n  ],'
        if p.parent.parent.name == "locations" and city_tail in t2 and YELP_URL not in t2:
            t2 = t2.replace(city_tail, '"https://www.facebook.com/signatureluxurycleaningca",\n    "%s"\n  ],' % YELP_URL, 1)
        if t2 != t:
            write(p, t2)
            n += 1
    home = ROOT / "index.html"
    t = read(home)
    t2 = t
    if HOME_DESC_OLD in t2:
        t2 = sub_count(t2, HOME_DESC_OLD, HOME_DESC_NEW, 1, "index (descrição do schema)")
    t2, k = re.subn(r'"areaServed": \[\n(?:\s*\{"@type": "City", "name": "[^"]+"\},?\n)+\s*\],',
                    _home_area_block(), t2, count=1)
    if k != 1:
        ERRORS.append("index: bloco areaServed do schema não encontrado")
    home_tail = '"%s"\n    ],' % GMAPS_REAL
    if YELP_URL not in t2:
        t2 = sub_count(t2, home_tail, '"%s",\n      "%s"\n    ],' % (GMAPS_REAL, YELP_URL), 1, "index (Yelp no sameAs)")
    if t2 != t:
        write(home, t2)
    write(ROOT / "_redirects", REDIRECTS)
    log(f"passo 15: Facebook novo, link do Google, Yelp, 12 reviews e cidades no schema ({n} página(s)); _redirects para /pricing, /contact, /about, /faq, /book…")


# ═════════════════════ 16. (02/10) link de review do Google quebrado ═════════

REVIEW_PID_OLD = "ChIJ4xtKfMPcIgInmQgTF-SAjA"   # 26 caracteres, faltava 1 byte: o Google dava 404
REVIEW_PID_NEW = "ChIJ4xtKfMPcIgIRJ5kIExfkgIw"  # da ficha 0x222dcc37c4a1be3:0x8c80e41713089927; testado em 02/10
REVIEW_LINK_OLD = "https://search.google.com/local/writereview?placeid=" + REVIEW_PID_OLD
REVIEW_LINK_NEW = "https://search.google.com/local/writereview?placeid=" + REVIEW_PID_NEW


def patch_step16():
    n = 0
    for p in sorted(ROOT.rglob("*.html")):
        t = read(p)
        if REVIEW_LINK_OLD in t:
            write(p, t.replace(REVIEW_LINK_OLD, REVIEW_LINK_NEW))
            n += 1
    log(f"passo 16: link 'Leave us a review' do Google consertado ({n} página(s))")



# ═════════════════════ 6. 404, robots, htaccess ══════════════════════════════

PAGE_404 = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>Page Not Found | Signature Luxury Cleaning</title>
<style>
  :root{--navy:#0C1A2E;--gold:#C8973A;--gold-light:#E2B96A}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--navy);color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem;text-align:center}
  .wrap{max-width:520px}
  .logo{font-family:Georgia,'Times New Roman',serif;font-size:1.4rem;color:var(--gold-light);letter-spacing:.04em;margin-bottom:2.5rem}
  h1{font-family:Georgia,'Times New Roman',serif;font-size:clamp(2.2rem,7vw,3.2rem);line-height:1.15;margin-bottom:1rem}
  h1 em{font-style:italic;color:var(--gold-light)}
  p{color:rgba(255,255,255,.7);line-height:1.7;margin-bottom:2rem}
  .btns{display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center}
  .btn{display:inline-block;padding:.8rem 1.6rem;border-radius:50px;font-weight:600;font-size:.9rem;text-decoration:none;transition:transform .2s}
  .btn:hover{transform:translateY(-2px)}
  .btn-gold{background:linear-gradient(135deg,var(--gold),var(--gold-light));color:var(--navy)}
  .btn-ghost{border:1px solid rgba(255,255,255,.3);color:#fff}
  .call{margin-top:2rem;font-size:.85rem;color:rgba(255,255,255,.55)}
  .call a{color:var(--gold-light);text-decoration:none;font-weight:600}
</style>
</head>
<body>
  <div class="wrap">
    <div class="logo">Signature Luxury Cleaning</div>
    <h1>This page took<br><em>a day off.</em></h1>
    <p>The page you're looking for doesn't exist or has moved. Everything else is spotless, we promise.</p>
    <div class="btns">
      <a class="btn btn-gold" href="/">Back to Home</a>
      <a class="btn btn-ghost" href="https://app.signatureluxurycleaning.com/?src=site-404">See Prices &amp; Book</a>
    </div>
    <p class="call">Or call/text us: <a href="tel:6506193504">(650) 619-3504</a></p>
  </div>
</body>
</html>
"""

ROBOTS = """User-agent: *
Allow: /

Sitemap: https://signatureluxurycleaning.com/sitemap.xml
"""

HTACCESS = """ErrorDocument 404 /404.html
"""


def add_new_files():
    write(ROOT / "404.html", PAGE_404)
    write(ROOT / "robots.txt", ROBOTS)
    write(ROOT / ".htaccess", HTACCESS)
    log("novos: 404.html (marca), robots.txt, .htaccess")


# ═════════════════════ 7. verificação final ══════════════════════════════════

def verify():
    ok = True

    def check(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print(f"  ✗ {msg}")
        else:
            print(f"  ✓ {msg}")

    idx = read(ROOT / "index.html")
    tr = read(ROOT / "assets/translations.js")
    css = read(ROOT / "assets/style.css")

    check("© 2025" not in idx and "&copy; 2025" not in idx, "index sem © 2025")
    leftover = [str(p) for p in ROOT.rglob("*.html") if "© 2025 Signature" in read(p)]
    check(not leftover, f"nenhuma página com © 2025 (restam: {leftover[:3]})")
    check(idx.count("hero-prices") >= 2, "faixa de preços mobile no hero (html+css)")
    n_price = idx.count('class="service-price"')
    check(n_price == 8, f"8 cards com preço (achei {n_price})")
    check("18 cities" not in idx and "18+" not in idx, "index sem '18 cities'/'18+'")
    check("eight services" in idx and "Eight professional" in idx, "contagem de serviços = 8 no index")
    check("ba-strip" in idx and "wg_kitchen_stove_before" in idx, "before/after na galeria")
    check("bonded &amp; fully insured" in idx, "topbar do index com bonded")
    check("booking@signatureluxurycleaning.com</a>" in idx, "e-mail por extenso no rodapé")
    check('data-lang="ja"' in idx, "botão 日本語 no index")
    check("'ja'];" in tr.replace('"', "'"), "SUPPORTED_LANGS com ja")
    check("ja: {" in tr, "dicionário ja presente")
    check("eight services" in tr and "八项服务" in tr and "8가지 서비스" in tr, "aeo_services corrigido en/zh/ko")
    stale_tr = [old for old, _new in TR_COUNT_SWAPS if old in tr]
    check("23 cities" in tr and "23개 도시" in tr and not stale_tr, f"contagem 23 nas traduções (restam: {stale_tr})")
    check("top: 132px" in css, "badge 5.0 reposicionado")
    check(".ba-strip" in css, "CSS do before/after")
    for f in ["404.html", "robots.txt", ".htaccess"]:
        check((ROOT / f).exists(), f"{f} existe")

    jen = [str(p) for p in (ROOT / "locations").rglob("*.html") if "Jennifer M." in read(p) or "David K." in read(p)]
    check(not jen, f"nenhuma cidade com depoimentos genéricos (restam: {jen[:3]})")
    tagged = sum(read(p).count("?src=site-") for p in (ROOT / "locations").rglob("*.html"))
    check(tagged >= 22, f"links do app marcados nas cidades ({tagged})")
    check(idx.count("?src=site-") >= 15, f"links do app marcados no index ({idx.count('?src=site-')})")

    left = [str(p) for p in ROOT.rglob("*.html") if "_LABEL'" in read(p)]
    check(not left, f"nenhum placeholder de conversão restante ({left[:3]})")
    check("RBjKCM2TsfkcEODfpNg_" in idx and "KbSHCOeFsPkcEODfpNg_" in idx, "rótulos reais no index")
    pages = [p for p in ROOT.rglob("*.html")]
    no_conv = [str(p.relative_to(ROOT)) for p in pages if "RBjKCM2TsfkcEODfpNg_" not in read(p)]
    check(not no_conv, f"TODAS as {len(pages)} páginas têm o evento de conversão (faltam: {no_conv[:4]})")
    no_fwd = [str(p.relative_to(ROOT)) for p in pages if "slc-forward-v2" not in read(p)]
    check(not no_fwd, f"TODAS as páginas encaminham gclid/utm para o app (faltam: {no_fwd[:4]})")
    dup = [str(p.relative_to(ROOT)) for p in pages if read(p).count("slc-forward-v") != 1 or read(p).count("RBjKCM2TsfkcEODfpNg_") != 1]
    check(not dup, f"nenhuma página com bloco duplicado ({dup[:4]})")
    svc = read(ROOT / "services/regular-cleaning/index.html")
    check("slc-conv-v1" in svc and "gclid" in svc, "página de serviço (onde caem os cliques pagos) mede e encaminha")
    qf_pages = [ROOT / "services" / s / "index.html" for s in QUOTE_SERVICE_BY_SLUG] + [ROOT / "index.html"]
    qf_missing = [str(p.relative_to(ROOT)) for p in qf_pages if 'id="quote-form"' not in read(p) or "slc-quote-v1 —" not in read(p)]
    check(not qf_missing, f"formulário de cotação nas 8 páginas de serviço + home (faltam: {qf_missing[:3]})")
    qf_dup = [str(p.relative_to(ROOT)) for p in qf_pages if read(p).count('id="quote-form"') != 1 or read(p).count("slc-quote-v1 —") != 1]
    check(not qf_dup, f"formulário sem duplicar ({qf_dup[:3]})")
    qf_old = [str(p.relative_to(ROOT)) for p in qf_pages if 'data-qf-version="2"' not in read(p) or "slc-quote-v1:" in read(p)]
    check(not qf_old, f"seção do formulário na versão atual (v2) em todas ({qf_old[:3]})")
    qf_app = [str(p.relative_to(ROOT)) for p in qf_pages if read(p).count("qf-app-btn") != 1 or "See your exact price" not in read(p)]
    check(not qf_app, f"vitrine do app (3 passos + botão) dentro do bloco em todas ({qf_app[:3]})")
    check("/* slc-quote-v1 */" in css and css.count("/* slc-quote-v1 */") == 1, "CSS do formulário presente uma vez")
    deep = read(ROOT / "services/deep-cleaning/index.html")
    check('data-default-service="deep"' in deep and 'data-default-frequency="onetime"' in deep, "deep-cleaning pré-seleciona Deep / one-time")
    check('data-default-service="regular"' in svc and 'data-default-frequency="biweekly"' in svc, "regular-cleaning pré-seleciona Regular / every 2 weeks")
    leak = [str(p.relative_to(ROOT)) for p in qf_pages if "qf-section" in read(p) and re.search(r'qf-[a-z]+[^<]*\$\d', read(p))]
    check(not leak, f"o formulário não mostra preço nenhum ({leak[:3]})")

    # passo 12 — cidades do norte
    fc_p = ROOT / "locations/foster-city/index.html"
    check(fc_p.exists(), "página /locations/foster-city/ existe")
    if fc_p.exists():
        fc = read(fc_p)
        check("<title>House Cleaning Foster City CA | Signature Luxury Cleaning</title>" in fc, "Foster City: título")
        check(f'<link rel="canonical" href="{SITE_URL}/locations/foster-city/">' in fc, "Foster City: canonical próprio")
        sobras = [s for s in ("Hillsdale", "Baywood", "Fiesta Gardens", "94401", "105,661", "site-san-mateo",
                              "Foster City Park", "Foster City County", "Coyote Point", "san+mateo", "37.563,") if s in fc]
        check(not sobras, f"Foster City: nada de San Mateo sobrando ({sobras})")
        check(fc.count("San Mateo County") >= 3 and 'href="/locations/san-mateo/"' in fc, "Foster City: condado certo + link para San Mateo")
        n_src = fc.count("?src=site-foster-city")
        check(n_src >= 1, f"Foster City: links do app com origem própria ({n_src})")
        check(all(s in fc for s in ("94404", "33,805", "Sea Colony", "Leo J. Ryan Park", "37.5514")),
              "Foster City: dados próprios (ZIP, população, bairros, marcos, coordenadas)")
        check("— Mia," not in fc and "— Harshita S.," in fc and fc.count('class="review-card"') == 3,
              "Foster City: 3 reviews reais, diferentes das de San Mateo")
        check(fc.count("<html") == 1 and fc.count("</html>") == 1 and fc.count("<body") == 1, "Foster City: HTML inteiro (1 html/body)")
    rc = read(ROOT / "locations/redwood-city/index.html")
    n_rs = rc.count("Redwood Shores")
    check(n_rs >= 7 and "94065" in rc, f"Redwood City cita Redwood Shores ({n_rs}x) e o ZIP 94065")
    stale_fc = [str(p.relative_to(ROOT)) for p in (ROOT / "locations").rglob("*.html")
                if re.search(r'href="/#areas"[^>]*>(?:<span[^>]*>📍</span>)?(?:<span>)?Foster City', read(p))]
    check(not stale_fc, f"nenhum link 'Foster City' caindo em /#areas ({stale_fc})")
    pills = re.findall(r'href="locations/([a-z-]+)/" class="area-pill"', idx)
    sem_pagina = [s for s in pills if not (ROOT / "locations" / s / "index.html").exists()]
    check(len(pills) == 23 and len(set(pills)) == 23 and not sem_pagina, f"home: 23 cidades na grade, todas com página ({len(pills)}; sem página: {sem_pagina})")
    check("22 cities" not in idx and '<span class="number">23</span>' in idx and "All 23 service areas" in idx, "home: contagem 23 em todo o index")
    check(AREAS_FAQ_SCHEMA in idx and AREAS_FAQ_HTML in idx, "home: FAQ de áreas cita o corredor da Península")
    check('"name": "Foster City"' in idx and "'Foster City']" in idx, "home: Foster City no schema e na lista do SMS")
    sm = read(ROOT / "sitemap.xml")
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(sm.encode("utf-8"))
        sm_ok = True
    except ET.ParseError:
        sm_ok = False
    check(sm_ok and f"{SITE_URL}/locations/foster-city/" in sm and sm.count("<url>") == 32, f"sitemap válido com a página nova ({sm.count('<url>')} URLs)")

    # dicionário ja cobre todas as chaves usadas no index
    keys = set(re.findall(r'data-i18n="([^"]+)"', idx))
    ja_keys = set(re.findall(r'^\s{4}(\w+):', tr[tr.index("ja: {"):], re.M))
    missing = keys - ja_keys
    check(not missing, f"ja cobre todas as chaves do index (faltam: {sorted(missing)[:8]})")

    # sanidade JS do translations.js
    import subprocess
    r = subprocess.run(["node", "--check", str(ROOT / "assets/translations.js")], capture_output=True, text=True)
    check(r.returncode == 0, f"translations.js parseia como JS ({r.stderr.strip()[:120]})")

    # passo 13: nenhum texto NOSSO cita o dono pelo nome (reviews dos clientes ficam)
    with_form = [p for p in quote_form_pages() if "qf-form-sub" in read(p)]
    check(len(with_form) == 9, f"9 páginas com formulário de cotação ({len(with_form)})")
    stale = []
    for p in ROOT.rglob("*.html"):
        body = re.sub(r"<!--.*?-->", "", read(p), flags=re.S)  # comentário HTML não é texto do cliente
        body = REVIEW_NAME_RE.sub("", body)
        if re.search(r"Raphael|Rafael|Veridiana", body):
            stale.append(str(p.relative_to(ROOT)))
    check(not stale, f"nenhum texto nosso cita Raphael/Veridiana (restam: {stale[:4]})")

    # passo 14: NENHUM nome em NENHUM arquivo de texto do site (comentários, JSON-LD e reviews inclusos)
    leaks = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
             if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and NAME_RE.search(read(p))]
    check(not leaks, f"nenhum nome (Raphael/Rafael/Christine/Cristine/Veridiana/Viridiane) em arquivo nenhum (restam: {leaks[:5]})")
    singular = [str(p.relative_to(ROOT)) for p in with_form
                if "the owners will text you a personalized price" not in read(p)
                or "<p>The owners will text <strong" not in read(p)
                or "the owners will text you shortly" not in read(p)
                or re.search(r"[Tt]he owner will", read(p))]
    check(not singular, f"formulário no plural ('the owners will text') nas 9 páginas (faltam: {singular[:3]})")
    check(FIRST_VISIT_NEW in idx and all(new in idx for _o, new in HOME_OWNERS_SWAPS)
          and not re.search(r"\b[Aa]n [Oo]wner\b", idx),
          "home: 1ª limpeza e cards dizem 'one of the owners' / 'the owners' (nenhum 'an owner')")
    check(all(idx.count(new) == 2 for _o, new in REVIEW_SWAPS), "home: 4 reviews com [They]/[their] no card e no JSON-LD")
    import json as _json
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', idx, re.S)
    try:
        for b in blocks:
            _json.loads(b)
        ld_ok = bool(blocks)
    except ValueError:
        ld_ok = False
    check(ld_ok, f"JSON-LD da home continua JSON válido ({len(blocks)} bloco(s))")

    # passo 15
    import json as _json
    htmls = sorted(ROOT.rglob("*.html"))
    old_fb = [str(p.relative_to(ROOT)) for p in htmls if FB_OLD_TOKEN in read(p)]
    check(not old_fb, f"nenhum link para a Página antiga do Facebook (restam: {old_fb[:3]})")
    ph = [str(p.relative_to(ROOT)) for p in htmls if "YOUR_GOOGLE_CID" in read(p) or GMAPS_PLACE_OLD in read(p)]
    check(not ph, f"nenhum 'YOUR_GOOGLE_CID' nem link place_id antigo (restam: {ph[:3]})")
    no_cid = [str(p.relative_to(ROOT)) for p in htmls if '"LocalBusiness"' in read(p) and GMAPS_REAL not in read(p)]
    check(not no_cid, f"link do Google (CID) no schema de todas as páginas com LocalBusiness (faltam: {no_cid[:3]})")
    bad_rc = [str(p.relative_to(ROOT)) for p in htmls if re.search(r'"ratingCount": "(?!12")', read(p))]
    check(not bad_rc, f"ratingCount = 12 em todo schema (fora: {bad_rc[:3]})")
    ld_bad, ld_n = [], 0
    for p in htmls:
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', read(p), re.S):
            ld_n += 1
            try:
                _json.loads(b)
            except ValueError:
                ld_bad.append(str(p.relative_to(ROOT)))
    check(not ld_bad, f"todos os {ld_n} blocos JSON-LD do site são JSON válido (com erro: {ld_bad[:3]})")
    hb = _json.loads(re.findall(r'<script type="application/ld\+json">(.*?)</script>', idx, re.S)[0])
    names = [a["name"] for a in hb["areaServed"]]
    check(names[:2] == ["Los Altos", "Palo Alto"] and len(names) == 23 and len(set(names)) == 23
          and {"Atherton", "Los Altos Hills", "Woodside", "San Carlos"} <= set(names),
          f"home: 23 cidades no schema, Los Altos e Palo Alto primeiro ({len(names)})")
    check(YELP_URL in hb["sameAs"] and "https://www.facebook.com/signatureluxurycleaningca" in hb["sameAs"],
          "home: sameAs com Facebook novo e Yelp")
    check(hb["description"].startswith("Small, owner-operated house cleaning company serving Los Altos"),
          "home: descrição do schema nova")
    cities_no_yelp = [p.parent.name for p in (ROOT / "locations").glob("*/index.html") if YELP_URL not in read(p)]
    check(not cities_no_yelp, f"páginas de cidade com Yelp no sameAs (faltam: {cities_no_yelp[:3]})")
    rd = read(ROOT / "_redirects")
    rules = [l.split() for l in rd.splitlines() if l.strip() and not l.startswith("#")]
    check(len(rules) == 32 and all(len(r) == 3 and r[2] in ("301", "302") for r in rules),
          f"_redirects com 32 regras bem formadas ({len(rules)})")
    targets_ok = all(r[1].startswith("https://app.signatureluxurycleaning.com/") or
                     ("#" in r[1] and f'id="{r[1].split("#")[1]}"' in idx) for r in rules)
    check(targets_ok, "_redirects: toda âncora de destino existe na home")

    # passo 16
    import base64 as _b64
    import struct as _struct
    raw = _b64.urlsafe_b64decode(REVIEW_PID_NEW + "=" * (-len(REVIEW_PID_NEW) % 4))
    check(len(REVIEW_PID_NEW) == 27 and raw[:3] == b"\x0a\x12\x09" and raw[11:12] == b"\x11"
          and _struct.unpack("<Q", raw[12:20])[0] == 10124342750083586343,
          "place ID novo é o da ficha da SLC (mesmo CID do Maps)")
    txt = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".html", ".js", ".xml", ".txt", ".css", "")]
    old_pid = [str(p.relative_to(ROOT)) for p in txt if REVIEW_PID_OLD in read(p)]
    check(not old_pid, f"nenhum place ID quebrado no site (restam: {old_pid[:3]})")
    with_link = [p for p in htmls if REVIEW_LINK_NEW in read(p)]
    check(len(with_link) == 24, f"link de review certo na home e nas 23 páginas de cidade ({len(with_link)})")


    return ok


def main():
    patch_translations()
    patch_index()
    patch_css()
    patch_cities()
    patch_services_legal()
    patch_conversion_labels()
    add_new_files()
    patch_measurement_everywhere()  # depois do 404.html, que é reescrito acima
    patch_quote_form()
    patch_step12()  # a página nova nasce da de San Mateo já completa
    patch_step13()  # depois do formulário (passo 11): troca o nome do dono nele
    patch_step14()  # por último: plural "owners" + nenhum nome em lugar nenhum
    patch_step15()  # dados certos para ChatGPT/Bing + _redirects
    patch_step16()  # link de review do Google consertado

    print("── mudanças ──")
    for c in CHANGES:
        print(" •", c)
    if ERRORS:
        print("── ERROS ──")
        for e in ERRORS:
            print(" ✗", e)
        sys.exit(1)
    print("── verificação ──")
    if not verify():
        sys.exit(1)
    print("OK: pacote v1 aplicado e verificado.")


if __name__ == "__main__":
    main()
