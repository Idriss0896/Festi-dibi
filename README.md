# Festival du Dibi — site officiel

Site web (PWA) du **Festival du Dibi**, le 1ᵉʳ festival gastronomique
d'Afrique de l'Ouest. Bamako, Mali.

Site en ligne : **https://idriss0896.github.io/Festi-dibi/**

## Pages

| Fichier | Rôle |
|---|---|
| `index.html` | Accueil : présentation, chiffres, histoire, billetterie, infos |
| `lineup.html` | Programme / line-up avec filtres (jour, scène, genre) |
| `galerie.html` | Galerie photo |

## Structure

```
index.html · lineup.html · galerie.html
manifest.webmanifest · sw.js          → PWA (installation + hors-ligne)
css/
  styles.css      base, tokens, sections
  header.css      header + footer partagés (injectés sur toutes les pages)
  pages.css       styles des pages internes
js/
  header.js       composant header/footer unique — source de vérité
  motion.js       apparitions au scroll, compteurs, cascades
  app.js          compte à rebours, menu, newsletter
  gallery.js      filtres et visionneuse de la galerie
  lineup.js       filtres du programme
  vendor/motion.min.js
assets/           logo, icônes PWA, photos WebP (800 et 1600 px)
presentation/     dossiers PDF et PowerPoint du projet
```

Aucun framework, aucun build : le dépôt **est** le site.

## Lancer en local

Ouvrir `index.html` fonctionne, mais le service worker (hors-ligne,
installation) exige HTTP :

```bash
python -m http.server 8000
```

Puis <http://localhost:8000>. N'importe quel serveur statique convient
(`npx serve`, Live Server, etc.).

## Déploiement

Automatique : à chaque `push` sur `main`, le workflow
`.github/workflows/deploy.yml` publie le site sur GitHub Pages.

## Charte

| Rôle | Valeur |
|---|---|
| Fond | `#0A0705` |
| Jaune | `#FFD400` |
| Jaune clair | `#FFE066` |
| Rouge | `#E11D2E` |
| Texte | `#F5F0EA` |

Typographie : **Bricolage Grotesque** (titres), **Outfit** (texte).

## À personnaliser

- Dates et numéro d'édition : `js/app.js`, constante `EDITION`
- Logo : `assets/logo.png`
- Les chiffres, horaires et tarifs affichés sont indicatifs et doivent être
  validés avec les organisateurs.

---

Projet de démonstration — contenus à confirmer avec InfluYence Group et le
ministère de l'Élevage et de la Pêche.
