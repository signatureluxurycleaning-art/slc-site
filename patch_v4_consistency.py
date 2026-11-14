# -*- coding: utf-8 -*-
"""Patch v4 (12/11/2026) — o site passa a dizer o mesmo que o app e que o dono confirmou.

RODA SOZINHO. Os patches v1, v2 e v3 NÃO devem mais ser reaplicados: o site
mudou depois deles (página de Unpacking, 9 serviços) e eles quebram/estragam.

O que este patch conserta (revisão completa de 12/11/2026):
 1. PRODUTOS — o site prometia "Eco-Friendly Products" como padrão (não tóxico,
    plant-based, biodegradável, EPA Safer Choice). O dono confirmou em 11/11:
    os produtos são PET-SAFE, com opção eco-friendly SOB PEDIDO.
 2. REVIEWS — os cartões de review mostravam frases genéricas de marketing
    com o nome de avaliadores REAIS do Google: na home o translations.js trocava
    o texto verdadeiro pelo genérico ao carregar, e nas páginas de cidade o
    texto genérico estava fixo, assinado "Google review". Agora cada nome
    mostra o que a pessoa escreveu de verdade.
 3. NOTA — o número grande da seção de reviews dizia 5.0 em 24 páginas; a nota
    real anunciada no resto do site é RATING (abaixo).
 4. PREÇO — Spring Cleaning aparecia "From $410" na home e nas 23 cidades;
    o app e a página do serviço dizem $240 ($410 é o Post-Construction).
 5. MESMO DIA — as 23 cidades e o guia de custo diziam 15%; o app cobra +20%
    no mesmo dia e +15% no horário das 7 PM (como já dizem os Termos).
 6. PRIMEIRA LIMPEZA — "First-time clients: appointment slots start at 2:00 PM"
    ficou velho: de segunda a sexta a partir das 2 PM; sábado e domingo qualquer
    horário; domingo é reservado para a primeira limpeza (regra de 12/11).
 7. TERMOS — a "Reactivation Fee" de 45/60 dias não existe no app. A regra é:
    passou de 1 mês + 1 semana (37 dias) da última limpeza, a taxa de primeira
    limpeza vale de novo uma vez (Regular +25%, Deep +15%).
 8. Airbnb: frase começando com "call" minúsculo.

AO MUDAR A NOTA DO GOOGLE: troque RATING abaixo e rode de novo.
"""
from pathlib import Path
import re
import sys

SITE = Path(__file__).parent / "site"
RATING = "4.7"          # nota real do Google anunciada no site
TODAY = "2026-11-12"    # lastmod das páginas alteradas

errors = []
changed = set()


def fail(msg):
    errors.append(msg)
    print(" ✗", msg)


def read(p):
    return p.read_text(encoding="utf-8")


def write(p, text, original):
    if text != original:
        p.write_text(text, encoding="utf-8")
        changed.add(str(p.relative_to(SITE)))


def swap(text, old, new, where, count=1):
    """Troca exata e idempotente: `old` precisa aparecer `count` vezes, ou já
    estar trocado (`new` presente e `old` ausente)."""
    have = text.count(old)
    if have == count:
        return text.replace(old, new)
    if have == 0 and new in text:
        return text
    fail(f"{where}: esperava {count}x o trecho {old[:70]!r}, achei {have}x")
    return text


# ───────────────────────── textos novos ─────────────────────────
PET_TITLE = "Pet-Safe Products"
PET_DESC = "Pet-safe products on every visit. Eco-friendly options are available on request."
SAME_DAY_OLD = "Same-day available with 15% urgency surcharge."
SAME_DAY_NEW = "Same-day available with a 20% urgency fee."

