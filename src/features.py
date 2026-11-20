"""
Table d'analyse et indicateurs de comportement (phase 4).

Chaque section correspond à un ticket Jira. Les fonctions de contrôle
(check_...) vérifient le critère de fin du ticket.

Les indicateurs qui regardent le passé (P4-04 à P4-07) n'utilisent que les
transactions précédentes : une transaction n'entre jamais dans le calcul de
son propre indicateur.
"""

from pathlib import Path
from statistics import median

import numpy as np
import pandas as pd

# =============================================================================
# P4-01 : Construire la table d'analyse
# =============================================================================

# Colonnes ajoutées depuis les tables de dimension
USER_COLUMNS = [
    "gender",
    "birth_year",
    "birth_month",
    "yearly_income",
    "total_debt",
    "credit_score",
    "suspicious_income",
]
CARD_COLUMNS = [
    "card_brand",
    "card_type",
    "has_chip",
    "credit_limit",
    "acct_open_date",
    "expires",
    "zero_credit_limit",
]

# Colonnes brutes remplacées en phase 3 par des colonnes nettoyées
# (merchant_state -> merchant_state_clean et merchant_country, zip -> zip_clean)
RAW_COLUMNS_REPLACED = ["merchant_state", "zip"]


def _map_column(keys: pd.Series, table: pd.DataFrame, column: str) -> pd.Series:
    """Ajoute une colonne d'une table de dimension en gardant son type."""
    values = keys.map(table[column])
    if isinstance(table[column].dtype, pd.CategoricalDtype):
        values = values.astype(table[column].dtype)
    elif values.notna().all():
        values = values.astype(table[column].dtype)
    return values


def build_analysis_table(
    df_transaction: pd.DataFrame,
    df_users: pd.DataFrame,
    df_card: pd.DataFrame,
    df_mcc: pd.DataFrame,
    df_labels: pd.DataFrame,
) -> pd.DataFrame:
    """
    P4-01 : une ligne par transaction, avec les informations du client,
    de la carte, la famille du code MCC et l'étiquette de fraude.

    Les colonnes sont ajoutées avec map (et non merge), pour ne pas copier
    la table de 13 millions de lignes à chaque jointure : la table des
    transactions reçue est complétée sur place, puis retournée.
    is_fraud vaut 1, 0 ou vide (transaction sans étiquette, voir P2-17).
    """
    df = df_transaction
    for col in RAW_COLUMNS_REPLACED:
        if col in df.columns:
            del df[col]

    users = df_users.set_index("id")
    for col in USER_COLUMNS:
        df[col] = _map_column(df["client_id"], users, col)

    cards = df_card.set_index("id")
    for col in CARD_COLUMNS:
        df[col] = _map_column(df["card_id"], cards, col)

    families = df_mcc.set_index("mcc_code")["famille"].astype("category")
    df["mcc_family"] = df["mcc"].map(families).astype(families.dtype)

    labels = df_labels.set_index("id")["is_fraud"]
    df["is_fraud"] = df["id"].map(labels).astype("Int8")

    # Types plus légers pour les montants des clients et des cartes
    for col in ["yearly_income", "total_debt", "credit_limit"]:
        df[col] = df[col].astype("int32")
    return df


def check_analysis_table(df: pd.DataFrame, n_transactions: int) -> pd.DataFrame:
    """
    Critère de fin de P4-01 : même nombre de lignes que la table des transactions.
    Vérifie aussi qu'aucun identifiant n'est en double et qu'aucune colonne
    ajoutée n'est vide (sauf is_fraud, partielle par nature).
    """
    added = USER_COLUMNS + CARD_COLUMNS + ["mcc_family"]
    rows = [
        ("lignes de la table d'analyse", len(df), len(df) == n_transactions),
        ("identifiants en double", int(df["id"].duplicated().sum()), not df["id"].duplicated().any()),
        (
            "valeurs vides dans les colonnes ajoutées",
            int(df[added].isna().sum().sum()),
            df[added].notna().all().all(),
        ),
        ("transactions étiquetées (is_fraud)", int(df["is_fraud"].notna().sum()), True),
    ]
    return pd.DataFrame(rows, columns=["contrôle", "obtenu", "statut"])


# =============================================================================
# Outils communs : ordre chronologique par carte ou par client
# =============================================================================

