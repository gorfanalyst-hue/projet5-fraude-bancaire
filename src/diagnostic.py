"""
Fonctions de contrôle pour le diagnostic de la qualité des données (phase 2).

Ces fonctions mesurent les problèmes sans rien modifier dans les tables.
Les corrections se font en phase 3, dans clean_data.py.
"""
import pandas as pd


# =============================================================================
# P2-17 : Contrôle des étiquettes de fraude
# =============================================================================

def check_fraud_labels(df_labels: pd.DataFrame, df_transaction: pd.DataFrame) -> bool:
    """
    Vérifie la table des étiquettes de fraude (voir load_fraud_labels) :
    - aucun identifiant en double ;
    - tous les identifiants existent dans les transactions ;
    puis affiche la couverture et le taux de fraude.
    Retourne True si les deux contrôles de cohérence passent.
    """
    n_labels = len(df_labels)
    n_tx = len(df_transaction)
    n_dup = int(df_labels["id"].duplicated().sum())
    n_absent = int((~df_labels["id"].isin(df_transaction["id"])).sum())
    n_fraud = int(df_labels["is_fraud"].sum())

    print("=== Contrôle P2-17 : étiquettes de fraude ===")
    print(f"  - Transactions étiquetées                 : {n_labels:>12,} "
          f"({100 * n_labels / n_tx:.1f} % des transactions)")
    print(f"  - Identifiants en double                  : {n_dup:>12,}")
    print(f"  - Identifiants absents des transactions   : {n_absent:>12,}")
    print(f"  - Fraudes                                 : {n_fraud:>12,} "
          f"({100 * n_fraud / n_labels:.3f} % des transactions étiquetées)")

    ok = n_dup == 0 and n_absent == 0
    print(f"Contrôles de cohérence validés : {ok}\n")
    return ok