# Frases genéricas que estavam assinadas com o nome de avaliadores reais.
GENERIC = {
    "Harshita S.": "I've tried 4 different services in Palo Alto and Signature is BY FAR the best. They're thorough, professional, and the house smells amazing after every visit.",
    "Danillo R.": "Booked a move-out clean and got my full deposit back — $3,200! They cleaned things I didn't even think about. Worth every single penny.",
    "Renata S.": "I have a 4-bedroom home and they finished in 3 hours perfectly. The team was polite, fast, and incredibly detailed. I've been a client for 8 months.",
    "Alday C.": "Deep cleaning before my parents visited. My mom said it was the cleanest she'd ever seen my house. That says everything! Booking again next month.",
    "Karla S.": "Best cleaning service in Silicon Valley, period. I've been a weekly client for over a year and the quality never drops. Highly recommend to everyone.",
    "Mia": "Post-construction cleaning after our full remodel — they removed all the dust and debris perfectly. The house looked brand new. Incredible job by the whole team.",
}


def real_reviews(home_html):
    """Nome -> texto verdadeiro, lido dos cartões da home (o HTML fixo e o
    JSON-LD da home sempre tiveram a review real)."""
    cards = re.findall(
        r'<p class="review-text" data-i18n="rev\d_text">"(.*?)"</p>.*?<span class="review-author-name">(.*?)</span>',
        home_html, re.S)
    found = {name.strip(): text.strip() for text, name in cards}
    for name in GENERIC:
        if name not in found:
            fail(f"home: não achei a review real de {name}")
        elif found[name] == GENERIC[name]:
            fail(f"home: a review de {name} no HTML fixo é a frase genérica")
    return found


# ───────────────────────── HOME ─────────────────────────
home_path = SITE / "index.html"
home = read(home_path)
home_original = home
REAL = real_reviews(home)

home = swap(home,
            '<div class="trust-icon">🌿</div>\n        <span data-i18n="trust_eco">Eco-Friendly Products</span>',
            f'<div class="trust-icon">🐾</div>\n        <span data-i18n="trust_eco">{PET_TITLE}</span>',
            "home: faixa de confiança")
home = swap(home,
            '<div class="why-point-icon">🌿</div>\n              <div class="why-point-text">\n                <h4 data-i18n="why_p1_title">Eco-Friendly Products</h4>\n'
            '                <p data-i18n="why_p1_desc">Non-toxic, plant-based, biodegradable products — safe for your kids, pets and the planet.</p>',
            '<div class="why-point-icon">🐾</div>\n              <div class="why-point-text">\n'
            f'                <h4 data-i18n="why_p1_title">{PET_TITLE}</h4>\n'
            f'                <p data-i18n="why_p1_desc">{PET_DESC}</p>',
            "home: cartão Why Us")
home = swap(home,
            "<p>We offer both regular and eco-friendly cleaning products at no extra charge. Safe for children, pets, and the environment.</p>",
            "<p>Our products are pet-safe. Prefer eco-friendly options? Just ask — we bring them on request at no extra charge.</p>",
            "home: bloco Eco-Friendly Options")
home = swap(home,
            "All include eco-friendly products and a 100% satisfaction guarantee.</p>",
            "All include pet-safe products, with eco-friendly options on request, and a 100% satisfaction guarantee.</p>",
            "home: resumo dos serviços")
home = swap(home,
            '<p data-i18n="footer_desc">Silicon Valley\'s most trusted luxury home cleaning service. Professional, eco-friendly, and 100% satisfaction guaranteed.</p>',
            '<p data-i18n="footer_desc">Silicon Valley &amp; Peninsula\'s most trusted luxury residential cleaning service. Serving Burlingame, Palo Alto, Cupertino, Mountain View, Sunnyvale &amp; 23 cities.</p>',
            "home: rodapé")
home = swap(home,
            "Yes! We bring all supplies and equipment. Choose between regular or eco-friendly products at no extra cost.",
            "Yes! We bring all supplies and equipment. Our products are pet-safe, and eco-friendly options are available on request at no extra cost.",
            "home: FAQ supplies")
home = swap(home,
            "Yes. We bring all cleaning supplies and equipment. We offer both regular and eco-friendly product options at no extra charge.",
            "Yes. We bring all cleaning supplies and equipment. Our products are pet-safe, and eco-friendly options are available on request at no extra charge.",
            "home: FAQ supplies (JSON-LD)")
