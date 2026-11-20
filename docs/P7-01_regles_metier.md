# P7-01 : Coder les règles métier

## Pourquoi cette étape ?

Une règle métier traduit un signal du catalogue (P4-09) en une condition simple et explicable : « 2 échecs d'authentification ou plus en 24 heures ». Les règles donnent la raison d'un signalement, ce qu'un modèle seul ne fait pas.

Le critère de fin du ticket est : **règles codées et comptées**.

## Où est le code ?

- `src/detection.py` : la liste `RULES`, et les fonctions `rules_table`, `apply_rules` et `count_rules`.
- `notebooks/07_detection_anomalies.ipynb` : section P7-01.

## Les règles

Chaque règle donne des points : 3 pour un signal fort, 2 pour un signal moyen, 1 pour un signal faible, trop fréquent pour compter seul. Les seuils sont fixés avec les distributions de la phase 4, **sans regarder les étiquettes de fraude** : une règle à 3 points touche moins de 0,3 % des transactions, une règle à 2 points moins de 1 %.

| Code | Règle | Points | Transactions touchées | Part |
| --- | --- | --- | --- | --- |
| R01 | 2 échecs d'authentification ou plus sur la carte en 24 h | 3 | 1 602 | 0,012 % |
| R02 | Échec d'authentification sur la transaction | 2 | 53 977 | 0,406 % |
| R03 | Montant au moins 20 fois plus élevé que d'habitude (300 $ ou plus) | 3 | 41 570 | 0,312 % |
| R04 | Rafale : 5 transactions ou plus de la carte dans l'heure précédente | 3 | 32 978 | 0,248 % |
| R05 | 15 transactions ou plus de la carte dans les 24 heures précédentes | 2 | 13 082 | 0,098 % |
| R06 | Premier achat du client dans ce pays (après 100 transactions) | 2 | 4 135 | 0,031 % |
| R07 | Achat sur place à l'étranger | 2 | 89 006 | 0,669 % |
| R08 | Nouveau commerçant dans une nouvelle catégorie (après 100 transactions) | 2 | 67 568 | 0,508 % |
| R09 | Achat de nuit (0 h à 5 h 59) | 1 | 770 383 | 5,790 % |
| R10 | Achat en ligne | 1 | 1 563 700 | 11,752 % |
| R11 | Achat sans centimes | 1 | 1 349 993 | 10,146 % |
| R12 | Transaction hors de la période de validité de la carte | 3 | 392 | 0,003 % |
| R13 | Doublon possible (seconde ligne d'un groupe répété) | 2 | 15 | 0,000 % |

Choix des seuils :

- **R01** : 2 échecs et non 3 comme dans l'exemple de Jira. Avec 3 échecs, la règle ne toucherait que 22 transactions (P4-06).
- **R03** : 300 $ correspond environ au 1 % des achats les plus chers (P6-01) ; le rapport de 20 évite de signaler les clients qui font souvent de gros achats.
- **R04 et R05** : au-delà du quantile 99,9 % de P4-05 (5 transactions dans l'heure, 14 dans les 24 heures).
- **R06 et R08** : seulement après 100 transactions du client, pour ne pas signaler le début normal de chaque historique (P4-07).

## La fonction `apply_rules`

```python
def apply_rules(df):
    flags = pd.DataFrame(index=df.index)
    rule_points = np.zeros(len(df), dtype=np.int16)
    n_rules = np.zeros(len(df), dtype=np.int8)
    for code, _, points, condition in RULES:
        flag = df.eval(condition).fillna(False).to_numpy().astype(np.int8)
        flags[code] = flag
        rule_points += flag * points
        n_rules += flag
    flags["rule_points"] = rule_points
    flags["n_rules"] = n_rules
    return flags
```

| Syntaxe | Rôle |
| --- | --- |
| `df.eval(condition)` | Évalue la condition écrite en texte (exemple : `"card_tx_1h >= 5"`) sur toute la table. Les règles restent lisibles dans `RULES`. |
| `rule_points` | Somme des points des règles déclenchées. |
| `n_rules` | Nombre de règles déclenchées. |

## Résultats obtenus

| Points de règles | Transactions |
| --- | --- |
| 0 | 9 644 775 |
| 1 | 3 173 967 |
| 2 | 339 657 |
| 3 | 100 029 |
| 4 | 29 763 |
| 5 | 11 422 |
| 6 | 5 015 |
| 7 | 820 |
| 8 ou plus | 467 |

3 661 140 transactions déclenchent au moins une règle, et 76 369 au moins une règle à 3 points.

**Critère de fin validé.**
