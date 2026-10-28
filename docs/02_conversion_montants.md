# P3-02 — Conversion des montants en nombres

## Pourquoi cette étape ?

Plusieurs colonnes financières sont lues comme du **texte** (type `object`) parce qu'elles contiennent le symbole `$` (et parfois des virgules) :

| Fichier | Colonnes concernées |
|---|---|
| `transactions_data.csv` | `amount` |
| `cards_data.csv` | `credit_limit` |
| `users_data.csv` | `per_capita_income`, `yearly_income`, `total_debt` |

Tant qu'elles sont en texte, impossible de calculer une moyenne, une médiane, un écart au montant habituel (P4-04) ou de comparer deux montants. Il faut les convertir en nombres décimaux (`float`).

Attention au format des montants négatifs : le signe moins est écrit **après** le `$` (exemple : `$-77.00`). La conversion doit donc d'abord retirer le `$`, puis lire le nombre avec son signe.

## Où est le code ?

Dans un fichier séparé, `src/clean_data.py`, qui contient les fonctions de **transformation**. Le fichier `src/load_data.py` ne fait que **charger** les données. Cette séparation permet de tracer chaque étape dans le journal des transformations (P3-12).

## Fonction 1 : `convert_currency_column`

Elle prend une colonne texte et retourne une colonne numérique.

```python
def convert_currency_column(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")
```

### Explication ligne par ligne

| Syntaxe | Rôle |
|---|---|
| `series.astype(str)` | Force tout en texte pour que les opérations `.str` fonctionnent sur toutes les valeurs. Les valeurs manquantes deviennent le texte `"nan"`, qui sera reconverti en `NaN` à la dernière étape. |
| `.str.replace("$", "", regex=False)` | Supprime le symbole `$`. Le paramètre `regex=False` est important : en mode regex, `$` signifie « fin de chaîne » et ne retirerait rien. |
| `.str.replace(",", "", regex=False)` | Supprime les séparateurs de milliers (`1,234.56` devient `1234.56`). |
| `.str.strip()` | Retire les espaces au début et à la fin. |
| `pd.to_numeric(..., errors="coerce")` | Convertit en nombre. Toute valeur impossible à convertir devient `NaN` au lieu de provoquer une erreur. |

Les enchaînements `.str.replace(...).str.replace(...)` se lisent de haut en bas : chaque opération s'applique au résultat de la précédente.

### Exemples

| Texte d'origine | Résultat |
|---|---|
| `$14.57` | `14.57` |
| `$-77.00` | `-77.0` |
| `$24295` | `24295.0` |
| `$1,234.56` | `1234.56` |
| `abc` | `NaN` |

## Fonction 2 : `report_conversion_issues`

Le critère de fin de P3-02 est : **« Aucune valeur non convertie, ou cas listés »**. Cette fonction vérifie exactement cela.

```python
def report_conversion_issues(original: pd.Series, converted: pd.Series, label: str):
    failed_mask = converted.isna() & original.notna()
    n_failed = failed_mask.sum()
    print(f"{label}: {n_failed} valeur(s) non convertie(s)")
    if n_failed > 0:
        print(original[failed_mask].unique()[:10])
```

### Explication

| Syntaxe | Rôle |
|---|---|
| `converted.isna() & original.notna()` | Repère les lignes où la valeur **était présente** avant la conversion mais **est devenue vide** après. Ce sont les vraies erreurs de conversion. Une valeur déjà manquante au départ n'est pas comptée. |
| `failed_mask.sum()` | Compte les lignes en échec (`True` vaut 1, `False` vaut 0). |
| `original[failed_mask].unique()[:10]` | Affiche jusqu'à 10 valeurs distinctes qui ont posé problème, pour pouvoir les documenter. |

## Comment l'utiliser dans le notebook

On garde une copie de la colonne **avant** conversion, puis on compare :

```python
from src.clean_data import convert_currency_column, report_conversion_issues

original = df_transaction["amount"].copy()
df_transaction["amount"] = convert_currency_column(df_transaction["amount"])
report_conversion_issues(original, df_transaction["amount"], "transactions.amount")
```

Pour les trois colonnes de la table des clients, une boucle évite de répéter le code :

```python
for col in ["per_capita_income", "yearly_income", "total_debt"]:
    original = df_users[col].copy()
    df_users[col] = convert_currency_column(df_users[col])
    report_conversion_issues(original, df_users[col], f"users.{col}")
```

Le `.copy()` est nécessaire : sans lui, `original` pointerait vers la même colonne et serait modifié en même temps.

## Ce que cette étape ne fait PAS

- **Les montants négatifs ne sont pas corrigés ni supprimés.** Ils correspondent probablement à des remboursements. Leur traitement (garder, exclure ou marquer d'un indicateur) relève de **P3-08**.
- **Les revenus ou limites de crédit nuls ne sont pas modifiés.** Même règle : P3-08.
- **Les dates ne sont pas converties.** C'est le sujet de **P3-03**.

## À noter dans le journal des transformations (P3-12)

Pour chaque colonne : nombre de valeurs avant et après conversion, nombre de valeurs non converties (idéalement 0), et type de la colonne avant (`object`) et après (`float64`).