home = swap(home,
            '"Eco-friendly cleaning",\n      "EPA Safer Choice products"',
            '"Pet-safe cleaning products",\n      "Eco-friendly cleaning options"',
            "home: knowsAbout")
home = swap(home,
            '<span class="service-price">From <strong>$410</strong></span>',
            '<span class="service-price">From <strong>$240</strong></span>',
            "home: preço do Spring Cleaning")
home = swap(home, '<div class="rating-big">5.0</div>', f'<div class="rating-big">{RATING}</div>', "home: nota grande")
home = swap(home,
            '<div class="rating-count" data-i18n="reviews_count">7 verified reviews — 100% five-star rating on Google</div>',
            '<div class="rating-count" data-i18n="reviews_count">Hundreds of happy families across Silicon Valley &amp; Peninsula</div>',
            "home: legenda da nota")

WG_OLD = " Same-day bookings include a +20% urgency fee. First-time clients: appointment slots start at 2:00 PM. We recommend"
WG_NEW = " We recommend"
home = swap(home, WG_OLD, WG_NEW, "home: FAQ White Glove (JSON-LD)")
# O navegador guarda o translations.js pela versão do endereço: sem trocar a
# versão, quem já visitou o site continuaria vendo o arquivo antigo (que
# trocava a review real pela genérica) por horas.
home = swap(home, "assets/translations.js?v=20261110", "assets/translations.js?v=20261112", "home: versão do translations.js")
write(home_path, home, home_original)

# ───────────────────────── CIDADES ─────────────────────────
city_pages = sorted((SITE / "locations").glob("*/index.html"))
if len(city_pages) != 23:
    fail(f"esperava 23 páginas de cidade, achei {len(city_pages)}")
for p in city_pages:
    slug = p.parent.name
    t = read(p)
    original = t
    t = swap(t, "eco-friendly products, and a 100% satisfaction guarantee",
             "pet-safe products, and a 100% satisfaction guarantee", f"{slug}: hero")
    t = swap(t,
             '<div class="why-point-icon">🌿</div>\n              <div class="why-point-text">\n                <h4>Eco-Friendly Products</h4>\n'
             '                <p>Safe for your family, pets, and the environment. We use professional-grade, non-toxic cleaning solutions.</p>',
             '<div class="why-point-icon">🐾</div>\n              <div class="why-point-text">\n'
             f'                <h4>{PET_TITLE}</h4>\n                <p>{PET_DESC}</p>',
             f"{slug}: cartão Why")
    t = swap(t, '<div class="rating-big">5.0</div>', f'<div class="rating-big">{RATING}</div>', f"{slug}: nota grande")
    t = swap(t, SAME_DAY_OLD, SAME_DAY_NEW, f"{slug}: mesmo dia (FAQ + JSON-LD)", count=2)
    # Spring Cleaning: o único "From $410" da página é o do cartão do Spring.
    spring_old = '<div class="service-price">From $410</div>'
    spring_new = '<div class="service-price">From $240</div>'
    if t.count(spring_old) == 1:
        at = t.index(spring_old)
        if "Spring Cleaning" not in t[max(0, at - 700):at]:
            fail(f"{slug}: o 'From $410' não está no cartão do Spring Cleaning")
        else:
            t = t.replace(spring_old, spring_new)
    elif not (t.count(spring_old) == 0 and spring_new in t):
        fail(f"{slug}: preço do Spring Cleaning não encontrado")
    # Reviews: cada nome mostra o que a pessoa escreveu de verdade.
    for name, generic in GENERIC.items():
        old = f'<p>"{generic}"</p>\n          <div class="review-author">— {name}, Silicon Valley · Google review</div>'
        if old in t:
            if name not in REAL:
                continue
            new = f'<p>"{REAL[name]}"</p>\n          <div class="review-author">— {name}, Silicon Valley · Google review</div>'
            t = t.replace(old, new)
    write(p, t, original)

# ───────────────────────── SERVIÇOS / GUIA / TERMOS ─────────────────────────
p = SITE / "services" / "regular-cleaning" / "index.html"
t = read(p); o = t
t = swap(t, "Background-checked team, eco-friendly products, 100% satisfaction guarantee.",
         "Background-checked team, pet-safe products, 100% satisfaction guarantee.", "regular: descrição (JSON-LD)")
