# P3-09 : Retirer les colonnes sensibles et inutiles

## Pourquoi cette étape ?

- **Colonnes sensibles :** `card_number` et `cvv` (cartes), `address` (clients). Elles ne servent à aucune analyse et ne doivent pas se retrouver dans les tables nettoyées, ni dans une sortie de notebook.
- **Colonne inutile :** `card_on_dark_web` a la même valeur pour les 6 146 cartes (P2-11).

Le critère de fin du ticket est : **colonnes absentes des tables nettoyées**.

## Où est le code ?

Dans `src/clean_data.py`, section P3-09.

```python
COLUMNS_TO_DROP = {
    "cards": ["card_number", "cvv", "card_on_dark_web"],
    "users": ["address"],
}

def drop_columns(df, columns):
    return df.drop(columns=[col for col in columns if col in df.columns])
```

| Syntaxe                                         | Rôle                                                                                          |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `COLUMNS_TO_DROP`                               | La liste des colonnes à retirer, au même endroit pour toute l'équipe.                         |
| `[col for col in columns if col in df.columns]` | Garde seulement les colonnes encore présentes : relancer la cellule ne provoque pas d'erreur. |
| `df.drop(columns=...)`                          | Retire les colonnes.                                                                          |

`check_columns_removed` vérifie, pour chaque colonne de la liste, qu'elle n'est plus dans sa table.

## Comment l'utiliser dans le notebook

```python
df_card = drop_columns(df_card, COLUMNS_TO_DROP["cards"])
df_users = drop_columns(df_users, COLUMNS_TO_DROP["users"])
check_columns_removed({"cards": df_card, "users": df_users})
```

## Résultats obtenus

| Table | Colonne            | Encore présente |
| ----- | ------------------ | --------------- |
| cards | `card_number`      | non             |
| cards | `cvv`              | non             |
| cards | `card_on_dark_web` | non             |
| users | `address`          | non             |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne modifie pas les fichiers bruts de `data/` : les colonnes y restent.
- Elle ne retire pas `latitude` et `longitude` des clients : elles décrivent la position, pas l'adresse exacte.
- Elle ne retire pas les colonnes d'origine `errors`, `merchant_state` et `zip`, gardées par P3-06 et P3-07.

## À noter dans le journal des transformations (P3-12)

- `cards` : 3 colonnes retirées (`card_number`, `cvv`, `card_on_dark_web`).
- `users` : 1 colonne retirée (`address`).
