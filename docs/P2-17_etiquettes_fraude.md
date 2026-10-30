# P2-17 : Contrôler les étiquettes de fraude

## Pourquoi cette étape ?

L'enseignant a ajouté au jeu de données le fichier `fraud_labels.json`. Il indique, pour une partie des transactions, s'il s'agit d'une fraude (`Yes`) ou non (`No`).

Avant de s'en servir pour répondre à Q3 et Q4, puis pour entraîner un modèle (phase 7), il faut savoir :

- combien de transactions ont une étiquette ;
- si ces étiquettes correspondent bien à des transactions existantes ;
- quelle est la part de fraudes ;
- si la partie étiquetée ressemble au reste des transactions.

Le critère de fin du ticket est : **couverture, taux de fraude et cohérence avec les transactions mesurés et documentés**.

## Où est le code ?

- `src/load_data.py` : la fonction de chargement `load_fraud_labels`, et un nouveau paramètre `usecols` dans `load_transactions`.
- `src/diagnostic.py` : un nouveau fichier pour les fonctions de contrôle de la phase 2. Elles mesurent sans rien modifier.
- `notebooks/02_diagnostic_qualite.ipynb` : le notebook de la phase 2, avec une section par ticket.

## Fonction 1 : `load_fraud_labels`

Le fichier a la forme `{"target": {"10649266": "No", "23410063": "No", ...}}` : un dictionnaire dont la clé est l'identifiant de la transaction.

```python
def load_fraud_labels(path=DATA_DIR / "fraud_labels.json"):
    with open(path, encoding="utf-8") as f:
        labels = json.load(f)["target"]

    values = pd.Series(list(labels.values()))
    unknown = set(values.unique()) - {"Yes", "No"}
    if unknown:
        raise ValueError(f"Valeurs d'étiquette inattendues : {sorted(unknown)}")

    return pd.DataFrame({
        "id": pd.to_numeric(pd.Series(list(labels.keys()))).astype("int32"),
        "is_fraud": (values == "Yes").astype("int8"),
    })
```

### Explication

| Syntaxe | Rôle |
|---|---|
| `json.load(f)["target"]` | Lit le fichier et garde le dictionnaire placé sous la clé `target`. |
| `set(values.unique()) - {"Yes", "No"}` | Cherche des valeurs autres que `Yes` et `No`. S'il y en a, la fonction s'arrête avec une erreur au lieu de les classer en silence. |
| `pd.to_numeric(...).astype("int32")` | Les identifiants sont du texte dans le JSON : on les convertit en nombres, avec le même type que la colonne `id` des transactions. |
| `(values == "Yes").astype("int8")` | Donne 1 pour une fraude et 0 sinon. |

La table obtenue a deux colonnes, `id` et `is_fraud`. Elle se joint aux transactions par la colonne `id`.

### Le paramètre `usecols` de `load_transactions`

```python
df_tx = load_transactions(usecols=["id", "date", "use_chip"])
```

Il permet de ne lire que les colonnes utiles. Le contrôle P2-17 n'a besoin que de trois colonnes : la lecture est plus rapide et prend beaucoup moins de mémoire. Sans `usecols`, la fonction lit toutes les colonnes, comme avant.

## Fonction 2 : `check_fraud_labels`

```python
ok = check_fraud_labels(df_labels, df_tx)
```

Elle affiche le nombre de transactions étiquetées, les identifiants en double, les identifiants absents des transactions et le nombre de fraudes. Elle retourne `True` s'il n'y a ni doublon ni identifiant absent.

## Fonctions 3 et 4 : `add_fraud_label` et `fraud_summary_by`

| Fonction | Rôle |
|---|---|
| `add_fraud_label(df_tx, df_labels)` | Ajoute la colonne `is_fraud` aux transactions : 1 (fraude), 0 (pas de fraude) ou vide (transaction sans étiquette). La jointure crée une copie : il vaut mieux ne passer que les colonnes utiles. |
| `fraud_summary_by(df, col)` | Pour chaque valeur d'une colonne (année, canal...) : nombre de transactions, part étiquetée, nombre de fraudes et taux de fraude parmi les transactions étiquetées. |

