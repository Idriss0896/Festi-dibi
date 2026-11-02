#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit le dossier de presentation Festi Dibi (16:9, 16 slides)."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- palette
CHARBON  = "1C1512"
BRAISE   = "B8452B"
BRAISE_D = "8E3320"
AMBRE    = "E09A3E"
SABLE    = "F3E7DA"
CREME    = "FBF7F2"
GRIS     = "6E625B"
GRIS_C   = "9C8F85"
BLANC    = "FFFFFF"
TRAIT    = "E2D5C7"

FONT = "Segoe UI"
SERIF = "Georgia"

W, H = 13.333, 7.5
ML = 0.75
CW = 11.833


def rgb(h):
    return RGBColor.from_string(h)


def blend(a, b, t):
    """t=0 -> a, t=1 -> b  (simule une transparence)."""
    ca = tuple(int(a[i:i + 2], 16) for i in (0, 2, 4))
    cb = tuple(int(b[i:i + 2], 16) for i in (0, 2, 4))
    return "".join("%02X" % int(round(x + (y - x) * t)) for x, y in zip(ca, cb))


# ---------------------------------------------------------------- primitives
def _clean(s):
    """Supprime le style de forme (ombres et effets du theme)."""
    el = s._element
    for st in el.findall(qn("p:style")):
        el.remove(st)
    s.shadow.inherit = False
    return s


def bg(slide, color=CREME):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(W), Inches(H))
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(color)
    s.line.fill.background()
    return _clean(s)


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.75, rounded=False, radius=0.08):
    shp = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shp, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        try:
            s.adjustments[0] = radius
        except Exception:
            pass
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    return _clean(s)


def oval(slide, x, y, w, h, fill=None, line=None, lw=1.0):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    return _clean(s)


