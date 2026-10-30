# P3-10 : Enregistrer les tables nettoyées

## Pourquoi cette étape ?

Refaire tout le nettoyage à chaque séance prend du temps et beaucoup de mémoire. Les tables nettoyées sont donc enregistrées une fois, puis relues directement par les phases suivantes.

Le format Parquet garde les types (nombres, dates, catégories) et prend moins de place qu'un CSV.

Le critère de fin du ticket est : **tables rechargées en quelques secondes**.

## Où sont les fichiers ?

Dans `data/clean/`. Comme tout le dossier `data/`, il n'est pas versionné : chaque membre crée ses fichiers en exécutant `notebooks/03_nettoyage_transformation.ipynb`.

| Fichier | Lignes | Colonnes | Taille | Contenu |
|---|---|---|---|---|
| `transactions.parquet` | 13 305 915 | 30 | 320,0 Mo | Transactions nettoyées, avec les colonnes des erreurs (P3-06), du lieu (P3-07) et les indicateurs de P3-08 |
| `cards.parquet` | 6 146 | 11 | 0,1 Mo | Cartes, sans les colonnes retirées en P3-09, avec `zero_credit_limit` |
| `users.parquet` | 2 000 | 14 | 0,1 Mo | Clients, sans `address`, avec `suspicious_income` |
| `mcc.parquet` | 109 | 4 | 0,0 Mo | Codes MCC avec leur famille et leur description en français |
| `fraud_labels.parquet` | 8 914 963 | 2 | 41,0 Mo | Étiquettes de fraude : `id` et `is_fraud` |

## Où est le code ?

- `src/clean_data.py` : `save_clean_tables`, qui enregistre chaque table et retourne le nombre de lignes, de colonnes et la taille de chaque fichier.
- `src/load_data.py` : `load_clean_table`, qui relit une table.

```python
def load_clean_table(name, columns=None, folder=CLEAN_DIR):
    return pd.read_parquet(folder / f"{name}.parquet", columns=columns)
```

| Syntaxe | Rôle |
|---|---|
| `name` | Nom de la table : `"transactions"`, `"cards"`, `"users"`, `"mcc"` ou `"fraud_labels"`. |
| `columns` | Liste de colonnes à lire. Sans liste, toute la table est lue. |
| `pd.read_parquet` | Lit le fichier. Il faut le paquet `pyarrow`, déjà dans `requirements.txt`. |

## Comment l'utiliser dans les phases suivantes

```python
from src.load_data import load_clean_table

df_transaction = load_clean_table("transactions")
df_card = load_clean_table("cards")

# Seulement quelques colonnes, pour économiser la mémoire
df_tx = load_clean_table("transactions", columns=["id", "date", "amount"])

# Étiquettes de fraude : table à part, à joindre par id (voir P2-17)
df_labels = load_clean_table("fraud_labels")
```

## Résultats obtenus

| Table | Secondes de lecture |
|---|---|
| transactions | 7,6 |
| cards | 0,0 |
| users | 0,0 |
| mcc | 0,0 |
| fraud_labels | 0,2 |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne joint pas les tables entre elles : c'est P4-01, qui construit la table d'analyse.
- Elle ne versionne pas les fichiers : ils restent sur l'ordinateur de chacun.

## À noter dans le journal des transformations (P3-12)

Cinq tables enregistrées au format Parquet dans `data/clean/`. Relecture : 7,6 s pour les transactions, 0,2 s pour les étiquettes, 0,0 s pour les trois autres.
