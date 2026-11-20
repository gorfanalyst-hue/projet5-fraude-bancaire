# P1-10 : Charte graphique

Statut : à valider par l'équipe (critère de fin de P1-10). Cette page est la référence pour tous les visuels : notebooks, rapport, diapositives et tableau de bord.

## Les règles

- **Un seul message par graphique.** Le titre annonce ce message (exemple : « La puce remplace la bande magnétique à partir de 2016 »), pas seulement le sujet.
- **Une seule couleur forte pour ce qui compte.** Le reste est en bleu ou en gris.
- **Textes en noir ou en gris**, jamais dans la couleur d'une série.
- **Pas de double axe.** Deux mesures d'échelles différentes : deux graphiques.
- **Une légende dès qu'il y a deux séries ou plus**, et des étiquettes directes quand il y a peu de séries. Jamais un chiffre sur chaque point.
- **Quadrillage discret**, sans cadre en haut ni à droite.
- **Nombres à la française** : espace pour les milliers (1 234 567), virgule pour les décimales.

## Les couleurs

Palette catégorielle, à utiliser **dans cet ordre** et sans la recycler. L'ordre a été vérifié pour les personnes daltoniennes : deux couleurs voisines restent distinctes.

| Ordre | Couleur | Code | Usage habituel dans le projet |
| --- | --- | --- | --- |
| 1 | Bleu | `#2a78d6` | Série principale, « autres transactions » |
| 2 | Orange | `#eb6834` | Ce qui doit ressortir : transactions signalées, seuil |
| 3 | Turquoise | `#1baf7a` | Troisième série (exemple : achats en ligne) |
| 4 | Jaune | `#eda100` | Quatrième série |
| 5 | Rose | `#e87ba4` | Cinquième série |
| 6 | Vert | `#008300` | Sixième série |
| 7 | Violet | `#6250d6` | Septième série |
| 8 | Rouge | `#e34948` | Huitième série |

Au-delà de trois séries dans un nuage de points ou une carte, regrouper les petites séries dans « Autres » ou faire plusieurs petits graphiques.

Autres couleurs :

| Rôle | Code |
| --- | --- |
| Texte principal | `#0b0b0b` |
| Texte secondaire (axes, notes) | `#52514e` |
| Quadrillage | `#e4e3df` |
| Fond | `#fcfcfb` |
| Gris neutre | `#b8b6af` |

Cartes de chaleur :

- **valeur seule** (exemple : nombre de transactions) : une seule teinte, du bleu clair `#cde2fb` au bleu foncé `#0d366b` ;
- **écart à une moyenne** (exemple : profils) : bleu en dessous, gris `#f0efec` au milieu, rouge `#e34948` au-dessus.

## Polices et tailles

| Élément | Police et taille |
| --- | --- |
| Titre du graphique | DejaVu Sans, 12, gras, aligné à gauche |
| Axes et légendes | DejaVu Sans, 10, gris |
| Notes sous le graphique | DejaVu Sans, 8, gris |

DejaVu Sans est la police par défaut de matplotlib : elle est la même sur tous les ordinateurs de l'équipe.

## Où est le code ?

`src/charte.py` contient la palette, les cartes de couleurs et deux fonctions :

```python
from src.charte import apply_style, save_figure

# Applique la charte aux graphiques qui suivent
apply_style()

# Enregistre docs/figures/P6-02_canaux.png
save_figure(fig, "P6-02_canaux")
```

| Syntaxe | Rôle |
| --- | --- |
| `apply_style()` | Règle une fois pour toutes les couleurs, les polices, le quadrillage et les cadres de matplotlib. |
| `save_figure(fig, nom)` | Enregistre la figure en PNG (150 points par pouce) dans `docs/figures/`, pour le rapport et les diapositives. |
| `sequential_cmap()`, `diverging_cmap()` | Cartes de couleurs pour les cartes de chaleur. |
| `THOUSANDS` | Formateur d'axe qui écrit 1 234 567. |

Le tableau de bord reprend les mêmes couleurs (`dashboard/pages.py`).
