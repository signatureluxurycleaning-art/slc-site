# -*- coding: utf-8 -*-
"""Pacote v2 de melhorias de SEO (01/11/2026) — aplicado sobre site/, DEPOIS do patch_v1.py.

Origem: auditoria de SEO pedida pelo dono em 01/11/2026 ("faça todas as melhorias").

O QUE ESTE SCRIPT FAZ (e por quê):
 1. PREÇO DO FAQ DAS CIDADES: o FAQ dizia "Regular cleaning starts at $145/visit
    (weekly service, −15% discount)" — $145 é o preço JÁ COM desconto semanal; a
    seção de serviços da mesma página diz $170. Preço inconsistente é exatamente
    o que o dono não tolera ("ou eu vou ser lesado ou o cliente vai ser lesado").
    Passa a dizer: começa em $170 e chega a ~$145 com o desconto semanal de 15%.
    Corrigido no HTML (<details>) e no JSON-LD FAQPage, nas 23 páginas de cidade.
 2. LINKS CIDADE→SERVIÇO: nas páginas de cidade, o nome de cada serviço no card
    vira link para a página do serviço (antes só o White Glove tinha link; as
    páginas de serviço ficavam órfãs para o Google). Aparência preservada
    (color:inherit, sem sublinhado).
 3. LINKS SERVIÇO→CIDADE: cada página de serviço ganha, antes do rodapé, um
    bloco "Serving Silicon Valley & the Peninsula" com links para as páginas
    das cidades-foco — fecha o ciclo de linkagem interna.
 4. HOME: logo deixa de linkar /index.html (duplicava a home para o Google) e
    passa a linkar /; meta description cai de ~250 para ~150 caracteres (não
    trunca mais no resultado); badge do hero troca o "#1 Rated" sem fonte por
    "5.0 on Google — 1,200+ cleanings" (número que a própria home já usa), no
    HTML e no translations.js (EN); "Belmont to Los Gatos" vira "Burlingame to
    San Jose" (área real, mesma frase usada no resto do site).
 5. PRIVACIDADE UNIFICADA: todos os rodapés linkavam /privacy.html enquanto o
    formulário linka /privacy-policy/ — dois URLs para a mesma política diluem
    o sinal. Tudo passa a /privacy-policy/ (o arquivo privacy.html continua no
    ar para links antigos).

DECISÕES REGISTRADAS: o <title> da home (76 chars) fica como está — as
palavras-chave vêm primeiro e o Google só trunca a marca; o banner do topo
"duplicado" é o loop do letreiro (de propósito, não é bug).

Idempotente: rodar duas vezes não muda nada na segunda. Verificação no final —
sai com erro se qualquer mudança esperada não foi aplicada.
"""
from pathlib import Path
import re
import sys

SITE = Path(__file__).parent / "site"
changed = {}
errors = []


def edit(path: Path, pairs, min_hits=1, optional=False):
    """Aplica pares (old, new); conta por arquivo. old ausente + new presente = já aplicado."""
    text = path.read_text(encoding="utf-8")
    original = text
    hits = 0
    for old, new in pairs:
        if old in text:
            hits += text.count(old)
            text = text.replace(old, new)
        elif new in text:
            hits += text.count(new)  # já aplicado antes (idempotência)
    if text != original:
        path.write_text(text, encoding="utf-8")
    changed[str(path.relative_to(SITE))] = changed.get(str(path.relative_to(SITE)), 0) + hits
    if hits < min_hits and not optional:
        errors.append(f"{path}: esperava >= {min_hits} mudanças, obtive {hits}")
    return hits


# ---------------------------------------------------------------- 1. FAQ $145
OLD_PRICE = "Regular cleaning starts at $145/visit (weekly service, −15% discount)."
NEW_PRICE = ("Regular cleaning starts at $170 per visit — and with weekly service "
             "it comes to about $145/visit after the 15% discount.")

location_pages = sorted(SITE.glob("locations/*/index.html"))
assert len(location_pages) == 23, f"esperava 23 páginas de cidade, achei {len(location_pages)}"
for page in location_pages:
    edit(page, [(OLD_PRICE, NEW_PRICE)], min_hits=2)  # HTML + JSON-LD

# ------------------------------------------------- 2. cidade -> serviço (links)
SERVICE_LINKS = [
    ("Regular Cleaning", "regular-cleaning"),
    ("Deep Cleaning", "deep-cleaning"),
    ("Move In / Move Out", "move-in-out-cleaning"),
    ("Post-Construction", "post-construction-cleaning"),
    ("Airbnb Turnover", "airbnb-cleaning"),
    ("Spring Cleaning", "spring-cleaning"),
    ("White Glove Deep Clean", "white-glove-deep-clean"),
]
LINK_STYLE = 'style="color:inherit;text-decoration:none"'
for page in location_pages:
    pairs = []
    for name, slug in SERVICE_LINKS:
        old = f'<h3>{name} <span class="city-tag">'
        new = f'<h3><a href="/services/{slug}/" {LINK_STYLE}>{name}</a> <span class="city-tag">'
        pairs.append((old, new))
    edit(page, pairs, min_hits=5)  # nem toda cidade lista todos os 7

