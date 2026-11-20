# P9-01 : Répondre aux questions de recherche

Statut : à valider par l'équipe (critère de fin de P9-01). Une réponse chiffrée par question. Chaque chiffre vient d'un notebook ; la source est indiquée entre parenthèses.

## Q1 : quels sont les principaux profils de clients ?

Les 1 208 clients actifs segmentés forment **quatre profils** (K-means, silhouette de 0,235, profils stables : indice de Rand ajusté moyen de 0,972) :

- **Clients courants** (686) : proches de la moyenne, revenu médian de 34 928 $ ;
- **Clients aisés et voyageurs** (321) : revenu de 59 872 $, achat moyen de 67,17 $, plus d'achats à l'étranger ;
- **Acheteurs en ligne très actifs** (138) : part en ligne de 0,352 et 131 transactions par mois ;
- **Clients sans dette** (63) : dette nulle, score de crédit de 733.

L'âge médian est le même partout (50 ou 51 ans). Les 781 clients sans transaction sont plus jeunes (âge médian de 28 ans). (Notebook 05.)

## Q2 : quels sont les comportements transactionnels des clients ?

- Petits achats fréquents : la moitié coûte moins de 31,92 $ ; achat moyen de 50,60 $.
- De jour : forte activité de 6 h à 16 h, pic à 12 h ; la nuit ne fait que 5,8 % des transactions.
- Sur place aux États-Unis à 87,58 %, en ligne à 11,75 %, à l'étranger à 0,67 %.
- Surtout en transport (25,19 % des transactions) et en alimentation (23,92 %).
- 4,96 % de remboursements, concentrés dans six familles. (Notebook 06.)

## Q3 : qu'est-ce qui distingue les transactions frauduleuses des autres ?

- **Transactions signalées par le score (seuil 1 %)** : sur les variables hors du score, seule la famille de commerçants a un effet réel (V de Cramér de 0,193). Âge, genre, revenu et score de crédit ont des effets négligeables. (Notebook 07, P7-05.)
- **Transactions étiquetées comme fraudes** : le modèle supervisé s'appuie surtout sur l'achat à l'étranger, la famille de commerçants, le canal et l'heure. (Notebook 07, P7-08.)
- **Raisons des signalements les plus précises** : nouveau pays (13,81 % de vraies fraudes), nouveau commerçant dans une nouvelle catégorie (8,47 %), achat à l'étranger (6,67 %), contre un taux de fraude moyen de 0,150 %. (Notebook 07, P7-11.)

## Q4 : quelles caractéristiques sont liées à un risque plus élevé ?

Taux de signalement au seuil de 1 % (taux global : 1 %) :

- achat à l'étranger : 19,437 % ;
- voyage et hébergement : 18,933 % ; industrie et fabrication : 14,926 % ;
- achat en ligne : 2,561 % ; nuit : de 2,124 % à 2,634 % entre 0 h et 5 h, 3,232 % à 23 h ;
- risque le plus faible : restauration (0,201 %), santé (0,260 %), puce (0,694 %).

Les profils et les cartes comptent peu (de 0,52 à 1,42 fois le taux global). (Notebook 07, P7-06.)

## Q5 : quels indicateurs repèrent les comportements inhabituels ?

- 16 indicateurs dans le catalogue (P4-09), traduits en 13 règles et combinés à Isolation Forest dans un score de 0 à 100.
- Quatre raisons font 81,5 % des signalements : rafales, montant inhabituel, nouveau commerçant dans une nouvelle catégorie, échec d'authentification.
- Avec les étiquettes : au seuil de 1 %, le score a une précision de 3,57 % (23,9 fois le hasard) et un rappel de 23,93 %. Les indicateurs de lieu et de nouveauté sont les plus utiles ; les rafales n'aident pas (0,04 % de précision). (Notebooks 04 et 07.)

## Q6 : comment les comportements évoluent-ils selon le temps, le lieu et la catégorie ?

- **Temps** : hausse de l'activité jusqu'en 2015 (de 1 240 880 transactions en 2010 à 1 399 308 en 2017), puis stabilité ; passage brutal de la bande magnétique à la puce en 2015 (puce : 70,8 %).
- **Lieu** : les achats à l'étranger restent rares (0,67 %), surtout au Mexique et au Canada ; trois États font 28 % des transactions sur place.
- **Catégorie** : la répartition entre familles change très peu en dix ans (0,91 point d'écart au plus). (Notebook 06.)

## Q7 : comment présenter les résultats aux décideurs ?

Un tableau de bord Streamlit à quatre pages : vue d'ensemble, profils de clients, lieux et catégories, transactions signalées. Il permet de filtrer par années, canaux et seuil, de trouver les transactions les plus risquées d'un client et de télécharger la liste. Ses 62 chiffres contrôlés sont égaux aux résultats des notebooks. (Notebook 08 ; guide : `docs/P8-11_guide_utilisation.md`.)
