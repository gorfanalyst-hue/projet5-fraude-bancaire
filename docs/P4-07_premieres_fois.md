# P4-07 : Repérer les premières fois

## Pourquoi cette étape ?

Un fraudeur achète là où le titulaire n'achète jamais : un nouveau commerçant, un nouveau type de commerce, un autre pays. Repérer la première fois qu'un client fait quelque chose permet de signaler ce changement.

Le critère de fin du ticket est : **indicateurs vérifiés sur un client**.

## Où est le code ?

- `src/features.py` : `add_first_time_flags` et `check_first_time_flags`.
- `notebooks/04_table_analyse.ipynb` : section P4-07.

## La fonction `add_first_time_flags`

```python
def add_first_time_flags(df):
    order = _sort_order(df, "client_id")
    ordered = pd.DataFrame({
        "client_id": df["client_id"].to_numpy()[order],
        "merchant_id": df["merchant_id"].to_numpy()[order],
        "mcc": df["mcc"].to_numpy()[order],
        "country": df["merchant_country"].cat.codes.to_numpy()[order],
    })
    for col, name in [("merchant_id", "is_first_merchant"), ("mcc", "is_first_mcc"),
                      ("country", "is_first_country")]:
        first = (~ordered.duplicated(["client_id", col])).to_numpy()
        df[name] = _back_to_original(first, order, np.int8)
    rank = ordered.groupby("client_id").cumcount().to_numpy()
    df["client_tx_rank"] = _back_to_original(rank, order, np.int32)
    return df
```

| Syntaxe | Rôle |
| --- | --- |
| `_sort_order(df, "client_id")` | Range les transactions de chaque client dans l'ordre chronologique. |
| `~ordered.duplicated(["client_id", col])` | Vaut vrai la première fois qu'un couple (client, commerçant), (client, catégorie) ou (client, pays) apparaît. |
| `merchant_country` | Pays du commerçant (P3-07). « ONLINE » compte comme un lieu : le premier achat en ligne est aussi une première fois. |
| `client_tx_rank` | Nombre de transactions précédentes du client (0 pour la première). |

Au début de l'historique d'un client, tout est une première fois. `client_tx_rank` permet aux règles de la phase 7 de ne garder que les premières fois après 100 transactions.

## Résultats obtenus

| Indicateur | Toutes les transactions | Après 100 transactions du client |
| --- | --- | --- |
| `is_first_merchant` | 357 697 | 318 859 |
| `is_first_mcc` | 94 163 | 67 657 |
| `is_first_country` | 6 615 | 4 135 |

Client vérifié : client 363, 9 832 transactions, toutes identiques au recalcul.

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne tient pas compte du temps écoulé : un commerçant revu après cinq ans n'est plus une première fois.

## À noter dans le journal des transformations (P3-12)

Quatre colonnes ajoutées : `is_first_merchant`, `is_first_mcc`, `is_first_country` et `client_tx_rank`.
