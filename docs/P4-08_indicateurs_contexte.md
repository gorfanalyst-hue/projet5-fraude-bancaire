# P4-08 : Créer les indicateurs de contexte

## Pourquoi cette étape ?

Certaines situations rendent une transaction plus exposée : un achat sans carte physique, un achat hors du pays, un montant rond, une carte utilisée hors de sa période de validité. Ces indicateurs simples complètent ceux qui regardent l'historique.

Le critère de fin du ticket est : **indicateurs créés**.

## Où est le code ?

- `src/features.py` : `add_context_flags` et `check_context_flags`.
- `notebooks/04_table_analyse.ipynb` : section P4-08.

## La fonction `add_context_flags`

```python
def add_context_flags(df):
    amount = df["amount"]
    df["is_round_amount"] = ((amount > 0) & (amount % 1 == 0)).astype("int8")
    before_open = df["date"] < df["acct_open_date"]
    after_expiry = df["date"] >= df["expires"] + pd.Timedelta(days=1)
    df["outside_card_validity"] = (before_open | after_expiry).astype("int8")
    return df
```

| Indicateur | Définition | Origine |
| --- | --- | --- |
| `is_online` | Achat en ligne | P3-07 |
| `is_foreign` | Achat sur place hors des États-Unis | P3-07 |
| `mcc_family` | Famille du commerçant | P3-05, ajoutée en P4-01 |
| `is_round_amount` | Achat (montant positif) sans centimes | P4-08 |
| `outside_card_validity` | Transaction avant le mois d'ouverture du compte, ou après la fin du mois d'expiration de la carte | P4-08, même règle que P2-11 |

## Résultats obtenus

| Indicateur | Transactions | Part |
| --- | --- | --- |
| `is_online` | 1 563 700 | 11,75 % |
| `is_foreign` | 89 006 | 0,67 % |
| `is_round_amount` | 1 349 993 | 10,15 % |
| `outside_card_validity` | 392 | 0,00 % |

Les 392 transactions hors validité se répartissent en 309 avant l'ouverture du compte et 83 après l'expiration : exactement les chiffres de P2-11.

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne dit pas si ces indicateurs sont liés à la fraude : c'est la phase 7.

## À noter dans le journal des transformations (P3-12)

Deux colonnes ajoutées : `is_round_amount` et `outside_card_validity` (règle de P2-11).
