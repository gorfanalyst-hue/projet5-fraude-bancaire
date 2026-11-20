# P4-03 : Calculer l'âge du client à la date de la transaction

## Pourquoi cette étape ?

`current_age` donne l'âge du client en février 2020 (P2-12). Pour une transaction de 2010, ce client avait jusqu'à dix ans de moins. Utiliser `current_age` fausserait toute analyse par âge, et la vérification éthique du score (P9-15).

Le critère de fin du ticket est : **âges vérifiés à la main sur 10 transactions**.

## Où est le code ?

- `src/features.py` : `add_age_at_transaction` et `check_age`.
- `notebooks/04_table_analyse.ipynb` : section P4-03.

## La fonction `add_age_at_transaction`

```python
def add_age_at_transaction(df):
    birthday_not_reached = (df["month"] < df["birth_month"]).astype("int16")
    age = df["year"].astype("int16") - df["birth_year"].astype("int16") - birthday_not_reached
    df["age_at_transaction"] = age.astype("int8")
    return df
```

| Syntaxe | Rôle |
| --- | --- |
| `df["year"] - df["birth_year"]` | Âge atteint dans l'année de la transaction. |
| `df["month"] < df["birth_month"]` | Vaut 1 si l'anniversaire n'est pas encore passé : on retire alors un an. |

Le jour de naissance n'est pas connu : l'anniversaire compte à partir du premier jour du mois de naissance.

`check_age` affiche, pour 10 transactions tirées au hasard, le calcul écrit en clair (exemple : `2010 - 1971 - 1 = 38`) et le compare à la colonne calculée.

## Résultats obtenus

| Contrôle | Résultat |
| --- | --- |
| 10 transactions vérifiées à la main | 10 identiques |
| Âge à la transaction | de 17 à 101 ans |
| Écart avec `current_age` | de 0 à 11 ans |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne met pas l'âge dans le score de risque : ce choix est discuté en P9-15.

## À noter dans le journal des transformations (P3-12)

Colonne `age_at_transaction` (int8) ajoutée : année de la transaction - `birth_year` - 1 si le mois de naissance n'est pas encore atteint.