## Comment l'utiliser dans le notebook

```python
from src.load_data import load_transactions, load_fraud_labels
from src.diagnostic import check_fraud_labels, add_fraud_label, fraud_summary_by

df_tx = load_transactions(usecols=["id", "date", "use_chip"])
df_labels = load_fraud_labels()
check_fraud_labels(df_labels, df_tx)

df_lab = add_fraud_label(df_tx, df_labels)
df_lab["annee"] = df_lab["date"].dt.year
fraud_summary_by(df_lab, "annee")
fraud_summary_by(df_lab, "use_chip")
```

## Résultats obtenus

| Contrôle | Résultat |
|---|---|
| Transactions étiquetées | 8 914 963, soit 67,0 % des 13 305 915 transactions |
| Identifiants en double | 0 |
| Identifiants absents des transactions | 0 |
| Fraudes | 13 332, soit 0,150 % des transactions étiquetées |

**Critère de fin validé.**

### Par année

| Année | Part étiquetée | Fraudes | Taux de fraude |
|---|---|---|---|
| 2010 | 67,0 % | 2 573 | 0,309 % |
| 2011 | 66,9 % | 37 | 0,004 % |
| 2012 | 67,0 % | 923 | 0,104 % |
| 2013 | 67,1 % | 1 337 | 0,147 % |
| 2014 | 67,0 % | 664 | 0,073 % |
| 2015 | 67,0 % | 2 189 | 0,235 % |
| 2016 | 67,0 % | 2 448 | 0,262 % |
| 2017 | 67,0 % | 172 | 0,018 % |
| 2018 | 67,0 % | 1 629 | 0,174 % |
| 2019 | 67,0 % | 1 360 | 0,175 % |

### Par canal de paiement

| Canal | Part étiquetée | Fraudes | Taux de fraude |
|---|---|---|---|
| En ligne (Online Transaction) | 67,0 % | 8 779 | 0,841 % |
| Puce (Chip Transaction) | 67,0 % | 3 176 | 0,099 % |
| Bande magnétique (Swipe Transaction) | 67,0 % | 1 377 | 0,029 % |

## Ce que ces résultats changent pour la suite

1. **La partie étiquetée est représentative.** Elle couvre entre 66,9 % et 67,1 % des transactions selon l'année, et 67,0 % pour chaque canal : les étiquettes semblent tirées au hasard. Les conclusions tirées sur cette partie peuvent donc s'étendre au reste.
2. **Les fraudes sont rares** (0,150 % des transactions étiquetées). L'exactitude d'un modèle ne suffira pas : il faudra mesurer la précision et le rappel (phase 7).
3. **Le taux varie beaucoup selon l'année.** 2011 et 2017 comptent très peu de fraudes. Il faudra en tenir compte pour séparer les données d'entraînement et de test (P7-08).
4. **Le canal compte beaucoup.** Les achats en ligne comptent 8 779 des 13 332 fraudes. Leur taux de fraude est de 0,841 %, contre 0,099 % par puce et 0,029 % par bande magnétique.

## Ce que cette étape ne fait PAS

- Elle n'ajoute pas `is_fraud` à la table d'analyse : ce sera fait en phase 4, à partir des tables nettoyées.
- Elle ne compare pas encore les fraudes et les transactions normales : c'est le sujet de Q3 (P7-05).
- Elle ne modifie aucune donnée.

## À noter dans le journal des transformations (P3-12)

Aucune transformation : P2-17 est un contrôle. Noter seulement que la table `fraud_labels.json` est chargée par `load_fraud_labels`, avec ses deux colonnes `id` (int32) et `is_fraud` (int8).
