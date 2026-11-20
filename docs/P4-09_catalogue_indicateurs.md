# P4-09 : Catalogue des indicateurs (Q5)

Statut : à valider par l'équipe (critère de fin de P4-09). Ce catalogue alimente la section « Indicateurs » du rapport.

## Pourquoi ce catalogue ?

La question Q5 demande quels indicateurs repèrent les comportements inhabituels. Le catalogue donne, pour chaque indicateur, sa définition, son calcul et la raison pour laquelle il peut signaler une fraude. Les règles de la phase 7 en partent : une règle par signal.

Les étiquettes de fraude ne servent pas à choisir les indicateurs : le choix ne doit pas dépendre d'elles (variante sans étiquettes de la phase 7).

## Le catalogue

| Indicateur (colonne) | Ticket | Définition et calcul | Pourquoi c'est un signal | Fréquence |
| --- | --- | --- | --- | --- |
| `is_night` | P4-02 | Heure de 0 h à 5 h 59 | Un achat en pleine nuit est inhabituel pour la plupart des clients | 5,790 % |
| `is_weekend` | P4-02 | Samedi ou dimanche | Contexte : le rythme des achats change le week-end | 28,569 % |
| `age_at_transaction` | P4-03 | Année de la transaction - année de naissance, moins 1 si l'anniversaire n'est pas passé | Sert à vérifier que le score ne désavantage pas un groupe d'âge (P9-15) | médiane de 47 ans |
| `amount_ratio` | P4-04 | Montant / médiane des achats précédents du client (au moins 10 achats) | Un fraudeur dépense souvent beaucoup plus que le titulaire | médiane de 0,95 ; 60,05 au quantile 99,9 % |
| `card_tx_1h` | P4-05 | Transactions précédentes de la carte dans l'heure | Une rafale peut indiquer une carte volée testée ou vidée | médiane de 0 ; 5 au quantile 99,9 % |
| `card_tx_24h` | P4-05 | Transactions précédentes de la carte dans les 24 heures | Même raison, sur une journée | médiane de 1 ; 14 au quantile 99,9 % |
| `card_auth_errors_24h` | P4-06 | Échecs d'authentification de la carte dans les 24 heures précédentes | Plusieurs mauvais PIN, CVV ou numéros : quelqu'un essaie la carte sans la connaître | médiane de 0 ; 1 au quantile 99,9 % |
| `is_first_merchant` | P4-07 | Premier achat du client chez ce commerçant | Le fraudeur achète chez des commerçants que le titulaire ne fréquente pas | 2,688 % |
| `is_first_mcc` | P4-07 | Premier achat du client dans cette catégorie MCC | Même raison, pour un type de commerce nouveau | 0,708 % |
| `is_first_country` | P4-07 | Premier achat du client dans ce pays (ou premier achat en ligne) | Une carte copiée est souvent utilisée dans un autre pays | 0,050 % |
| `is_online` | P3-07 | Ville « ONLINE » ou canal « Online Transaction » | Le paiement sans carte physique est le plus exposé à la fraude | 11,752 % |
| `is_foreign` | P3-07 | Achat sur place hors des États-Unis | Les clients achètent presque toujours aux États-Unis | 0,669 % |
| `is_round_amount` | P4-08 | Achat sans centimes | Les fraudeurs testent parfois des montants ronds | 10,146 % |
| `outside_card_validity` | P4-08 | Avant l'ouverture du compte ou après l'expiration de la carte | Une carte ne devrait pas servir hors de sa période de validité | 392 transactions (0,003 %) |
| `has_auth_error` | P3-06 | La transaction elle-même a un échec d'authentification | Signe direct d'une tentative avec de mauvaises informations | 0,406 % |
| `is_repeated` | P3-08 | Seconde ligne d'un groupe répété sans erreur | Possible double débit | 15 transactions |

Les fréquences viennent de `describe_indicators` (notebook 04, section P4-09).

## Ce que le catalogue dit déjà

- **Trois indicateurs sont trop fréquents pour être des signaux forts seuls** : achat en ligne (11,752 %), montant rond (10,146 %) et nuit (5,790 %). Dans le score, ils ne valent qu'un point.
- **Les signaux rares sont les plus précis**, mais ils touchent peu de transactions : hors validité (392), premier pays (6 615), doublon (15).
- Deux indicateurs ne servent qu'au contexte et au contrôle éthique : le week-end et l'âge.

## Où est le code ?

`src/features.py` : la liste `INDICATOR_CATALOGUE`, et les fonctions `indicator_catalogue()` et `describe_indicators(df)`.
