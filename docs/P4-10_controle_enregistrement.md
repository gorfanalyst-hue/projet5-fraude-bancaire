# P4-10 : Contrôler et enregistrer la table d'analyse

## Pourquoi cette étape ?

Toutes les phases suivantes partent de la table d'analyse. Avant de l'enregistrer, on vérifie qu'aucune valeur vide n'est inexpliquée et que chaque nouvelle colonne reste dans ses bornes. On l'enregistre ensuite une fois pour toutes, dans un format léger.

Le critère de fin du ticket est : **table rechargée sans erreur**.

## Où est le code ?

- `src/features.py` : `check_missing_and_bounds` et `save_analysis_table`.
- `notebooks/04_table_analyse.ipynb` : section P4-10.

## Les fonctions

| Fonction | Rôle |
| --- | --- |
| `check_missing_and_bounds(df)` | Liste les colonnes avec des valeurs vides et dit si elles sont attendues (`EXPECTED_MISSING`), puis vérifie les bornes des colonnes créées (`EXPECTED_BOUNDS` : années de 2010 à 2019, mois de 1 à 12, heures de 0 à 23, âge de 0 à 120 ans, compteurs positifs). |
| `save_analysis_table(df)` | Enregistre la table dans `data/clean/analysis.parquet`, avec la compression zstd, et donne lignes, colonnes, mémoire et taille du fichier. |

Pour relire la table, comme les tables de P3-10 :

```python
from src.load_data import load_clean_table

df = load_clean_table("analysis")

# Seulement quelques colonnes, pour économiser la mémoire
df = load_clean_table("analysis", columns=["id", "client_id", "amount", "amount_ratio"])
```

## Résultats obtenus

| Contrôle | Résultat |
| --- | --- |
| Valeurs vides de `errors` | 13 094 522 : transactions sans erreur |
| Valeurs vides de `is_fraud` | 4 390 952 : transactions sans étiquette (P2-17) |
| Valeurs vides du montant habituel (3 colonnes) | 12 787 : moins de 10 achats précédents |
| Bornes des colonnes créées | toutes respectées (âge de 17 à 101 ans) |

| Table enregistrée | Valeur |
| --- | --- |
| Lignes | 13 305 915 |
| Colonnes | 63 |
| Mémoire | 1 800,0 Mo |
| Taille du fichier | 530,1 Mo |
| Relecture | 11,7 s, mêmes lignes, colonnes et types |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne versionne pas le fichier : comme tout `data/`, il reste sur l'ordinateur de chacun. Chaque membre le crée en exécutant `notebooks/04_table_analyse.ipynb` (environ une minute).

## À noter dans le journal des transformations (P3-12)

Table d'analyse enregistrée dans `data/clean/analysis.parquet` : 13 305 915 lignes, 63 colonnes, 530,1 Mo. Relecture en 11,7 s.
