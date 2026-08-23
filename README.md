# Opera Upholstering — site web

Site bilingue (FR/EN) pour **Opera Upholstering / Opéra Rembourrage**
7498, rue Saint-Hubert, Montréal (Québec) H2R 2N3 · (514) 270-4352

Statique, sans dépendances, sans étape de compilation. Les pages HTML
sont générées à partir de partials communs par `build.py`.

## Structure

| Fichier | Rôle |
|---|---|
| `index.html` | Accueil — enseigne, services, atelier, aperçu de la bibliothèque, cannage, soumission |
| `tissus.html` | La bibliothèque — 58 collections, 323 coloris, filtres maison / texture / tenue / couleur |
| `savoir-faire.html` | La coupe d'un siège en dix couches, le procédé, le glossaire |
| `cannage.html` | Cannage tissé à la main ou en feuille, les vingt maillages |
| `calculateur.html` | Calculateur de verges, ce qui décide du prix, questions courantes |
| `assets/site.css` | Feuille de style unique (thèmes clair et sombre, mouvement) |
| `assets/site.js` | Langue, bibliothèque, plateau, coupe animée, calculateur, heures |
| `content.json` | Le corps de chaque section, source de la génération |
| `build.py` | Assemble les cinq pages à partir des partials + `content.json` |
| `build_artifact.py` | Replie le tout en un fichier unique autonome (aperçu, partage) |

## Régénérer

```bash
python3 build.py            # réécrit les cinq pages
python3 build_artifact.py   # produit ../opera-site-preview.html
```

Servir localement :

```bash
python3 -m http.server 8788
```

## Identité

- Marque : `assets/logo-opera.png` — encre **#26282C**
- Titrage **Archivo** · interface **Jost** · texte courant **Newsreader**
- Accent grenat **#8C1F2F**, laiton **#8A6A2A**

## À confirmer avant la mise en ligne

Ces éléments sont des valeurs de travail et doivent être validés par l'atelier :

- [ ] **L'année de fondation (1955).** Rien en ligne ne la confirme; les annuaires
      répètent « 40 ans ». Un document d'époque serait la meilleure preuve.
- [ ] **Les heures d'ouverture.** Les annuaires se contredisent. Valeurs actuelles :
      lundi au vendredi 9 h–17 h, samedi 10 h–17 h, dimanche fermé.
- [ ] **Les délais par service** affichés sur l'accueil.
- [ ] **Les photographies.** Celles du site sont générées et servent de gabarit
      de direction artistique. Elles doivent être remplacées par de vraies
      photographies de l'atelier avant la mise en ligne — en particulier
      l'enseigne et tout ce qui se lit comme un travail livré.
- [ ] **La fiche Google.** Non revendiquée, sans lien vers un site, et doublée
      par une fiche « 31 rue Saint-Viateur Est » qui divise les avis.

## Licence

Tous droits réservés — Opera Upholstering.
