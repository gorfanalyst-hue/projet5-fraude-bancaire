"""
Détection des transactions à risque (phase 7).

Deux variantes :
- sans étiquettes (P7-01 à P7-07) : règles métier et anomalies combinées en
  un score de risque de 0 à 100. Les étiquettes de fraude ne servent pas ;
- avec étiquettes (P7-08 et P7-11) : modèle supervisé, et évaluation du score
  avec les étiquettes de fraude.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, IsolationForest
from sklearn.metrics import average_precision_score

# =============================================================================
# P7-01 : Règles métier
# =============================================================================

# Un client doit avoir un historique pour qu'une « première fois » compte (P4-07)
MIN_HISTORY = 100

# Une règle par signal du catalogue (P4-09) : code, libellé, points, condition.
# Points : 3 = signal fort, 2 = signal moyen, 1 = signal faible (fréquent seul).
# Seuils fixés avec les distributions de la phase 4, sans les étiquettes de fraude :
# une règle à 3 points touche moins de 0,3 % des transactions, une règle à 2 points moins de 1 %.
RULES = [
    ("R01", "2 échecs d'authentification ou plus sur la carte en 24 h", 3, "card_auth_errors_24h >= 2"),
    ("R02", "échec d'authentification sur la transaction", 2, "has_auth_error == 1"),
    ("R03", "montant au moins 20 fois plus élevé que d'habitude (300 $ ou plus)", 3,
     "amount_ratio >= 20 and amount >= 300"),
    ("R04", "rafale : 5 transactions ou plus de la carte dans l'heure précédente", 3, "card_tx_1h >= 5"),
    ("R05", "15 transactions ou plus de la carte dans les 24 heures précédentes", 2, "card_tx_24h >= 15"),
    ("R06", "premier achat du client dans ce pays (après 100 transactions)", 2,
     f"is_first_country == 1 and client_tx_rank >= {MIN_HISTORY}"),
    ("R07", "achat sur place à l'étranger", 2, "is_foreign == 1"),
    ("R08", "nouveau commerçant dans une nouvelle catégorie (après 100 transactions)", 2,
     f"is_first_merchant == 1 and is_first_mcc == 1 and client_tx_rank >= {MIN_HISTORY}"),
    ("R09", "achat de nuit (0 h à 5 h 59)", 1, "is_night == 1"),
    ("R10", "achat en ligne", 1, "is_online == 1"),
    ("R11", "achat sans centimes", 1, "is_round_amount == 1"),
    ("R12", "transaction hors de la période de validité de la carte", 3, "outside_card_validity == 1"),
    ("R13", "doublon possible (seconde ligne d'un groupe répété)", 2, "is_repeated == 1"),
]
# Libellés courts, pour les graphiques et le tableau de bord
SHORT_LABELS = {
    "R01": "échecs d'authentification répétés",
    "R02": "échec d'authentification",
    "R03": "montant inhabituel",
    "R04": "rafale dans l'heure",
    "R05": "journée très active",
    "R06": "nouveau pays",
    "R07": "achat à l'étranger",
    "R08": "nouveau commerçant et nouvelle catégorie",
    "R09": "achat de nuit",
    "R10": "achat en ligne",
    "R11": "montant rond",
    "R12": "hors validité de la carte",
    "R13": "doublon possible",
}

RULE_COLUMNS = sorted({c for *_, cond in RULES for c in cond.replace("(", " ").split() if c.isidentifier()
                       and c not in ("and", "or", "not")})


def rules_table() -> pd.DataFrame:
    """Les règles, sous forme de tableau."""
    return pd.DataFrame(RULES, columns=["code", "règle", "points", "condition"]).set_index("code")


def apply_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    P7-01 : une colonne 0/1 par règle, puis rule_points (somme des points des
    règles déclenchées) et n_rules (nombre de règles déclenchées).
    """
    flags = pd.DataFrame(index=df.index)
    rule_points = np.zeros(len(df), dtype=np.int16)
    n_rules = np.zeros(len(df), dtype=np.int8)
    for code, _, points, condition in RULES:
        flag = df.eval(condition).fillna(False).to_numpy().astype(np.int8)
        flags[code] = flag
        rule_points += flag * points
        n_rules += flag
    flags["rule_points"] = rule_points
    flags["n_rules"] = n_rules
    return flags