# Écart entre deux groupes dans la clé de tri : plus grand que toute la période
# en minutes (environ 5,2 millions de minutes de 2010 à 2019)
_GROUP_OFFSET = 10_000_000


def _sort_order(df: pd.DataFrame, group_col: str) -> np.ndarray:
    """Positions des lignes triées par groupe, puis date, puis identifiant."""
    return np.lexsort(
        (df["id"].to_numpy(), df["date"].to_numpy(), df[group_col].to_numpy())
    )


def _minutes(dates: pd.Series) -> np.ndarray:
    """Dates converties en nombre de minutes (entiers)."""
    return dates.to_numpy().astype("datetime64[m]").astype(np.int64)


def _back_to_original(values_sorted: np.ndarray, order: np.ndarray, dtype) -> np.ndarray:
    """Remet dans l'ordre de la table des valeurs calculées dans l'ordre trié."""
    out = np.empty(len(order), dtype=dtype)
    out[order] = values_sorted
    return out


def count_previous_in_window(
    df: pd.DataFrame, group_col: str, window_minutes: int, values=None
) -> np.ndarray:
    """
    Pour chaque transaction : nombre de transactions précédentes du même groupe
    (carte ou client) dans la fenêtre ]date - window_minutes, date].
    Avec values (colonne 0/1), compte seulement les transactions où values = 1.

    Les lignes sont triées par groupe et par date. La clé de tri
    groupe * _GROUP_OFFSET + minutes permet une recherche binaire
    (np.searchsorted) sur toute la table d'un coup, sans boucle.
    """
    order = _sort_order(df, group_col)
    minutes = _minutes(df["date"])[order]
    group = df[group_col].to_numpy()[order].astype(np.int64)
    key = group * _GROUP_OFFSET + (minutes - minutes.min())

    # Première position dont la date est dans la fenêtre
    start = np.searchsorted(key, key - window_minutes, side="right")
    position = np.arange(len(key))
    if values is None:
        counts = position - start
    else:
        flags = np.asarray(values)[order].astype(np.int64)
        cumulative = np.concatenate([[0], np.cumsum(flags)])
        counts = cumulative[position] - cumulative[start]
    return _back_to_original(counts, order, np.int32)


# =============================================================================
# P4-02 : Variables de temps
# =============================================================================

# La nuit va de 0 h à 5 h 59
NIGHT_END_HOUR = 6


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4-02 : année, mois, jour de la semaine (0 = lundi), heure,
    indicateurs « nuit » (0 h à 5 h 59) et « week-end » (samedi et dimanche).
    """
    dates = df["date"]
    df["year"] = dates.dt.year.astype("int16")
    df["month"] = dates.dt.month.astype("int8")
    df["weekday"] = dates.dt.weekday.astype("int8")
    df["hour"] = dates.dt.hour.astype("int8")
    df["is_night"] = (df["hour"] < NIGHT_END_HOUR).astype("int8")
    df["is_weekend"] = (df["weekday"] >= 5).astype("int8")
    return df


def check_time_features(df: pd.DataFrame, n: int = 10, seed: int = 0) -> pd.DataFrame:
    """
    Critère de fin de P4-02 : colonnes vérifiées sur un échantillon.
    Recalcule chaque variable avec les objets date de Python, ligne par ligne.
    """
    sample = df.sample(n, random_state=seed)[
        ["id", "date", "year", "month", "weekday", "hour", "is_night", "is_weekend"]
    ].copy()
    rows = []
    for _, r in sample.iterrows():
        d = r["date"].to_pydatetime()
        attendu = (d.year, d.month, d.weekday(), d.hour, int(d.hour < NIGHT_END_HOUR), int(d.weekday() >= 5))
        obtenu = (r["year"], r["month"], r["weekday"], r["hour"], r["is_night"], r["is_weekend"])
        rows.append(tuple(int(v) for v in obtenu) == attendu)
    sample["identique au recalcul"] = rows
    return sample


# =============================================================================
# P4-03 : Âge du client à la date de la transaction
# =============================================================================


def add_age_at_transaction(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4-03 : âge à la date de la transaction, calculé avec birth_year et
    birth_month (current_age est l'âge en février 2020, voir P2-12).
    Le jour de naissance n'est pas connu : l'anniversaire compte à partir
    du premier jour du mois de naissance.
    """
    birthday_not_reached = (df["month"] < df["birth_month"]).astype("int16")
    age = df["year"].astype("int16") - df["birth_year"].astype("int16") - birthday_not_reached
    df["age_at_transaction"] = age.astype("int8")
    return df


