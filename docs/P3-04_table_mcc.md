# P3-04 : Table des catégories MCC

## Pourquoi cette étape ?

Dans `transactions_data.csv`, la colonne `mcc` contient un code numérique à quatre chiffres (par exemple `5812`) qui désigne le type de commerçant. Ce code ne dit rien à un lecteur. Le fichier `mcc_codes.json` fait la correspondance entre chaque code et sa description (par exemple `5812` : « Eating Places and Restaurants »).

Cette table est une **table de dimension** : elle est petite (109 codes) et sert à donner du sens à la table de faits (13 millions de transactions). Elle sera utilisée pour :

- regrouper les codes en familles lisibles (P3-05)
- analyser les comportements par catégorie de commerçant (P6-05)
- créer des indicateurs de contexte (P4-08)

Le critère de fin du ticket est : **jointure avec les transactions sans perte**.

## Ce qui est déjà fait avant cette tâche

La fonction `load_mcc_codes()` (P3-01) lit déjà `mcc_codes.json` et convertit les codes du JSON, qui sont écrits en texte (`"5812"`), en nombres entiers (`int16`). Cette conversion est indispensable : la colonne `mcc` des transactions est numérique, et une jointure entre un nombre et un texte ne trouverait aucune correspondance.

## Où est le code ?

Dans `src/clean_data.py`, avec les autres fonctions de nettoyage.

## Fonction 1 : `build_mcc_table`

```python
def build_mcc_table(df_mcc: pd.DataFrame) -> pd.DataFrame:
    table = df_mcc.copy()
    table["description"] = table["description"].str.strip()
    table = table.sort_values("mcc_code").reset_index(drop=True)
    n_dup = table["mcc_code"].duplicated().sum()
    if n_dup:
        raise ValueError(f"{n_dup} code(s) MCC en double")
    return table
```

### Explication

| Syntaxe | Rôle |
|---|---|
| `df_mcc.copy()` | Travaille sur une copie pour ne pas modifier la table d'origine. |
| `.str.strip()` | Retire les espaces au début et à la fin des descriptions. |
| `.sort_values("mcc_code")` | Trie la table par code, ce qui la rend plus lisible. |
| `.reset_index(drop=True)` | Renumérote les lignes de 0 à 108 après le tri. |
| `duplicated().sum()` | Compte les codes qui apparaissent plus d'une fois. |
| `raise ValueError(...)` | Arrête le programme avec un message clair si un code est en double. Un code en double multiplierait des transactions lors de la jointure. |

## Fonction 2 : `check_mcc_join`

```python
def check_mcc_join(df_transaction: pd.DataFrame, df_mcc: pd.DataFrame) -> bool:
    n_before = len(df_transaction)
    joined = df_transaction[["id", "mcc"]].merge(
        df_mcc, left_on="mcc", right_on="mcc_code",
        how="left", validate="many_to_one"
    )
    n_after = len(joined)
    orphan_mask = joined["description"].isna()
    n_orphan = orphan_mask.sum()

    print(f"Lignes avant : {n_before:,} | après : {n_after:,}")
    print(f"Transactions sans catégorie : {n_orphan:,}")
    if n_orphan:
        print("Codes MCC sans correspondance :",
              sorted(joined.loc[orphan_mask, "mcc"].unique()))
    return n_before == n_after and n_orphan == 0
```

### Explication

| Syntaxe | Rôle |
|---|---|
| `df_transaction[["id", "mcc"]]` | Ne garde que deux colonnes pour la jointure, ce qui économise la mémoire sur 13 millions de lignes. La table d'analyse complète sera construite en P4-01. |
| `.merge(df_mcc, left_on="mcc", right_on="mcc_code")` | Associe chaque transaction à la description de son code, en comparant `mcc` (transactions) à `mcc_code` (table MCC). |
| `how="left"` | Garde **toutes** les transactions, même celles dont le code n'existe pas dans la table MCC. Elles auront une description vide, ce qui permet de les repérer. |
| `validate="many_to_one"` | Vérifie qu'un code MCC n'apparaît qu'une fois dans la table. Sinon, pandas arrête la jointure avec une erreur. Plusieurs transactions pour un même code est le cas normal. |
| `joined["description"].isna()` | Repère les transactions sans catégorie. |
| `return n_before == n_after and n_orphan == 0` | Retourne `True` seulement si aucune ligne n'a été perdue ou dupliquée et si toutes les transactions ont une catégorie. |

## Comment l'utiliser dans le notebook

```python
from src.load_data import load_transactions, load_mcc_codes
from src.clean_data import build_mcc_table, check_mcc_join

df_transaction = load_transactions()
df_mcc = load_mcc_codes()

df_mcc = build_mcc_table(df_mcc)
print(df_mcc.shape)
print(df_mcc.dtypes)

ok = check_mcc_join(df_transaction, df_mcc)
print("Jointure sans perte :", ok)
```

## Résultats obtenus

| Contrôle | Résultat |
|---|---|
| Taille de la table MCC | 109 lignes, 2 colonnes |
| Type de `mcc_code` | `int16` |
| Type de `description` | `str` (texte) |
| Lignes de transactions avant la jointure | 13 305 915 |
| Lignes de transactions après la jointure | 13 305 915 |
| Transactions sans catégorie | 0 |
| Jointure sans perte | `True` |

Le type affiché pour `description` dépend de la version de pandas : selon la version, il peut apparaître comme `str` ou `object`. Cela n'a aucune incidence sur les calculs.

La table contient les descriptions **en anglais**, telles que fournies. Leur traduction en français et leur regroupement en familles relèvent de P3-05.

## Ce que cette étape ne fait PAS

- Elle ne traduit pas les descriptions et ne crée pas de familles : c'est **P3-05**.
- Elle n'ajoute pas la description à la table des transactions : c'est **P4-01**, qui construit la table d'analyse complète.
- Elle n'enregistre pas la table sur disque : c'est **P3-10**.
- Elle ne corrige aucune anomalie : ici, il n'y en a pas, car toutes les transactions ont une catégorie.

## À noter dans le journal des transformations (P3-12)

- Table MCC : 109 codes uniques, `mcc_code` converti de texte en `int16`, espaces retirés des descriptions.
- Jointure avec les transactions : 13 305 915 lignes avant et après, 0 transaction sans catégorie.
- Ce résultat répond aussi au contrôle « transactions vers codes MCC » de **P2-02** du diagnostic.