write(p, t, o)

p = SITE / "services" / "white-glove-deep-clean" / "index.html"
t = read(p); o = t
t = swap(t, WG_OLD, WG_NEW, "white glove: FAQ (JSON-LD)")
write(p, t, o)

p = SITE / "services" / "airbnb-cleaning" / "index.html"
t = read(p); o = t
t = swap(t, "From $155. call or text us to schedule.", "From $155. Call or text us to schedule.", "airbnb: meta description")
t = swap(t, "vary by home size. call or text us to schedule for an instant, personalized quote.",
         "vary by home size. Call or text us to schedule and get a personalized quote.", "airbnb: parágrafo de preço")
write(p, t, o)

p = SITE / "guides" / "house-cleaning-cost-bay-area" / "index.html"
t = read(p); o = t
t = swap(t, "Same-day / urgent evening cleanings carry a 15% surcharge.",
         "Same-day cleanings carry a 20% urgency fee, and the 7:00 PM evening slot carries a 15% fee.", "guia: Timing")
write(p, t, o)

p = SITE / "terms-and-conditions" / "index.html"
t = read(p); o = t
P_STYLE = '<p style="color:#4a4a6a;line-height:1.8;">'
H2 = '<h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.5rem;margin-top:2rem;color:#0C1A2E;">'
t = swap(t, "<em>Last updated: July 2026</em>", "<em>Last updated: November 2026</em>", "termos: data")
t = swap(t, "number of bedrooms and bathrooms, and service frequency.",
         "number of bedrooms and bathrooms, square footage (for houses), and service frequency.", "termos: 1. Service Rates")
t = swap(t,
         f'{H2}2. First Visit Setup Rate</h2>\n    {P_STYLE}Your first cleaning visit includes a one-time setup rate of approximately 25% above the recurring rate. This covers the initial deep assessment and setup of your home profile. Subsequent visits are charged at the standard recurring rate.</p>',
         f'{H2}2. First-Cleaning Rate</h2>\n    {P_STYLE}Your first cleaning includes a one-time first-cleaning rate: <strong>+25%</strong> for Regular Cleaning and <strong>+15%</strong> for Deep Cleaning. The first visit is always the heaviest, and one of the owners works alongside your team. Move-in/move-out, post-construction and spring cleaning have no first-cleaning rate. From your next visit you pay the standard rate, as long as you keep a regular schedule (see section 4).</p>',
         "termos: 2. First-Cleaning Rate")
t = swap(t,
         f'{H2}4. Reactivation Fee</h2>\n    {P_STYLE}If your recurring service has been inactive:</p>\n    <ul style="color:#4a4a6a;line-height:1.8;margin-left:1.5rem;">\n      <li><strong>After 45 days without cleaning:</strong> +15% reactivation fee</li>\n      <li><strong>After 60 days without cleaning:</strong> +25% reactivation fee</li>\n    </ul>',
         f'{H2}4. Keeping Your Regular Price</h2>\n    {P_STYLE}To keep your regular price, each cleaning needs to happen within <strong>1 month and 1 week (37 days)</strong> of the previous one. If more time than that passes, the first-cleaning rate applies once again (+25% for Regular Cleaning, +15% for Deep Cleaning) to bring your home back to standard, and then your regular price returns.</p>',
         "termos: 4. Keeping Your Regular Price")
t = swap(t,
         f'{H2}6. Same-Day Bookings</h2>\n    {P_STYLE}Same-day bookings are subject to a <strong>+20% urgency fee</strong> based on availability. First-time clients: appointment slots start at 2:00 PM.</p>',
         f'{H2}6. Same-Day Bookings and First-Time Appointments</h2>\n    {P_STYLE}Same-day bookings are subject to a <strong>+20% urgency fee</strong> based on availability. First-time clients: Monday to Friday, appointments start at 2:00 PM; on Saturday and Sunday, any time slot is available. Sundays are reserved for first-time cleanings.</p>',
         "termos: 6. Same-Day / First-Time")