def check_age(df: pd.DataFrame, n: int = 10, seed: int = 1) -> pd.DataFrame:
    """
    Critère de fin de P4-03 : âges vérifiés à la main sur 10 transactions.
    Affiche le calcul écrit en clair pour chaque ligne.
    """
    sample = df.sample(n, random_state=seed)[
        ["id", "date", "birth_year", "birth_month", "age_at_transaction"]
    ].copy()
    calculs, attendus = [], []
    for _, r in sample.iterrows():
        annee, mois = r["date"].year, r["date"].month
        retrait = 1 if mois < r["birth_month"] else 0
        attendu = annee - r["birth_year"] - retrait
        calculs.append(f"{annee} - {r['birth_year']} - {retrait} = {attendu}")
        attendus.append(attendu)
    sample["calcul à la main"] = calculs
    sample["identique"] = sample["age_at_transaction"].to_numpy() == np.array(attendus)
    return sample


# =============================================================================
# P4-04 : Écart au montant habituel du client
# =============================================================================

# Nombre d'achats précédents nécessaires pour calculer un montant habituel
MIN_PURCHASES_HISTORY = 10


def add_amount_gap(df: pd.DataFrame, min_history: int = MIN_PURCHASES_HISTORY) -> pd.DataFrame:
    """
    P4-04 : montant habituel du client = médiane de ses achats précédents
    (montants positifs, transactions précédentes seulement, au moins
    min_history achats). Ajoute :
    - client_median_amount : ce montant habituel (vide si historique trop court) ;
    - amount_gap : montant - montant habituel, en dollars ;
    - amount_ratio : montant / montant habituel (2 = deux fois le montant habituel).
    """
    order = _sort_order(df, "client_id")
    client = df["client_id"].to_numpy()[order]
    amount = df["amount"].to_numpy()[order].astype("float64")

    # Les remboursements et les montants nuls ne comptent pas dans la médiane
    purchases = pd.Series(np.where(amount > 0, amount, np.nan))
    previous = purchases.groupby(client).shift(1)
    med = (
        previous.groupby(client)
        .expanding(min_periods=min_history)
        .median()
        .reset_index(level=0, drop=True)
        .sort_index()
        .to_numpy()
    )
    df["client_median_amount"] = _back_to_original(med, order, np.float32)
    df["amount_gap"] = (df["amount"] - df["client_median_amount"]).astype("float32")
    df["amount_ratio"] = (df["amount"] / df["client_median_amount"]).astype("float32")
    return df


def check_amount_gap(df: pd.DataFrame, client_id: int, n: int = 15) -> pd.DataFrame:
    """
    Critère de fin de P4-04 : colonne vérifiée sur un client.
    Recalcule la médiane des achats précédents avec une boucle Python simple
    (statistics.median), pour les n premières transactions après l'historique minimal.
    """
    tx = df.loc[df["client_id"] == client_id, ["id", "date", "amount", "client_median_amount"]]
    tx = tx.sort_values(["date", "id"])
    rows, history = [], []
    for _, r in tx.iterrows():
        attendu = median(history) if len(history) >= MIN_PURCHASES_HISTORY else np.nan
        rows.append((r["id"], r["date"], r["amount"], len(history), attendu, r["client_median_amount"]))
        if r["amount"] > 0:
            history.append(r["amount"])
    result = pd.DataFrame(
        rows, columns=["id", "date", "amount", "achats précédents", "médiane recalculée", "client_median_amount"]
    )
    ecart = (result["médiane recalculée"] - result["client_median_amount"]).abs()
    both_empty = result["médiane recalculée"].isna() & result["client_median_amount"].isna()
    result["identique"] = (ecart < 0.01) | both_empty
    print(f"Client {client_id} : {len(result)} transactions, toutes identiques au recalcul : {result['identique'].all()}")
    return result[result["achats précédents"] >= MIN_PURCHASES_HISTORY - 2].head(n)


# =============================================================================
# P4-05 : Fréquence d'utilisation de la carte
# =============================================================================