def count_rules(flags: pd.DataFrame) -> pd.DataFrame:
    """P7-01 : nombre et part des transactions touchées par chaque règle."""
    table = rules_table()[["règle", "points"]]
    table["transactions touchées"] = [int(flags[c].sum()) for c in table.index]
    table["part_%"] = (100 * table["transactions touchées"] / len(flags)).round(3)
    return table


# =============================================================================
# P7-02 : Anomalies avec Isolation Forest
# =============================================================================

BEHAVIOUR_FEATURES = [
    "log_amount",
    "log_amount_ratio",
    "card_tx_1h",
    "card_tx_24h",
    "card_auth_errors_24h",
    "hour",
    "is_online",
    "is_foreign",
    "is_first_merchant",
    "is_first_mcc",
    "is_first_country",
    "has_auth_error",
]


def behaviour_matrix(df: pd.DataFrame) -> np.ndarray:
    """
    P7-02 : variables de comportement pour Isolation Forest, dans l'ordre de
    BEHAVIOUR_FEATURES (tableau numpy float32, une ligne par transaction).
    - log_amount : logarithme du montant (le signe est gardé pour les remboursements) ;
    - log_amount_ratio : logarithme du rapport au montant habituel
      (0 quand le rapport n'est pas calculé : historique trop court ou remboursement).
    Le tableau est rempli colonne par colonne pour limiter la mémoire.
    """
    x = np.empty((len(df), len(BEHAVIOUR_FEATURES)), dtype=np.float32)
    amount = df["amount"].to_numpy(dtype="float64")
    x[:, 0] = np.sign(amount) * np.log1p(np.abs(amount))
    ratio = df["amount_ratio"].to_numpy(dtype="float64")
    x[:, 1] = np.log(np.where(np.isfinite(ratio) & (ratio > 0), ratio, 1.0))
    del amount, ratio
    for j, col in enumerate(BEHAVIOUR_FEATURES[2:], start=2):
        x[:, j] = df[col].to_numpy()
    return x


def train_isolation_forest(x: np.ndarray, sample_size: int = 500_000, seed: int = 42) -> IsolationForest:
    """
    P7-02 : Isolation Forest entraîné sur un échantillon aléatoire (la mémoire ne
    permet pas les 13 millions de lignes d'un coup ; 500 000 lignes suffisent).
    """
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(x), size=min(sample_size, len(x)), replace=False)
    model = IsolationForest(n_estimators=100, max_samples=256, random_state=seed, n_jobs=-1)
    return model.fit(x[idx])


def anomaly_scores(model: IsolationForest, x: np.ndarray, chunk: int = 1_000_000) -> np.ndarray:
    """
    P7-02 : score d'anomalie de chaque transaction, calculé par morceaux.
    Plus le score est haut, plus la transaction est isolée facilement (atypique).
    """
    parts = [-model.score_samples(x[i:i + chunk]) for i in range(0, len(x), chunk)]
    return np.concatenate(parts).astype("float32")


# =============================================================================
# P7-03 : Score de risque
# =============================================================================

# Au-delà de 8 points, les règles ne font plus monter le score
RULE_POINTS_CAP = 8
RULE_WEIGHT = 0.5
SHARES = (0.005, 0.01, 0.02)


