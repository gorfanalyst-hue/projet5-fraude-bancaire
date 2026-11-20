"""
Profils de clients (phase 5).

Chaque section correspond à un ticket Jira. Les profils décrivent les clients
actifs (au moins une transaction) ; les clients sans transaction servent
seulement à décrire la population (P5-01, règle de P2-04).
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

# =============================================================================
# P5-01 : Décrire la population des clients
# =============================================================================


def describe_population(df_users: pd.DataFrame, active_ids) -> pd.DataFrame:
    """
    P5-01 : compare les clients actifs et les clients sans transaction.
    L'âge est celui de février 2020 (current_age, voir P2-12).
    """
    users = df_users.assign(
        statut=np.where(df_users["id"].isin(active_ids), "actifs", "sans transaction"),
        femme=(df_users["gender"] == "Female").astype(int),
    )
    resume = users.groupby("statut").agg(
        clients=("id", "size"),
        age_median=("current_age", "median"),
        part_femmes=("femme", "mean"),
        revenu_median=("yearly_income", "median"),
        dette_mediane=("total_debt", "median"),
        score_credit_median=("credit_score", "median"),
        cartes_credit_median=("num_credit_cards", "median"),
        revenus_suspects=("suspicious_income", "sum"),
    )
    resume["part_femmes"] = (100 * resume["part_femmes"]).round(1)
    resume = resume.rename(
        columns={
            "age_median": "âge médian (février 2020)",
            "part_femmes": "part de femmes (%)",
            "revenu_median": "revenu annuel médian ($)",
            "dette_mediane": "dette médiane ($)",
            "score_credit_median": "score de crédit médian",
            "cartes_credit_median": "cartes de crédit (médiane)",
            "revenus_suspects": "revenus suspects (P3-08)",
        }
    )
    return resume.T


# =============================================================================
# P5-02 : Construire les variables de profil
# =============================================================================

PROFILE_INPUT_COLUMNS = [
    "client_id", "card_id", "merchant_id", "amount", "year", "month",
    "is_online", "is_foreign", "is_night", "has_error",
]


def build_profile_table(df: pd.DataFrame, df_users: pd.DataFrame) -> pd.DataFrame:
    """
    P5-02 : une ligne par client actif.
    - Dépenses : nombre de transactions, transactions par mois d'activité,
      montant moyen et médian des achats, dépenses par mois, parts en ligne,
      à l'étranger et de nuit, part de remboursements, taux d'erreur,
      nombre de cartes et de commerçants.
    - Finances : revenu annuel, dette, score de crédit, dette / revenu.
    - Description : genre et âge au 31 octobre 2019 (dernière transaction).
    Les achats sont les montants positifs ; les remboursements, les montants négatifs.
    """
    tmp = pd.DataFrame(
        {
            "client_id": df["client_id"],
            "card_id": df["card_id"],
            "merchant_id": df["merchant_id"],
            "achat": df["amount"].where(df["amount"] > 0),
            "remboursement": (df["amount"] < 0).astype("int8"),
            "mois": df["year"].astype("int32") * 12 + df["month"].astype("int32"),
            "is_online": df["is_online"],
            "is_foreign": df["is_foreign"],
            "is_night": df["is_night"],
            "has_error": df["has_error"],
        }
    )
    agg = tmp.groupby("client_id").agg(
        n_transactions=("client_id", "size"),
        premier_mois=("mois", "min"),
        dernier_mois=("mois", "max"),
        mean_purchase=("achat", "mean"),
        median_purchase=("achat", "median"),
        total_purchases=("achat", "sum"),
        share_online=("is_online", "mean"),
        share_foreign=("is_foreign", "mean"),
        share_night=("is_night", "mean"),
        share_refund=("remboursement", "mean"),
        error_rate=("has_error", "mean"),
        n_cards=("card_id", "nunique"),
        n_merchants=("merchant_id", "nunique"),
    )
    agg["months_active"] = agg["dernier_mois"] - agg["premier_mois"] + 1
    agg["tx_per_month"] = agg["n_transactions"] / agg["months_active"]
    agg["spend_per_month"] = agg["total_purchases"] / agg["months_active"]
    agg = agg.drop(columns=["premier_mois", "dernier_mois", "total_purchases"])

    users = df_users.set_index("id")
    profiles = agg.join(
        users[["gender", "birth_year", "birth_month", "yearly_income", "total_debt",
               "credit_score", "num_credit_cards", "suspicious_income"]]
    )
    profiles["age_2019"] = (
        2019 - profiles["birth_year"].astype(int) - (10 < profiles["birth_month"]).astype(int)
    )
    profiles["debt_to_income"] = profiles["total_debt"] / profiles["yearly_income"]
    return profiles.drop(columns=["birth_year", "birth_month"])


# =============================================================================
# P5-03 : Préparer la segmentation
# =============================================================================

# Variables retenues pour K-means : trois financières et quatre de dépense.
# Le genre et l'âge n'entrent pas dans la segmentation : ils servent à décrire les profils.
CLUSTER_VARIABLES = [
    "yearly_income",
    "total_debt",
    "credit_score",
    "mean_purchase",
    "tx_per_month",
    "share_online",
    "share_foreign",
]
# Variables très asymétriques : log(1 + x) avant la mise à l'échelle
LOG_VARIABLES = ["yearly_income", "total_debt", "mean_purchase", "tx_per_month", "share_foreign"]


def prepare_features(profiles: pd.DataFrame, variables=CLUSTER_VARIABLES, log_variables=LOG_VARIABLES) -> pd.DataFrame:
    """
    P5-03 : transformation log(1 + x) des variables asymétriques,
    puis mise à la même échelle (moyenne 0, écart-type 1).
    """
    x = profiles[variables].astype(float).copy()
    for col in log_variables:
        x[col] = np.log1p(x[col])
    scaled = StandardScaler().fit_transform(x)
    return pd.DataFrame(scaled, index=profiles.index, columns=variables)


# =============================================================================
# P5-04 : Segmenter les clients avec K-means
# =============================================================================


def scan_kmeans(x: pd.DataFrame, k_values=range(2, 11), seed: int = 42) -> pd.DataFrame:
    """P5-04 : inertie (méthode du coude) et score de silhouette de 2 à 10 groupes."""
    rows = []
    for k in k_values:
        model = KMeans(n_clusters=k, n_init=20, random_state=seed).fit(x)
        rows.append({"k": k, "inertie": model.inertia_, "silhouette": silhouette_score(x, model.labels_)})
    return pd.DataFrame(rows).set_index("k")


def fit_profiles(x: pd.DataFrame, k: int, seed: int = 42) -> np.ndarray:
    """
    P5-04 : K-means avec k groupes. Les groupes sont renumérotés du plus grand
    au plus petit (1 = le plus grand), pour garder les mêmes numéros d'un essai à l'autre.
    """
    labels = KMeans(n_clusters=k, n_init=20, random_state=seed).fit_predict(x)
    return _renumber_by_size(labels)


def _renumber_by_size(labels: np.ndarray) -> np.ndarray:
    sizes = pd.Series(labels).value_counts()
    mapping = {old: new for new, old in enumerate(sizes.index, start=1)}
    return pd.Series(labels).map(mapping).to_numpy()


# =============================================================================
# P5-05 : Décrire et nommer chaque profil
# =============================================================================


def profile_medians(profiles: pd.DataFrame, labels, variables) -> pd.DataFrame:
    """P5-05 : taille et médiane de chaque variable, par profil."""
    df = profiles.assign(profil=labels)
    med = df.groupby("profil")[variables].median()
    med.insert(0, "clients", df["profil"].value_counts().sort_index())
    return med


def profile_zscores(x: pd.DataFrame, labels) -> pd.DataFrame:
    """
    P5-05 : moyenne de chaque variable mise à l'échelle, par profil.
    +1 veut dire un écart-type au-dessus de la moyenne de tous les clients.
    """
    return x.assign(profil=labels).groupby("profil").mean()


def distinctive_traits(zscores: pd.DataFrame, labels_fr: dict, threshold: float = 0.5) -> pd.Series:
    """
    P5-05 : pour chaque profil, les variables à plus de threshold écart-type de la moyenne.
    labels_fr donne, pour chaque variable, son nom en français et s'il est féminin :
    {"share_online": ("part en ligne", True), ...}.
    """
    traits = {}
    for profil, row in zscores.iterrows():
        forts = row[row.abs() >= threshold].sort_values(key=abs, ascending=False)
        morceaux = []
        for v, z in forts.items():
            nom, feminin = labels_fr.get(v, (v, False))
            sens = ("élevée" if feminin else "élevé") if z > 0 else "faible"
            morceaux.append(f"{nom} {sens} ({z:+.1f})".replace(".", ","))
        traits[profil] = " ; ".join(morceaux) or "proche de la moyenne"
    return pd.Series(traits, name="traits distinctifs")


# =============================================================================
# P5-06 : Vérifier la stabilité des profils
# =============================================================================


def check_stability(x: pd.DataFrame, k: int, reference, seeds=(1, 2, 3, 4, 5), n_samples: int = 5,
                    sample_frac: float = 0.8) -> pd.DataFrame:
    """
    P5-06 : relance K-means avec d'autres graines, puis sur des échantillons de
    80 % des clients. L'indice de Rand ajusté (ARI) compare chaque essai aux
    profils de référence : 1 = groupes identiques, 0 = groupes au hasard.
    """
    reference = np.asarray(reference)
    rows = []
    for seed in seeds:
        labels = KMeans(n_clusters=k, n_init=20, random_state=seed).fit_predict(x)
        rows.append({"essai": f"graine {seed}", "clients": len(x), "ARI": adjusted_rand_score(reference, labels)})
    rng = np.random.default_rng(0)
    for i in range(n_samples):
        idx = np.sort(rng.choice(len(x), int(sample_frac * len(x)), replace=False))
        labels = KMeans(n_clusters=k, n_init=20, random_state=42).fit_predict(x.iloc[idx])
        rows.append({"essai": f"échantillon {i + 1} (80 %)", "clients": len(idx),
                     "ARI": adjusted_rand_score(reference[idx], labels)})
    result = pd.DataFrame(rows)
    result["ARI"] = result["ARI"].round(3)
    return result