def add_card_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4-05 : card_tx_1h et card_tx_24h, nombre de transactions précédentes
    de la carte dans l'heure et dans les 24 heures.
    """
    df["card_tx_1h"] = count_previous_in_window(df, "card_id", 60).astype("int16")
    df["card_tx_24h"] = count_previous_in_window(df, "card_id", 24 * 60).astype("int16")
    return df


# =============================================================================
# P4-06 : Échecs d'authentification récents
# =============================================================================


def add_recent_auth_errors(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4-06 : card_auth_errors_24h, nombre de transactions précédentes de la
    carte dans les 24 heures avec un échec d'authentification
    (PIN, CVV, numéro, expiration ou code postal : has_auth_error, P3-06).
    """
    df["card_auth_errors_24h"] = count_previous_in_window(
        df, "card_id", 24 * 60, values=df["has_auth_error"]
    ).astype("int16")
    return df


def recount_card_activity(df: pd.DataFrame, card_id: int) -> pd.DataFrame:
    """
    Critères de fin de P4-05 et P4-06 : colonnes vérifiées sur une carte.
    Recompte avec une boucle simple, transaction par transaction, ce qui
    s'est passé sur la carte dans l'heure et dans les 24 heures précédentes.
    """
    counters = [c for c in ["card_tx_1h", "card_tx_24h", "card_auth_errors_24h"] if c in df.columns]
    cols = ["id", "date", "has_auth_error"] + counters
    tx = df.loc[df["card_id"] == card_id, cols].sort_values(["date", "id"]).reset_index(drop=True)
    dates = tx["date"].to_list()
    errors = tx["has_auth_error"].to_list()
    one_hour, one_day = pd.Timedelta(hours=1), pd.Timedelta(hours=24)
    recount = []
    for i, d in enumerate(dates):
        # On remonte dans le passé de la carte tant qu'on reste dans les 24 heures
        n1 = n24 = e24 = 0
        j = i - 1
        while j >= 0 and dates[j] > d - one_day:
            n24 += 1
            e24 += errors[j]
            if dates[j] > d - one_hour:
                n1 += 1
            j -= 1
        recount.append((n1, n24, e24))
    tx[["recompte_1h", "recompte_24h", "recompte_erreurs_24h"]] = recount
    if "card_tx_1h" in tx.columns:
        tx["identique_frequence"] = (tx["card_tx_1h"] == tx["recompte_1h"]) & (tx["card_tx_24h"] == tx["recompte_24h"])
    if "card_auth_errors_24h" in tx.columns:
        tx["identique_erreurs"] = tx["card_auth_errors_24h"] == tx["recompte_erreurs_24h"]
    return tx


# =============================================================================
# P4-07 : Premières fois
# =============================================================================


