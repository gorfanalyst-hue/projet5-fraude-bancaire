# P3-01 — Fonction de chargement commune des données

## Pourquoi une fonction commune ?

Jusqu'ici, chacun chargeait les fichiers à sa façon (`pd.read_csv("fichier.csv")` tout simple). Le problème : pandas devine automatiquement les types de chaque colonne, et il devine presque toujours trop large (`int64` au lieu de `int8`/`int16`, `object` au lieu de `category`). Sur un petit fichier ça ne change rien, mais sur `transactions_data.csv` (13 millions de lignes), ça peut faire la différence entre un notebook fluide et un notebook qui plante par manque de mémoire.

L'objectif de cette tâche est donc d'avoir **un seul code de chargement, partagé par toute l'équipe**, pour que :

- tout le monde travaille avec les mêmes types de données dès le départ
- on évite que chacun réinvente sa propre façon de lire les fichiers
- les futures étapes de nettoyage (P3-02, P3-03...) partent toutes de la même base

## Ce que fait la fonction

Le fichier `src/load_data.py` contient 4 fonctions : `load_transactions()`, `load_cards()`, `load_users()` et `load_mcc_codes()`, ainsi qu'une fonction interne `load_csv_chunked()`.

Chacune fait deux choses :

1. **Lit le fichier par morceaux (chunks)** plutôt que d'un coup, pour limiter la charge mémoire pendant la lecture elle-même (surtout utile pour le fichier des transactions).
2. **Impose des types de données légers** dès la lecture, par exemple :
   - `int32` ou `int8` pour les identifiants et petits nombres (au lieu du `int64` par défaut)
   - `category` pour les colonnes répétitives comme `card_brand`, `merchant_city`, `errors` (au lieu de `object`), ce qui économise énormément de mémoire quand peu de valeurs différentes se répètent des millions de fois
   - `datetime` directement pour la colonne `date` des transactions

## Où sont lus les fichiers ?

Les fonctions lisent les fichiers dans le dossier `data/` à la racine du dépôt. Le chemin est calculé automatiquement par la constante `DATA_DIR`, à partir de l'emplacement de `load_data.py`. Il ne dépend donc pas du dossier d'où le notebook est lancé.

Chacun doit placer les cinq fichiers de données dans son propre dossier `data/` (ce dossier n'est pas versionné dans Git) :

- `transactions_data.csv`
- `cards_data.csv`
- `users_data.csv`
- `mcc_codes.json`
- `fraud_labels.json`

## Ce que la fonction ne fait PAS (volontairement)

Certaines colonnes restent **telles quelles pour l'instant** :

- Les montants en texte avec `$` (`amount`, `credit_limit`, `yearly_income`, etc.) → traités dans **P3-02**
- Les dates au format `mm/aaaa` (`expires`, `acct_open_date`) → traitées dans **P3-03**

**Pourquoi ne pas tout faire d'un coup ?** Pour que chaque transformation reste **séparée et traçable** dans le journal des transformations (P3-12). Si on mélange tout dans une seule fonction, on perd la trace de « qui a changé quoi et pourquoi » étape par étape.

## Comment l'utiliser

```python
from src.load_data import load_transactions, load_cards, load_users, load_mcc_codes

df_transaction = load_transactions()
df_card = load_cards()
df_users = load_users()
df_mcc = load_mcc_codes()
```

**Important** : à partir de maintenant, on importe ces fonctions plutôt que de refaire un `pd.read_csv()` à la main dans son propre notebook, sinon on perd l'intérêt d'avoir une base commune.

Si l'import échoue avec `ModuleNotFoundError: No module named 'src'`, vérifier que VS Code a bien ouvert le dossier **racine du dépôt** et que le fichier `.vscode/settings.json` est présent.

## Comment vérifier que ça fonctionne

Un petit contrôle rapide après chargement :

```python
for name, df in [("transactions", df_transaction), ("cards", df_card),
                  ("users", df_users), ("mcc", df_mcc)]:
    print(f"{name}: {df.shape[0]:,} lignes, {df.shape[1]} colonnes, "
          f"{df.memory_usage(deep=True).sum()/1e6:.1f} MB")
```

Si on compare avec une lecture « brute » (sans `dtype` précisé), on doit voir une réduction nette de la mémoire utilisée : c'est le signe que la fonction fait son travail.

## Correction : garder le type `category` (P3-01, 29 octobre 2026)

### Le problème

La lecture par morceaux produit un tableau par morceau. Dans chaque morceau, une colonne de type `category` a ses propres catégories. Si ces catégories ne sont pas exactement les mêmes dans tous les morceaux, `pd.concat` remet la colonne en texte (`object`).

Avant la correction, `use_chip`, `merchant_city`, `merchant_state` et `errors` étaient donc en `object` après le chargement de `transactions_data.csv`.

### La correction

Dans `load_csv_chunked`, après la concaténation :

```python
if dtype:
    for col, col_type in dtype.items():
        if col_type == "category" and col in df.columns:
            df[col] = df[col].astype("category")
```

| Syntaxe | Rôle |
|---|---|
| `for col, col_type in dtype.items()` | Parcourt les types demandés au chargement. |
| `col_type == "category" and col in df.columns` | Garde les colonnes qui devaient être des catégories et qui ont bien été lues. |
| `df[col].astype("category")` | Remet le type `category` sur la table complète. |

En pratique, seul `load_transactions` est concerné : `cards_data.csv` et `users_data.csv` tiennent en un seul morceau.

### Résultats sur le fichier complet des transactions

| Mesure | Avant | Après |
|---|---|---|
| Colonnes de type `category` | aucune | `use_chip`, `merchant_city`, `merchant_state`, `errors` |
| `memory_usage(deep=True)` | 4 321,9 Mo | 1 371,0 Mo |
| `memory_usage(deep=False)` | 984,6 Mo | 639,1 Mo |
| Mémoire ajoutée par une copie de la table | 832 Mo | 312 Mo |
| Regroupement par ville (`groupby`) | 1,0 s | 0,2 s |
| Mémoire du processus après le chargement | 1 476 Mo | 1 485 Mo |

- La mémoire mesurée par pandas baisse fortement.
- La mémoire du processus juste après le chargement ne change presque pas.
- Le gain se voit dans les étapes suivantes : une copie de la table coûte 312 Mo au lieu de 832 Mo, et un regroupement par ville prend 0,2 s au lieu de 1,0 s.

La colonne `amount` reste en texte : sa conversion se fait en P3-02.
