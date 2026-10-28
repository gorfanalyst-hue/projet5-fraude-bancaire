# P3-07 : Structurer le lieu des transactions

## Pourquoi cette étape ?

Dans `transactions_data.csv`, le lieu d'une transaction est décrit par `merchant_city`, `merchant_state`, `zip` et `use_chip`. Ces colonnes contiennent des valeurs vides, la ville « ONLINE » pour les achats en ligne, et des codes d'États américains mélangés à des noms de pays étrangers. Telles quelles, elles ne permettent pas de répondre simplement à : la transaction est-elle en ligne ? à l'étranger ? aux États-Unis ?

On les transforme donc en colonnes propres, sans valeur manquante, avec deux indicateurs binaires : `is_online` et `is_foreign`.

Ces colonnes serviront aux indicateurs de contexte (P4-08), à l'analyse des lieux de transaction (P6) et à la comparaison des taux de signalement en ligne, à l'étranger et sur place (P7).

Le critère de fin du ticket est : **aucune valeur manquante dans les colonnes de lieu**.

## Où est le code ?

Dans `src/clean_data.py`. Le code a été écrit par Martin ; la relecture a ajouté le code d'État `AA`, l'indicateur `online_channel_mismatch` et un contrôle des valeurs `UNKNOWN`.

## Règles de transformation

| Colonne créée | Règle |
|---|---|
| `is_online` | 1 si la ville est « ONLINE » **ou** si `use_chip` vaut « Online Transaction ». |
| `merchant_country` | « USA » si le code d'État est un État américain ou un territoire reconnu. Sinon, le nom du pays figurant dans la colonne d'État. |
| `merchant_state_clean` | Code d'État pour les transactions américaines physiques. Une valeur de remplacement explicite pour les achats en ligne et à l'étranger, jamais une case vide. |
| `merchant_city` | Ville propre, avec une valeur explicite pour les achats en ligne. |
| `is_foreign` | 1 si le pays n'est pas « USA » pour une transaction physique. |
| `zip_clean` | Code postal sur 5 chiffres (`zfill(5)` rétablit les zéros initiaux perdus, par exemple 2134 devient 02134). Valeur explicite pour les achats en ligne et à l'étranger. |
| `online_channel_mismatch` | 1 si la ville est « ONLINE » mais que le canal n'est pas « Online Transaction ». C'est un indicateur de qualité, pas une correction. |

## Décisions prises

**1. La ville « ONLINE » est la source fiable pour `is_online`.**
5 788 transactions ont la ville « ONLINE » mais un canal « Chip Transaction ». Toutes ont en plus un État et un code postal vides, ce qui confirme qu'il s'agit bien d'achats en ligne. On les garde donc avec `is_online = 1` et on les repère avec `online_channel_mismatch = 1`, au lieu de les supprimer ou de les modifier en silence.

**2. Le code `AA` est classé aux États-Unis.**
`AA` (Armed Forces Americas) désigne des adresses postales militaires et diplomatiques. Six transactions sont concernées (ville « Dpo », code postal 34004). Le code a été ajouté à la liste `US_STATES_AND_TERRITORIES`. Elles sont comptées avec `is_foreign = 0`.

**3. Seul `DC` parmi les territoires.**
Parmi les territoires de la liste, seul le district de Columbia (`DC`) est présent dans les données.

## Comment l'utiliser dans le notebook

```python
from src.clean_data import structurer_lieu_transactions, check_location_structuration

df_transaction = structurer_lieu_transactions(df_transaction)
check_location_structuration(df_transaction)
```

Après une modification de `clean_data.py`, il faut redémarrer le kernel.

## Résultats obtenus

Contrôle des valeurs manquantes :

| Colonne | Valeurs manquantes | Valeurs « UNKNOWN » |
|---|---|---|
| `merchant_city` | 0 | 0 |
| `merchant_state_clean` | 0 | 0 |
| `merchant_country` | 0 | 0 |
| `is_online` | 0 | sans objet |
| `is_foreign` | 0 | sans objet |
| `zip_clean` | 0 | 0 |

**Critère de fin validé.**

Répartition des 13 305 915 transactions :

| Catégorie | Transactions | Part |
|---|---|---|
| Aux États-Unis, sur place | 11 653 209 | 87,6 % |
| À l'étranger | 89 006 | 0,7 % |
| En ligne (`is_online = 1`) | 1 563 700 | 11,8 % |
| **Total** | **13 305 915** | **100 %** |

Contrôle : 11 653 209 + 89 006 = 11 742 215, soit exactement le nombre de lignes dont la ville n'est pas « ONLINE ». En ajoutant les 1 563 700 achats en ligne, on retrouve 13 305 915.

Parmi les achats en ligne, 5 788 ont un canal différent de « Online Transaction » (`online_channel_mismatch = 1`).

## Ce que cette étape ne fait PAS

- Elle ne supprime aucune transaction.
- Elle ne corrige pas `use_chip` pour les 5 788 cas en désaccord : elle les signale.
- Elle ne vérifie pas que le code postal correspond à la ville ou à l'État.
- Elle ne distingue pas un voyage d'un achat frauduleux à l'étranger : `is_foreign` est un indicateur de contexte, pas une conclusion.
- Elle n'enregistre pas la table sur disque : c'est **P3-10**.

## À noter dans le journal des transformations (P3-12)

- Six colonnes de lieu structurées, plus l'indicateur `online_channel_mismatch` ; aucune valeur manquante ni « UNKNOWN ».
- `is_online` = 1 563 700 (11,8 %), `is_foreign` = 89 006 (0,7 %), USA sur place = 11 653 209 (87,6 %).
- Règle : ville « ONLINE » ou canal « Online Transaction » donne `is_online = 1`.
- 5 788 transactions avec ville « ONLINE » et canal « Chip Transaction » : conservées, signalées par `online_channel_mismatch`.
- Code `AA` (6 transactions, ville « Dpo ») classé aux États-Unis ; `DC` seul territoire présent.
- Cohérence avec P2-06 : tous les codes postaux manquants correspondent à un achat en ligne ou à l'étranger.
