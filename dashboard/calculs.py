"""
Calculs du tableau de bord (phase 8).

Fonctions sans Streamlit : elles filtrent les tables de data/dashboard/ et
calculent les chiffres affichés. Le notebook 08 les réutilise pour vérifier
chaque chiffre (P8-08).
"""

from pathlib import Path

import pandas as pd

DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "data" / "dashboard"
TABLES = ["jours", "mois", "familles", "etats", "pays", "profils_annees", "clients_annees", "profils", "signalees",
          "evaluation"]

# Seuil de signalement : colonne des tables résumées et colonne de la table des signalées
SEUILS = {"0,5 %": "signalees_0_5", "1 %": "signalees_1", "2 %": "signalees_2"}
SEUILS_LISTE = {"0,5 %": "flag_0_5", "1 %": "flag_1", "2 %": None}
CANAUX = ["Bande magnétique", "Puce", "En ligne"]
LIEUX = ["Sur place aux États-Unis", "En ligne", "À l'étranger"]


def charger(folder: Path = DASHBOARD_DIR) -> dict:
    """Lit toutes les tables du tableau de bord."""
    return {name: pd.read_parquet(folder / f"{name}.parquet") for name in TABLES}


def filtrer(table: pd.DataFrame, annees, canaux=None, lieux=None) -> pd.DataFrame:
    """Garde les années de la période (début, fin) et, si la table les a, les canaux et lieux choisis."""
    masque = table["year"].between(annees[0], annees[1])
    if canaux is not None and "canal" in table.columns:
        masque &= table["canal"].isin(canaux)
    if lieux is not None and "lieu" in table.columns:
        masque &= table["lieu"].isin(lieux)
    return table[masque]


def indicateurs(tables: dict, annees, canaux, seuil: str) -> dict:
    """
    P8-04 : chiffres clés de la période. Les clients actifs ne dépendent pas
    du canal choisi : un client utilise souvent plusieurs canaux.
    """
    mois = filtrer(tables["mois"], annees, canaux)
    col = SEUILS[seuil]
    transactions = int(mois["transactions"].sum())
    clients = filtrer(tables["clients_annees"], annees)
    clients_signales = clients.groupby("client_id", observed=True)[col].sum()
    return {
        "transactions": transactions,
        "achats": float(mois["achats"].sum()),
        "achat_moyen": float(mois["achats"].sum() / max(mois["nb_achats"].sum(), 1)),
        "signalees": int(mois[col].sum()),
        "taux_signalement": 100 * mois[col].sum() / max(transactions, 1),
        "part_en_ligne": 100 * mois["en_ligne"].sum() / max(transactions, 1),
        "taux_erreur": 100 * mois["erreurs"].sum() / max(transactions, 1),
        "clients_actifs": int(clients["client_id"].nunique()),
        "clients_signales": int((clients_signales > 0).sum()),
    }


def tendance_mensuelle(tables: dict, annees, canaux, seuil: str) -> pd.DataFrame:
    """P8-04 : transactions, achats et signalements par mois."""
    mois = filtrer(tables["mois"], annees, canaux)
    col = SEUILS[seuil]
    t = mois.groupby(["year", "month"], observed=True).agg(
        transactions=("transactions", "sum"), achats=("achats", "sum"), signalees=(col, "sum")
    ).reset_index()
    t["mois"] = pd.to_datetime(dict(year=t["year"], month=t["month"], day=1))
    return t[["mois", "transactions", "achats", "signalees"]]


def parts_canaux(tables: dict, annees) -> pd.DataFrame:
    """P8-04 : part de chaque canal dans les transactions de chaque année (%)."""
    mois = filtrer(tables["mois"], annees)
    t = mois.groupby(["year", "canal"], observed=True)["transactions"].sum().reset_index()
    t["part"] = 100 * t["transactions"] / t.groupby("year", observed=True)["transactions"].transform("sum")
    return t