def risk_score(rule_points, anomaly) -> np.ndarray:
    """
    P7-03 : score de risque de 0 à 100.
    - partie règles : points des règles déclenchées, plafonnés à 8, ramenés entre 0 et 1 ;
    - partie anomalies : rang de la transaction selon le score d'anomalie, entre 0 et 1
      (0,99 = plus atypique que 99 % des transactions).
    Score = 100 × (0,5 × partie règles + 0,5 × partie anomalies).
    """
    rule_part = np.minimum(np.asarray(rule_points, dtype=float), RULE_POINTS_CAP) / RULE_POINTS_CAP
    anomaly_part = pd.Series(anomaly).rank(pct=True).to_numpy()
    return np.round(100 * (RULE_WEIGHT * rule_part + (1 - RULE_WEIGHT) * anomaly_part), 3)


def threshold_for_share(score, share: float) -> float:
    """Valeur du score à partir de laquelle on garde la part `share` la plus risquée."""
    return float(np.quantile(score, 1 - share))


# =============================================================================
# P7-04 : Valider le score
# =============================================================================


def threshold_summary(df: pd.DataFrame, score, shares=SHARES) -> pd.DataFrame:
    """
    P7-04 : pour chaque seuil, transactions, clients et cartes signalés, et
    charge de travail moyenne par jour (transactions signalées / jours couverts).
    """
    days = df["date"].dt.normalize().nunique()
    n_clients = df["client_id"].nunique()
    rows = []
    for share in shares:
        threshold = threshold_for_share(score, share)
        flagged = score >= threshold
        clients = df.loc[flagged, "client_id"].nunique()
        rows.append({
            "seuil": f"{100 * share:g} %",
            "score minimal": round(threshold, 2),
            "transactions signalées": int(flagged.sum()),
            "clients signalés": clients,
            "part des clients actifs_%": round(100 * clients / n_clients, 1),
            "cartes signalées": df.loc[flagged, "card_id"].nunique(),
            "signalements par jour": round(flagged.sum() / days, 1),
        })
    return pd.DataFrame(rows).set_index("seuil")


def yearly_flag_rates(year: pd.Series, score, shares=SHARES) -> pd.DataFrame:
    """P7-04 : taux de signalement de chaque année, pour chaque seuil (stabilité)."""
    table = {}
    for share in shares:
        flagged = pd.Series(score >= threshold_for_share(score, share), index=year.index)
        table[f"seuil {100 * share:g} %"] = (100 * flagged.groupby(year).mean()).round(3)
    return pd.DataFrame(table)


def review_sample(flagged: pd.DataFrame, n: int = 50, seed: int = 0) -> pd.DataFrame:
    """P7-04 : échantillon aléatoire de n transactions signalées pour la revue manuelle."""
    return flagged.sample(n=min(n, len(flagged)), random_state=seed).sort_values("risk_score", ascending=False)


# =============================================================================
# P7-07 : Liste priorisée
# =============================================================================

ANOMALY_REASON = "comportement atypique (Isolation Forest)"


def main_reason(flags: pd.DataFrame) -> pd.Series:
    """
    P7-07 : raison principale = la règle déclenchée qui a le plus de points
    (en cas d'égalité, la première de la liste). Sans règle déclenchée, la
    raison est l'anomalie détectée par Isolation Forest.
    """
    codes = [r[0] for r in RULES]
    points = np.array([r[2] for r in RULES], dtype=np.int8)
    weighted = flags[codes].to_numpy(dtype=np.int8) * points
    best = weighted.argmax(axis=1)
    labels = np.array([f"{r[0]} : {r[1]}" for r in RULES], dtype=object)
    reason = labels[best]
    reason[weighted.max(axis=1) == 0] = ANOMALY_REASON
    return pd.Series(reason, index=flags.index, name="raison principale")


def triggered_rules(flags: pd.DataFrame) -> pd.Series:
    """P7-07 : liste des codes des règles déclenchées (exemple : « R03, R10 »)."""
    codes = [r[0] for r in RULES]
    values = flags[codes].to_numpy().astype(bool)
    text = [", ".join(c for c, on in zip(codes, row) if on) or "aucune" for row in values]
    return pd.Series(text, index=flags.index, name="règles déclenchées")


# =============================================================================
# P7-08 et P7-11 : Variante avec étiquettes de fraude
# =============================================================================

