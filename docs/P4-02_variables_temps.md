# P4-02 : Créer les variables de temps

## Pourquoi cette étape ?

La date seule ne permet pas de comparer les habitudes. Pour savoir si les clients achètent plus le week-end ou la nuit, ou si l'activité change selon le mois, il faut découper la date en variables simples.

Le critère de fin du ticket est : **colonnes vérifiées sur un échantillon**.

## Où est le code ?

- `src/features.py` : `add_time_features` et `check_time_features`.
- `notebooks/04_table_analyse.ipynb` : section P4-02.

## La fonction `add_time_features`

```python
NIGHT_END_HOUR = 6

def add_time_features(df):
    dates = df["date"]
    df["year"] = dates.dt.year.astype("int16")
    df["month"] = dates.dt.month.astype("int8")
    df["weekday"] = dates.dt.weekday.astype("int8")
    df["hour"] = dates.dt.hour.astype("int8")
    df["is_night"] = (df["hour"] < NIGHT_END_HOUR).astype("int8")
    df["is_weekend"] = (df["weekday"] >= 5).astype("int8")
    return df
```

| Colonne | Contenu |
| --- | --- |
| `year`, `month`, `hour` | Année, mois (1 à 12), heure (0 à 23) |
| `weekday` | Jour de la semaine : 0 = lundi, 6 = dimanche |
| `is_night` | 1 si la transaction a lieu entre 0 h et 5 h 59 |
| `is_weekend` | 1 le samedi et le dimanche |

Les types `int8` et `int16` prennent 4 à 8 fois moins de mémoire que le type par défaut.

`check_time_features` tire 10 transactions au hasard et recalcule chaque variable ligne par ligne, avec les objets date de Python.

## Résultats obtenus

| Contrôle | Résultat |
| --- | --- |
| Échantillon de 10 transactions | 10 sur 10 identiques au recalcul |
| Transactions de nuit (0 h à 5 h 59) | 770 383 |
| Transactions le week-end | 3 801 414 |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle n'analyse pas l'effet du jour et de l'heure : c'est P6-03.

## À noter dans le journal des transformations (P3-12)

Six colonnes ajoutées à la table d'analyse : `year`, `month`, `weekday`, `hour`, `is_night` (0 h à 5 h 59), `is_weekend`.