# ------------------------------------------------- 3. serviço -> cidade (bloco)
CITIES = [
    ("Los Altos", "los-altos"), ("Los Altos Hills", "los-altos-hills"),
    ("Palo Alto", "palo-alto"), ("Menlo Park", "menlo-park"),
    ("Mountain View", "mountain-view"), ("Belmont", "belmont"),
    ("San Carlos", "san-carlos"), ("Redwood City", "redwood-city"),
    ("San Mateo", "san-mateo"), ("Burlingame", "burlingame"),
    ("Sunnyvale", "sunnyvale"), ("Cupertino", "cupertino"),
]
MARKER = "<!-- v2-city-links -->"
city_anchors = " · ".join(
    f'<a href="/locations/{slug}/" style="color:inherit">{name}</a>' for name, slug in CITIES
)
service_pages = sorted(SITE.glob("services/*/index.html"))
assert len(service_pages) == 8, f"esperava 8 páginas de serviço, achei {len(service_pages)}"
for page in service_pages:
    text = page.read_text(encoding="utf-8")
    if MARKER in text:
        changed[str(page.relative_to(SITE))] = changed.get(str(page.relative_to(SITE)), 0) + 1
        continue
    block = (
        f'\n{MARKER}\n'
        '<section style="padding:40px 20px;text-align:center">\n'
        '  <h2 style="font-size:1.15rem;margin-bottom:12px">Serving Silicon Valley &amp; the Peninsula</h2>\n'
        f'  <p style="max-width:720px;margin:0 auto;line-height:1.9;opacity:.85">{city_anchors}</p>\n'
        '</section>\n'
    )
    index = text.find("<footer")
    if index == -1:
        errors.append(f"{page}: <footer não encontrado")
        continue
    page.write_text(text[:index] + block + text[index:], encoding="utf-8")
    changed[str(page.relative_to(SITE))] = changed.get(str(page.relative_to(SITE)), 0) + 1

# ----------------------------------------------------------------- 4. home
home = SITE / "index.html"
NEW_DESC = ("Luxury house cleaning in Silicon Valley & the Peninsula. Owner-led first "
            "cleaning, background-checked team, 5.0★ on Google. See your price and book online.")
old_desc_match = re.search(r'<meta name="description" content="([^"]*)"', home.read_text(encoding="utf-8"))
if old_desc_match and old_desc_match.group(1) != NEW_DESC:
    edit(home, [(old_desc_match.group(1), NEW_DESC)])

OLD_BADGE = "⭐ #1 Rated Cleaning Service in Silicon Valley & Peninsula"
NEW_BADGE = "⭐ 5.0 on Google — 1,200+ cleanings across Silicon Valley & Peninsula"
edit(home, [
    ('<a href="index.html" class="nav-logo">', '<a href="/" class="nav-logo">'),
    (OLD_BADGE, NEW_BADGE),
    ("Belmont to Los Gatos", "Burlingame to San Jose"),
], min_hits=3)

translations = SITE / "assets" / "translations.js"
edit(translations, [
    ('hero_badge:       "⭐ #1 Rated Cleaning Service in Silicon Valley & Peninsula"',
     'hero_badge:       "⭐ 5.0 on Google — 1,200+ cleanings across Silicon Valley & Peninsula"'),
    ("Belmont to Los Gatos", "Burlingame to San Jose"),
], min_hits=1, optional=True)

# ---------------------------------------------------------- 5. privacidade
for page in sorted(SITE.rglob("index.html")) + [SITE / "privacy.html", SITE / "404.html"]:
    if not page.exists():
        continue
    edit(page, [('href="/privacy.html"', 'href="/privacy-policy/"')], min_hits=0, optional=True)

# ---------------------------------------------------------------- verificação
left_145 = sum(p.read_text(encoding="utf-8").count("$145/visit (weekly") for p in location_pages)
if left_145:
    errors.append(f"ainda restam {left_145} ocorrências do preço antigo $145")
left_privacy = sum(1 for p in SITE.rglob("*.html") if 'href="/privacy.html"' in p.read_text(encoding="utf-8"))
if left_privacy:
    errors.append(f"ainda restam {left_privacy} páginas linkando /privacy.html")
desc_len = len(NEW_DESC)
if not 120 <= desc_len <= 160:
    errors.append(f"meta description com {desc_len} chars (fora de 120-160)")
for page in service_pages:
    if MARKER not in page.read_text(encoding="utf-8"):
        errors.append(f"{page}: bloco de cidades não aplicado")

total = sum(changed.values())
print(f"patch_v2_seo: {total} mudanças em {sum(1 for v in changed.values() if v)} arquivos")
if errors:
    print("ERROS:")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print("verificação: OK")