SUPERVISED_FEATURES = BEHAVIOUR_FEATURES + [
    "is_night", "is_weekend", "weekday", "is_round_amount", "outside_card_validity",
    "family_code", "channel_code",
]
CATEGORICAL_FEATURES = ["family_code", "channel_code"]


def supervised_matrix(df: pd.DataFrame) -> np.ndarray:
    """
    P7-08 : variables du modèle supervisé, dans l'ordre de SUPERVISED_FEATURES :
    variables de comportement + contexte. Le genre et l'âge ne sont pas utilisés
    (choix éthique, voir P9-15).
    """
    x = np.empty((len(df), len(SUPERVISED_FEATURES)), dtype=np.float32)
    x[:, :len(BEHAVIOUR_FEATURES)] = behaviour_matrix(df)
    j = len(BEHAVIOUR_FEATURES)
    for col in ["is_night", "is_weekend", "weekday", "is_round_amount", "outside_card_validity"]:
        x[:, j] = df[col].to_numpy()
        j += 1
    x[:, j] = df["mcc_family"].cat.codes.to_numpy()
    x[:, j + 1] = df["use_chip"].cat.codes.to_numpy()
    return x


def training_rows(y, train_mask, negative_share: float = 0.2, seed: int = 42) -> np.ndarray:
    """
    P7-08 : positions des lignes d'apprentissage. Toutes les fraudes sont gardées,
    avec une part des autres transactions (20 %), pour un apprentissage plus rapide.
    """
    y = np.asarray(y)
    rng = np.random.default_rng(seed)
    keep = np.asarray(train_mask) & ((y == 1) | (rng.random(len(y)) < negative_share))
    return np.flatnonzero(keep)


def train_supervised(x: np.ndarray, y, seed: int = 42) -> HistGradientBoostingClassifier:
    """
    P7-08 : gradient boosting (HistGradientBoostingClassifier).
    class_weight="balanced" compense le déséquilibre entre fraudes et autres transactions.
    """
    model = HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.1, max_leaf_nodes=31, class_weight="balanced",
        categorical_features=[SUPERVISED_FEATURES.index(c) for c in CATEGORICAL_FEATURES],
        early_stopping=False, random_state=seed,
    )
    return model.fit(x, np.asarray(y))


def precision_recall_at_shares(y_true, score, shares=SHARES) -> pd.DataFrame:
    """
    Précision et rappel quand on signale la part `share` des transactions
    les plus risquées selon `score`.
    - précision : part de vraies fraudes parmi les transactions signalées ;
    - rappel : part des fraudes qui sont signalées.
    """
    y_true = np.asarray(y_true)
    score = np.asarray(score)
    order = np.argsort(-score, kind="stable")
    positives = y_true.sum()
    rows = []
    for share in shares:
        k = int(np.ceil(share * len(score)))
        top = y_true[order[:k]]
        rows.append({"seuil": f"{100 * share:g} %", "signalées": k, "fraudes signalées": int(top.sum()),
                     "précision_%": round(100 * top.mean(), 2),
                     "rappel_%": round(100 * top.sum() / positives, 2)})
    return pd.DataFrame(rows).set_index("seuil")


def precision_recall_fixed_threshold(y_true, flagged) -> dict:
    """P7-11 : précision et rappel d'un signalement déjà décidé (seuil fixé sur toutes les transactions)."""
    y_true = np.asarray(y_true)
    flagged = np.asarray(flagged).astype(bool)
    tp = int((y_true[flagged] == 1).sum())
    return {"signalées (étiquetées)": int(flagged.sum()), "fraudes signalées": tp,
            "précision_%": round(100 * tp / max(flagged.sum(), 1), 2),
            "rappel_%": round(100 * tp / max(y_true.sum(), 1), 2)}


def average_precision(y_true, score) -> float:
    """Aire sous la courbe précision-rappel (1 = parfait ; le hasard vaut le taux de fraude)."""
    return float(average_precision_score(np.asarray(y_true), np.asarray(score)))
