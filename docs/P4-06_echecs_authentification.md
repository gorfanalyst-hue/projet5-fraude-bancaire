# P4-06 : Compter les échecs d'authentification récents

## Pourquoi cette étape ?

Quelqu'un qui ne connaît pas les informations de la carte se trompe souvent : mauvais PIN, CVV, numéro, date d'expiration ou code postal. Plusieurs échecs sur la même carte en peu de temps sont un signal classique de fraude.

Le critère de fin du ticket est : **colonne vérifiée sur une carte**.

## Où est le code ?

- `src/features.py` : `add_recent_auth_errors` et `recount_card_activity`.
- `notebooks/04_table_analyse.ipynb` : section P4-06.

## La fonction `add_recent_auth_errors`

```python
def add_recent_auth_errors(df):
    df["card_auth_errors_24h"] = count_previous_in_window(
        df, "card_id", 24 * 60, values=df["has_auth_error"]
    ).astype("int16")
    return df
```

| Syntaxe | Rôle |
| --- | --- |
| `has_auth_error` | Indicateur de P3-06 : 1 si la transaction a un échec de PIN, CVV, numéro, expiration ou code postal. Le solde insuffisant et la panne technique ne comptent pas. |
| `values=df["has_auth_error"]` | Au lieu de compter toutes les transactions de la fenêtre, la fonction additionne seulement celles qui ont un échec (somme cumulée). |
| `24 * 60` | Fenêtre de 24 heures, en minutes. |

La transaction en cours ne compte pas : la colonne dit combien d'échecs la carte a connus **avant** elle.

## Résultats obtenus

| Échecs dans les 24 heures précédentes | Transactions |
| --- | --- |
| 0 | 13 185 427 |
| 1 | 118 886 |
| 2 | 1 580 |
| 3 | 22 |

Carte vérifiée : carte 11, 1 939 transactions, toutes identiques au recompte.

**Critère de fin validé.**

## Ce que ces résultats changent pour la suite

Aucune transaction n'a plus de trois échecs précédents en 24 heures. La règle « 3 échecs ou plus » donnée en exemple dans Jira ne toucherait que 22 transactions. La règle R01 de P7-01 est donc fixée à 2 échecs ou plus (1 602 transactions).

## À noter dans le journal des transformations (P3-12)

Colonne `card_auth_errors_24h` ajoutée : échecs d'authentification de la même carte dans les 24 heures précédentes.
