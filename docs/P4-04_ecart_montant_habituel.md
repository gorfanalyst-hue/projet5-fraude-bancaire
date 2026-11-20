# P4-04 : Mesurer l'écart au montant habituel du client

## Pourquoi cette étape ?

Un achat de 300 $ est banal pour un client qui dépense souvent 200 $, mais très inhabituel pour un client qui paie surtout des péages à 4 $. Le montant seul ne suffit donc pas : il faut le comparer aux habitudes du client.

Le critère de fin du ticket est : **colonne vérifiée sur un client**.

## Où est le code ?

- `src/features.py` : `add_amount_gap` et `check_amount_gap`.
- `notebooks/04_table_analyse.ipynb` : section P4-04.

## La fonction `add_amount_gap`

```python
MIN_PURCHASES_HISTORY = 10

def add_amount_gap(df, min_history=MIN_PURCHASES_HISTORY):
    order = _sort_order(df, "client_id")
    client = df["client_id"].to_numpy()[order]
    amount = df["amount"].to_numpy()[order].astype("float64")

    purchases = pd.Series(np.where(amount > 0, amount, np.nan))
    previous = purchases.groupby(client).shift(1)
    med = (previous.groupby(client).expanding(min_periods=min_history).median()
           .reset_index(level=0, drop=True).sort_index().to_numpy())
    df["client_median_amount"] = _back_to_original(med, order, np.float32)
    df["amount_gap"] = (df["amount"] - df["client_median_amount"]).astype("float32")
    df["amount_ratio"] = (df["amount"] / df["client_median_amount"]).astype("float32")
    return df
```

| Syntaxe | Rôle |
| --- | --- |
| `_sort_order(df, "client_id")` | Ordre des lignes trié par client, puis par date, puis par identifiant. |
| `np.where(amount > 0, amount, np.nan)` | Seuls les achats comptent : les remboursements et les montants nuls deviennent vides. |
| `groupby(client).shift(1)` | Décale d'une ligne dans chaque client : la transaction en cours n'entre jamais dans son propre calcul. |
| `expanding(min_periods=10).median()` | Médiane de tous les achats précédents, à partir de 10 achats. Avant, la valeur reste vide. |
| `amount_gap` | Écart en dollars au montant habituel. |
| `amount_ratio` | Rapport au montant habituel : 2 veut dire deux fois le montant habituel. |

La médiane est préférée à la moyenne : un seul très gros achat ne la déplace presque pas.

`check_amount_gap` reprend toutes les transactions d'un client avec une boucle Python simple (`statistics.median`) et compare.

## Résultats obtenus

| Contrôle ou mesure | Résultat |
| --- | --- |
| Client vérifié | client 363 : 9 832 transactions, toutes identiques au recalcul |
| Temps de calcul | 37 s |
| Transactions sans montant habituel (moins de 10 achats précédents) | 12 787 |
| Rapport médian (achats) | 1,00 |
| Rapport au quantile 99 % | 16,85 |
| Rapport au quantile 99,9 % | 61,63 |
| Achats à 10 fois le montant habituel ou plus | 305 792 |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne fixe pas le seuil d'un montant « inhabituel » : c'est la règle R03 de P7-01 (20 fois le montant habituel et 300 $ ou plus).

## À noter dans le journal des transformations (P3-12)

Trois colonnes ajoutées : `client_median_amount` (médiane des achats précédents du client, à partir de 10 achats), `amount_gap` et `amount_ratio`. 12 787 valeurs vides, expliquées.
