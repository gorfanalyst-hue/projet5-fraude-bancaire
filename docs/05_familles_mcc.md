# P3-05 : Regrouper les codes MCC en familles

## Pourquoi cette étape ?

La table des catégories MCC (P3-04) contient 109 codes. C'est trop pour des graphiques ou des modèles lisibles : un diagramme à 109 barres ne dit rien. On regroupe donc les codes en une dizaine de **familles** de commerçants (alimentation, transport, santé, etc.), avec des libellés en français.

Les familles serviront à :

- analyser les catégories de commerçants les plus fréquentes, en nombre et en montant (P6-05)
- créer des indicateurs de contexte, comme la famille de commerçant d'une transaction (P4-08)
- calculer des taux de signalement par famille de commerçant (P7-06)

Le critère de fin du ticket est : **table de correspondance validée**. Le classement a été validé par Channel et Anaclet le 28 octobre 2026.

## Où est le code ?

| Fichier | Contenu |
|---|---|
| `src/mcc_families.py` | La table de correspondance : les familles, leurs codes, et les descriptions françaises |
| `src/clean_data.py` | Les fonctions `add_mcc_families` et `check_mcc_families` |

La table est écrite en **Python** et non dans un fichier CSV, parce que le `.gitignore` du dépôt ignore tous les fichiers `.csv` et `.json`. Une table CSV ne serait pas partagée avec l'équipe.

## Structure de `mcc_families.py`

Le fichier contient trois éléments.

**1. `MCC_FAMILLES`** : un dictionnaire où chaque famille est associée à la liste de ses codes.

```python
MCC_FAMILLES = {
    "Alimentation": [
        5411,  # Épiceries et supermarchés
        5499,  # Magasins d'alimentation divers
        5921,  # Magasins de bière, vin et spiritueux
    ],
    "Restauration et bars": [
        5812, 5813, 5814,
    ],
    ...
}
```

C'est la partie à modifier pour changer un classement : il suffit de déplacer un code d'une liste à une autre.

**2. `MCC_DESCRIPTIONS_FR`** : un dictionnaire `code : description en français` pour les 109 codes.

**3. `MCC_TO_FAMILLE`** : le dictionnaire inversé `code : famille`, construit automatiquement.

```python
MCC_TO_FAMILLE = {}
for _famille, _codes in MCC_FAMILLES.items():
    for _code in _codes:
        if _code in MCC_TO_FAMILLE:
            raise ValueError(...)
        MCC_TO_FAMILLE[_code] = _famille
```

La construction vérifie qu'**aucun code n'est classé dans deux familles**. Si c'est le cas, Python s'arrête dès l'import avec un message qui nomme le code et les deux familles. Cela évite qu'un code soit compté deux fois.

## Fonction 1 : `add_mcc_families`

```python
def add_mcc_families(df_mcc: pd.DataFrame) -> pd.DataFrame:
    table = df_mcc.copy()
    table["famille"] = table["mcc_code"].map(MCC_TO_FAMILLE)
    table["description_fr"] = table["mcc_code"].map(MCC_DESCRIPTIONS_FR)
    return table
```

| Syntaxe | Rôle |
|---|---|
| `df_mcc.copy()` | Travaille sur une copie, la table d'origine reste intacte. |
| `.map(MCC_TO_FAMILLE)` | Remplace chaque code par la famille correspondante dans le dictionnaire. Un code absent du dictionnaire devient une valeur vide, ce qui permet de le repérer. |
| `table["famille"] = ...` | Crée la nouvelle colonne `famille`. |

## Fonction 2 : `check_mcc_families`

```python
def check_mcc_families(df_mcc, df_transaction) -> bool:
    missing_family = df_mcc.loc[df_mcc["famille"].isna(), "mcc_code"].tolist()
    missing_fr = df_mcc.loc[df_mcc["description_fr"].isna(), "mcc_code"].tolist()
    extra = sorted(set(MCC_TO_FAMILLE) - set(df_mcc["mcc_code"]))
    ...
    return not (missing_family or missing_fr or extra)
```

| Contrôle | Ce qu'il détecte |
|---|---|
| `missing_family` | Codes de la table MCC qui n'ont pas de famille (code oublié). |
| `missing_fr` | Codes sans description française. |
| `extra` | Codes présents dans le dictionnaire mais absents de la table MCC (faute de frappe dans un code). `set(...) - set(...)` calcule la différence entre deux ensembles. |

La fonction construit ensuite un résumé :

| Syntaxe | Rôle |
|---|---|
| `df_transaction["mcc"].value_counts()` | Compte le nombre de transactions pour chaque code. |
| `.merge(n_tx, left_on="mcc_code", right_index=True)` | Associe ce nombre à chaque ligne de la table MCC. |
| `.groupby("famille").agg(...)` | Regroupe par famille : nombre de codes (`count`) et nombre de transactions (`sum`). |
| `part_%` | Part de chaque famille dans l'ensemble des transactions. |