def add_first_time_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4-07 : premier achat du client chez ce commerçant (is_first_merchant),
    dans cette catégorie MCC (is_first_mcc) et dans ce pays (is_first_country,
    « ONLINE » compte comme un lieu). Ajoute aussi client_tx_rank, le nombre
    de transactions précédentes du client : au début de l'historique, tout
    est une première fois.
    """
    order = _sort_order(df, "client_id")
    ordered = pd.DataFrame(
        {
            "client_id": df["client_id"].to_numpy()[order],
            "merchant_id": df["merchant_id"].to_numpy()[order],
            "mcc": df["mcc"].to_numpy()[order],
            "country": df["merchant_country"].cat.codes.to_numpy()[order],
        }
    )
    for col, name in [
        ("merchant_id", "is_first_merchant"),
        ("mcc", "is_first_mcc"),
        ("country", "is_first_country"),
    ]:
        first = (~ordered.duplicated(["client_id", col])).to_numpy()
        df[name] = _back_to_original(first, order, np.int8)
    rank = ordered.groupby("client_id").cumcount().to_numpy()
    df["client_tx_rank"] = _back_to_original(rank, order, np.int32)
    return df


def check_first_time_flags(df: pd.DataFrame, client_id: int, n: int = 15) -> pd.DataFrame:
    """
    Critère de fin de P4-07 : indicateurs vérifiés sur un client.
    Recalcule les trois indicateurs avec des ensembles Python, ligne par ligne.
    """
    cols = ["id", "date", "merchant_id", "mcc", "merchant_country", "client_tx_rank",
            "is_first_merchant", "is_first_mcc", "is_first_country"]
    tx = df.loc[df["client_id"] == client_id, cols].sort_values(["date", "id"]).reset_index(drop=True)
    seen = {"merchant_id": set(), "mcc": set(), "merchant_country": set()}
    expected = []
    for _, r in tx.iterrows():
        row = []
        for col in ["merchant_id", "mcc", "merchant_country"]:
            row.append(int(r[col] not in seen[col]))
            seen[col].add(r[col])
        expected.append(row)
    expected = np.array(expected)
    tx["identique"] = (
        (tx["is_first_merchant"].to_numpy() == expected[:, 0])
        & (tx["is_first_mcc"].to_numpy() == expected[:, 1])
        & (tx["is_first_country"].to_numpy() == expected[:, 2])
        & (tx["client_tx_rank"].to_numpy() == np.arange(len(tx)))
    )
    print(f"Client {client_id} : {len(tx)} transactions, toutes identiques au recalcul : {tx['identique'].all()}")
    later = tx[(tx["client_tx_rank"] > 100) & (tx[["is_first_merchant", "is_first_mcc", "is_first_country"]].sum(axis=1) > 0)]
    return later.head(n)


# =============================================================================
# P4-08 : Indicateurs de contexte
# =============================================================================


def add_context_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4-08 : indicateurs de contexte.
    - is_online et is_foreign existent déjà (P3-07), mcc_family vient de P4-01 ;
    - is_round_amount : achat (montant positif) sans centimes ;
    - outside_card_validity : transaction avant le mois d'ouverture du compte
      ou après la fin du mois d'expiration de la carte (règle de P2-11).
    """
    amount = df["amount"]
    df["is_round_amount"] = ((amount > 0) & (amount % 1 == 0)).astype("int8")
    before_open = df["date"] < df["acct_open_date"]
    after_expiry = df["date"] >= df["expires"] + pd.Timedelta(days=1)
    df["outside_card_validity"] = (before_open | after_expiry).astype("int8")
    return df


def check_context_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Critère de fin de P4-08 : nombre de transactions par indicateur de contexte."""
    flags = ["is_online", "is_foreign", "is_round_amount", "outside_card_validity"]
    resume = pd.DataFrame(
        {
            "transactions avec l'indicateur": [int(df[c].sum()) for c in flags],
            "part_%": [round(100 * df[c].mean(), 2) for c in flags],
        },
        index=flags,
    )
    return resume


# =============================================================================
# P4-09 : Catalogue des indicateurs
# =============================================================================

INDICATOR_CATALOGUE = [
    # (colonne, ticket, définition, raison pour laquelle il peut signaler une fraude)
    ("is_night", "P4-02", "Transaction entre 0 h et 5 h 59",
     "Un achat en pleine nuit est inhabituel pour la plupart des clients"),
    ("is_weekend", "P4-02", "Transaction le samedi ou le dimanche",
     "Sert de contexte : le rythme des achats change le week-end"),
    ("age_at_transaction", "P4-03", "Âge du client à la date de la transaction",
     "Sert à vérifier que le score ne désavantage pas un groupe d'âge (P9-15)"),
    ("amount_ratio", "P4-04", "Montant divisé par la médiane des achats précédents du client",
     "Un fraudeur dépense souvent beaucoup plus que le titulaire"),
    ("card_tx_1h", "P4-05", "Transactions précédentes de la carte dans l'heure",
     "Une rafale d'achats peut indiquer une carte volée testée ou vidée"),
    ("card_tx_24h", "P4-05", "Transactions précédentes de la carte dans les 24 heures",
     "Même raison, sur une journée"),
    ("card_auth_errors_24h", "P4-06", "Échecs d'authentification de la carte dans les 24 heures",
     "Plusieurs mauvais PIN, CVV ou numéros : quelqu'un essaie la carte sans la connaître"),
    ("is_first_merchant", "P4-07", "Premier achat du client chez ce commerçant",
     "Le fraudeur achète chez des commerçants que le titulaire ne fréquente pas"),
    ("is_first_mcc", "P4-07", "Premier achat du client dans cette catégorie MCC",
     "Même raison, pour un type de commerce nouveau"),
    ("is_first_country", "P4-07", "Premier achat du client dans ce pays (ou premier achat en ligne)",
     "Une carte copiée est souvent utilisée dans un autre pays"),
    ("is_online", "P3-07", "Achat en ligne",
     "Le paiement sans carte physique est le plus exposé à la fraude"),
    ("is_foreign", "P3-07", "Achat sur place hors des États-Unis",
     "Les clients achètent presque toujours aux États-Unis"),
    ("is_round_amount", "P4-08", "Achat sans centimes",
     "Les fraudeurs testent parfois des montants ronds"),
    ("outside_card_validity", "P4-08", "Transaction avant l'ouverture du compte ou après l'expiration",
     "Une carte ne devrait pas servir hors de sa période de validité"),
    ("has_auth_error", "P3-06", "La transaction elle-même a un échec d'authentification",
     "Signe direct d'une tentative avec de mauvaises informations"),
    ("is_repeated", "P3-08", "Seconde ligne d'un groupe répété sans erreur",
     "Possible double débit"),
]


def indicator_catalogue() -> pd.DataFrame:
    """P4-09 : le catalogue des indicateurs, sous forme de tableau."""
    return pd.DataFrame(
        INDICATOR_CATALOGUE, columns=["colonne", "ticket", "définition", "pourquoi c'est un signal"]
    )


def describe_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pour chaque indicateur du catalogue : part des transactions concernées
    (indicateurs 0/1) ou médiane et quantile 99,9 % (indicateurs numériques).
    """
    rows = []
    for col, ticket, *_ in INDICATOR_CATALOGUE:
        s = df[col]
        if s.dropna().isin([0, 1]).all():
            rows.append({"colonne": col, "type": "0/1", "transactions à 1": int(s.sum()),
                         "part_%": round(100 * s.mean(), 3), "médiane": np.nan, "quantile 99,9 %": np.nan})
        else:
            rows.append({"colonne": col, "type": "nombre", "transactions à 1": np.nan, "part_%": np.nan,
                         "médiane": round(float(s.median()), 2), "quantile 99,9 %": round(float(s.quantile(0.999)), 2)})
    return pd.DataFrame(rows).set_index("colonne")


