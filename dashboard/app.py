"""
Tableau de bord : détection de fraude bancaire (phase 8).

Lancer depuis la racine du dépôt :
    streamlit run dashboard/app.py

Les tables lues sont créées par notebooks/08_tableau_de_bord.ipynb (P8-03).
"""

import sys
from pathlib import Path

import streamlit as st

RACINE = Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from dashboard import pages  # noqa: E402
from dashboard.calculs import CANAUX, DASHBOARD_DIR, SEUILS, charger  # noqa: E402

st.set_page_config(page_title="Détection de fraude bancaire", layout="wide")


@st.cache_data(show_spinner="Chargement des données...")
def tables():
    return charger()


if not (DASHBOARD_DIR / "mois.parquet").exists():
    st.error("Les tables du tableau de bord sont absentes. Exécuter d'abord notebooks/08_tableau_de_bord.ipynb.")
    st.stop()

t = tables()
annee_min, annee_max = int(t["mois"]["year"].min()), int(t["mois"]["year"].max())

st.sidebar.header("Filtres")
annees = st.sidebar.slider("Années", annee_min, annee_max, (annee_min, annee_max), key="annees")
seuil = st.sidebar.radio(
    "Seuil de signalement", list(SEUILS), index=1, key="seuil",
    help="Part des transactions les plus risquées qui sont signalées (score de risque, phase 7).",
)
canaux = st.sidebar.multiselect("Canaux de paiement", CANAUX, default=CANAUX, key="canaux", placeholder="Tous") or CANAUX
st.sidebar.caption("Projet 5 : détection de fraude bancaire. Données de janvier 2010 à octobre 2019.")
filtres = {"annees": annees, "seuil": seuil, "canaux": canaux}


def vue_ensemble():
    pages.vue_ensemble(t, filtres)


def profils():
    pages.profils(t, filtres)


def lieux_categories():
    pages.lieux_categories(t, filtres)


def transactions_signalees():
    pages.transactions_signalees(t, filtres)


navigation = st.navigation([
    st.Page(vue_ensemble, title="Vue d'ensemble", url_path="vue-ensemble", default=True),
    st.Page(profils, title="Profils de clients", url_path="profils"),
    st.Page(lieux_categories, title="Lieux et catégories", url_path="lieux-categories"),
    st.Page(transactions_signalees, title="Transactions signalées", url_path="transactions-signalees"),
])
navigation.run()
