# P3-06 : Transformer la colonne errors

## Pourquoi cette étape ?

Dans `transactions_data.csv`, la colonne `errors` est un texte : elle est vide quand la transaction s'est bien passée, et contient un ou plusieurs types d'erreur, séparés par une virgule, quand elle a échoué. Tant qu'elle reste dans ce format, on ne peut ni compter facilement les erreurs d'un type donné, ni les croiser avec d'autres variables, ni s'en servir dans un modèle.

On la transforme donc en colonnes binaires (0 ou 1), plus simples à manipuler :

- une colonne par type d'erreur ;
- un indicateur « au moins une erreur » ;
- un indicateur « échec d'authentification ».

Ces colonnes alimenteront l'indicateur P4-06 (échecs d'authentification récents sur une carte), l'analyse des erreurs et des refus (P6-06) et le score de risque (Phase 7).

Le critère de fin du ticket est : **totaux identiques à ceux de P2-13**.

## Les sept types d'erreur

Le diagnostic montre sept types, tous connus :

| Type d'erreur | Occurrences | Part des occurrences |
|---|---|---|
| Insufficient Balance (solde insuffisant) | 131 621 | 62,0 % |
| Bad PIN | 32 482 | 15,3 % |
| Technical Glitch (incident technique) | 26 633 | 12,5 % |
| Bad Card Number | 7 925 | 3,7 % |
| Bad Expiration | 6 295 | 3,0 % |
| Bad CVV | 6 241 | 2,9 % |
| Bad Zipcode | 1 138 | 0,5 % |
| **Total** | **212 335** | **100 %** |

Ce sont des **occurrences** : une transaction qui cumule deux erreurs est comptée deux fois.