# =============================================================================
# P4-10 : Contrôler et enregistrer la table d'analyse
# =============================================================================

# Bornes attendues pour les colonnes créées en phase 4
EXPECTED_BOUNDS = {
    "year": (2010, 2019),
    "month": (1, 12),
    "weekday": (0, 6),
    "hour": (0, 23),
    "age_at_transaction": (0, 120),
    "card_tx_1h": (0, None),
    "card_tx_24h": (0, None),
    "card_auth_errors_24h": (0, None),
    "client_tx_rank": (0, None),
}

# Colonnes où des valeurs vides sont normales
EXPECTED_MISSING = {
    "is_fraud": "transactions sans étiquette (P2-17)",
    "errors": "transactions sans erreur",
    "client_median_amount": "moins de 10 achats précédents",
    "amount_gap": "moins de 10 achats précédents",
    "amount_ratio": "moins de 10 achats précédents",
}

ANALYSIS_PATH = Path(__file__).resolve().parent.parent / "data" / "clean" / "analysis.parquet"


def check_missing_and_bounds(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4-10 : valeurs vides par colonne (avec leur explication) et contrôle
    des bornes des colonnes créées en phase 4.
    """
    rows = []
    missing = df.isna().sum()
    for col, n in missing[missing > 0].items():
        raison = EXPECTED_MISSING.get(col, "inattendu")
        rows.append({"contrôle": f"valeurs vides : {col}", "obtenu": int(n),
                     "explication": raison, "statut": raison != "inattendu"})
    for col, (low, high) in EXPECTED_BOUNDS.items():
        lo, hi = df[col].min(), df[col].max()
        ok = lo >= low and (high is None or hi <= high)
        rows.append({"contrôle": f"bornes : {col}", "obtenu": f"{lo} à {hi}",
                     "explication": f"attendu de {low} à {high if high is not None else '...'}", "statut": bool(ok)})
    return pd.DataFrame(rows)


def save_analysis_table(df: pd.DataFrame, path: Path = ANALYSIS_PATH) -> pd.Series:
    """
    P4-10 : enregistre la table d'analyse au format Parquet (compression zstd).
    Retourne lignes, colonnes, mémoire et taille du fichier.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False, compression="zstd")
    return pd.Series(
        {
            "lignes": len(df),
            "colonnes": df.shape[1],
            "mémoire en Mo": round(df.memory_usage(deep=True).sum() / 1e6, 1),
            "taille du fichier en Mo": round(path.stat().st_size / 1e6, 1),
        }
    )