def resume_profils(tables: dict, annees, seuil: str) -> pd.DataFrame:
    """P8-05 : transactions, part en ligne et taux de signalement par profil sur la période."""
    t = filtrer(tables["profils_annees"], annees)
    col = SEUILS[seuil]
    r = t.groupby("profil_nom", observed=True).agg(
        transactions=("transactions", "sum"), achats=("achats", "sum"), nb_achats=("nb_achats", "sum"),
        en_ligne=("en_ligne", "sum"), etranger=("etranger", "sum"), signalees=(col, "sum"),
    )
    r["achat_moyen"] = r["achats"] / r["nb_achats"]
    r["part_en_ligne"] = 100 * r["en_ligne"] / r["transactions"]
    r["part_etranger"] = 100 * r["etranger"] / r["transactions"]
    r["taux_signalement"] = 100 * r["signalees"] / r["transactions"]
    return r.reset_index()


def resume_lieux(tables: dict, annees, canaux, seuil: str) -> pd.DataFrame:
    """P8-06 : transactions, achats et taux de signalement par type de lieu."""
    mois = filtrer(tables["mois"], annees, canaux)
    col = SEUILS[seuil]
    r = mois.groupby("lieu", observed=True).agg(
        transactions=("transactions", "sum"), achats=("achats", "sum"), signalees=(col, "sum")
    )
    r["part_transactions"] = 100 * r["transactions"] / r["transactions"].sum()
    r["taux_signalement"] = 100 * r["signalees"] / r["transactions"]
    return r.reset_index()


def classement(tables: dict, nom: str, cle: str, annees, seuil: str, n: int = 15) -> pd.DataFrame:
    """P8-06 : États (nom = "etats") ou pays étrangers (nom = "pays") les plus fréquents."""
    t = filtrer(tables[nom], annees)
    col = SEUILS[seuil]
    r = t.groupby(cle, observed=True).agg(
        transactions=("transactions", "sum"), achats=("achats", "sum"), signalees=(col, "sum")
    )
    r["taux_signalement"] = 100 * r["signalees"] / r["transactions"]
    return r.sort_values("transactions", ascending=False).head(n).reset_index()


def resume_familles(tables: dict, annees, lieux, seuil: str) -> pd.DataFrame:
    """P8-06 : transactions, montant et taux de signalement par famille de commerçants."""
    t = filtrer(tables["familles"], annees, lieux=lieux)
    col = SEUILS[seuil]
    r = t.groupby("mcc_family", observed=True).agg(
        transactions=("transactions", "sum"), achats=("achats", "sum"), signalees=(col, "sum")
    )
    r["part_transactions"] = 100 * r["transactions"] / r["transactions"].sum()
    r["part_achats"] = 100 * r["achats"] / r["achats"].sum()
    r["taux_signalement"] = 100 * r["signalees"] / r["transactions"]
    return r.sort_values("transactions", ascending=False).reset_index()


def liste_signalee(tables: dict, annees, seuil: str, client=None, familles=None, canaux=None, raisons=None,
                   score_min=None) -> pd.DataFrame:
    """P8-07 : transactions signalées au seuil choisi, triées par score, avec les filtres demandés."""
    t = tables["signalees"]
    t = t[t["year"].between(annees[0], annees[1])]
    col = SEUILS_LISTE[seuil]
    if col is not None:
        t = t[t[col] == 1]
    if client:
        t = t[t["client_id"] == int(client)]
    if familles:
        t = t[t["famille"].isin(familles)]
    if canaux:
        t = t[t["canal"].isin(canaux)]
    if raisons:
        t = t[t["raison_principale"].isin(raisons)]
    if score_min is not None:
        t = t[t["score"] >= score_min]
    return t.sort_values("score", ascending=False)


def fr(x, decimales: int = 0) -> str:
    """Nombre au format français : espace pour les milliers, virgule pour les décimales."""
    texte = f"{x:,.{decimales}f}"
    return texte.replace(",", " ").replace(".", ",")