def text(slide, x, y, w, h, s, size=14, color=CHARBON, bold=False, font=FONT,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=None,
         space_after=0, space_before=0, italic=False, margins=(0, 0, 0, 0)):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = Inches(margins[0])
    tf.margin_right = Inches(margins[1])
    tf.margin_top = Inches(margins[2])
    tf.margin_bottom = Inches(margins[3])
    tf.vertical_anchor = anchor
    for i, line in enumerate(s.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.line_spacing = spacing
        p.space_after = Pt(space_after)
        p.space_before = Pt(space_before)
        r = p.add_run()
        r.text = line
        f = r.font
        f.name = font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = rgb(color)
    return tb


def shape_text(shape, s, size=11, color=BLANC, bold=True, font=FONT, align=PP_ALIGN.CENTER):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = s
    f = r.font
    f.name = font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = rgb(color)
    return shape


def header(slide, kicker, title):
    text(slide, ML, 0.50, CW, 0.24, kicker.upper(), size=9.5, color=BRAISE, bold=True)
    text(slide, ML, 0.78, CW, 0.66, title, size=29, color=CHARBON, bold=True, spacing=0.92)
    rect(slide, ML, 1.50, 0.85, 0.045, fill=AMBRE)


def footer(slide, n, label="Festival du Dibi  ·  Plateforme digitale 2026"):
    rect(slide, ML, 6.94, CW, 0.01, fill=TRAIT)
    text(slide, ML, 7.04, 8.0, 0.2, label, size=8, color=GRIS_C)
    text(slide, 11.3, 7.04, 1.28, 0.2, "%02d" % n, size=8, color=GRIS_C, align=PP_ALIGN.RIGHT)


def notes(slide, s):
    slide.notes_slide.notes_text_frame.text = s


def set_cell(c, s, size=11, color=CHARBON, bold=False, fill=None,
             align=PP_ALIGN.LEFT, font=FONT):
    if fill:
        c.fill.solid()
        c.fill.fore_color.rgb = rgb(fill)
    else:
        c.fill.background()
    c.vertical_anchor = MSO_ANCHOR.MIDDLE
    c.margin_left = Inches(0.16)
    c.margin_right = Inches(0.12)
    c.margin_top = Inches(0.04)
    c.margin_bottom = Inches(0.04)
    tf = c.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = s
    f = r.font
    f.name = font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = rgb(color)


def table(slide, x, y, widths, rows, heights):
    n_r, n_c = len(rows), len(rows[0])
    gs = slide.shapes.add_table(n_r, n_c, Inches(x), Inches(y),
                                Inches(sum(widths)), Inches(sum(heights)))
    tbl = gs.table
    tbl.horz_banding = False
    tbl.first_row = False
    for i, wd in enumerate(widths):
        tbl.columns[i].width = Inches(wd)
    for i, ht in enumerate(heights):
        tbl.rows[i].height = Inches(ht)
    return tbl


# ---------------------------------------------------------------- slides
def s01_cover(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, CHARBON)

    # cercles decoratifs (braise)
    for (x, y, d) in ((9.2, -1.9, 7.4), (10.6, 2.1, 5.2), (11.8, 4.9, 3.2)):
        oval(s, x, y, d, d, fill=None, line=blend(BRAISE, CHARBON, 0.55), lw=1.0)

    rect(s, 0, 0, 0.16, H, fill=BRAISE)

    mark = rect(s, 0.92, 0.86, 0.62, 0.62, fill=BRAISE, rounded=True, radius=0.18)
    shape_text(mark, "FD", size=15, color=BLANC, bold=True)

    text(s, 1.70, 0.98, 6.0, 0.36, "FESTI  DIBI", size=11, color=AMBRE, bold=True)

    text(s, 0.92, 2.02, 9.4, 0.28, "DOSSIER DE PRÉSENTATION  ·  NOVEMBRE 2026",
         size=10, color=AMBRE, bold=True)

    text(s, 0.92, 2.42, 9.6, 1.0, "Festival du Dibi", size=56, color=BLANC, bold=True, spacing=0.9)
    text(s, 0.92, 3.40, 9.6, 0.7, "La plateforme digitale officielle", size=32,
         color=SABLE, spacing=0.95)

    rect(s, 0.92, 4.42, 1.1, 0.05, fill=AMBRE)

    text(s, 0.92, 4.66, 9.0, 0.6,
         "Site web  ·  Billetterie mobile  ·  Pilotage de l’événement", size=15, color=GRIS_C)

    text(s, 0.92, 6.38, 10.5, 0.3,
         "Bamako  ·  Place du Cinquantenaire  ·  18 jours non-stop  ·  200 000 visiteurs",
         size=10, color=blend(SABLE, CHARBON, 0.45))
    text(s, 0.92, 6.70, 10.5, 0.3,
         "Document de travail — chiffres et budgets à valider avec les organisateurs",
         size=8.5, color=blend(SABLE, CHARBON, 0.6))

    notes(s, "Ouvrir en remerciant pour le temps accordé. Une phrase : « Je viens vous "
             "proposer de transformer les 200 000 visiteurs du festival en données, "
             "en recettes et en notoriété — avec un seul outil. » Ne pas parler technique "
             "avant la diapositive 4.")


def s02_chiffres(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le point de départ", "Un événement de dimension nationale")

    stats = [
        ("11", "éditions", "Déc. 2025 – janv. 2026"),
        ("200 000", "visiteurs", "sur 18 jours"),
        ("200+", "stands & exposants", "grilladiers, artisans"),
        ("18", "jours non-stop", "7 nuits thématiques"),
    ]
    for i, (val, lab, note) in enumerate(stats):
        x = ML + i * 2.99
        rect(s, x, 1.82, 2.80, 2.02, fill=BLANC, rounded=True, radius=0.06)
        text(s, x + 0.22, 2.02, 2.4, 0.72, val, size=34, color=BRAISE, bold=True, spacing=0.9)
        text(s, x + 0.22, 2.84, 2.4, 0.3, lab, size=12, color=CHARBON, bold=True)
        text(s, x + 0.22, 3.16, 2.4, 0.5, note, size=9.5, color=GRIS)

    text(s, ML, 4.32, 11.0, 0.9,
         "Le plus grand rendez-vous de la gastronomie\nmalienne et africaine.",
         size=21, color=CHARBON, bold=True, spacing=1.08)
    text(s, ML, 5.42, 11.3, 0.3,
         "Haut parrainage du Président de la Transition  ·  Ministère de l’Élevage et de la Pêche  ·  "
         "Organisation InfluYence Group", size=10.5, color=GRIS)

    pills = ["7 nuits thématiques", "Fan Zone CAN", "Concours du meilleur dibi", "Village artisanal"]
    x = ML
    for p in pills:
        wd = 0.30 + len(p) * 0.078
        shp = rect(s, x, 5.94, wd, 0.40, fill=SABLE, rounded=True, radius=0.5)
        shape_text(shp, p, size=9.5, color=BRAISE_D, bold=True)
        x += wd + 0.14

    footer(s, 2)
    notes(s, "Ces chiffres viennent de la presse et des organisateurs. Les citer ouvre la "
             "conversation : on parle de LEUR réalité, pas d’un projet abstrait. "
             "Si un chiffre les surprend, noter la correction : c’est déjà un signe d’intérêt.")


def s03_constat(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le constat", "Ce que 200 000 visiteurs laissent aujourd’hui : rien")

    text(s, 1.32, 1.70, 5.0, 0.24, "AUJOURD’HUI", size=8.5, color=GRIS_C, bold=True)
    text(s, 6.60, 1.70, 5.4, 0.24, "CE QUE ÇA COÛTE", size=8.5, color=GRIS_C, bold=True)

    rows = [
        ("Inscriptions par WhatsApp, appels et papier",
         "Doublons, places perdues, paiements jamais suivis"),
        ("Billetterie en espèces, entrées non comptées",
         "Recettes non tracées, files d’attente, aucune donnée sur le public"),
        ("Programme diffusé en posts Facebook",
         "Le visiteur ne sait pas qui passe quand — et repart"),
        ("Sponsors sans chiffres d’audience",
         "Un sponsoring sous-vendu de 30 à 50 % chaque année"),
        ("Rien ne reste après le 4 janvier",
         "Ni base clients, ni replay, ni bilan chiffré pour l’édition suivante"),
    ]
    for i, (a, b) in enumerate(rows):
        y = 2.04 + i * 0.95
        text(s, ML, y, 0.45, 0.3, "0%d" % (i + 1), size=10.5, color=AMBRE, bold=True)
        text(s, 1.32, y - 0.02, 5.0, 0.7, a, size=13.5, color=CHARBON, bold=True, spacing=1.0)
        text(s, 6.60, y + 0.01, 5.6, 0.7, b, size=12, color=GRIS, spacing=1.06)
        if i < len(rows) - 1:
            rect(s, ML, y + 0.80, CW, 0.008, fill=TRAIT)

    footer(s, 3)
    notes(s, "Marcquer une pause après chaque ligne. Ne pas accuser : constater. "
             "La dernière ligne est la plus importante — c’est elle qui justifie un outil "
             "qui reste toute l’année, pas seulement 18 jours.")


def s04_reponse(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Notre réponse", "Une application web, pas une application à télécharger")

    text(s, ML, 1.80, 3.95, 1.5,
         "Une PWA : un site qui s’ouvre dans le navigateur,\ns’installe sur l’écran d’accueil "
         "et fonctionne\nmême sans réseau.", size=13, color=GRIS, spacing=1.25)

    bullets = ["Zéro téléchargement", "Mise à jour instantanée", "Un simple lien WhatsApp"]
    for i, b in enumerate(bullets):
        y = 3.42 + i * 0.52
        text(s, ML, y, 0.24, 0.3, "—", size=12, color=AMBRE, bold=True)
        text(s, ML + 0.30, y - 0.02, 3.6, 0.34, b, size=12.5, color=CHARBON, bold=True)

    rows = [
        ["", "App à télécharger", "Application web"],
        ["Installation", "Store, 40 Mo, 3 étapes", "1 clic"],
        ["Coût de départ", "× 3 (iOS + Android)", "× 1"],
        ["Mise à jour", "Validation 1 à 7 jours", "Immédiate"],
        ["Hors-ligne", "Oui, une fois installée", "Oui, en natif (PWA)"],
        ["Partage WhatsApp", "Lien mort pour qui n’a pas l’app", "Lien direct"],
        ["Maintenance", "2 équipes, 2 cycles", "1 prestataire"],
    ]
    tbl = table(s, 5.05, 1.78, [1.62, 2.85, 2.85], rows, [0.42] + [0.53] * 6)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            is_head = (i == 0)
            if j == 2:
                fill = BRAISE if is_head else SABLE
                color = BLANC if is_head else BRAISE_D
            elif is_head:
                fill, color = CHARBON, BLANC
            else:
                fill, color = (BLANC if i % 2 else CREME), (CHARBON if j == 0 else GRIS)
            set_cell(tbl.cell(i, j), val, size=10 if not is_head else 9.5,
                     color=color, bold=(is_head or j == 0), fill=fill)

    text(s, 5.05, 5.72, 7.3, 0.3, "Résultat : zéro friction entre la publicité et l’inscription.",
         size=11.5, color=BRAISE_D, bold=True)

    rect(s, ML, 5.42, 3.95, 1.02, fill=SABLE, rounded=True, radius=0.10)
    text(s, ML + 0.24, 5.56, 3.5, 0.7,
         "Une application native coûte 3 à 5 M F de plus — pour trois fois moins d’utilisateurs.",
         size=9.5, color=BRAISE_D, bold=True, spacing=1.15)

    footer(s, 4)
    notes(s, "C’est LA diapositive qui doit tuer l’idée d’une app native. "
             "Si quelqu’un dit « il faut une app sur Play Store », répondre : "
             "« on peut, mais on perdra 70 % des utilisateurs entre le lien et l’installation ». "
             "Insister sur le hors-ligne : c’est la vraie contrainte au Mali.")


def s05_archi(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "L’architecture", "Quatre briques, une seule plateforme")

    cards = [
        ("01", "Vitrine publique",
         ["Programme en temps réel", "Fiches exposants et artistes", "Espace média et revue de presse"]),
        ("02", "Espace professionnel",
         ["Inscription des stands", "Candidatures artistes", "Accréditations presse"]),
        ("03", "Terrain",
         ["Scan QR et contrôle d’accès", "Badges et caisses des stands", "Vote du concours"]),
        ("04", "Q.G. organisateur",
         ["Ventes et entrées en direct", "Suivi des dossiers et paiements", "Reporting sponsors"]),
    ]
    for i, (num, title, items) in enumerate(cards):
        x = ML + (i % 2) * 6.08
        y = 1.80 + (i // 2) * 2.22
        rect(s, x, y, 5.72, 2.06, fill=BLANC, rounded=True, radius=0.06)
        text(s, x + 0.26, y + 0.20, 0.6, 0.24, num, size=9.5, color=AMBRE, bold=True)
        text(s, x + 0.26, y + 0.46, 5.0, 0.34, title, size=17, color=CHARBON, bold=True)
        for k, it in enumerate(items):
            yy = y + 0.96 + k * 0.34
            text(s, x + 0.26, yy, 0.2, 0.28, "·", size=14, color=BRAISE, bold=True)
            text(s, x + 0.44, yy, 5.0, 0.28, it, size=10.5, color=GRIS)

    text(s, ML, 6.42, CW, 0.3,
         "Règle du projet : jamais la brique 01 sans la brique 04 — sinon tout le monde "
         "revient sur WhatsApp dès le deuxième jour.",
         size=10.5, color=BRAISE_D, bold=True)

    footer(s, 5)
    notes(s, "Expliquer avec le doigt : 01 c’est ce que le public voit, 04 c’est ce que "
             "l’équipe utilise. Les deux doivent exister ensemble, sinon l’outil meurt "
             "au bout d’une semaine.")


def phone(slide, x, y, w, h, kind):
    """Maquette filaire d’un écran."""
    rect(slide, x, y, w, h, fill=CHARBON, rounded=True, radius=0.10)
    sx, sy, sw, sh = x + 0.09, y + 0.13, w - 0.18, h - 0.26
    rect(slide, sx, sy, sw, sh, fill=CREME, rounded=True, radius=0.03)

    bar = rect(slide, sx, sy, sw, 0.24, fill=CHARBON)
    shape_text(bar, "FESTI DIBI", size=6.5, color=AMBRE, bold=True, align=PP_ALIGN.LEFT)
    bar.text_frame.margin_left = Inches(0.09)

    if kind == "home":
        hero = rect(slide, sx + 0.10, sy + 0.33, sw - 0.20, 0.86, fill=BRAISE, rounded=True, radius=0.06)
        shape_text(hero, "LE FESTIVAL\nDU DIBI", size=8, color=BLANC, bold=True)
        rect(slide, sx + 0.10, sy + 1.30, sw - 0.20, 0.07, fill=blend(GRIS, CREME, 0.6))
        rect(slide, sx + 0.10, sy + 1.44, sw * 0.62, 0.07, fill=blend(GRIS, CREME, 0.6))
        b1 = rect(slide, sx + 0.10, sy + 1.66, sw * 0.44, 0.22, fill=AMBRE, rounded=True, radius=0.4)
        shape_text(b1, "Programme", size=6, color=CHARBON, bold=True)
        b2 = rect(slide, sx + sw * 0.58, sy + 1.66, sw * 0.32, 0.22, fill=None, line=BRAISE, lw=0.75, rounded=True, radius=0.4)
        shape_text(b2, "Billets", size=6, color=BRAISE, bold=True)
        text(slide, sx + 0.10, sy + 2.02, 1.0, 0.16, "À LA UNE", size=5, color=GRIS_C, bold=True)
        for k in range(3):
            rect(slide, sx + 0.10 + k * (sw - 0.20) / 3, sy + 2.22, (sw - 0.30) / 3, 0.52,
                 fill=SABLE, rounded=True, radius=0.08)
        rect(slide, sx + 0.10, sy + 2.90, sw - 0.20, 0.08, fill=blend(GRIS, CREME, 0.7))
        rect(slide, sx + 0.10, sy + 3.05, sw * 0.7, 0.08, fill=blend(GRIS, CREME, 0.7))
        nav = rect(slide, sx, sy + sh - 0.26, sw, 0.26, fill=BLANC)
        for k in range(4):
            oval(slide, sx + 0.18 + k * (sw - 0.36) / 3.2, sy + sh - 0.18, 0.07, 0.07,
                 fill=(BRAISE if k == 0 else blend(GRIS, CREME, 0.55)))

    elif kind == "prog":
        for k in range(3):
            fill = BRAISE if k == 0 else SABLE
            col = BLANC if k == 0 else GRIS
            p = rect(slide, sx + 0.10 + k * 0.44, sy + 0.34, 0.40, 0.19, fill=fill, rounded=True, radius=0.45)
            shape_text(p, ["Ven", "Sam", "Dim"][k], size=5, color=col, bold=True)
        for k in range(4):
            yy = sy + 0.66 + k * 0.78
            rect(slide, sx + 0.10, yy, sw - 0.20, 0.66, fill=WHITEBLOCK, rounded=True, radius=0.07)
            text(slide, sx + 0.17, yy + 0.08, 0.5, 0.16, "17h", size=5.5, color=BRAISE, bold=True)
            rect(slide, sx + 0.17, yy + 0.26, sw * 0.66, 0.07, fill=blend(GRIS, CREME, 0.45))
            rect(slide, sx + 0.17, yy + 0.40, sw * 0.44, 0.06, fill=blend(GRIS, CREME, 0.72))

    else:  # billet
        t = rect(slide, sx + 0.10, sy + 0.36, sw - 0.20, 1.05, fill=CHARBON, rounded=True, radius=0.07)
        text(slide, sx + 0.20, sy + 0.46, 1.4, 0.16, "PASS 18 JOURS", size=5, color=AMBRE, bold=True)
        text(slide, sx + 0.20, sy + 0.64, 1.4, 0.30, "10 000 F", size=13, color=BLANC, bold=True)
        text(slide, sx + 0.20, sy + 1.10, 1.4, 0.16, "accès à toutes les nuits", size=5, color=GRIS_C)
        pay = rect(slide, sx + 0.10, sy + 1.52, sw - 0.20, 0.26, fill=BRAISE, rounded=True, radius=0.35)
        shape_text(pay, "Payer avec Orange Money", size=6, color=BLANC, bold=True)
        pay2 = rect(slide, sx + 0.10, sy + 1.84, sw - 0.20, 0.26, fill=None, line=BRAISE, lw=0.75, rounded=True, radius=0.35)
        shape_text(pay2, "Moov Money", size=6, color=BRAISE, bold=True)
        qr = rect(slide, sx + (sw - 0.62) / 2, sy + 2.28, 0.62, 0.62, fill=BLANC, line=TRAIT, lw=0.75)
        for a in range(5):
            for b in range(5):
                if (a + b) % 2 == 0:
                    rect(slide, qr.left / 914400 + 0.045 + a * 0.105, qr.top / 914400 + 0.045 + b * 0.105,
                         0.085, 0.085, fill=CHARBON)
        text(slide, sx + 0.10, sy + 3.02, sw - 0.20, 0.3, "QR reçu par SMS et WhatsApp",
             size=5.5, color=GRIS, align=PP_ALIGN.CENTER)


WHITEBLOCK = "FFFFFF"


def s06_maquettes(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Aperçu", "Trois écrans, toute l’expérience")

    pw, ph = 2.30, 4.62
    xs = [1.62, 5.52, 9.42]
    labels = [("Accueil", "Le festival, la promesse, deux boutons"),
              ("Programme", "Jour par jour, filtres, ajout au calendrier"),
              ("Billetterie", "Paiement mobile money et QR d’entrée")]
    kinds = ["home", "prog", "billet"]
    for i, kind in enumerate(kinds):
        phone(s, xs[i], 1.72, pw, ph, kind)
        text(s, xs[i] - 0.30, 6.48, pw + 0.60, 0.24, labels[i][0], size=11.5,
             color=CHARBON, bold=True, align=PP_ALIGN.CENTER)
        text(s, xs[i] - 0.34, 6.74, pw + 0.68, 0.22, labels[i][1], size=8,
             color=GRIS, align=PP_ALIGN.CENTER)

    footer(s, 6)
    notes(s, "Ce ne sont pas les vraies maquettes : ce sont des repères de volume. "
             "Le message : le public n’a rien à installer, tout tient sur une page. "
             "Si vous avez une démo cliquable, c’est ici qu’il faut la montrer à la place.")


def s07_pages(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le site public", "Douze pages, une seule promesse : tout trouver en 3 clics")

    pages = [
        ("Accueil", "Compte à rebours, chiffres, 2 boutons"),
        ("Le Festival", "Histoire, mission, édition en cours"),
        ("Programme", "Jour par jour, 7 nuits, filtres"),
        ("Dibi & gastronomie", "Le produit, les grilladiers, la filière"),
        ("Exposants & artisans", "Annuaire, fiches, contact WhatsApp"),
        ("Billetterie", "Pass, mobile money, QR"),
        ("Concours", "Règlement, inscription, vote du public"),
        ("Espace pro", "Stands, artistes, presse, bénévoles"),
        ("Infos pratiques", "Plan, navettes, sécurité, FAQ"),
        ("Média", "Photos, replays, revue de presse"),
        ("Partenaires", "Offres et dossier chiffré"),
        ("Contact", "WhatsApp, newsletter, réseaux"),
    ]
    for i, (t, d) in enumerate(pages):
        x = ML + (i % 3) * 3.87
        y = 1.76 + (i // 3) * 1.13
        rect(s, x, y, 3.72, 1.02, fill=BLANC, rounded=True, radius=0.08)
        rect(s, x, y + 0.16, 0.03, 0.70, fill=AMBRE)
        text(s, x + 0.22, y + 0.19, 3.3, 0.26, t, size=11.5, color=CHARBON, bold=True)
        text(s, x + 0.22, y + 0.50, 3.35, 0.4, d, size=8.5, color=GRIS, spacing=1.0)

    footer(s, 7)
    notes(s, "Ne pas lire les douze lignes. En citer trois : Programme, Billetterie, "
             "Espace pro. Ce sont les seules qui changent vraiment leur travail.")


def s08_billet(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Billetterie", "Du cash au paiement mobile, sans file d’attente")

    text(s, ML, 1.72, 5.0, 0.24, "LES PASS", size=8.5, color=GRIS_C, bold=True)
    pass_ = [("Pass journée", "1 000 – 2 000 F", "accès 1 jour"),
             ("Pass 18 jours", "10 000 – 15 000 F", "toutes les nuits"),
             ("Pass famille", "Tarif dégressif", "2 adultes + 2 enfants"),
             ("VIP / tribune", "Sur devis", "places numérotées")]
    for i, (t, p, d) in enumerate(pass_):
        x = ML + (i % 2) * 2.55
        y = 2.00 + (i // 2) * 1.28
        rect(s, x, y, 2.38, 1.14, fill=BLANC, rounded=True, radius=0.08)
        text(s, x + 0.20, y + 0.18, 2.0, 0.26, t, size=11.5, color=CHARBON, bold=True)
        text(s, x + 0.20, y + 0.50, 2.0, 0.24, p, size=9.5, color=BRAISE)
        text(s, x + 0.20, y + 0.78, 2.0, 0.2, d, size=7.5, color=GRIS_C)

    text(s, ML, 4.72, 5.0, 0.24,
         "Tarifs indicatifs, à valider avec les organisateurs.", size=8, color=GRIS_C, italic=True)

    text(s, 6.20, 1.72, 6.0, 0.24, "LE PARCOURS", size=8.5, color=GRIS_C, bold=True)
    steps = [
        ("01", "Choisit son pass", "Sur le site, en 2 minutes, en français ou en bambara"),
        ("02", "Paie par mobile money", "Orange Money ou Moov Money, sans carte bancaire"),
        ("03", "Reçoit son QR", "Par SMS et WhatsApp — pas besoin de l’imprimer"),
        ("04", "Scanne à l’entrée", "Contrôle même sans réseau, avec synchronisation différée"),
    ]
    for i, (n, t, d) in enumerate(steps):
        y = 2.00 + i * 1.12
        oval(s, 6.20, y + 0.06, 0.36, 0.36, fill=SABLE)
        text(s, 6.20, y + 0.11, 0.36, 0.24, n, size=8.5, color=BRAISE, bold=True, align=PP_ALIGN.CENTER)
        text(s, 6.74, y + 0.02, 5.2, 0.26, t, size=12, color=CHARBON, bold=True)
        text(s, 6.74, y + 0.32, 5.3, 0.5, d, size=9.5, color=GRIS, spacing=1.05)

    band = rect(s, ML, 5.96, CW, 0.62, fill=SABLE, rounded=True, radius=0.10)
    shape_text(band, "Agents de vente terrain équipés  ·  Reversement automatique  ·  "
                     "Journal des ventes consultable en direct",
               size=10, color=BRAISE_D, bold=True)

    footer(s, 8)
    notes(s, "Point délicat : la billetterie suppose une décision politique sur la gratuité. "
             "Proposer un démarrage en « entrée libre + pass premium », qui ne bloque personne "
             "et teste le paiement. Toujours mentionner les agents terrain : c’est ce qui "
             "rassure sur la fraude et sur l’accès des non-connectés.")


def s09_pro(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Espace professionnel", "Leurs 200 dossiers sortent de WhatsApp")

    cols = [
        ("Exposants & grilladiers",
         ["Dossier en ligne", "Devis du stand automatique", "Paiement à la réservation", "Badge et place attribués"]),
        ("Artistes & performers",
         ["Candidature et press-kit", "Validation et contrat", "Ordre de passage", "Accréditations"]),
        ("Presse & partenaires",
         ["Accréditation en ligne", "Kit presse téléchargeable", "Livrables sponsors", "Retombées mesurées"]),
    ]
    for i, (title, items) in enumerate(cols):
        x = ML + i * 3.87
        rect(s, x, 1.78, 3.72, 3.34, fill=BLANC, rounded=True, radius=0.06)
        text(s, x + 0.24, 1.98, 3.3, 0.3, title, size=12, color=BRAISE, bold=True)
        rect(s, x + 0.24, 2.34, 0.5, 0.04, fill=AMBRE)
        for k, it in enumerate(items):
            y = 2.52 + k * 0.68
            text(s, x + 0.24, y, 0.18, 0.24, "·", size=13, color=BRAISE, bold=True)
            text(s, x + 0.42, y, 3.1, 0.5, it, size=10, color=GRIS, spacing=1.05)

    text(s, ML, 5.62, 11.2, 0.7,
         "Effet immédiat : la trésorerie rentre avant le festival, pas trois mois après.",
         size=15, color=CHARBON, bold=True)
    text(s, ML, 6.16, 11.2, 0.3,
         "Aujourd’hui, chaque stand se négocie par téléphone et se paie sur place.",
         size=10.5, color=GRIS)

    footer(s, 9)
    notes(s, "C’est l’argument qui parle le plus aux organisateurs : l’argent. "
             "Un stand payé à la réservation, c’est un stand qui ne se désiste pas "
             "la veille, et une trésorerie qui finance l’installation.")


def s10_jourj(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le jour J", "Le site physique devient lisible")

    tiles = [
        ("Scan QR", "Contrôle des entrées et des accréditations, même hors-ligne"),
        ("Badges", "Exposants, artistes, presse, staff — imprimés depuis le back-office"),
        ("Caisses des stands", "Encaissement mobile money, récapitulatif quotidien"),
        ("Écrans programme", "Pilotés depuis le back-office, pas de PDF à réimprimer"),
        ("Vote du concours", "Un vote par numéro et par jour, traçable et viral"),
        ("QR géant", "Une seule affiche : programme, plan, contacts utiles"),
    ]
    for i, (t, d) in enumerate(tiles):
        x = ML + (i % 3) * 3.87
        y = 1.78 + (i // 3) * 1.72
        rect(s, x, y, 3.72, 1.56, fill=BLANC, rounded=True, radius=0.07)
        text(s, x + 0.24, y + 0.22, 3.2, 0.28, t, size=12.5, color=CHARBON, bold=True)
        text(s, x + 0.24, y + 0.58, 3.25, 0.8, d, size=9.5, color=GRIS, spacing=1.1)

    band = rect(s, ML, 5.94, CW, 0.66, fill=CHARBON, rounded=True, radius=0.10)
    shape_text(band, "Mode dégradé obligatoire : coupure réseau, groupe électrogène, "
                     "listes papier de secours, synchronisation différée",
               size=10.5, color=AMBER_LIGHT, bold=True)

    footer(s, 10)
    notes(s, "Anticiper l’objection : « ici le réseau tombe ». Répondre oui, et c’est "
             "justement pour ça que le scan fonctionne hors-ligne et qu’on garde "
             "des listes papier. Rien ne dépend d’une connexion permanente.")


AMBER_LIGHT = "F0C98A"


def s11_qg(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le Q.G.", "Un tableau de bord, pas un rapport de 40 pages")

    items = [
        "Entrées du jour, heure par heure",
        "Ventes par stand et par catégorie",
        "Dossiers exposants payés ou en attente",
        "Livrables sponsors et contreparties",
        "Incidents, équipes, bénévoles sur site",
        "Export du bilan pour le ministère",
    ]
    for i, it in enumerate(items):
        y = 1.80 + i * 0.60
        text(s, ML, y, 0.2, 0.26, "—", size=10, color=AMBRE, bold=True)
        text(s, ML + 0.28, y - 0.02, 4.3, 0.3, it, size=11, color=GRIS)

    px, py, pw2, ph2 = 5.90, 1.78, 6.70, 4.62
    rect(s, px, py, pw2, ph2, fill=BLANC, rounded=True, radius=0.04)
    rect(s, px + 0.28, py + 0.30, 0.09, 0.09, fill=BRAISE)
    text(s, px + 0.46, py + 0.24, 4.0, 0.2, "APERÇU — DONNÉES D’EXEMPLE", size=7.5,
         color=GRIS_C, bold=True)

    kpis = [("12 480", "entrées du jour"), ("3,2 M", "F de ventes"), ("87 %", "stands payés")]
    for i, (v, l) in enumerate(kpis):
        x = px + 0.28 + i * 2.05
        rect(s, x, py + 0.52, 1.92, 0.86, fill=CREME, rounded=True, radius=0.08)
        text(s, x + 0.16, py + 0.60, 1.7, 0.34, v, size=15, color=CHARBON, bold=True)
        text(s, x + 0.16, py + 0.98, 1.7, 0.24, l, size=8, color=GRIS)

    base_x, base_y, bar_w = px + 0.34, py + 3.86, 0.52
    heights = [0.55, 0.78, 0.92, 1.35, 1.62, 1.48, 1.20]
    days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    for i, (hh, d) in enumerate(zip(heights, days)):
        x = base_x + i * (bar_w + 0.34)
        rect(s, x, base_y - hh, bar_w, hh, fill=(BRAISE if i == 4 else blend(BRAISE, BLANC, 0.62)))
        text(s, x - 0.12, base_y + 0.08, bar_w + 0.24, 0.2, d, size=7, color=GRIS_C, align=PP_ALIGN.CENTER)

    text(s, px + 0.28, py + 4.22, 5.0, 0.24, "Fréquentation par jour", size=7.5, color=GRIS, bold=True)

    footer(s, 11)
    notes(s, "C’est ce que vous montrez au ministère et aux sponsors. "
             "Un sponsor qui voit son logo et ses chiffres en direct renouvelle. "
             "Un ministère qui reçoit un bilan chiffré vous rappelle l’année suivante.")


def s12_roi(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le retour", "Ce que la plateforme rapporte, en francs")

    rows = [
        ["Levier", "Hypothèse prudente", "Impact"],
        ["Billetterie digitale", "10 % de 200 000 visiteurs à 1 000 F", "20 M F"],
        ["Inscriptions des stands", "200 stands × 50 000 F, payés d’avance", "10 M F"],
        ["Sponsoring digital", "+ 30 % sur un budget sponsor de 30 M F", "+ 9 M F"],
        ["E-commerce diaspora", "Ventes de produits du terroir toute l’année", "2 M F"],
        ["Total", "", "≈ 41 M F"],
    ]
    tbl = table(s, ML, 1.80, [3.30, 5.60, 2.90], rows, [0.48, 0.62, 0.62, 0.62, 0.62, 0.64])
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            is_head = i == 0
            is_total = i == len(rows) - 1
            if is_head:
                fill, col = CHARBON, BLANC
            elif is_total:
                fill, col = SABLE, BRAISE_D
            else:
                fill, col = (BLANC if i % 2 else CREME), (CHARBON if j == 0 else GRIS)
            if is_total and j == 2:
                fill, col = BRAISE, BLANC
            set_cell(tbl.cell(i, j), val, size=(10 if not is_head else 9.5) if not is_total else 11.5,
                     color=col, bold=(is_head or is_total or j == 0), fill=fill,
                     align=PP_ALIGN.RIGHT if j == 2 else PP_ALIGN.LEFT)

    text(s, ML, 5.52, 11.2, 0.34,
         "Coût de la plateforme : 5 à 8 M F. L’investissement est couvert par la seule billetterie.",
         size=13, color=CHARBON, bold=True)
    text(s, ML, 5.96, 11.0, 0.5,
         "Ordres de grandeur, à recalibrer avec vos chiffres réels. Les tarifs de billetterie "
         "restent une décision des organisateurs.", size=9, color=GRIS_C, spacing=1.1)

    footer(s, 12)
    notes(s, "Ne pas défendre ces chiffres comme des promesses : les présenter comme "
             "un ordre de grandeur à valider ensemble. La question à poser : "
             "« combien de stands payez-vous réellement aujourd’hui, et quand ? »")


def s13_terrain(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Contexte malien", "Conçu pour le terrain, pas pour la vitrine")

    cards = [
        ("Réseau 3G", "Site sous 1 Mo, images sous 100 Ko, chargement en moins de 3 s"),
        ("WhatsApp d’abord", "Chaque page et chaque billet partageable en un clic"),
        ("Hors-ligne", "Programme et scan QR disponibles sans réseau"),
        ("Trois langues", "Français, bambara, anglais pour la diaspora"),
        ("Mobile money", "Orange Money et Moov Money, sans carte bancaire"),
        ("Données protégées", "Loi 2013-015 : consentement, mentions, APDP"),
        ("Terrain", "Écrans, badges, agents équipés, listes de secours"),
        ("Toute l’année", "Le site vit après le festival : médias, bilan, édition suivante"),
    ]
    for i, (t, d) in enumerate(cards):
        x = ML + (i % 4) * 2.98
        y = 1.85 + (i // 4) * 1.90
        rect(s, x, y, 2.80, 1.62, fill=BLANC, rounded=True, radius=0.07)
        text(s, x + 0.22, y + 0.22, 2.35, 0.28, t, size=11, color=BRAISE, bold=True)
        text(s, x + 0.22, y + 0.60, 2.38, 0.9, d, size=9, color=GRIS, spacing=1.12)

    text(s, ML, 6.02, 11.3, 0.5,
         "Aucune de ces contraintes n’est un détail : ce sont elles qui font la différence "
         "entre un site qui sert et un site qui décore.",
         size=11.5, color=CHARBON, bold=True, spacing=1.1)

    footer(s, 13)
    notes(s, "C’est la diapositive qui prouve que vous connaissez le terrain. "
             "La citer avant qu’on vous pose la question du réseau vous fait gagner "
             "toute la crédibilité de la réunion.")


def s14_scenarios(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Démarrage", "Deux façons de lancer le projet")

    cards = [
        ("A", "Pilote sur l’édition en cours", "4 semaines", False,
         ["Vitrine, programme, inscriptions stands", "Paiement en ligne des stands",
          "Partage WhatsApp et collecte des contacts"],
         "Objectif : prouver l’usage et ramener les premiers chiffres."),
        ("B", "Plateforme complète", "3 à 4 mois", True,
         ["Les quatre briques, billetterie et QR", "Terrain, badges, caisses, votes",
          "Q.G., reporting sponsors, bilan chiffré"],
         "Objectif : des recettes traçables et un dossier sponsor solide."),
    ]
    for i, (letter, title, delay, reco, items, goal) in enumerate(cards):
        x = ML + i * 6.08
        rect(s, x, 1.78, 5.72, 4.08, fill=(CHARBON if reco else BLANC), rounded=True, radius=0.05)
        base = BLANC if reco else CHARBON
        muted = blend(SABLE, CHARBON, 0.25) if reco else GRIS
        text(s, x + 0.30, 2.02, 1.0, 0.24, letter, size=10, color=AMBRE, bold=True)
        text(s, x + 0.30, 2.30, 4.6, 0.3, title, size=16, color=base, bold=True)
        text(s, x + 0.30, 2.68, 3.0, 0.24, delay, size=9.5, color=AMBRE, bold=True)
        if reco:
            tag = rect(s, x + 4.10, 2.04, 1.34, 0.30, fill=BRAISE, rounded=True, radius=0.5)
            shape_text(tag, "RECOMMANDÉ", size=6.5, color=BLANC, bold=True)
        for k, it in enumerate(items):
            y = 3.16 + k * 0.62
            text(s, x + 0.30, y, 0.2, 0.24, "·", size=13, color=AMBRE, bold=True)
            text(s, x + 0.50, y, 4.9, 0.42, it, size=9.5, color=muted, spacing=1.05)
        rect(s, x + 0.30, 4.98, 5.10, 0.008,
             fill=(blend(BLANC, CHARBON, 0.82) if reco else TRAIT))
        text(s, x + 0.30, 5.14, 5.05, 0.6, goal, size=9,
             color=(SABLE if reco else GRIS), spacing=1.15)

    text(s, ML, 6.34, CW, 0.4,
         "Mon conseil : démarrer par le pilote, et réserver la plateforme complète à l’édition "
         "suivante — avec les chiffres du pilote comme argument.",
         size=10.5, color=BRAISE_D, bold=True, spacing=1.1)

    footer(s, 14)
    notes(s, "Être honnête sur le calendrier : on est début novembre, un projet complet "
             "ne tient pas avant le 18 décembre. Proposer le pilote, c’est montrer "
             "qu’on connaît la contrainte — et ça ouvre la porte au contrat suivant.")


def s15_budget(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Budget", "Trois formules, un seul prestataire")

    rows = [
        ["Formule", "Contenu", "Délai", "Budget"],
        ["Essentiel", "Vitrine, programme, inscription des stands", "4 – 6 sem.", "2,5 – 4 M F"],
        ["Standard", "+ billetterie, back-office, tableau de bord", "8 – 12 sem.", "5 – 8 M F"],
        ["Complet", "+ terrain, votes, e-commerce, data", "4 – 5 mois", "8 – 11 M F"],
    ]
    tbl = table(s, ML, 1.80, [2.10, 5.90, 1.75, 2.10], rows, [0.46, 0.62, 0.62, 0.62])
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            is_head = i == 0
            if is_head:
                fill, col = CHARBON, BLANC
            else:
                fill, col = (BLANC if i % 2 else CREME), (CHARBON if j == 0 else GRIS)
            if i == 2 and not is_head:
                fill = SABLE
                col = BRAISE_D if j == 3 else (CHARBON if j == 0 else GRIS)
            set_cell(tbl.cell(i, j), val, size=10 if not is_head else 9.5, color=col,
                     bold=(is_head or j == 0 or (i == 2 and j == 3)), fill=fill,
                     align=PP_ALIGN.RIGHT if j == 3 else PP_ALIGN.LEFT)

    text(s, ML, 4.30, 11.2, 0.24, "CE QUI EST INCLUS DANS CHAQUE FORMULE", size=8.5,
         color=GRIS_C, bold=True)
    included = ["Design et développement", "Contenu et textes", "Formation des équipes",
                "Hébergement et nom de domaine", "Support pendant le festival"]
    for i, it in enumerate(included):
        text(s, ML + (i % 3) * 3.87, 4.62 + (i // 3) * 0.34, 0.2, 0.24, "—", size=9, color=AMBRE, bold=True)
        text(s, ML + (i % 3) * 3.87 + 0.26, 4.62 + (i // 3) * 0.34, 3.4, 0.26, it, size=9.5, color=GRIS)

    rect(s, ML, 5.56, CW, 0.78, fill=SABLE, rounded=True, radius=0.10)
    text(s, ML + 0.28, 5.72, 11.2, 0.24,
         "Récurrent : hébergement et domaine 200 – 400 k F / an  ·  maintenance 10 – 15 % par an",
         size=10, color=BRAISE_D, bold=True)
    text(s, ML + 0.28, 6.00, 11.2, 0.24,
         "Paiement échelonné possible : 40 % à la commande, 30 % à la recette, 30 % à la mise en ligne.",
         size=9, color=GRIS)

    footer(s, 15)
    notes(s, "Ne jamais donner un prix unique. Trois formules = on choisit au lieu de dire non. "
             "La formule Standard est celle à pousser : elle contient la billetterie, "
             "donc elle se rembourse.")


def s16_fin(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, CHARBON)

    text(s, ML, 0.52, 6.0, 0.24, "PROCHAINES ÉTAPES", size=9.5, color=AMBRE, bold=True)
    text(s, ML, 0.80, 10.5, 0.7, "Quatre étapes, trois semaines", size=30, color=BLANC, bold=True)
    rect(s, ML, 1.50, 0.85, 0.045, fill=AMBRE)

    steps = [
        ("01", "Validation du principe", "Cette semaine"),
        ("02", "Atelier de cadrage (2 h) avec l’équipe et le ministère", "Semaine du 9 novembre"),
        ("03", "Maquette et devis ferme", "15 novembre"),
        ("04", "Démarrage du pilote", "17 novembre"),
    ]
    for i, (n, t, d) in enumerate(steps):
        y = 2.10 + i * 0.90
        text(s, ML, y, 0.5, 0.26, n, size=10, color=AMBRE, bold=True)
        text(s, ML + 0.60, y - 0.04, 7.4, 0.4, t, size=12.5, color=BLANC, bold=True)
        text(s, 9.30, y - 0.02, 3.3, 0.3, d, size=9.5, color=blend(SABLE, CHARBON, 0.35))
        if i < 3:
            rect(s, ML, y + 0.60, CW, 0.006, fill=blend(SABLE, CHARBON, 0.78))

    text(s, ML, 5.78, 8.6, 0.7,
         "Le festival a 200 000 visiteurs. Il lui manque 200 000 contacts,\n"
         "200 stands payés d’avance et un bilan chiffré à présenter.",
         size=12, color=SABLE, italic=True, font=SERIF, spacing=1.15)
    text(s, ML, 6.54, 8.0, 0.3, "Merci de votre attention.", size=10, color=AMBRE, bold=True)

    rect(s, 9.55, 5.74, 3.05, 1.06, fill=blend(BLANC, CHARBON, 0.9), rounded=True, radius=0.08)
    text(s, 9.78, 5.86, 2.7, 0.22, "VOTRE CONTACT", size=7, color=AMBRE, bold=True)
    text(s, 9.78, 6.08, 2.7, 0.24, "Nom · Fonction", size=9, color=BLANC, bold=True)
    text(s, 9.78, 6.32, 2.7, 0.24, "+223 ···  ···  ···", size=8.5, color=blend(SABLE, CHARBON, 0.25))
    text(s, 9.78, 6.54, 2.7, 0.22, "email@domaine.ml", size=8.5, color=blend(SABLE, CHARBON, 0.25))

    notes(s, "Terminer par une demande claire et datée : un atelier de cadrage de deux heures. "
             "Ne pas demander « une décision » tout de suite, demander un rendez-vous de travail. "
             "Laisser le dossier, et proposer de revenir avec la maquette.")


def build(path):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    for fn in (s01_cover, s02_chiffres, s03_constat, s04_reponse, s05_archi,
               s06_maquettes, s07_pages, s08_billet, s09_pro, s10_jourj,
               s11_qg, s12_roi, s13_terrain, s14_scenarios, s15_budget, s16_fin):
        fn(prs)

    cp = prs.core_properties
    cp.title = "Festival du Dibi — La plateforme digitale officielle"
    cp.subject = "Dossier de présentation — application web de l'événement"
    cp.author = "Dossier de présentation"
    cp.keywords = "Festi Dibi, Mali, Bamako, festival, plateforme, billetterie"
    cp.category = "Proposition"

    prs.save(path)
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "Festival_Dibi_Dossier.pptx")
    print(build(out))
