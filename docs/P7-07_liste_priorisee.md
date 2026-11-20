# P7-07 : Produire la liste priorisée (Q5)

## Pourquoi cette étape ?

L'analyste ne peut pas tout contrôler. La liste priorisée lui donne, dans l'ordre, les transactions à regarder en premier, avec la raison du signalement. C'est le résultat concret du score pour la banque, et la source de la page « Transactions signalées » du tableau de bord.

Le critère de fin du ticket est : **fichier exporté et commenté**.

## Où est le code ?

- `src/detection.py` : `main_reason` et `triggered_rules`.
- `notebooks/07_detection_anomalies.ipynb` : section P7-07.

| Fonction | Rôle |
| --- | --- |
| `main_reason(flags)` | Raison principale : la règle déclenchée qui a le plus de points (en cas d'égalité, la première de la liste). Sans règle, la raison serait « comportement atypique (Isolation Forest) ». |
| `triggered_rules(flags)` | Liste des codes des règles déclenchées (exemple : « R03, R08 »). |

## Le fichier exporté

`data/resultats/P7-07_liste_priorisee.csv` (non versionné, 26,9 Mo), une ligne par transaction signalée au seuil de 1 %, triée par score décroissant :

| Colonne | Contenu |
| --- | --- |
| `rang` | 1 = la plus risquée |
| `id`, `date`, `client_id`, `card_id` | Identification de la transaction |
| `amount`, `canal`, `mcc_family`, `merchant_city`, `merchant_country` | Ce qui a été acheté, comment et où |
| `risk_score` | Score de 0 à 100 |
| `raison_principale`, `regles` | Pourquoi la transaction est signalée |
| `anomaly_pct` | Rang selon Isolation Forest (0,99 = plus atypique que 99 % des transactions) |

Aucune donnée sensible : pas de numéro de carte ni de CVV (retirés en P3-09).

Les scores de toutes les transactions sont aussi enregistrés dans `data/clean/risk_scores.parquet` pour le tableau de bord.

## Résultats obtenus

133 075 transactions signalées. Raisons principales :

| Raison principale | Transactions |
| --- | --- |
| R04 : rafale dans l'heure | 32 908 |
| R03 : montant inhabituel | 26 260 |
| R08 : nouveau commerçant et nouvelle catégorie | 24 901 |
| R02 : échec d'authentification | 24 382 |
| R07 : achat à l'étranger | 12 068 |
| R05 : journée très active | 4 862 |
| R06 : nouveau pays | 3 885 |
| R09 : achat de nuit | 1 949 |
| R01 : échecs d'authentification répétés | 1 595 |
| R12 : hors validité de la carte | 215 |
| R10 : achat en ligne | 47 |
| R13 : doublon possible | 3 |

**Critère de fin validé.**

## Commentaire

- Quatre raisons font 81,5 % de la liste : R04, R03, R08 et R02.
- Aucune transaction n'est signalée par Isolation Forest seul : chaque ligne a une règle, donc une explication.
- Les 10 premières transactions (score de 100,0) sont surtout des achats à l'étranger (Pakistan, Italie, Haïti, Corée du Sud, Taïwan, Thaïlande) et de gros achats en ligne (jusqu'à 1 739,54 $), avec 4 à 6 règles chacune.
- Attention : la première raison (R04, rafales) est aussi la moins précise (P7-11). La liste gagnerait à descendre ces transactions.
