# P4-05 : Mesurer la fréquence d'utilisation de la carte

## Pourquoi cette étape ?

Une carte volée est souvent utilisée plusieurs fois très vite, avant que le titulaire ne s'en rende compte. Compter les transactions récentes de la carte permet de repérer ces rafales.

Le critère de fin du ticket est : **colonnes vérifiées sur une carte**.

## Où est le code ?

- `src/features.py` : `count_previous_in_window`, `add_card_frequency` et `recount_card_activity`.
- `notebooks/04_table_analyse.ipynb` : section P4-05.

## La fonction `count_previous_in_window`

Une boucle sur 13 millions de lignes serait beaucoup trop lente. La fonction trie les lignes par carte et par date, puis fait une recherche binaire sur toute la table d'un coup.

```python
def count_previous_in_window(df, group_col, window_minutes, values=None):
    order = _sort_order(df, group_col)
    minutes = _minutes(df["date"])[order]
    group = df[group_col].to_numpy()[order].astype(np.int64)
    key = group * _GROUP_OFFSET + (minutes - minutes.min())

    start = np.searchsorted(key, key - window_minutes, side="right")
    position = np.arange(len(key))
    if values is None:
        counts = position - start
    ...
    return _back_to_original(counts, order, np.int32)
```

| Syntaxe | Rôle |
| --- | --- |
| `key = group * _GROUP_OFFSET + minutes` | Une seule clé qui range les lignes par carte, puis par minute. L'écart entre deux cartes (10 millions) est plus grand que toute la période : une fenêtre ne déborde jamais sur une autre carte. |
| `np.searchsorted(key, key - window_minutes, side="right")` | Pour chaque ligne, première position dont la date est dans la fenêtre. |
| `position - start` | Nombre de lignes de la même carte entre le début de la fenêtre et la ligne : ce sont les transactions précédentes. |
| `_back_to_original` | Remet les résultats dans l'ordre de la table. |

`add_card_frequency` appelle cette fonction avec une fenêtre de 60 minutes (`card_tx_1h`) et de 24 heures (`card_tx_24h`).

`recount_card_activity` recompte, pour une carte, les transactions précédentes avec une boucle simple qui remonte dans le temps.

## Résultats obtenus

| Contrôle ou mesure | Résultat |
| --- | --- |
| Carte vérifiée | carte 2048 : 4 693 transactions, toutes identiques au recompte |
| Temps de calcul | 32 s |
| Médiane | 0 dans l'heure, 1 dans les 24 heures |
| Quantile 99,9 % | 5 dans l'heure, 14 dans les 24 heures |
| Maximum | 12 dans l'heure, 30 dans les 24 heures |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne dit pas à partir de combien de transactions une rafale est suspecte : ce sont les règles R04 et R05 de P7-01.

## À noter dans le journal des transformations (P3-12)

Deux colonnes ajoutées : `card_tx_1h` et `card_tx_24h`, transactions précédentes de la même carte dans l'heure et dans les 24 heures.
