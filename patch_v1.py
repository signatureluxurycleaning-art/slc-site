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
    cities = sorted((ROOT / "locations").iterdir())
    for ci, cdir in enumerate(c for c in cities if c.is_dir()):
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
    check("22 cities" in tr and "22개 도시" in tr, "contagem 22 nas traduções")
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

    # dicionário ja cobre todas as chaves usadas no index
    keys = set(re.findall(r'data-i18n="([^"]+)"', idx))
    ja_keys = set(re.findall(r'^\s{4}(\w+):', tr[tr.index("ja: {"):], re.M))
    missing = keys - ja_keys
    check(not missing, f"ja cobre todas as chaves do index (faltam: {sorted(missing)[:8]})")

    # sanidade JS do translations.js
    import subprocess
    r = subprocess.run(["node", "--check", str(ROOT / "assets/translations.js")], capture_output=True, text=True)
    check(r.returncode == 0, f"translations.js parseia como JS ({r.stderr.strip()[:120]})")

    return ok


def main():
    patch_translations()
    patch_index()
    patch_css()
    patch_cities()
    patch_services_legal()
    patch_conversion_labels()
    add_new_files()

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