Elle retourne `True` si les trois listes de contrôle sont vides.

## Comment l'utiliser dans le notebook

```python
from src.clean_data import build_mcc_table, add_mcc_families, check_mcc_families

df_mcc = build_mcc_table(df_mcc)
df_mcc = add_mcc_families(df_mcc)

ok = check_mcc_families(df_mcc, df_transaction)
print("Table de correspondance valide :", ok)
```

Après un changement dans `clean_data.py` ou `mcc_families.py`, il faut **redémarrer le kernel** : Python ne recharge pas un module déjà importé.

## Résultats obtenus

Contrôles : aucun code sans famille, aucun code sans description française, aucun code du dictionnaire absent de la table. Résultat : `True`.

| Famille | Codes | Transactions | Part |
|---|---|---|---|
| Transport, carburant et automobile | 15 | 3 352 312 | 25,2 % |
| Alimentation | 3 | 3 182 334 | 23,9 % |
| Restauration et bars | 3 | 1 747 967 | 13,1 % |
| Grandes surfaces et commerces divers | 5 | 1 332 087 | 10,0 % |
| Santé et soins | 8 | 886 034 | 6,7 % |
| Services professionnels et financiers | 7 | 718 301 | 5,4 % |
| Loisirs, culture et divertissement | 13 | 638 844 | 4,8 % |
| Services publics et télécommunications | 5 | 626 682 | 4,7 % |
| Maison, jardin et électronique | 15 | 352 851 | 2,7 % |
| Vêtements, beauté et services personnels | 9 | 265 742 | 2,0 % |
| Industrie et fabrication | 22 | 150 735 | 1,1 % |
| Voyage et hébergement | 4 | 52 026 | 0,4 % |
| **Total** | **109** | **13 305 915** | **100 %** |

Les 109 codes sont classés, et les 13 305 915 transactions ont toutes une famille.

## Choix de classement retenus

| Code | Description | Famille retenue | Raison |
|---|---|---|---|
| 4829 | Transferts d'argent | Services professionnels et financiers | Service financier |
| 9402 | Services postaux (gouvernement) | Services publics et télécommunications | Service public |
| 3132 | Articles en cuir | Vêtements, beauté et services personnels | Articles destinés aux consommateurs |
| 3260 | Poterie et céramique | Maison, jardin et électronique | Décoration |
| 3722, 3771, 3775, 4112 | Chemins de fer | Transport, carburant et automobile | Transport de voyageurs ou de marchandises, pas un service touristique |
| 5921 | Magasins de bière, vin et spiritueux | Alimentation | Magasin de détail, distinct des bars |
| 5815, 5816 | Biens numériques (médias, jeux) | Loisirs, culture et divertissement | Contenu de loisir |

Il n'y a pas de famille « Autres » : chaque code entre dans une famille précise. La famille « Grandes surfaces et commerces divers » regroupe les clubs-entrepôts, les magasins à rabais et les grands magasins.

## Limites à garder en tête

- **Une famille peut être dominée par un seul code.** Dans « Services professionnels et financiers », le code 4829 (transferts d'argent, 589 140 transactions) représente environ 82 % de la famille. Dans « Transport, carburant et automobile », quatre codes (stations-service, péages, taxis, ateliers d'entretien) font environ 92 %. Les résultats par famille doivent être interprétés en conséquence. La table conserve le code MCC et la famille : on peut donc toujours revenir au détail.
- **Les familles sont de tailles très inégales.** Quatre familles concentrent 72 % des transactions, alors que « Voyage et hébergement » n'en représente que 0,4 %. Pour un graphique en parts, les petites familles seront peu visibles.
- **Le regroupement est un choix de jugement.** Un autre découpage serait défendable. Le classement est modifiable en déplaçant un code dans `MCC_FAMILLES`, sans changer le reste du code.

## Ce que cette étape ne fait PAS

- Elle n'ajoute pas la famille à la table des transactions : c'est **P4-01**, qui joint les tables, et **P4-08**, qui crée les indicateurs de contexte.
- Elle n'enregistre pas la table sur disque : c'est **P3-10**.
- Elle ne modifie pas les codes MCC des transactions.

## À noter dans le journal des transformations (P3-12)

- Table MCC enrichie de deux colonnes : `famille` (12 valeurs) et `description_fr`.
- 109 codes classés, aucun code sans famille ni sans description française.
- 13 305 915 transactions couvertes, soit 100 %.
- Classement validé par Channel et Anaclet le 28 octobre 2026.
- Limites : familles dominées par un seul code (4829, quatre codes de transport) et répartition très inégale des transactions.