Les cinq erreurs dont le nom commence par « Bad » sont des **échecs d'authentification** : le client ou la carte n'a pas fourni la bonne information (PIN, CVV, numéro, date d'expiration, code postal). Elles forment l'indicateur `has_auth_error`. Les deux autres (solde insuffisant et incident technique) n'en font pas partie.

## Où est le code ?

Dans `src/clean_data.py`. Le code a été écrit par Martin ; un contrôle des types d'erreur inconnus y a été ajouté lors de la relecture.

## Les constantes

```python
ALL_ERROR_TYPES = [
    "Bad PIN", "Bad CVV", "Bad Card Number", "Bad Expiration",
    "Bad Zipcode", "Insufficient Balance", "Technical Glitch",
]

AUTH_ERROR_TYPES = [
    "Bad PIN", "Bad CVV", "Bad Card Number", "Bad Expiration", "Bad Zipcode",
]
```

`ALL_ERROR_TYPES` liste les sept types, `AUTH_ERROR_TYPES` le sous-ensemble des échecs d'authentification. Si un nouveau type apparaissait un jour dans les données, il faudrait l'ajouter ici : le contrôle ci-dessous le signalerait.

## Fonction 1 : `transform_errors_column`

```python
def transform_errors_column(df, error_col="errors"):
    s_err = df[error_col].astype("string").fillna("")

    df["has_error"] = (s_err != "").astype("int8")

    unique_vals = s_err.unique()
    for err_type in ALL_ERROR_TYPES:
        col_name = _slugify_error_name(err_type)
        mapping = {
            val: int(err_type in [token.strip() for token in val.split(",")])
            for val in unique_vals
        }
        df[col_name] = s_err.map(mapping).astype("int8")

    auth_cols = [_slugify_error_name(e) for e in AUTH_ERROR_TYPES]
    df["has_auth_error"] = (df[auth_cols].sum(axis=1) > 0).astype("int8")
    return df
```

### Explication

| Syntaxe | Rôle |
|---|---|
| `.astype("string").fillna("")` | Convertit la colonne en texte et remplace les valeurs vides (transactions sans erreur) par une chaîne vide. |
| `(s_err != "").astype("int8")` | `has_error` vaut 1 si le texte n'est pas vide. Le type `int8` prend un seul octet par ligne, ce qui limite la mémoire sur 13 millions de lignes. |
| `s_err.unique()` | Liste les **valeurs distinctes** de la colonne (quelques dizaines de combinaisons), au lieu de travailler sur 13 millions de lignes. |
| `val.split(",")` puis `token.strip()` | Découpe une valeur sur la virgule et retire les espaces autour de chaque morceau. |
| `err_type in [...]` | Teste la présence **exacte** du type d'erreur parmi les morceaux. Une recherche de texte simple pourrait confondre deux types dont les noms se ressemblent. |
| `mapping` | Dictionnaire `valeur : 0 ou 1`, calculé une seule fois par valeur distincte. |
| `s_err.map(mapping)` | Applique ce dictionnaire à toute la colonne : c'est l'astuce qui rend la transformation rapide. |
| `_slugify_error_name` | Construit le nom de la colonne : `Bad Card Number` devient `err_bad_card_number`. |
| `df[auth_cols].sum(axis=1) > 0` | Additionne les cinq colonnes d'authentification sur chaque ligne : si le résultat est positif, l'indicateur `has_auth_error` vaut 1. |

Les colonnes créées sont : `has_error`, `err_bad_pin`, `err_bad_cvv`, `err_bad_card_number`, `err_bad_expiration`, `err_bad_zipcode`, `err_insufficient_balance`, `err_technical_glitch` et `has_auth_error`. La colonne d'origine `errors` est conservée.

## Fonction 2 : `check_errors_transformation`

```python
def check_errors_transformation(df, error_col="errors"):
    s_err = df[error_col].dropna().astype(str)
    ref_counts = s_err.str.split(",").explode().str.strip().value_counts()

    all_match = True
    for err_type in ALL_ERROR_TYPES:
        col_name = _slugify_error_name(err_type)
        col_total = int(df[col_name].sum()) if col_name in df.columns else 0
        ref_total = int(ref_counts.get(err_type, 0))
        all_match = all_match and (col_total == ref_total)
        ...

    inconnus = sorted(set(ref_counts.index) - set(ALL_ERROR_TYPES))
    all_match = all_match and not inconnus
    ...
```

### Explication

| Syntaxe | Rôle |
|---|---|
| `.str.split(",").explode()` | Découpe chaque valeur sur la virgule, puis place chaque morceau sur sa propre ligne. |
| `.value_counts()` | Compte les occurrences de chaque type : c'est la référence calculée directement sur les données d'origine. |
| `df[col_name].sum()` | Total de la colonne binaire (nombre de 1). |
| `col_total == ref_total` | Compare le total de la colonne créée avec la référence. |
| `set(ref_counts.index) - set(ALL_ERROR_TYPES)` | Repère les types présents dans les données mais absents de la liste du code. Sans ce test, un type oublié serait ignoré sans avertissement. |

La fonction retourne un résultat positif seulement si les sept totaux sont égaux **et** qu'il n'existe aucun type inconnu.

## Comment l'utiliser dans le notebook

```python
from src.clean_data import transform_errors_column, check_errors_transformation

df_transaction = transform_errors_column(df_transaction)
check_errors_transformation(df_transaction)
```

Après une modification de `clean_data.py`, il faut redémarrer le kernel.

## Résultats obtenus

| Colonne | Total | Référence P2-13 | Statut |
|---|---|---|---|
| `err_bad_pin` | 32 482 | 32 482 | OK |
| `err_bad_cvv` | 6 241 | 6 241 | OK |
| `err_bad_card_number` | 7 925 | 7 925 | OK |
| `err_bad_expiration` | 6 295 | 6 295 | OK |
| `err_bad_zipcode` | 1 138 | 1 138 | OK |
| `err_insufficient_balance` | 131 621 | 131 621 | OK |
| `err_technical_glitch` | 26 633 | 26 633 | OK |

| Indicateur | Transactions | Part du total |
|---|---|---|
| `has_error` (au moins une erreur) | 211 393 | 1,6 % |
| `has_auth_error` (échec d'authentification) | 53 977 | 0,4 % |

Aucun type d'erreur inconnu. **Critère de fin validé.**

### Contrôles de cohérence

- `has_error` (211 393) est inférieur au total des occurrences (212 335) : l'écart de 942 vient des transactions qui cumulent plusieurs erreurs. Il est supérieur à 131 621, le total du type le plus fréquent, ce qui est logique.
- `has_auth_error` (53 977) est inférieur à la somme des cinq erreurs d'authentification (54 081) : l'écart de 104 vient de transactions qui cumulent plusieurs erreurs d'authentification.

## Ce que cette étape ne fait PAS

- Elle ne supprime pas la colonne d'origine `errors`.
- Elle n'interprète pas les erreurs comme des fraudes : un solde insuffisant ou un incident technique n'est pas un signal de fraude. Le choix des erreurs utilisées comme indicateurs relève des Phases 4 et 7.
- Elle ne calcule pas les échecs « récents » sur une carte (dans les 24 heures précédentes) : c'est P4-06.

## À noter dans le journal des transformations (P3-12)

- Colonne `errors` transformée en 9 colonnes binaires de type `int8` : 7 types d'erreur, `has_error` et `has_auth_error`.
- Totaux identiques à la référence P2-13 pour les 7 types, aucun type inconnu.
- 211 393 transactions avec au moins une erreur (1,6 %), dont 53 977 avec un échec d'authentification (0,4 %).
- Les échecs d'authentification sont : Bad PIN, Bad CVV, Bad Card Number, Bad Expiration, Bad Zipcode.