t = swap(t,
         f'{H2}7. Overtime (After 7:00 PM)</h2>\n    {P_STYLE}Services that extend beyond 7:00 PM are subject to a <strong>+15% overtime fee</strong>.</p>',
         f'{H2}7. Overtime (7:00 PM Slot)</h2>\n    {P_STYLE}Appointments in the 7:00 PM slot are subject to a <strong>+15% overtime fee</strong>.</p>',
         "termos: 7. Overtime")
write(p, t, o)

# ───────────────────────── TRADUÇÕES ─────────────────────────
p = SITE / "assets" / "translations.js"
t = read(p); o = t
JS_PAIRS = [
    # inglês
    ('trust_eco:        "Eco-Friendly Products"', f'trust_eco:        "{PET_TITLE}"'),
    ('trust_2: "🌿 Eco-Friendly Products"', f'trust_2: "🐾 {PET_TITLE}"'),
    ('why_p1_title: "Eco-Friendly Products"', f'why_p1_title: "{PET_TITLE}"'),
    ('why_p1_desc:  "Non-toxic, plant-based, biodegradable products — safe for your kids, pets and the planet."', f'why_p1_desc:  "{PET_DESC}"'),
    ('why2_title:   "Eco-Friendly Products"', f'why2_title:   "{PET_TITLE}"'),
    ('why2_desc:    "Safe for your family, pets, and the environment. We use professional-grade, non-toxic cleaning solutions."', f'why2_desc:    "{PET_DESC}"'),
    ('and the White Glove Deep Clean. All include eco-friendly products and a 100% satisfaction guarantee."',
     'and the White Glove Deep Clean. All include pet-safe products, with eco-friendly options on request, and a 100% satisfaction guarantee."'),
    ('svc6_price: "From $410"', 'svc6_price: "From $240"'),
    # 中文
    ('trust_2: "🌿 环保清洁产品"', 'trust_2: "🐾 宠物安全清洁产品"'),
    ('why2_title:   "环保产品"', 'why2_title:   "宠物安全产品"'),
    ('why2_desc:    "对您的家人、宠物和环境安全。我们使用专业级无毒清洁溶液。"', 'why2_desc:    "每次清洁均使用对宠物安全的产品。如需环保产品，可按要求提供。"'),
    ('所有服务均使用环保产品，并提供100%满意保证。"', '所有服务均使用对宠物安全的产品（可按要求提供环保产品），并提供100%满意保证。"'),
    ('svc6_price: "起价 $410"', 'svc6_price: "起价 $240"'),
    # हिन्दी
    ('trust_2: "🌿 पर्यावरण-अनुकूल उत्पाद"', 'trust_2: "🐾 पालतू-सुरक्षित उत्पाद"'),
    ('why2_title:   "पर्यावरण-अनुकूल उत्पाद"', 'why2_title:   "पालतू-सुरक्षित उत्पाद"'),
    ('why2_desc:    "आपके परिवार, पालतू जानवरों और पर्यावरण के लिए सुरक्षित। हम पेशेवर-ग्रेड, गैर-विषाक्त सफाई समाधान उपयोग करते हैं।"',
     'why2_desc:    "हर विजिट पर पालतू जानवरों के लिए सुरक्षित उत्पाद। अनुरोध पर इको-फ्रेंडली विकल्प उपलब्ध हैं।"'),
    ('सभी में इको-फ्रेंडली उत्पाद और 100% संतुष्टि की गारंटी शामिल है।"', 'सभी में पालतू-सुरक्षित उत्पाद (अनुरोध पर इको-फ्रेंडली विकल्प) और 100% संतुष्टि की गारंटी शामिल है।"'),
    ('svc6_price: "$410 से शुरू"', 'svc6_price: "$240 से शुरू"'),
    # Filipino
    ('trust_2: "🌿 Eco-Friendly na Produkto"', 'trust_2: "🐾 Pet-Safe na Produkto"'),
    ('why2_title:   "Eco-Friendly na Produkto"', 'why2_title:   "Pet-Safe na Produkto"'),
    ('why2_desc:    "Ligtas para sa iyong pamilya, alagang hayop, at kalikasan. Gumagamit kami ng propesyonal na non-toxic na solusyon sa paglilinis."',
     'why2_desc:    "Pet-safe na mga produkto sa bawat bisita. May eco-friendly na opsyon kapag hiniling."'),
    ('Kasama sa lahat ang eco-friendly na produkto at 100% satisfaction guarantee."',
     'Kasama sa lahat ang pet-safe na produkto (may eco-friendly na opsyon kapag hiniling) at 100% satisfaction guarantee."'),
    ('svc6_price: "Mula $410"', 'svc6_price: "Mula $240"'),
    # Tiếng Việt
    ('trust_2: "🌿 Sản Phẩm Thân Thiện Môi Trường"', 'trust_2: "🐾 Sản Phẩm An Toàn Cho Thú Cưng"'),
    ('why2_title:   "Sản Phẩm Thân Thiện Môi Trường"', 'why2_title:   "Sản Phẩm An Toàn Cho Thú Cưng"'),
    ('why2_desc:    "An toàn cho gia đình, thú cưng và môi trường của bạn. Chúng tôi sử dụng dung dịch làm sạch chuyên nghiệp, không độc hại."',
     'why2_desc:    "Sản phẩm an toàn cho thú cưng trong mỗi lần dọn dẹp. Có lựa chọn thân thiện môi trường theo yêu cầu."'),
    ('Tất cả đều dùng sản phẩm thân thiện môi trường và bảo đảm hài lòng 100%."',
     'Tất cả đều dùng sản phẩm an toàn cho thú cưng (có lựa chọn thân thiện môi trường theo yêu cầu) và bảo đảm hài lòng 100%."'),
    ('svc6_price: "Từ $410"', 'svc6_price: "Từ $240"'),
    # 한국어
    ('trust_2: "🌿 친환경 제품"', 'trust_2: "🐾 반려동물에 안전한 제품"'),
    ('why2_title:   "친환경 제품"', 'why2_title:   "반려동물에 안전한 제품"'),
    ('why2_desc:    "가족, 반려동물, 환경에 안전합니다. 전문가급 무독성 청소 솔루션을 사용합니다."',
     'why2_desc:    "매 방문마다 반려동물에 안전한 제품을 사용합니다. 요청 시 친환경 제품도 가능합니다."'),
    ('모든 서비스에 친환경 제품과 100% 만족 보장이 포함됩니다."', '모든 서비스에 반려동물에 안전한 제품(요청 시 친환경 제품 가능)과 100% 만족 보장이 포함됩니다."'),
    ('svc6_price: "$410부터"', 'svc6_price: "$240부터"'),
    # 日本語
    ('trust_eco: "環境にやさしい洗剤"', 'trust_eco: "ペットに安全な洗剤"'),
    ('why_p1_title: "環境にやさしい洗剤"', 'why_p1_title: "ペットに安全な洗剤"'),
    ('why_p1_desc: "無毒・植物由来・生分解性 — お子様にもペットにも地球にも安心。"', 'why_p1_desc: "毎回ペットに安全な洗剤を使用。ご希望の場合は環境にやさしい洗剤もご用意します。"'),
    ('すべて環境にやさしい洗剤と100%満足保証付きです。"', 'すべてペットに安全な洗剤（ご希望により環境にやさしい洗剤も対応）と100%満足保証付きです。"'),
    ('svc6_price: "$410〜"', 'svc6_price: "$240〜"'),
]
for old, new in JS_PAIRS:
    t = swap(t, old, new, "translations.js")
