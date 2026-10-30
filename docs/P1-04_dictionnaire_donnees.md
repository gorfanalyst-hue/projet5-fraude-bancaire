# P1-04 : Dictionnaire des données

Une ligne par colonne des cinq fichiers reçus. Les types, le nombre de valeurs distinctes et les exemples viennent des sorties de `notebooks/01_exploration_donnees.ipynb`. Les colonnes sensibles sont masquées.

Les colonnes créées pendant le nettoyage sont listées dans `docs/P3-12_journal_transformations.md`.

## `users_data.csv` : clients (2 000 lignes, 14 colonnes)

| Colonne             | Description                                             | Type au chargement | Valeurs distinctes | Exemple  | Traitement                                                                                      |
| ------------------- | ------------------------------------------------------- | ------------------ | ------------------ | -------- | ----------------------------------------------------------------------------------------------- |
| `id`                | Identifiant du client                                   | int32              | 2 000              | 825      | Clé vers `cards.client_id` et `transactions.client_id`                                          |
| `current_age`       | Âge du client, calculé à la fin de février 2020 (P2-12) | int8               | 80                 | 53       | Âge à la date de chaque transaction recalculé en P4-03                                          |
| `retirement_age`    | Âge de la retraite                                      | int8               | 29                 | 66       | Aucun                                                                                           |
| `birth_year`        | Année de naissance                                      | int16              | 80                 | 1966     | Sert au calcul de l'âge (P4-03)                                                                 |
| `birth_month`       | Mois de naissance                                       | int8               | 12                 | 11       | Sert au calcul de l'âge (P4-03)                                                                 |
| `gender`            | Genre                                                   | category           | 2                  | Female   | Aucun                                                                                           |
| `address`           | Adresse                                                 | object             | 1 999              | (masqué) | Retirée (P3-09)                                                                                 |
| `latitude`          | Latitude du domicile                                    | float64            | 989                | 34.15    | Aucun                                                                                           |
| `longitude`         | Longitude du domicile                                   | float64            | 1 224              | -117.76  | Aucun                                                                                           |
| `per_capita_income` | Revenu par habitant                                     | object             | 1 754              | $29278   | Converti en nombre (P3-02) ; valeur nulle signalée par `suspicious_income` (P3-08)              |
| `yearly_income`     | Revenu annuel                                           | object             | 1 948              | $59696   | Converti en nombre (P3-02) ; valeur inférieure à 1 000 signalée par `suspicious_income` (P3-08) |
| `total_debt`        | Dette totale                                            | object             | 1 880              | $127613  | Converti en nombre (P3-02)                                                                      |
| `credit_score`      | Score de crédit                                         | int16              | 321                | 787      | Aucun                                                                                           |
| `num_credit_cards`  | Nombre de cartes de crédit du client                    | int8               | 9                  | 5        | Aucun                                                                                           |

## `cards_data.csv` : cartes (6 146 lignes, 13 colonnes)

| Colonne                 | Description                               | Type au chargement | Valeurs distinctes | Exemple  | Traitement                                                                         |
| ----------------------- | ----------------------------------------- | ------------------ | ------------------ | -------- | ---------------------------------------------------------------------------------- |
| `id`                    | Identifiant de la carte                   | int32              | 6 146              | 4524     | Clé vers `transactions.card_id`                                                    |
| `client_id`             | Titulaire de la carte                     | int32              | 2 000              | 825      | Clé vers `users.id`                                                                |
| `card_brand`            | Marque de la carte                        | category           | 4                  | Visa     | Aucun                                                                              |
| `card_type`             | Type de carte : crédit, débit ou prépayée | category           | 3                  | Debit    | Aucun                                                                              |
| `card_number`           | Numéro de la carte                        | int64              | 6 146              | (masqué) | Retiré (P3-09)                                                                     |
| `expires`               | Mois d'expiration (mm/aaaa)               | object             | 259                | 12/2022  | Converti en date, dernier jour du mois (P3-03)                                     |
| `cvv`                   | Code de sécurité                          | int64              | 998                | (masqué) | Retiré (P3-09)                                                                     |
| `has_chip`              | Carte à puce (YES ou NO)                  | category           | 2                  | YES      | Aucun                                                                              |
| `num_cards_issued`      | Nombre de cartes émises pour le compte    | int8               | 3                  | 2        | Aucun                                                                              |
| `credit_limit`          | Limite de crédit                          | object             | 3 654              | $24295   | Converti en nombre (P3-02) ; valeur nulle signalée par `zero_credit_limit` (P3-08) |
| `acct_open_date`        | Mois d'ouverture du compte (mm/aaaa)      | object             | 303                | 09/2002  | Converti en date, premier jour du mois (P3-03)                                     |
| `year_pin_last_changed` | Dernière année de changement du PIN       | int64              | 19                 | 2008     | Aucun                                                                              |
| `card_on_dark_web`      | Carte trouvée sur le dark web             | category           | 1                  | No       | Retirée : une seule valeur (P3-09)                                                 |

