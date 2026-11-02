# -*- coding: utf-8 -*-
"""Patch v3 (01/11/2026) — nota REAL do Google no site inteiro. Roda depois do v1 e do v2.

Por quê: uma review de 1 estrela (2 semanas atrás) derrubou a nota do Google de
5.0 para 4.7 (13 avaliações). O site inteiro dizia "5.0★ Perfect score on
Google Reviews" em 7 línguas, no schema (aggregateRating 5.0/12) e nas metas —
anunciar nota falsa quebra a confiança e pode punir o ranking. Este patch troca
todas as alegações pela nota real e remove o "Perfect score"/"nota máxima".

AO MUDAR A NOTA DE NOVO: basta atualizar RATING/COUNT abaixo e rodar de novo
(as trocas numéricas são parametrizadas; os textos "perfect" já terão sumido).
"""
from pathlib import Path
import sys

SITE = Path(__file__).parent / "site"
RATING_OLD = ["5.0", "12"]  # nota e contagem anunciadas até 01/11/2026
RATING = "4.7"
COUNT = "13"

PAIRS = [
    # nota com estrela (cobre topbar, trust, aeo_reviews e metas em todas as línguas)
    ("5.0★", f"{RATING}★"),
    # hero badge e frases soltas
    ("5.0 on Google", f"{RATING} on Google"),
    ("5.0 stars on Google", f"{RATING} stars on Google"),
    ("5.0 — Perfect Score", f"{RATING} — Google Rating"),
    ("5.0 — 満点評価", f"{RATING} — Google評価"),
    # schema.org
    ('"ratingValue": "5.0"', f'"ratingValue": "{RATING}"'),
    ('"ratingCount": "12"', f'"ratingCount": "{COUNT}"'),
    ('"reviewCount": "12"', f'"reviewCount": "{COUNT}"'),
    # seção de reviews da home (texto fixo que o robô lê antes do i18n)
    ('<div class="rating-big">5.0</div>', '<div class="rating-big">4.7</div>'),
    ("7 verified reviews — 100% five-star rating on Google",
     "Hundreds of happy families across Silicon Valley &amp; Peninsula"),
    # "nota máxima" por língua (depois da troca numérica acima)
    ("</span> Perfect score on Google Reviews", "</span> Google Reviews rating"),
    (">Perfect score on Google Reviews<", ">Google Reviews rating<"),
    ("</span> Google 评分满分", "</span> Google 评分"),
    ("</span> Google पर परफेक्ट स्कोर", "</span> Google रेटिंग"),
    ("</span> Perpektong marka sa Google Reviews", "</span> Rating sa Google Reviews"),
    ("</span> Điểm hoàn hảo trên Google Reviews", "</span> Đánh giá trên Google Reviews"),
    ("</span> Google 리뷰 만점", "</span> Google 리뷰 평점"),
    ("</span> Googleレビュー満点評価", "</span> Googleレビュー評価"),
]

# "perfeito" como elogio à limpeza (how4_desc hi/vi) é idioma, não alegação de
# nota — por isso os termos abaixo são os de NOTA, não a palavra solta.
FORBIDDEN = ["5.0★", '"rating-big">5.0<', "100% five-star",
             "Perfect score", "Perfect Score", "评分满分", "परफेक्ट स्कोर",
             "Perpektong marka", "hoàn hảo trên Google", "리뷰 만점", "満点評価",
             '"ratingValue": "5.0"', '"ratingCount": "12"']

total = 0
files = sorted(SITE.rglob("*.html")) + [SITE / "assets" / "translations.js"]
for path in files:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in PAIRS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        total += 1

errors = []
for path in files:
    text = path.read_text(encoding="utf-8")
    for bad in FORBIDDEN:
        if bad in text:
            errors.append(f"{path.relative_to(SITE)}: ainda contém {bad!r}")

print(f"patch_v3_rating: {total} arquivos alterados")
if errors:
    print("ERROS:")
    for error in errors[:20]:
        print(" -", error)
    sys.exit(1)
print("verificação: OK — nenhuma alegação de 5.0/nota máxima restante")
