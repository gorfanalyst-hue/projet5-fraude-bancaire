# P4-01 : Construire la table d'analyse

## Pourquoi cette étape ?

Les informations utiles sont réparties dans plusieurs tables : la transaction d'un côté, le client, la carte et la catégorie du commerçant de l'autre. Pour comparer les transactions selon le genre, le type de carte ou la famille de commerçant, il faut tout réunir sur une seule ligne.

Le critère de fin du ticket est : **même nombre de lignes que la table des transactions**.

## Où est le code ?

- `src/features.py` : `build_analysis_table` et `check_analysis_table`.
- `notebooks/04_table_analyse.ipynb` : section P4-01.

## La fonction `build_analysis_table`

```python
def build_analysis_table(df_transaction, df_users, df_card, df_mcc, df_labels):
    df = df_transaction
    for col in RAW_COLUMNS_REPLACED:
        if col in df.columns:
            del df[col]

    users = df_users.set_index("id")
    for col in USER_COLUMNS:
        df[col] = _map_column(df["client_id"], users, col)

    cards = df_card.set_index("id")
    for col in CARD_COLUMNS:
        df[col] = _map_column(df["card_id"], cards, col)

    families = df_mcc.set_index("mcc_code")["famille"].astype("category")
    df["mcc_family"] = df["mcc"].map(families).astype(families.dtype)

    labels = df_labels.set_index("id")["is_fraud"]
    df["is_fraud"] = df["id"].map(labels).astype("Int8")
    ...
    return df
```

| Syntaxe | Rôle |
| --- | --- |
| `RAW_COLUMNS_REPLACED` | `merchant_state` et `zip` : colonnes brutes remplacées en P3-07 par `merchant_state_clean`, `merchant_country` et `zip_clean`. Elles sont retirées pour alléger la table. |
| `set_index("id")` puis `map` | Pour chaque transaction, va chercher la valeur du client ou de la carte. `map` ajoute une colonne sans copier la table de 13 millions de lignes, contrairement à `merge`. |
| `USER_COLUMNS` | Genre, année et mois de naissance, revenu, dette, score de crédit, `suspicious_income`. |
| `CARD_COLUMNS` | Marque, type, puce, limite de crédit, dates d'ouverture et d'expiration, `zero_credit_limit`. |
| `mcc_family` | Famille du code MCC (P3-05). |
| `astype("Int8")` | `is_fraud` vaut 1, 0 ou vide (transaction sans étiquette, P2-17). Le type `Int8` accepte les valeurs vides. |

`check_analysis_table` compare le nombre de lignes à celui des transactions, cherche les identifiants en double et les valeurs vides dans les colonnes ajoutées.

## Résultats obtenus

| Contrôle | Résultat |
| --- | --- |
| Lignes de la table d'analyse | 13 305 915 (comme la table des transactions) |
| Identifiants en double | 0 |
| Valeurs vides dans les colonnes ajoutées | 0 |
| Transactions étiquetées (`is_fraud`) | 8 914 963 |
| Taille à cette étape | 44 colonnes, 1 334,3 Mo en mémoire |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne crée pas encore les indicateurs : ce sont P4-02 à P4-08.
- Elle ne garde pas `current_age` : l'âge à la date de la transaction est calculé en P4-03.

## À noter dans le journal des transformations (P3-12)

Table d'analyse : transactions + 7 colonnes des clients + 7 colonnes des cartes + `mcc_family` + `is_fraud`. Colonnes `merchant_state` et `zip` retirées (remplacées en P3-07). 13 305 915 lignes avant et après.
