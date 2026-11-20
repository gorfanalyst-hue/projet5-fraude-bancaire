# P7-05 : Comparer les transactions signalées aux autres (Q3)

## Pourquoi cette étape ?

Q3 demande ce qui distingue les transactions frauduleuses des autres. Sans colonne de fraude dans les quatre fichiers de départ, la note de cadrage lit Q3 comme « transactions signalées par nos indicateurs » (P1-02). On compare donc les transactions signalées au seuil de 1 % aux autres.

Trois précautions, demandées dans le ticket :

- **seulement des variables qui n'ont pas servi au signalement**, sinon on retrouve ce qu'on a mis dans le score ;
- **correction de Holm**, car on fait 12 tests : plus on fait de tests, plus on risque un faux résultat significatif ;
- **taille d'effet** : avec 13 millions de lignes, tout écart devient significatif. La taille d'effet dit si l'écart compte vraiment.

Le critère de fin du ticket est : **tableau des tests : p-valeurs et taille des écarts**.

## Où est le code ?

- `src/comparisons.py` : `chi2_test`, `mann_whitney_test`, `holm_correction`, `effect_label`.
- `notebooks/07_detection_anomalies.ipynb` : section P7-05.

| Test | Pour quelles variables | Taille d'effet |
| --- | --- | --- |
| Khi-deux | Catégorielles : marque et type de carte, puce, genre, famille de commerçants, week-end, profil | V de Cramér, de 0 à 1 |
| Mann-Whitney | Numériques : score de crédit, revenu, dette, limite de crédit de la carte, âge | Corrélation rang-bisériale, de -1 à 1 (positive : valeurs plus hautes pour les signalées) |

Lecture des tailles d'effet : négligeable (moins de 0,1), faible (de 0,1 à 0,3), moyen (de 0,3 à 0,5), fort (0,5 ou plus).

Variables exclues, car utilisées par le score : montant, heure, canal, lieu, et tous les indicateurs de la phase 4.

## Résultats obtenus

| Variable | Test | p-valeur corrigée (Holm) | Taille d'effet | Lecture | Médiane signalées / autres |
| --- | --- | --- | --- | --- | --- |
| Famille de commerçants | khi-deux | < 0,001 | 0,193 | **faible** | |
| Profil de client | khi-deux | < 0,001 | 0,024 | négligeable | |
| Type de carte | khi-deux | < 0,001 | 0,016 | négligeable | |
| Marque de carte | khi-deux | < 0,001 | 0,011 | négligeable | |
| Puce sur la carte | khi-deux | < 0,001 | 0,004 | négligeable | |
| Genre | khi-deux | < 0,001 | 0,002 | négligeable | |
| Week-end | khi-deux | 0,430 | 0,000 | négligeable | |
| Revenu annuel | Mann-Whitney | < 0,001 | 0,093 | négligeable | 43 133 $ / 41 069 $ |
| Limite de crédit | Mann-Whitney | < 0,001 | 0,085 | négligeable | 14 231 $ / 13 452 $ |
| Dette | Mann-Whitney | < 0,001 | 0,083 | négligeable | 57 727 $ / 51 679 $ |
| Score de crédit | Mann-Whitney | < 0,001 | -0,039 | négligeable | 713 / 716 |
| Âge à la transaction | Mann-Whitney | < 0,001 | -0,035 | négligeable | 46 ans / 47 ans |

Pour information seulement (variable utilisée par le score) : montant médian de 85,00 $ pour les signalées, contre 28,68 $ pour les autres.

**Critère de fin validé.**

## Réponse à Q3

- 11 tests sur 12 sont significatifs, mais **10 ont une taille d'effet négligeable** : les clients et les cartes des transactions signalées ressemblent à ceux des autres transactions. C'est l'effet du nombre de lignes, pas une vraie différence.
- **Seule la famille de commerçants compte vraiment** (effet faible, V de Cramér de 0,193) : voyage et industrie sont très présents parmi les signalées (P7-06).
- Ce résultat est rassurant pour l'éthique (P9-15) : le genre (0,002) et l'âge (-0,035) ne distinguent pas les transactions signalées.
