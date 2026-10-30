# P3-12 : Journal des transformations

Ce journal trace, table par table, ce que le nettoyage a changé. Tous les chiffres viennent des sorties de `notebooks/03_nettoyage_transformation.ipynb`. Le détail de chaque étape est dans les pages `docs/P3-01` à `docs/P3-11`.

## Vue d'ensemble

| Table | Lignes avant | Lignes après | Colonnes avant | Colonnes après |
|---|---|---|---|---|
| transactions | 13 305 915 | 13 305 915 | 12 | 30 |
| cards | 6 146 | 6 146 | 13 | 11 |
| users | 2 000 | 2 000 | 14 | 14 |
| mcc | 109 | 109 | 2 | 4 |
| fraud_labels | 8 914 963 | 8 914 963 | 2 | 2 |

Aucune ligne n'a été supprimée.

## Étapes, dans l'ordre

| Étape | Ticket | Table | Colonnes | Résultat |
|---|---|---|---|---|
| Chargement par morceaux, types légers | P3-01 | toutes | toutes | Transactions : 1 371,0 Mo en mémoire, colonnes de texte répétées en `category` |
| Montants convertis en nombres | P3-02 | transactions, cards, users | `amount`, `credit_limit`, `per_capita_income`, `yearly_income`, `total_debt` | 0 valeur non convertie |
| Dates converties | P3-03 | cards, transactions | `expires` (dernier jour du mois), `acct_open_date` (1er jour du mois) ; `date` est lue comme date dès le chargement | 0 valeur non convertie, 0 date manquante |
| Table MCC nettoyée et jointure contrôlée | P3-04 | mcc | `mcc_code`, `description` | 13 305 915 lignes avant et après la jointure, 0 transaction sans catégorie |
| Familles MCC | P3-05 | mcc | ajout de `famille`, `description_fr` | 109 codes classés en 12 familles |
| Colonne `errors` en colonnes binaires | P3-06 | transactions | ajout de 9 colonnes : 7 `err_*`, `has_error`, `has_auth_error` | Totaux identiques à P2-13 ; 211 393 transactions avec erreur, dont 53 977 échecs d'authentification |
| Lieu structuré | P3-07 | transactions | ajout de `is_online`, `online_channel_mismatch`, `merchant_country`, `merchant_state_clean`, `is_foreign`, `zip_clean` | 0 manquant ou « UNKNOWN » ; 1 563 700 en ligne, 89 006 à l'étranger, 11 653 209 aux États-Unis sur place ; 5 788 désaccords signalés |
| Valeurs suspectes signalées | P3-08 | transactions, users, cards | ajout de `is_negative_amount`, `is_zero_amount`, `is_repeated`, `suspicious_income`, `zero_credit_limit` | 660 049, 10 639, 15, 15 et 31 lignes signalées ; rien de supprimé ni de modifié |
| Colonnes retirées | P3-09 | cards, users | `card_number`, `cvv`, `card_on_dark_web`, `address` | Colonnes absentes des tables nettoyées |
| Tables enregistrées en Parquet | P3-10 | toutes | toutes | 5 fichiers dans `data/clean/` ; relecture des transactions en 7,6 s |
| Contrôles rejoués | P3-11 | toutes | toutes | 18 contrôles sur 18 réussis |

## Colonnes ajoutées et retirées

| Table | Colonnes ajoutées | Colonnes retirées |
|---|---|---|
| transactions | `has_error`, `err_bad_pin`, `err_bad_cvv`, `err_bad_card_number`, `err_bad_expiration`, `err_bad_zipcode`, `err_insufficient_balance`, `err_technical_glitch`, `has_auth_error`, `is_online`, `online_channel_mismatch`, `merchant_country`, `merchant_state_clean`, `is_foreign`, `zip_clean`, `is_negative_amount`, `is_zero_amount`, `is_repeated` | aucune |
| cards | `zero_credit_limit` | `card_number`, `cvv`, `card_on_dark_web` |
| users | `suspicious_income` | `address` |
| mcc | `famille`, `description_fr` | aucune |
| fraud_labels | aucune | aucune |

## Pour le rapport final : section « Préparation des données »

- Les données brutes comptent 13 305 915 transactions, 6 146 cartes, 2 000 clients, 109 codes MCC et 8 914 963 étiquettes de fraude.
- Le nettoyage ne supprime aucune ligne.
- Les montants et les dates, stockés en texte, sont convertis sans aucune valeur perdue.
- Les codes MCC sont classés en 12 familles, avec une description en français.
- Les erreurs de paiement deviennent des colonnes binaires, dont un indicateur d'échec d'authentification.
- Le lieu de chaque transaction est classé en ligne, à l'étranger ou aux États-Unis sur place. Tous les manquants sont expliqués.
- Les valeurs suspectes (montants négatifs ou nuls, revenus trop bas, limites nulles, doubles débits possibles) sont signalées par des indicateurs, sans être modifiées.
- Les colonnes sensibles (numéro de carte, CVV, adresse) sont retirées.
- Les tables nettoyées sont enregistrées au format Parquet. Les 18 contrôles de cohérence rejoués sur ces fichiers réussissent tous.
