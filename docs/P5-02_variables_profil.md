# P5-02 : Construire les variables de profil

## Pourquoi cette étape ?

K-means regroupe des lignes qui se ressemblent. Pour regrouper des clients, il faut une ligne par client, avec des variables qui résument ses finances et ses habitudes de dépense sur toute la période.

Le critère de fin du ticket est : **table des profils créée**.

## Où est le code ?

- `src/profiles.py` : `build_profile_table`.
- `notebooks/05_profils_clients.ipynb` : section P5-02.

## Les variables

| Variable | Calcul |
| --- | --- |
| `n_transactions` | Nombre de transactions du client |
| `months_active` | Mois entre la première et la dernière transaction, inclus |
| `tx_per_month` | Transactions par mois d'activité (fréquence) |
| `mean_purchase`, `median_purchase` | Montant moyen et médian des achats (montants positifs) |
| `spend_per_month` | Total des achats / mois d'activité |
| `share_online`, `share_foreign`, `share_night` | Parts des transactions en ligne, à l'étranger et de nuit |
| `share_refund`, `error_rate` | Parts des remboursements et des transactions avec erreur |
| `n_cards`, `n_merchants` | Cartes utilisées et commerçants différents |
| `yearly_income`, `total_debt`, `credit_score` | Finances du client (table `users`) |
| `debt_to_income` | Dette / revenu annuel |
| `age_2019` | Âge au 31 octobre 2019 (dernière transaction), calculé comme en P4-03 |
| `gender`, `num_credit_cards`, `suspicious_income` | Description du client |

Les parts sont des proportions entre 0 et 1 (0,065 = 6,5 %).

## Résultats obtenus

La table a 1 219 lignes (une par client actif), 21 colonnes et aucune valeur vide.

| Variable | Médiane | Minimum | Maximum |
| --- | --- | --- | --- |
| Transactions | 9 832 | 760 | 48 479 |
| Transactions par mois | 84,9 | 6,4 | 410,8 |
| Montant moyen des achats | 48,46 $ | 5,59 $ | 178,01 $ |
| Dépenses par mois | 3 881 $ | 349 $ | 25 442 $ |
| Part en ligne | 0,065 | 0,008 | 0,740 |
| Part à l'étranger | 0,004 | 0,000 | 0,095 |
| Mois d'activité | 118 | 28 | 118 |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne choisit pas les variables de la segmentation : c'est P5-03.
- Elle ne garde pas les clients sans transaction (règle de P2-04).