# Reviews: as chaves rev1_text…rev6_text (só existiam em inglês e japonês)
# trocavam a review real por uma frase genérica ao carregar a página. Sem a
# chave fica o texto fixo do HTML — a review verdadeira, como foi escrita.
t, removed = re.subn(r'^[ \t]*rev[1-6]_text:[^\n]*\n', "", t, flags=re.M)
if removed not in (0, 12):
    fail(f"translations.js: esperava remover 12 linhas rev*_text (inglês e japonês x 6), removi {removed}")
write(p, t, o)

# ───────────────────────── SITEMAP ─────────────────────────
p = SITE / "sitemap.xml"
sm = read(p); sm_o = sm
for rel in sorted(changed):
    if not rel.endswith("index.html"):
        continue
    url_path = "/" + rel[:-len("index.html")]
    loc = f"<loc>https://signatureluxurycleaning.com{url_path}</loc>"
    if loc in sm:
        sm = re.sub(re.escape(loc) + r"(\s*)<lastmod>[^<]*</lastmod>", loc + r"\g<1>" + f"<lastmod>{TODAY}</lastmod>", sm)
write(p, sm, sm_o)

# ───────────────────────── VERIFICAÇÃO ─────────────────────────
FORBIDDEN = [
    "Eco-Friendly Products", "eco-friendly products", "Eco-Friendly na Produkto", "eco-friendly na produkto",
    "non-toxic", "Non-toxic", "plant-based", "biodegradable", "EPA Safer Choice",
    "环保清洁产品", "无毒", "पर्यावरण-अनुकूल उत्पाद", "गैर-विषाक्त", "Thân Thiện Môi Trường\"", "không độc hại",
    "친환경 제품\"", "무독성", "環境にやさしい洗剤\"", "無毒",
    "15% urgency surcharge", "urgent evening cleanings carry a 15%", "slots start at 2:00 PM",
    'rating-big">5.0<', "100% five-star", "Reactivation Fee", "reactivation fee",
    "From $410</div>", "From <strong>$410</strong></span>", 'svc6_price: "From $410"', "起价 $410", "$410 से शुरू", "Mula $410", "Từ $410", "$410부터", "$410〜",
    ". call or text us",
] + list(GENERIC.values())
files = sorted(SITE.rglob("*.html")) + [SITE / "assets" / "translations.js"]
for f in files:
    text = read(f)
    rel = str(f.relative_to(SITE))
    for bad in FORBIDDEN:
        if bad in text:
            fail(f"{rel}: ainda contém {bad[:60]!r}")

