# P3-03 : Conversion des dates

## Pourquoi cette étape ?

Deux colonnes de la table des cartes contiennent des dates écrites en texte au format `mm/aaaa` (par exemple `12/2022`) :

| Fichier | Colonne | Contenu |
|---|---|---|
| `cards_data.csv` | `expires` | Date d'expiration de la carte |
| `cards_data.csv` | `acct_open_date` | Date d'ouverture du compte |

Tant qu'elles sont en texte, on ne peut ni les comparer, ni calculer une durée (ancienneté du compte, temps restant avant l'expiration), ni les croiser avec la date des transactions (P4-02, P4-03).

La colonne `date` de `transactions_data.csv` est déjà lue comme une vraie date par `load_transactions()` (paramètre `parse_dates`). Elle n'a pas besoin d'être convertie, seulement **vérifiée**.

## Un choix à documenter : quel jour du mois ?

Le format `mm/aaaa` ne contient pas de jour. Pandas choisit le 1er du mois par défaut. C'est acceptable pour l'ouverture d'un compte, mais pas pour l'expiration d'une carte :

- une carte qui expire en `12/2022` est valable **jusqu'au 31 décembre 2022**
- avec le 1er décembre, une transaction du 15 décembre paraîtrait faite après l'expiration

Choix retenu :

| Colonne | Jour retenu |
|---|---|
| `acct_open_date` | 1er du mois |
| `expires` | Dernier jour du mois |

Ce choix doit figurer dans le journal des transformations (P3-12).

## Où est le code ?

Dans `src/clean_data.py`, avec les fonctions de nettoyage déjà écrites pour P3-02.

## Fonction 1 : `convert_month_year_column`

```python
def convert_month_year_column(series: pd.Series, end_of_month: bool = False) -> pd.Series:
    dates = pd.to_datetime(series, format="%m/%Y", errors="coerce")
    if end_of_month:
        dates = dates + pd.offsets.MonthEnd(0)
    return dates
```

### Explication

| Syntaxe | Rôle |
|---|---|
| `pd.to_datetime(series, ...)` | Convertit une colonne de texte en dates. |
| `format="%m/%Y"` | Décrit le format attendu : `%m` pour le mois sur deux chiffres, `%Y` pour l'année sur quatre chiffres. Préciser le format évite les erreurs d'interprétation et accélère la conversion. |
| `errors="coerce"` | Toute valeur impossible à convertir devient `NaT` (l'équivalent de `NaN` pour les dates) au lieu de provoquer une erreur. |
| `end_of_month=False` | Paramètre qui choisit le jour retenu. Par défaut, c'est le 1er du mois. |
| `pd.offsets.MonthEnd(0)` | Avance la date jusqu'à la fin de son mois. Le `0` signifie « reste dans le mois courant » : sans lui, la date sauterait au mois suivant. |

### Exemples

| Texte d'origine | `end_of_month=False` | `end_of_month=True` |
|---|---|---|
| `12/2022` | 2022-12-01 | 2022-12-31 |
| `02/2024` | 2024-02-01 | 2024-02-29 |
| `09/2002` | 2002-09-01 | 2002-09-30 |
| `abc` | `NaT` | `NaT` |

La conversion tient compte des mois de longueur différente et des années bissextiles (février 2024 se termine le 29).

## Fonction 2 : `check_datetime_column`

```python
def check_datetime_column(series: pd.Series, label: str):
    print(f"{label}: type={series.dtype}, "
          f"manquantes={series.isna().sum()}, "
          f"min={series.min()}, max={series.max()}")
```

Elle affiche en une ligne le type de la colonne, le nombre de dates manquantes et la plage de dates. On s'en sert pour vérifier chaque colonne de date après conversion.

## Comment l'utiliser dans le notebook

```python
from src.clean_data import (
    convert_month_year_column, check_datetime_column, report_conversion_issues
)

original = df_card["expires"].copy()
df_card["expires"] = convert_month_year_column(df_card["expires"], end_of_month=True)
report_conversion_issues(original, df_card["expires"], "cards.expires")

original = df_card["acct_open_date"].copy()
df_card["acct_open_date"] = convert_month_year_column(df_card["acct_open_date"])
report_conversion_issues(original, df_card["acct_open_date"], "cards.acct_open_date")

check_datetime_column(df_card["expires"], "cards.expires")
check_datetime_column(df_card["acct_open_date"], "cards.acct_open_date")
check_datetime_column(df_transaction["date"], "transactions.date")
```

La fonction `report_conversion_issues` est celle de P3-02 : elle compte les valeurs présentes avant la conversion qui sont devenues vides après.

## Résultats attendus

- `cards.expires` et `cards.acct_open_date` : **0 valeur non convertie**, type `datetime64[ns]`
- `transactions.date` : type `datetime64[ns]`, aucune date manquante, plage de **janvier 2010 à octobre 2019**. Cette plage est cohérente avec l'année de référence 2019 trouvée dans la table des clients.

## Contrôle de cohérence

Une carte ne peut pas expirer avant l'ouverture du compte :

```python
print((df_card["expires"] < df_card["acct_open_date"]).sum())
```

Résultat attendu : **0**. S'il est supérieur, aucune correction n'est faite ici. On note le nombre de cas et quelques exemples, qui seront traités dans **P3-08** (valeurs suspectes).

## Ce que cette étape ne fait PAS

- Elle ne repère pas les transactions faites **après** l'expiration de la carte. Cet indicateur potentiel de fraude relève de la Phase 4.
- Elle ne modifie pas `year_pin_last_changed`, qui est déjà une année sous forme de nombre entier.
- Elle ne corrige aucune valeur suspecte (P3-08).

## À noter dans le journal des transformations (P3-12)

Pour chaque colonne : type avant (`object`) et après (`datetime64[ns]`), nombre de valeurs non converties (idéalement 0), plage de dates obtenue, et le choix du jour du mois (1er pour `acct_open_date`, dernier jour pour `expires`) avec sa justification.
