"""
Préparation des données du tableau de bord (P8-03).

Le tableau de bord ne lit pas la table d'analyse de 13 millions de lignes :
il lit de petites tables résumées, enregistrées dans data/dashboard/.
"""

from pathlib import Path

import numpy as np
import pandas as pd

DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "data" / "dashboard"

CHANNELS = {"Swipe Transaction": "Bande magnétique", "Chip Transaction": "Puce", "Online Transaction": "En ligne"}
FLAGS = ["flag_0_5", "flag_1", "flag_2"]

DASHBOARD_INPUT_COLUMNS = [
    "id", "date", "year", "month", "client_id", "card_id", "amount", "use_chip", "is_online", "is_foreign",
    "merchant_city", "merchant_state_clean", "merchant_country", "mcc_family", "has_error", "is_night",
]


def prepare_base(df: pd.DataFrame, scores: pd.DataFrame, profiles: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute à la table d'analyse les colonnes utiles au tableau de bord :
    canal en français, lieu (en ligne, sur place aux États-Unis, à l'étranger),
    montant d'achat, signalements aux trois seuils, raison principale et profil.
    Les scores sont dans le même ordre que la table d'analyse (P7-07) ; on le vérifie.
    La table reçue est complétée sur place (pas de copie de 13 millions de lignes).
    """
    if not np.array_equal(df["id"].to_numpy(), scores["id"].to_numpy()):
        raise ValueError("Les scores ne sont pas dans le même ordre que la table d'analyse")
    base = df
    base["canal"] = base["use_chip"].map(CHANNELS).astype("category")
    codes = np.where(base["is_online"] == 1, 0, np.where(base["is_foreign"] == 1, 1, 2)).astype("int8")
    base["lieu"] = pd.Categorical.from_codes(codes, ["En ligne", "À l'étranger", "Sur place aux États-Unis"])
    base["achat"] = base["amount"].where(base["amount"] > 0, 0.0)
    base["est_achat"] = (base["amount"] > 0).astype("int8")
    for col in FLAGS + ["risk_score", "main_reason", "anomaly_pct"]:
        base[col] = scores[col].to_numpy()
    base["profil_nom"] = base["client_id"].map(profiles.set_index("client_id")["profil_nom"]).astype("category")
    return base


def _summary(base: pd.DataFrame, by: list) -> pd.DataFrame:
    """Transactions, achats, erreurs et signalements aux trois seuils, par groupe."""
    table = base.groupby(by, observed=True).agg(
        transactions=("id", "size"),
        achats=("achat", "sum"),
        nb_achats=("est_achat", "sum"),
        erreurs=("has_error", "sum"),
        en_ligne=("is_online", "sum"),
        etranger=("is_foreign", "sum"),
        signalees_0_5=("flag_0_5", "sum"),
        signalees_1=("flag_1", "sum"),
        signalees_2=("flag_2", "sum"),
    )
    return table.reset_index()


def build_dashboard_tables(base: pd.DataFrame, profiles: pd.DataFrame, fiches: pd.DataFrame) -> dict:
    """
    P8-03 : tables résumées par jour, mois, catégorie et État, plus la table
    des transactions signalées (seuil 2 %, avec les colonnes des seuils 0,5 % et 1 %).
    """
    tables = {}
    jour = base.assign(jour=base["date"].dt.normalize())
    tables["jours"] = _summary(jour, ["jour"])
    tables["mois"] = _summary(base, ["year", "month", "canal", "lieu"])
    tables["familles"] = _summary(base, ["year", "mcc_family", "lieu"])
    sur_place = base[base["lieu"] == "Sur place aux États-Unis"]
    tables["etats"] = _summary(sur_place, ["year", "merchant_state_clean"])
    tables["etats"] = tables["etats"][tables["etats"]["transactions"] > 0]
    etranger = base[base["lieu"] == "À l'étranger"]
    tables["pays"] = _summary(etranger, ["year", "merchant_country"])
    tables["pays"] = tables["pays"][tables["pays"]["transactions"] > 0]
    tables["profils_annees"] = _summary(base, ["year", "profil_nom"])

    # Présence des clients par année, pour compter les clients actifs sur une période
    tables["clients_annees"] = base.groupby(["client_id", "year"], observed=True).agg(
        transactions=("id", "size"),
        signalees_0_5=("flag_0_5", "sum"),
        signalees_1=("flag_1", "sum"),
        signalees_2=("flag_2", "sum"),
    ).reset_index()

    # Fiches des profils (phase 5) et comportements par profil (P6-07)
    tables["profils"] = fiches

    signalees = base[base["flag_2"] == 1].sort_values("risk_score", ascending=False)
    lieu_detail = np.where(signalees["lieu"] == "En ligne", "En ligne",
                           np.where(signalees["lieu"] == "À l'étranger", signalees["merchant_country"].astype(str),
                                    signalees["merchant_state_clean"].astype(str)))
    tables["signalees"] = pd.DataFrame({
        "rang": np.arange(1, len(signalees) + 1),
        "id": signalees["id"].to_numpy(),
        "date": signalees["date"].to_numpy(),
        "year": signalees["year"].to_numpy(),
        "client_id": signalees["client_id"].to_numpy(),
        "card_id": signalees["card_id"].to_numpy(),
        "montant": signalees["amount"].to_numpy(),
        "canal": signalees["canal"].astype(str).to_numpy(),
        "famille": signalees["mcc_family"].astype(str).to_numpy(),
        "ville": signalees["merchant_city"].astype(str).to_numpy(),
        "lieu": lieu_detail,
        "profil": signalees["profil_nom"].astype(str).to_numpy(),
        "score": signalees["risk_score"].round(2).to_numpy(),
        "raison_principale": signalees["main_reason"].astype(str).to_numpy(),
        "flag_0_5": signalees["flag_0_5"].to_numpy(),
        "flag_1": signalees["flag_1"].to_numpy(),
    })
    for name in ["mois", "familles", "profils_annees", "signalees"]:
        for col in ["canal", "lieu", "mcc_family", "profil_nom", "famille", "raison_principale", "profil"]:
            if col in tables[name].columns:
                tables[name][col] = tables[name][col].astype(str)
    return tables


def save_dashboard_tables(tables: dict, folder: Path = DASHBOARD_DIR) -> pd.DataFrame:
    """P8-03 : enregistre chaque table en Parquet et retourne lignes et taille des fichiers."""
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, table in tables.items():
        path = folder / f"{name}.parquet"
        table.to_parquet(path, index=False)
        rows.append({"table": name, "lignes": len(table), "colonnes": table.shape[1],
                     "taille (Mo)": round(path.stat().st_size / 1e6, 2)})
    return pd.DataFrame(rows).set_index("table")
