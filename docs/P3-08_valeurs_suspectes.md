# P3-08 : Appliquer les règles aux valeurs suspectes

## Pourquoi cette étape ?

Le diagnostic (P2-09, P2-10, P2-11, P2-14) a trouvé des valeurs suspectes : montants négatifs ou nuls, revenus trop bas, limites de crédit nulles, transactions répétées. Le rapport P2-16 fixe une règle pour chacune.

Règle commune : **aucune ligne n'est supprimée et aucune valeur n'est modifiée**. Chaque cas est signalé par un indicateur 0/1. Chaque analyse décide ensuite si elle garde ou retire ces lignes.

Le critère de fin du ticket est : **chaque règle appliquée et tracée**.

## Les règles

| Table        | Indicateur           | Vaut 1 quand...                                                                                                                    |
| ------------ | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| transactions | `is_negative_amount` | le montant est négatif                                                                                                             |
| transactions | `is_zero_amount`     | le montant est nul                                                                                                                 |
| transactions | `is_repeated`        | la ligne est la seconde d'un groupe répété (même carte, même minute, même montant, même commerçant) dont aucune ligne n'a d'erreur |
| users        | `suspicious_income`  | le revenu annuel est inférieur à 1 000 ou le revenu par habitant est nul                                                           |
| cards        | `zero_credit_limit`  | la limite de crédit est nulle                                                                                                      |

Pour les groupes répétés avec une erreur, la seconde ligne n'est pas signalée : le diagnostic montre que le client a refait l'achat après un échec.

## Où est le code ?

Dans `src/clean_data.py`, section P3-08 : `flag_suspicious_transactions`, `flag_suspicious_users`, `flag_suspicious_cards` et `check_suspicious_flags`.

## Fonction 1 : `flag_suspicious_transactions`

```python
df["is_negative_amount"] = (df["amount"] < 0).astype("int8")
df["is_zero_amount"] = (df["amount"] == 0).astype("int8")

in_group = df.duplicated(subset=REPEAT_KEYS, keep=False)
group = df.loc[in_group, REPEAT_KEYS + ["errors"]]
group_has_error = (
    group["errors"].notna()
    .groupby([group[k] for k in REPEAT_KEYS])
    .transform("any")
)
not_first = group.duplicated(subset=REPEAT_KEYS, keep="first")
flagged = not_first & ~group_has_error
```

### Explication

| Syntaxe                                         | Rôle                                                                                                                      |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `(df["amount"] < 0).astype("int8")`             | Donne 1 pour un montant négatif, 0 sinon.                                                                                 |
| `df.duplicated(subset=REPEAT_KEYS, keep=False)` | Marque toutes les lignes qui ont la même carte, la même minute, le même montant et le même commerçant qu'une autre ligne. |
| `group["errors"].notna()...transform("any")`    | Pour chaque groupe, indique si au moins une ligne a une erreur. Le résultat est recopié sur chaque ligne du groupe.       |
| `group.duplicated(..., keep="first")`           | Marque les lignes qui ne sont pas la première de leur groupe.                                                             |
| `not_first & ~group_has_error`                  | Garde les secondes lignes des groupes sans aucune erreur.                                                                 |

Seules les lignes des groupes répétés passent par le `groupby`, ce qui évite de regrouper 13 millions de lignes.

## Fonctions 2 et 3 : `flag_suspicious_users` et `flag_suspicious_cards`

```python
df["suspicious_income"] = (
    (df["yearly_income"] < 1000) | (df["per_capita_income"] == 0)
).astype("int8")

df["zero_credit_limit"] = (df["credit_limit"] == 0).astype("int8")
```

Le symbole `|` veut dire « ou » : il suffit d'une des deux conditions.

## Fonction 4 : `check_suspicious_flags`

Elle affiche, pour chaque indicateur, la table, la règle, le nombre de lignes et le nombre de lignes signalées.

## Comment l'utiliser dans le notebook

```python
df_transaction = flag_suspicious_transactions(df_transaction)
df_users = flag_suspicious_users(df_users)
df_card = flag_suspicious_cards(df_card)
check_suspicious_flags(df_transaction, df_users, df_card)
```

Les montants doivent déjà être numériques (P3-02).

Pour retirer les lignes signalées dans une analyse :

```python
depenses = df_transaction[(df_transaction["is_negative_amount"] == 0)
                          & (df_transaction["is_repeated"] == 0)]
```

## Résultats obtenus

| Indicateur           | Lignes     | Lignes signalées |
| -------------------- | ---------- | ---------------- |
| `is_negative_amount` | 13 305 915 | 660 049          |
| `is_zero_amount`     | 13 305 915 | 10 639           |
| `is_repeated`        | 13 305 915 | 15               |
| `suspicious_income`  | 2 000      | 15               |
| `zero_credit_limit`  | 6 146      | 31               |

- Les 15 lignes `is_repeated` correspondent aux 15 groupes sans erreur de P2-14.
- `suspicious_income` signale 15 clients, comme le nombre de revenus par habitant nuls : les 8 revenus annuels inférieurs à 1 000 en font tous partie.

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne supprime aucune ligne et ne modifie aucune valeur.
- Elle ne signale pas les transactions faites avant l'ouverture du compte ou après l'expiration de la carte : cet indicateur sera créé en phase 4.
- Elle ne traite pas les 34 clients dont le revenu par habitant dépasse le revenu annuel, ni les 268 cartes au PIN changé après l'expiration : ces cas sont gardés sans règle (voir P2-16).

## À noter dans le journal des transformations (P3-12)

Cinq indicateurs ajoutés, sans suppression ni modification : `is_negative_amount` (660 049), `is_zero_amount` (10 639), `is_repeated` (15), `suspicious_income` (15), `zero_credit_limit` (31).
