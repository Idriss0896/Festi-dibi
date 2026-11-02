# Festival du Dibi — site officiel

Site web (PWA) du **Festival du Dibi**, le premier festival gastronomique
d'Afrique de l'Ouest. Bamako, Mali.

## Contenu

| Dossier | Rôle |
|---|---|
| 	pwa/ | Le site complet (HTML, CSS, JS, images, service worker) |
| 	pwa/index.html | Accueil |
| 	pwa/lineup.html | Programme / line-up |
| 	pwa/galerie.html | Galerie photo |
| 	pwa/css/ | styles.css (base), header.css (header + footer partagés), pages.css (pages internes) |
| 	pwa/js/ | header.js (composant unique injecté partout), motion.js, pp.js, gallery.js, lineup.js |
| 	pwa/assets/ | Logo, icônes, photographies (WebP 800 et 1600 px) |
| *.pdf, *.pptx | Dossiers de présentation du projet |

## Lancer en local

Le site fonctionne en ouvrant pwa/index.html, mais le service worker
(mode hors-ligne, installation) exige HTTP :

``bash
cd pwa
python -m http.server 8000
``

Puis <http://localhost:8000>.

## Stack

- HTML5 sémantique, CSS moderne (variables, clamp(), grid)
- JavaScript vanilla, aucun framework
- [Motion](https://motion.dev) (vendorisé dans js/vendor/) pour les apparitions
- Service worker + manifest : installable, fonctionne hors-ligne
- Polices : Bricolage Grotesque (titres), Outfit (texte)

## Charte

| Rôle | Valeur |
|---|---|
| Fond | #0A0705 |
| Jaune | #FFD400 |
| Rouge | #E11D2E |
| Texte | #F5F0EA |

## À personnaliser

- Dates et numéro d'édition : pwa/js/app.js (constante EDITION)
- Logo : pwa/assets/logo.png
- Les chiffres affichés sont indicatifs et à valider avec les organisateurs.

---

Projet de démonstration — contenus, chiffres et programme à confirmer avec
InfluYence Group et le ministère de l'Élevage et de la Pêche.