if re.search(r'rev[1-6]_text', read(SITE / "assets" / "translations.js")):
    fail("translations.js: ainda existe chave rev*_text (troca a review real pela genérica)")
home = read(SITE / "index.html")
for name, text in REAL.items():
    if home.count(text) != 2:
        fail(f"home: a review real de {name} deveria aparecer 2x (cartão + JSON-LD), achei {home.count(text)}")
with_real = 0
for cp in city_pages:
    ct = read(cp)
    for name, text in REAL.items():
        if f"— {name}, Silicon Valley · Google review" in ct:
            if f'<p>"{text}"</p>\n          <div class="review-author">— {name}, Silicon Valley · Google review</div>' not in ct:
                fail(f"{cp.parent.name}: o cartão de {name} não mostra a review real")
            else:
                with_real += 1
    for need in (PET_TITLE, PET_DESC, SAME_DAY_NEW, f'rating-big">{RATING}<', "From $240</div>"):
        if need not in ct:
            fail(f"{cp.parent.name}: falta {need[:50]!r}")
if "assets/translations.js?v=20261112" not in home:
    fail("home: o translations.js precisa da versão nova no endereço")
if with_real != 60:
    fail(f"esperava 60 cartões de review real nas cidades (20 páginas x 3), achei {with_real}")
terms = read(SITE / "terms-and-conditions" / "index.html")
for need in ("1 month and 1 week (37 days)", "Sundays are reserved for first-time cleanings", "on Saturday and Sunday, any time slot is available",
             "+25%</strong> for Regular Cleaning", "+15%</strong> for Deep Cleaning", "+20% urgency fee", "+15% overtime fee", "48 hours", "30% fee"):
    if need not in terms:
        fail(f"termos: falta {need!r}")

print(f"patch_v4_consistency: {len(changed)} arquivos alterados")
for rel in sorted(changed):
    print("  ·", rel)
if errors:
    print(f"verificação: FALHOU ({len(errors)} problema(s))")
    sys.exit(1)
print("verificação: OK — produtos, reviews, nota, preços, mesmo dia, primeira limpeza e termos batem com o app")