def add_fraud_label(df_transaction: pd.DataFrame, df_labels: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute la colonne is_fraud aux transactions (jointure à gauche sur id).
    is_fraud vaut 1 (fraude), 0 (pas de fraude) ou NaN (transaction sans étiquette).

    La jointure crée une copie de la table : pour économiser la mémoire,
    passer seulement les colonnes utiles, par exemple df[["id", "date"]].
    """
    return df_transaction.merge(df_labels, on="id", how="left", validate="one_to_one")


def fraud_summary_by(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Pour chaque valeur de `col` : nombre de transactions, part étiquetée,
    nombre de fraudes et taux de fraude parmi les transactions étiquetées.
    df doit contenir la colonne is_fraud (voir add_fraud_label).
    """
    resume = (
        df.assign(etiquetee=df["is_fraud"].notna())
        .groupby(col, observed=True)
        .agg(n_transactions=("is_fraud", "size"),
             n_etiquetees=("etiquetee", "sum"),
             n_fraudes=("is_fraud", "sum"))
    )
    resume["n_fraudes"] = resume["n_fraudes"].astype("int64")
    resume["part_etiquetee_%"] = (100 * resume["n_etiquetees"] / resume["n_transactions"]).round(1)
    resume["taux_fraude_%"] = (100 * resume["n_fraudes"] / resume["n_etiquetees"]).round(3)
    return resume


# =============================================================================
# Vue d'ensemble : valeurs manquantes
# =============================================================================

def count_missing(tables: dict) -> pd.DataFrame:
    """
    Nombre de valeurs manquantes par colonne, pour chaque table.
    tables : dictionnaire {nom de la table : DataFrame}.
    Seules les colonnes avec au moins une valeur manquante sont gardées.
    """
    rows = []
    for name, df in tables.items():
        n_missing = df.isna().sum()
        for col, n in n_missing[n_missing > 0].items():
            rows.append({"table": name, "colonne": col, "lignes": len(df), "manquantes": int(n)})
    return pd.DataFrame(rows, columns=["table", "colonne", "lignes", "manquantes"])


# =============================================================================
# P2-02 : Liens entre les tables
# =============================================================================

def check_table_links(df_transaction, df_users, df_card, df_mcc) -> pd.DataFrame:
    """
    Compte les lignes sans correspondance (orphelines) pour chaque lien entre tables.
    """
    links = [
        ("transactions.client_id -> users.id", df_transaction["client_id"], df_users["id"]),
        ("transactions.card_id -> cards.id", df_transaction["card_id"], df_card["id"]),
        ("cards.client_id -> users.id", df_card["client_id"], df_users["id"]),
        ("transactions.mcc -> mcc_codes.mcc_code", df_transaction["mcc"], df_mcc["mcc_code"]),
    ]
    rows = []
    for name, keys, ref in links:
        rows.append({"lien": name, "lignes": len(keys), "orphelines": int((~keys.isin(ref)).sum())})
    return pd.DataFrame(rows).set_index("lien")


# =============================================================================
# P2-03 : La carte utilisée appartient-elle au client ?
# =============================================================================

def check_card_owner(df_transaction, df_card) -> pd.Series:
    """
    Compare le client de chaque transaction au titulaire de la carte utilisée.
    """
    owner = df_transaction["card_id"].map(df_card.set_index("id")["client_id"])
    known = owner.notna()
    mismatch = known & (owner != df_transaction["client_id"])
    return pd.Series({
        "transactions": len(df_transaction),
        "transactions avec une carte connue": int(known.sum()),
        "client différent du titulaire de la carte": int(mismatch.sum()),
    })


# =============================================================================
# P2-04 : Clients et cartes sans activité
# =============================================================================

def count_inactive(df_transaction, df_users, df_card) -> pd.Series:
    """
    Compte les clients et les cartes qui n'ont aucune transaction.
    """
    active_clients = df_transaction["client_id"].unique()
    active_cards = df_transaction["card_id"].unique()
    inactive_clients = ~df_users["id"].isin(active_clients)
    inactive_cards = ~df_card["id"].isin(active_cards)
    return pd.Series({
        "clients": len(df_users),
        "clients sans transaction": int(inactive_clients.sum()),
        "cartes": len(df_card),
        "cartes sans transaction": int(inactive_cards.sum()),
        "cartes sans transaction d'un client actif": int(
            (inactive_cards & df_card["client_id"].isin(active_clients)).sum()),
    })


# =============================================================================
# P2-05 et P2-06 : Manquants de merchant_state et de zip
# =============================================================================

def explain_missing_location(df_transaction, us_codes) -> pd.DataFrame:
    """
    Répartit les manquants de merchant_state et de zip par type de lieu :
    en ligne (ville « ONLINE »), à l'étranger (État qui n'est pas un code
    américain) ou aux États-Unis sur place.
    us_codes : ensemble des codes d'États américains (US_STATES_AND_TERRITORIES).
    """
    state = df_transaction["merchant_state"]
    online = df_transaction["merchant_city"] == "ONLINE"
    foreign = ~online & state.notna() & ~state.isin(us_codes)
    usa = ~online & ~foreign
    state_missing = state.isna()
    zip_missing = df_transaction["zip"].isna()

    rows = []
    for name, mask in [("en ligne", online), ("à l'étranger", foreign), ("États-Unis, sur place", usa)]:
        rows.append({
            "type de lieu": name,
            "transactions": int(mask.sum()),
            "merchant_state manquant": int((mask & state_missing).sum()),
            "zip manquant": int((mask & zip_missing).sum()),
        })
    return pd.DataFrame(rows).set_index("type de lieu")


# =============================================================================
# P2-07 : Ville « ONLINE » et canal en ligne
# =============================================================================

def compare_online_city_channel(df_transaction) -> pd.DataFrame:
    """Tableau croisé : ville « ONLINE » (oui/non) et canal de paiement."""
    return pd.crosstab(df_transaction["merchant_city"] == "ONLINE",
                       df_transaction["use_chip"],
                       rownames=["ville ONLINE"], colnames=["canal"])


# =============================================================================
# P2-08 : Valeurs de merchant_state
# =============================================================================

def count_state_values(df_transaction, us_codes) -> pd.Series:
    """
    Sépare les valeurs de merchant_state en codes d'États américains et en
    autres valeurs (noms de pays).
    """
    values = pd.Series(df_transaction["merchant_state"].dropna().unique()).astype(str)
    is_us = values.isin(us_codes)
    unknown_codes = values[(values.str.len() == 2) & ~is_us]
    return pd.Series({
        "valeurs distinctes": len(values),
        "codes d'États américains": int(is_us.sum()),
        "autres valeurs (pays)": int((~is_us).sum()),
        "codes à deux lettres inconnus": len(unknown_codes),
    })


# =============================================================================
# P2-09 : Montants des transactions
# =============================================================================

def describe_amounts(amount: pd.Series) -> pd.Series:
    """
    Montants négatifs, nuls et extrêmes. amount doit déjà être numérique (P3-02).
    """
    q = amount.quantile([0.001, 0.5, 0.999])
    return pd.Series({
        "transactions": len(amount),
        "montants négatifs": int((amount < 0).sum()),
        "montants nuls": int((amount == 0).sum()),
        "minimum": amount.min(),
        "quantile 0,1 %": round(q[0.001], 2),
        "médiane": round(q[0.5], 2),
        "quantile 99,9 %": round(q[0.999], 2),
        "maximum": amount.max(),
    }, dtype=object)


def round_amounts_by_family(df_transaction, mcc_to_family: dict) -> pd.DataFrame:
    """
    Montants entiers (sans centimes, hors montants nuls) par famille de commerçants.
    mcc_to_family : dictionnaire code MCC -> famille (MCC_TO_FAMILLE, P3-05).
    """
    family = df_transaction["mcc"].map(mcc_to_family)
    amount = df_transaction["amount"]
    is_round = (amount != 0) & (amount == amount.round(0))
    resume = (
        pd.DataFrame({"famille": family, "entier": is_round})
        .groupby("famille")
        .agg(transactions=("entier", "size"), montants_entiers=("entier", "sum"))
    )
    resume["part_entiers_%"] = (100 * resume["montants_entiers"] / resume["transactions"]).round(1)
    return resume.sort_values("part_entiers_%", ascending=False)


# =============================================================================
# P2-10 : Valeurs financières des clients
# =============================================================================

def check_user_finances(df_users) -> pd.Series:
    """
    Revenus et dettes nuls, et cohérence entre revenu par habitant et revenu annuel.
    Les colonnes doivent déjà être numériques (P3-02).
    """
    return pd.Series({
        "clients": len(df_users),
        "revenu annuel nul": int((df_users["yearly_income"] == 0).sum()),
        "revenu annuel inférieur à 1 000": int((df_users["yearly_income"] < 1000).sum()),
        "revenu par habitant nul": int((df_users["per_capita_income"] == 0).sum()),
        "dette totale nulle": int((df_users["total_debt"] == 0).sum()),
        "revenu par habitant supérieur au revenu annuel": int(
            (df_users["per_capita_income"] > df_users["yearly_income"]).sum()),
        "revenu annuel minimum": df_users["yearly_income"].min(),
        "revenu annuel maximum": df_users["yearly_income"].max(),
        "score de crédit minimum": int(df_users["credit_score"].min()),
        "score de crédit maximum": int(df_users["credit_score"].max()),
    }, dtype=object)


# =============================================================================
# P2-11 : Informations des cartes
# =============================================================================

def single_value_columns(df) -> list:
    """Colonnes qui n'ont qu'une seule valeur (manquants compris)."""
    return [col for col in df.columns if df[col].nunique(dropna=False) == 1]


def check_card_info(df_card) -> pd.Series:
    """
    Limites de crédit nulles et cohérence entre ouverture du compte,
    expiration et changement de PIN. Les dates doivent déjà être converties (P3-03).
    """
    open_year = df_card["acct_open_date"].dt.year
    expiry_year = df_card["expires"].dt.year
    return pd.Series({
        "cartes": len(df_card),
        "limite de crédit nulle": int((df_card["credit_limit"] == 0).sum()),
        "expiration avant l'ouverture du compte": int(
            (df_card["expires"] < df_card["acct_open_date"]).sum()),
        "PIN changé avant l'année d'ouverture": int((df_card["year_pin_last_changed"] < open_year).sum()),
        "PIN changé après l'année d'expiration": int((df_card["year_pin_last_changed"] > expiry_year).sum()),
    })


def check_card_dates_vs_transactions(df_transaction, df_card) -> pd.DataFrame:
    """
    Transactions faites avant le mois d'ouverture du compte ou après la fin du
    mois d'expiration de la carte : nombre de transactions et de cartes.
    """
    cards = df_card.set_index("id")
    open_date = df_transaction["card_id"].map(cards["acct_open_date"])
    expiry_end = df_transaction["card_id"].map(cards["expires"]) + pd.Timedelta(days=1)
    before_open = df_transaction["date"] < open_date
    after_expiry = df_transaction["date"] >= expiry_end
    rows = []
    for name, mask in [("avant l'ouverture du compte", before_open),
                       ("après l'expiration de la carte", after_expiry)]:
        rows.append({
            "cas": name,
            "transactions": int(mask.sum()),
            "cartes": int(df_transaction.loc[mask, "card_id"].nunique()),
        })
    return pd.DataFrame(rows).set_index("cas")


# =============================================================================
# P2-12 : Date des informations des clients et des cartes
# =============================================================================

def age_reference_table(df_users) -> pd.DataFrame:
    """
    Tableau croisé : mois de naissance et année birth_year + current_age.
    Il montre à quelle date l'âge a été calculé.
    """
    return pd.crosstab(df_users["birth_month"], df_users["birth_year"] + df_users["current_age"],
                       rownames=["mois de naissance"], colnames=["birth_year + current_age"])


def date_card_info(df_card, last_transaction) -> pd.Series:
    """
    Dates les plus récentes des cartes, comparées à la dernière transaction.
    """
    return pd.Series({
        "dernière transaction": last_transaction,
        "ouverture de compte la plus récente": df_card["acct_open_date"].max(),
        "cartes ouvertes après la dernière transaction": int((df_card["acct_open_date"] > last_transaction).sum()),
        "dernière année de changement de PIN": int(df_card["year_pin_last_changed"].max()),
        "cartes avec un changement de PIN après l'année de la dernière transaction": int(
            (df_card["year_pin_last_changed"] > last_transaction.year).sum()),
    }, dtype=object)


# =============================================================================
# P2-13 : Colonne errors
# =============================================================================

def count_error_types(df_transaction) -> pd.Series:
    """Nombre d'occurrences de chaque type d'erreur simple."""
    return (
        df_transaction["errors"].dropna().astype(str)
        .str.split(",").explode().str.strip()
        .value_counts()
    )


# =============================================================================
# P2-14 : Transactions répétées
# =============================================================================

REPEAT_KEYS = ["card_id", "date", "amount", "merchant_id"]


def find_repeated_transactions(df_transaction, keys=REPEAT_KEYS) -> pd.Series:
    """
    Transactions répétées : même carte, même minute, même montant, même commerçant.
    Compte aussi les groupes où au moins une ligne a une erreur.
    """
    in_group = df_transaction.duplicated(subset=keys, keep=False)
    extra = df_transaction.duplicated(subset=keys, keep="first")
    rep = df_transaction.loc[in_group, keys + ["errors"]]
    has_error = rep["errors"].notna().groupby([rep[k] for k in keys], observed=True).any()
    return pd.Series({
        "lignes dans un groupe répété": int(in_group.sum()),
        "groupes répétés": int(in_group.sum() - extra.sum()),
        "lignes en plus de la première de chaque groupe": int(extra.sum()),
        "groupes avec au moins une erreur": int(has_error.sum()),
        "groupes sans aucune erreur": int((~has_error).sum()),
    })


def repeated_examples(df_transaction, keys=REPEAT_KEYS, n_groups=3) -> pd.DataFrame:
    """Lignes des premiers groupes répétés, pour les exemples."""
    rep = df_transaction[df_transaction.duplicated(subset=keys, keep=False)]
    first_keys = rep[keys].drop_duplicates().head(n_groups)
    cols = ["id"] + keys + ["use_chip", "errors"]
    return rep.merge(first_keys, on=keys)[cols].sort_values(keys + ["id"])


# =============================================================================
# P2-15 : Continuité dans le temps
# =============================================================================

def monthly_counts(df_transaction) -> pd.Series:
    """Nombre de transactions par mois."""
    return df_transaction.groupby(df_transaction["date"].dt.to_period("M")).size()


def check_monthly_continuity(counts: pd.Series) -> pd.Series:
    """Mois couverts, mois manquants, mois le plus faible et le plus fort."""
    expected = pd.period_range(counts.index.min(), counts.index.max(), freq="M")
    return pd.Series({
        "premier mois": str(counts.index.min()),
        "dernier mois": str(counts.index.max()),
        "mois attendus": len(expected),
        "mois présents": len(counts),
        "mois manquants": len(expected.difference(counts.index)),
        "mois le plus faible": f"{counts.idxmin()} ({counts.min()} transactions)",
        "mois le plus fort": f"{counts.idxmax()} ({counts.max()} transactions)",
    }, dtype=object)
