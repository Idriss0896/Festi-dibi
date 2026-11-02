#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dossier de presentation simplifie — Festi Dibi (11 slides, gros caracteres)."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

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
    ca = tuple(int(a[i:i + 2], 16) for i in (0, 2, 4))
    cb = tuple(int(b[i:i + 2], 16) for i in (0, 2, 4))
    return "".join("%02X" % int(round(x + (y - x) * t)) for x, y in zip(ca, cb))


def _clean(s):
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


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0, rounded=False, radius=0.08):
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


def oval(slide, x, y, w, h, fill=None, line=None, lw=1.5):
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


def text(slide, x, y, w, h, s, size=18, color=CHARBON, bold=False, font=FONT,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=None,
         italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, line in enumerate(s.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing:
            p.line_spacing = spacing
        r = p.add_run()
        r.text = line
        f = r.font
        f.name = font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = rgb(color)
    return tb


def shape_text(shape, s, size=12, color=BLANC, bold=True, font=FONT, align=PP_ALIGN.CENTER):
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


def header(slide, kicker, title, size=38):
    text(slide, ML, 0.46, CW, 0.3, kicker.upper(), size=12, color=BRAISE, bold=True)
    text(slide, ML, 0.80, CW, 0.9, title, size=size, color=CHARBON, bold=True, spacing=0.95)
    rect(slide, ML, 1.82, 1.0, 0.05, fill=AMBRE)


def footer(slide, n, label="Festival du Dibi  ·  Le site web du festival"):
    rect(slide, ML, 6.94, CW, 0.01, fill=TRAIT)
    text(slide, ML, 7.06, 8.0, 0.2, label, size=10, color=GRIS_C)
    text(slide, 11.3, 7.06, 1.28, 0.2, "%02d" % n, size=10, color=GRIS_C, align=PP_ALIGN.RIGHT)


def notes(slide, s):
    slide.notes_slide.notes_text_frame.text = s


def pill(slide, x, y, s, size=16, fill=SABLE, color=BRAISE_D, h=0.56):
    wd = 0.50 + len(s) * 0.115 * (size / 16.0)
    shp = rect(slide, x, y, wd, h, fill=fill, rounded=True, radius=0.5)
    shape_text(shp, s, size=size, color=color, bold=True)
    return x + wd


# ------------------------------------------------------------------ slides
def s01(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, CHARBON)

    for (x, y, d) in ((9.0, -2.2, 7.8), (10.4, 1.9, 5.6), (11.7, 4.8, 3.4)):
        oval(s, x, y, d, d, fill=None, line=blend(BRAISE, CHARBON, 0.55), lw=1.5)

    rect(s, 0, 0, 0.18, H, fill=BRAISE)

    mark = rect(s, 0.95, 0.85, 0.75, 0.75, fill=BRAISE, rounded=True, radius=0.18)
    shape_text(mark, "FD", size=19, color=BLANC, bold=True)

    text(s, 0.95, 2.00, 8.0, 0.3, "DOSSIER DE PRÉSENTATION  ·  NOVEMBRE 2026",
         size=12, color=AMBRE, bold=True)

    text(s, 0.95, 2.40, 9.8, 1.1, "Festival du Dibi", size=64, color=BLANC, bold=True, spacing=0.9)
    text(s, 0.95, 3.55, 9.8, 0.7, "Le site web du festival", size=34, color=SABLE, spacing=0.95)

    rect(s, 0.95, 4.45, 1.2, 0.06, fill=AMBRE)

    x = 0.95
    for lab in ("Stands", "Programme", "Billets", "Photos"):
        x = pill(s, x, 4.75, lab, size=16,
                 fill=blend(BRAISE, CHARBON, 0.35), color=SABLE) + 0.22

    text(s, 0.95, 6.45, 10.6, 0.3,
         "Bamako  ·  Place du Cinquantenaire  ·  18 jours  ·  200 000 visiteurs",
         size=14, color=blend(SABLE, CHARBON, 0.35))

    notes(s, "Une phrase d'ouverture : « Aujourd'hui, tout passe par WhatsApp et Facebook. "
             "Je vous propose un site unique qui fait quatre choses, et rien de plus. »")


def s02(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le point de départ", "Le festival en trois chiffres")

    text(s, ML, 2.30, 7.4, 1.45, "200 000", size=84, color=BRAISE, bold=True, spacing=0.9)
    text(s, ML, 3.85, 7.0, 0.55, "visiteurs", size=30, color=CHARBON, bold=True)
    text(s, ML, 4.45, 6.6, 0.9, "en 18 jours non-stop,\nplace du Cinquantenaire",
         size=17, color=GRIS, spacing=1.15)

    stats = [("11", "éditions"), ("200+", "stands"), ("7", "nuits thématiques")]
    for i, (v, l) in enumerate(stats):
        y = 2.32 + i * 1.05
        text(s, 8.55, y, 1.9, 0.55, v, size=30, color=CHARBON, bold=True)
        text(s, 10.55, y + 0.14, 2.0, 0.35, l, size=15, color=GRIS)
        if i < 2:
            rect(s, 8.55, y + 0.90, 4.0, 0.01, fill=TRAIT)

    rect(s, ML, 5.65, CW, 0.012, fill=TRAIT)
    text(s, ML, 5.85, 11.4, 0.5,
         "Le plus grand rendez-vous de la gastronomie malienne et africaine.",
         size=20, color=CHARBON, bold=True)
    text(s, ML, 6.45, 11.4, 0.3,
         "Sous le haut parrainage du Président de la Transition  ·  Ministère de l’Élevage et de la Pêche",
         size=12, color=GRIS_C)

    footer(s, 2)
    notes(s, "Trois chiffres, un point. Ne pas s'attarder : c'est juste pour montrer qu'on "
             "a lu le dossier du festival.")


def s03(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le constat", "Aujourd’hui, tout passe par WhatsApp")

    rows = [
        ("Les dossiers de stands arrivent par messages",
         "Doublons, places perdues, paiements jamais suivis."),
        ("Les billets se vendent en espèces",
         "Aucune trace des entrées, files d’attente aux portes."),
        ("Le programme et les photos vivent sur Facebook",
         "Ils disparaissent dans le fil, et personne ne les retrouve."),
    ]
    for i, (a, b) in enumerate(rows):
        y = 2.15 + i * 1.30
        text(s, ML, y + 0.04, 0.6, 0.4, "0%d" % (i + 1), size=15, color=AMBRE, bold=True)
        text(s, ML + 0.75, y, 9.6, 0.45, a, size=24, color=CHARBON, bold=True, spacing=1.05)
        text(s, ML + 0.75, y + 0.52, 9.6, 0.4, b, size=16, color=GRIS)
        if i < 2:
            rect(s, ML, y + 1.10, CW, 0.01, fill=TRAIT)

    text(s, ML, 6.20, 11.4, 0.45,
         "Et le 5 janvier, il ne reste rien.", size=19, color=BRAISE_D, bold=True)

    footer(s, 3)
    notes(s, "Ne pas accuser. Constater. La derniere phrase est celle qui compte : "
             "c'est elle qui justifie un site qui reste toute l'annee.")


def s04(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "La proposition", "Quatre fonctions, c’est tout")

    cards = [
        ("01", "Demander un stand", "Le dossier en ligne, en 5 minutes."),
        ("02", "Voir le programme", "Les 18 jours, nuit par nuit."),
        ("03", "Acheter un billet", "Orange Money ou Moov Money."),
        ("04", "Voir les photos", "La galerie, classée par édition."),
    ]
    for i, (num, title, desc) in enumerate(cards):
        x = ML + (i % 2) * 6.08
        y = 2.10 + (i // 2) * 2.15
        rect(s, x, y, 5.72, 1.95, fill=BLANC, rounded=True, radius=0.06)
        text(s, x + 0.34, y + 0.28, 0.6, 0.3, num, size=13, color=AMBRE, bold=True)
        text(s, x + 0.34, y + 0.62, 5.0, 0.5, title, size=27, color=CHARBON, bold=True)
        text(s, x + 0.34, y + 1.22, 5.0, 0.4, desc, size=17, color=GRIS, spacing=1.1)

    footer(s, 4)
    notes(s, "C'est la diapositive centrale. Si on ne retient qu'une chose, c'est celle-la. "
             "Répéter : « quatre fonctions, pas trente ».")


def s05(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Fonction 1", "Demander un stand, en 3 étapes")

    cx = [2.45, 6.55, 10.65]
    rect(s, cx[0] + 0.42, 2.62, cx[2] - cx[0] - 0.84, 0.02, fill=TRAIT)

    steps = [
        ("1", "Il remplit le dossier", "Nom, activité, type de stand, photo. Depuis son téléphone."),
        ("2", "Il paie en ligne", "Orange Money ou Moov Money. Sa place est réservée."),
        ("3", "Il reçoit son badge", "Confirmation et QR code par WhatsApp. Entrée sans file."),
    ]
    for i, (n, t, d) in enumerate(steps):
        oval(s, cx[i] - 0.42, 2.20, 0.84, 0.84, fill=BRAISE)
        text(s, cx[i] - 0.42, 2.40, 0.84, 0.45, n, size=24, color=BLANC, bold=True,
             align=PP_ALIGN.CENTER)
        text(s, cx[i] - 1.75, 3.32, 3.50, 0.45, t, size=21, color=CHARBON, bold=True,
             align=PP_ALIGN.CENTER)
        text(s, cx[i] - 1.65, 3.85, 3.30, 1.0, d, size=15, color=GRIS, align=PP_ALIGN.CENTER,
             spacing=1.15)

    band = rect(s, ML, 5.35, CW, 1.0, fill=SABLE, rounded=True, radius=0.12)
    shape_text(band, "Résultat : la trésorerie rentre avant le festival, pas trois mois après.",
               size=18, color=BRAISE_D, bold=True)

    footer(s, 5)
    notes(s, "C'est l'argument qui parle le plus aux organisateurs : l'argent. "
             "Un stand payé à la réservation ne se désiste pas la veille.")


def s06(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Fonction 2", "Le programme, jour par jour")

    items = [
        ("Les 18 jours", "Une page par jour, du 18 décembre au 4 janvier."),
        ("Les 7 nuits thématiques", "Chaque soirée, son invité et son horaire."),
        ("Toujours à jour", "Modifié sur place, visible en ligne dans la minute."),
    ]
    for i, (t, d) in enumerate(items):
        y = 2.15 + i * 1.05
        rect(s, ML, y + 0.10, 0.05, 0.62, fill=AMBRE)
        text(s, ML + 0.28, y, 5.3, 0.4, t, size=20, color=CHARBON, bold=True)
        text(s, ML + 0.28, y + 0.44, 5.2, 0.5, d, size=15, color=GRIS, spacing=1.1)

    days = [
        ("18", "DÉC", "Nuit d’ouverture", "Concerts · 20h · Grande scène"),
        ("24", "DÉC", "Nuit de Noël", "Arbre géant · cadeaux aux enfants"),
        ("31", "DÉC", "Nuit du réveillon", "Dibi géant · DJ · feu d’artifice"),
    ]
    for i, (d, m, t, sub) in enumerate(days):
        y = 2.05 + i * 1.55
        rect(s, 6.35, y, 6.20, 1.35, fill=BLANC, rounded=True, radius=0.08)
        text(s, 6.60, y + 0.26, 1.0, 0.5, d, size=30, color=BRAISE, bold=True)
        text(s, 6.60, y + 0.78, 1.0, 0.3, m, size=12, color=GRIS_C, bold=True)
        rect(s, 7.70, y + 0.25, 0.015, 0.85, fill=TRAIT)
        text(s, 8.00, y + 0.30, 4.3, 0.4, t, size=19, color=CHARBON, bold=True)
        text(s, 8.00, y + 0.75, 4.3, 0.35, sub, size=13, color=GRIS)

    footer(s, 6)
    notes(s, "La question à poser : « combien de personnes vous demandent encore le "
             "programme par téléphone pendant le festival ? »")


def s07(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Fonction 3", "Le billet, depuis son téléphone")

    passes = [("Pass journée", "1 000 F"), ("Pass 18 jours", "10 000 F"), ("Pass famille", "25 000 F")]
    for i, (t, p) in enumerate(passes):
        y = 2.20 + i * 1.05
        text(s, ML, y, 3.4, 0.45, t, size=21, color=CHARBON, bold=True)
        text(s, ML + 3.5, y, 2.2, 0.45, p, size=21, color=BRAISE, bold=True, align=PP_ALIGN.RIGHT)
        rect(s, ML, y + 0.60, 5.75, 0.012, fill=TRAIT)

    text(s, ML, 5.50, 5.8, 0.4, "Orange Money  ·  Moov Money", size=17, color=CHARBON, bold=True)
    text(s, ML, 5.95, 5.8, 0.8,
         "Le billet arrive par SMS et WhatsApp.\nUn QR code suffit à l’entrée.",
         size=15, color=GRIS, spacing=1.2)

    px, py, pw, ph = 7.95, 1.98, 2.70, 4.70
    rect(s, px, py, pw, ph, fill=CHARBON, rounded=True, radius=0.10)
    sx, sy, sw, sh = px + 0.10, py + 0.14, pw - 0.20, ph - 0.28
    rect(s, sx, sy, sw, sh, fill=CREME, rounded=True, radius=0.03)

    bar = rect(s, sx, sy, sw, 0.30, fill=CHARBON)
    shape_text(bar, "FESTI DIBI", size=8, color=AMBRE, bold=True, align=PP_ALIGN.LEFT)
    bar.text_frame.margin_left = Inches(0.12)

    t1 = rect(s, sx + 0.12, sy + 0.45, sw - 0.24, 1.15, fill=CHARBON, rounded=True, radius=0.08)
    text(s, sx + 0.24, sy + 0.56, 1.6, 0.2, "PASS 18 JOURS", size=6.5, color=AMBRE, bold=True)
    text(s, sx + 0.24, sy + 0.78, 1.8, 0.35, "10 000 F", size=16, color=BLANC, bold=True)
    text(s, sx + 0.24, sy + 1.30, 1.8, 0.2, "toutes les nuits", size=6.5, color=GRIS_C)

    b1 = rect(s, sx + 0.12, sy + 1.78, sw - 0.24, 0.32, fill=BRAISE, rounded=True, radius=0.4)
    shape_text(b1, "Payer avec Orange Money", size=7, color=BLANC, bold=True)
    b2 = rect(s, sx + 0.12, sy + 2.18, sw - 0.24, 0.32, fill=None, line=BRAISE, lw=1.0,
              rounded=True, radius=0.4)
    shape_text(b2, "Moov Money", size=7, color=BRAISE, bold=True)

    qx, qy, qd = sx + (sw - 0.85) / 2, sy + 2.75, 0.85
    rect(s, qx, qy, qd, qd, fill=BLANC, line=TRAIT, lw=1.0)
    for a in range(5):
        for b in range(5):
            if (a + b) % 2 == 0:
                rect(s, qx + 0.06 + a * 0.148, qy + 0.06 + b * 0.148, 0.115, 0.115, fill=CHARBON)

    text(s, sx + 0.12, sy + 3.75, sw - 0.24, 0.4, "QR reçu par SMS\net WhatsApp",
         size=7.5, color=GRIS, align=PP_ALIGN.CENTER, spacing=1.2)

    footer(s, 7)
    notes(s, "Préciser que le paiement mobile money est déjà dans les usages : "
             "on ne demande à personne d'ouvrir un compte bancaire.")


def s08(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Fonction 4", "Les photos du festival")

    text(s, ML, 2.15, 4.5, 1.9,
         "Chaque édition laisse des milliers d’images.\nAujourd’hui, elles se perdent dans "
         "les téléphones et les fils Facebook.",
         size=17, color=GRIS, spacing=1.25)

    for i, t in enumerate(["Classées par année", "Téléchargeables par la presse",
                           "Alimentées par les visiteurs"]):
        y = 4.35 + i * 0.55
        text(s, ML, y, 0.25, 0.3, "—", size=15, color=AMBRE, bold=True)
        text(s, ML + 0.32, y, 4.3, 0.35, t, size=15, color=CHARBON, bold=True)

    tiles = [("2025", blend(BRAISE, CREME, 0.60)), ("2024", blend(AMBRE, CREME, 0.55)),
             ("2023", blend(CHARBON, CREME, 0.86)), ("2025", blend(BRAISE, CREME, 0.40)),
             ("2024", SABLE), ("2022", blend(AMBRE, CREME, 0.78))]
    tw, th, gap = 2.20, 1.95, 0.18
    for i, (lab, col) in enumerate(tiles):
        x = 5.55 + (i % 3) * (tw + gap)
        y = 2.05 + (i // 3) * (th + gap)
        rect(s, x, y, tw, th, fill=col, rounded=True, radius=0.05)
        ic = blend(col, CHARBON, 0.34)
        oval(s, x + tw * 0.60, y + th * 0.24, tw * 0.13, tw * 0.13, fill=ic)
        tri = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,
                                 Inches(x + tw * 0.15), Inches(y + th * 0.34),
                                 Inches(tw * 0.70), Inches(th * 0.34))
        tri.fill.solid()
        tri.fill.fore_color.rgb = rgb(ic)
        tri.line.fill.background()
        _clean(tri)
        text(s, x + 0.18, y + th - 0.42, 1.2, 0.28, lab, size=12, color=CHARBON, bold=True)

    footer(s, 8)
    notes(s, "Le point stratégique : ce sont ces photos qui font revenir les sponsors "
             "et qui prouvent l'ampleur de l'événement d'une année sur l'autre.")


def s09(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "La technique", "Un site web, pas une application")

    text(s, ML, 2.10, 11.3, 0.8,
         "Rien à télécharger. On ouvre un lien, et tout est là.",
         size=22, color=GRIS, spacing=1.1)

    pts = [
        ("Il s’ouvre partout", "Sur n’importe quel téléphone, même ancien."),
        ("Il s’installe", "Sur l’écran d’accueil, comme une application."),
        ("Il marche sans réseau", "Le programme reste lisible hors connexion."),
    ]
    for i, (t, d) in enumerate(pts):
        x = ML + i * 3.95
        rect(s, x, 3.20, 3.70, 1.85, fill=BLANC, rounded=True, radius=0.08)
        text(s, x + 0.30, 3.45, 3.1, 0.4, t, size=19, color=CHARBON, bold=True)
        text(s, x + 0.30, 3.95, 3.1, 0.8, d, size=15, color=GRIS, spacing=1.15)

    band = rect(s, ML, 5.45, CW, 0.95, fill=CHARBON, rounded=True, radius=0.12)
    shape_text(band, "Coût d’une application à télécharger : trois fois plus cher, pour dix fois moins d’utilisateurs.",
               size=16, color=AMBRE, bold=True)

    footer(s, 9)
    notes(s, "Si on vous demande « et l'application ? », répondre : c'est le même produit, "
             "sans les frais de store et sans le téléchargement.")


def s10(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, "Le cadre", "Le prix et le délai")

    cards = [
        ("A", "Pour cette édition", "4 semaines", "2,5 – 4 M F", False,
         ["Les 4 fonctions du site", "Photos et programme en ligne", "Formation de l’équipe"]),
        ("B", "Pour l’édition suivante", "8 – 10 semaines", "5 – 8 M F", True,
         ["Tout, + billetterie et QR", "Tableau de bord organisateur", "Suivi des stands et des paiements"]),
    ]
    for i, (letter, title, delay, price, reco, items) in enumerate(cards):
        x = ML + i * 6.08
        rect(s, x, 2.05, 5.72, 3.55, fill=(CHARBON if reco else BLANC), rounded=True, radius=0.05)
        base = BLANC if reco else CHARBON
        muted = blend(SABLE, CHARBON, 0.30) if reco else GRIS
        text(s, x + 0.34, 2.28, 0.6, 0.3, letter, size=13,
             color=(AMBRE if reco else BRAISE), bold=True)
        text(s, x + 0.34, 2.60, 4.9, 0.4, title, size=20, color=base, bold=True)
        text(s, x + 0.34, 3.10, 2.4, 0.5, delay, size=15,
             color=(AMBRE if reco else BRAISE), bold=True)
        text(s, x + 0.34, 3.45, 4.9, 0.6, price, size=30, color=(AMBRE if reco else BRAISE), bold=True)
        for k, it in enumerate(items):
            yy = 4.20 + k * 0.44
            text(s, x + 0.34, yy, 0.2, 0.3, "·", size=17,
                 color=(AMBRE if reco else BRAISE), bold=True)
            text(s, x + 0.58, yy, 4.8, 0.35, it, size=15, color=muted)
        if reco:
            tag = rect(s, x + 4.10, 2.26, 1.32, 0.32, fill=BRAISE, rounded=True, radius=0.5)
            shape_text(tag, "RECOMMANDÉ", size=7, color=BLANC, bold=True)

    text(s, ML, 5.95, 11.3, 0.35,
         "Hébergement et nom de domaine : 200 – 400 k F par an.",
         size=14, color=GRIS)

    footer(s, 10)
    notes(s, "Toujours deux options, jamais un prix unique : on choisit au lieu de refuser.")


def s11(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s, CHARBON)

    text(s, ML, 0.55, 6.0, 0.3, "PROCHAINES ÉTAPES", size=12, color=AMBRE, bold=True)
    text(s, ML, 0.88, 10.5, 0.9, "On commence quand ?", size=40, color=BLANC, bold=True)
    rect(s, ML, 1.82, 1.0, 0.05, fill=AMBRE)

    steps = [
        ("01", "Un atelier de 2 heures", "Cette semaine"),
        ("02", "La maquette et le devis", "Sous 10 jours"),
        ("03", "Le site en ligne", "Avant le 18 décembre"),
    ]
    for i, (n, t, d) in enumerate(steps):
        y = 2.35 + i * 1.05
        text(s, ML, y, 0.7, 0.4, n, size=14, color=AMBRE, bold=True)
        text(s, ML + 0.75, y - 0.05, 6.8, 0.45, t, size=21, color=BLANC, bold=True)
        text(s, 8.20, y, 4.2, 0.35, d, size=15, color=blend(SABLE, CHARBON, 0.30))
        if i < 2:
            rect(s, ML, y + 0.72, CW, 0.008, fill=blend(SABLE, CHARBON, 0.80))

    text(s, ML, 5.75, 8.4, 0.8,
         "Le festival a 200 000 visiteurs.\nIl lui manque un site qui les garde.",
         size=17, color=SABLE, italic=True, font=SERIF, spacing=1.25)

    rect(s, 9.55, 5.60, 3.05, 1.15, fill=blend(BLANC, CHARBON, 0.90), rounded=True, radius=0.10)
    text(s, 9.78, 5.74, 2.7, 0.24, "VOTRE CONTACT", size=8, color=AMBRE, bold=True)
    text(s, 9.78, 5.98, 2.7, 0.28, "Nom · Fonction", size=11, color=BLANC, bold=True)
    text(s, 9.78, 6.26, 2.7, 0.26, "+223 ···  ···  ···", size=10, color=blend(SABLE, CHARBON, 0.25))
    text(s, 9.78, 6.50, 2.7, 0.26, "email@domaine.ml", size=10, color=blend(SABLE, CHARBON, 0.25))

    notes(s, "Terminer par une demande précise et datée : un atelier de deux heures. "
             "Pas « une décision », un rendez-vous de travail.")


def build(path):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    for fn in (s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11):
        fn(prs)

    cp = prs.core_properties
    cp.title = "Festival du Dibi — Le site web du festival"
    cp.subject = "Dossier de présentation du projet"
    cp.author = "Dossier de présentation"
    cp.keywords = "Festi Dibi, Mali, Bamako, festival, site web, billetterie"
    prs.save(path)
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Festival_Dibi_Presentation.pptx")
    print(build(out))