## `transactions_data.csv` : transactions (13 305 915 lignes, 12 colonnes)

| Colonne          | Description                                            | Type au chargement | Valeurs distinctes | Exemple             | Traitement                                                          |
| ---------------- | ------------------------------------------------------ | ------------------ | ------------------ | ------------------- | ------------------------------------------------------------------- |
| `id`             | Identifiant de la transaction                          | int32              | 13 305 915         | 7475327             | Clé vers `fraud_labels.id`                                          |
| `date`           | Date et heure, à la minute                             | datetime64[ns]     | 4 136 496          | 2010-01-01 00:01:00 | Lue comme date dès le chargement (P3-01)                            |
| `client_id`      | Client                                                 | int32              | 1 219              | 1556                | Clé vers `users.id`                                                 |
| `card_id`        | Carte utilisée                                         | int32              | 4 071              | 2972                | Clé vers `cards.id`                                                 |
| `amount`         | Montant, parfois négatif                               | object             | 81 161             | $-77.00             | Converti en nombre (P3-02) ; montant négatif ou nul signalé (P3-08) |
| `use_chip`       | Canal : puce, bande magnétique ou en ligne             | category           | 3                  | Swipe Transaction   | Sert à `is_online` (P3-07)                                          |
| `merchant_id`    | Commerçant                                             | int32              | 74 831             | 59935               | Aucun                                                               |
| `merchant_city`  | Ville du commerçant, « ONLINE » pour un achat en ligne | category           | 12 492             | Beulah              | Valeur explicite à la place des manquants (P3-07)                   |
| `merchant_state` | Code d'État américain ou nom de pays                   | category           | 199                | ND                  | Séparé en `merchant_state_clean` et `merchant_country` (P3-07)      |
| `zip`            | Code postal du commerçant                              | float64            | 25 256             | 58523.0             | Code à 5 chiffres dans `zip_clean` (P3-07)                          |
| `mcc`            | Code de catégorie du commerçant                        | int16              | 109                | 5499                | Clé vers `mcc_codes` ; famille ajoutée en P3-05                     |
| `errors`         | Erreurs de la transaction, vide s'il n'y en a pas      | category           | 22                 | Technical Glitch    | Une colonne binaire par type d'erreur (P3-06)                       |

## `mcc_codes.json` : catégories de commerçants (109 lignes, 2 colonnes)

| Colonne       | Description            | Type au chargement | Valeurs distinctes | Exemple                       | Traitement                                          |
| ------------- | ---------------------- | ------------------ | ------------------ | ----------------------------- | --------------------------------------------------- |
| `mcc_code`    | Code MCC               | int16              | 109                | 5812                          | Famille et description en français ajoutées (P3-05) |
| `description` | Description en anglais | object             | 108                | Eating Places and Restaurants | Espaces retirés (P3-04)                             |

## `fraud_labels.json` : étiquettes de fraude (8 914 963 lignes, 2 colonnes)

| Colonne    | Description                                            | Type au chargement | Valeurs distinctes | Exemple  | Traitement                               |
| ---------- | ------------------------------------------------------ | ------------------ | ------------------ | -------- | ---------------------------------------- |
| `id`       | Identifiant de la transaction                          | int32              | 8 914 963          | 10649266 | Clé vers `transactions.id`               |
| `is_fraud` | 1 pour une fraude, 0 sinon (Yes ou No dans le fichier) | int8               | 2                  | 0        | Converti par `load_fraud_labels` (P2-17) |
