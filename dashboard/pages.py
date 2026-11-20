"""
Les quatre pages du tableau de bord (P8-04 à P8-07).
Les chiffres viennent des fonctions de dashboard/calculs.py.
"""

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from dashboard.calculs import (
    CANAUX, LIEUX, SEUILS, classement, fr, indicateurs, liste_signalee, parts_canaux, resume_familles,
    resume_lieux, resume_profils, tendance_mensuelle,
)
from src.charte import CATEGORIES, TEXT_SECONDARY
from src.detection import SHORT_LABELS

BLEU, ORANGE = CATEGORIES[0], CATEGORIES[1]
COULEURS_CANAUX = alt.Scale(domain=CANAUX, range=CATEGORIES[:3])
FIGURE_PROFILS = Path(__file__).resolve().parent.parent / "docs" / "figures" / "P5-07_profils_clients.png"


# Format français des nombres et des dates dans les graphiques (Vega-Lite)
LOCALE_FR = {
    "number": {"decimal": ",", "thousands": "\u202f", "grouping": [3], "currency": ["", " $"]},
    "time": {
        "dateTime": "%A %e %B %Y à %X", "date": "%d/%m/%Y", "time": "%H:%M:%S", "periods": ["AM", "PM"],
        "days": ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
        "shortDays": ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."],
        "months": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
                   "octobre", "novembre", "décembre"],
        "shortMonths": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.",
                        "nov.", "déc."],
    },
}


def _afficher(fonction, *args, **kwargs):
    """
    Affiche un élément sur toute la largeur. Les versions récentes de Streamlit
    utilisent width="stretch", les plus anciennes use_container_width=True.
    """
    if fonction is st.altair_chart:
        args = (args[0].configure(locale=LOCALE_FR),) + args[1:]
    try:
        return fonction(*args, width="stretch", **kwargs)
    except TypeError:
        return fonction(*args, use_container_width=True, **kwargs)


def _periode(f) -> str:
    debut, fin = f["annees"]
    periode = f"{debut}" if debut == fin else f"{debut} à {fin}"
    return f"Période : {periode}. Seuil de signalement : {f['seuil']} des transactions les plus risquées."


def _barres(data, categorie, valeur, titre_valeur, couleur=BLEU, format_valeur=",.0f", tri="-x", hauteur=None):
    """Barres horizontales avec info-bulle."""
    graphique = alt.Chart(data).mark_bar(color=couleur, cornerRadiusEnd=3).encode(
        x=alt.X(f"{valeur}:Q", title=titre_valeur),
        y=alt.Y(f"{categorie}:N", sort=tri, title=None, axis=alt.Axis(labelLimit=320)),
        tooltip=[alt.Tooltip(f"{categorie}:N", title="valeur"), alt.Tooltip(f"{valeur}:Q", title=titre_valeur,
                                                                            format=format_valeur)],
    )
    return graphique.properties(height=hauteur or max(160, 36 * len(data)))


# =============================================================================
# P8-04 : Vue d'ensemble
# =============================================================================


def vue_ensemble(t: dict, f: dict):
    st.title("Vue d'ensemble")
    st.caption(_periode(f))
    k = indicateurs(t, f["annees"], f["canaux"], f["seuil"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Transactions", fr(k["transactions"]))
    c2.metric("Montant des achats", f"{fr(k['achats'] / 1e6, 1)} M$")
    c3.metric("Achat moyen", f"{fr(k['achat_moyen'], 2)} $")
    c4.metric("Clients actifs", fr(k["clients_actifs"]), help="Tous canaux confondus")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Transactions signalées", fr(k["signalees"]), help=f"Taux : {fr(k['taux_signalement'], 2)} %")
    c2.metric("Taux de signalement", f"{fr(k['taux_signalement'], 2)} %")
    c3.metric("Part des achats en ligne", f"{fr(k['part_en_ligne'], 1)} %")
    c4.metric("Clients signalés", fr(k["clients_signales"]),
              help="Clients avec au moins une transaction signalée, tous canaux confondus")

    st.subheader("Évolution mensuelle")
    mesure = st.radio("Mesure", ["transactions", "achats", "signalees"], horizontal=True,
                      format_func={"transactions": "Transactions", "achats": "Montant des achats ($)",
                                   "signalees": "Transactions signalées"}.get)
    tendance = tendance_mensuelle(t, f["annees"], f["canaux"], f["seuil"])
    titres = {"transactions": "transactions", "achats": "achats ($)", "signalees": "transactions signalées"}
    ligne = alt.Chart(tendance).mark_line(color=BLEU, strokeWidth=2).encode(
        x=alt.X("mois:T", title=None, axis=alt.Axis(format="%Y", tickCount="year")),
        y=alt.Y(f"{mesure}:Q", title=titres[mesure]),
        tooltip=[alt.Tooltip("mois:T", title="mois", format="%Y-%m"),
                 alt.Tooltip(f"{mesure}:Q", title=titres[mesure], format=",.0f")],
    )
    points = ligne.mark_point(size=40, opacity=0).encode()
    _afficher(st.altair_chart, (ligne + points).properties(height=280))

    st.subheader("Canaux de paiement par année")
    canaux = parts_canaux(t, f["annees"])
    graphique = alt.Chart(canaux).mark_line(point=alt.OverlayMarkDef(size=50), strokeWidth=2).encode(
        x=alt.X("year:O", title=None),
        y=alt.Y("part:Q", title="part des transactions (%)", scale=alt.Scale(domain=[0, 100])),
        color=alt.Color("canal:N", scale=COULEURS_CANAUX, legend=alt.Legend(title="Canal", orient="top")),
        tooltip=[alt.Tooltip("year:O", title="année"), alt.Tooltip("canal:N"),
                 alt.Tooltip("part:Q", title="part (%)", format=".1f"),
                 alt.Tooltip("transactions:Q", format=",.0f")],
    )
    _afficher(st.altair_chart, graphique.properties(height=280))


# =============================================================================
# P8-05 : Profils de clients
# =============================================================================


def profils(t: dict, f: dict):
    st.title("Profils de clients")
    st.caption(_periode(f) + " Profils calculés sur toute la période (phase 5).")
    fiches = t["profils"]

    if FIGURE_PROFILS.exists():
        _afficher(st.image, str(FIGURE_PROFILS))

    choix = st.selectbox("Fiche d'un profil", fiches["profil_nom"].tolist())
    fiche = fiches.set_index("profil_nom").loc[choix]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clients", fr(fiche["clients"]))
    c2.metric("Revenu annuel médian", f"{fr(fiche['revenu_median'])} $")
    c3.metric("Transactions par mois (médiane)", fr(fiche["transactions_par_mois"], 1))
    c4.metric("Achat moyen (médiane)", f"{fr(fiche['achat_moyen'], 2)} $")
    st.markdown(f"**Traits distinctifs :** {fiche['traits']}")

    st.subheader("Comportements et signalements par profil")
    r = resume_profils(t, f["annees"], f["seuil"])
    r = r[r["profil_nom"].isin(fiches["profil_nom"])]
    taux_global = 100 * r["signalees"].sum() / r["transactions"].sum()
    barres = _barres(r, "profil_nom", "taux_signalement", "transactions signalées (%)", format_valeur=".2f")
    regle = alt.Chart(pd.DataFrame({"x": [taux_global]})).mark_rule(color=TEXT_SECONDARY, strokeDash=[4, 3]).encode(x="x:Q")
    _afficher(st.altair_chart, barres + regle)
    st.caption(f"Ligne pointillée : taux de tous les profils ({fr(taux_global, 2)} %).")
    tableau = r[["profil_nom", "transactions", "achat_moyen", "part_en_ligne", "part_etranger", "taux_signalement"]]
    tableau = tableau.rename(columns={"profil_nom": "profil", "achat_moyen": "achat moyen ($)",
                                      "part_en_ligne": "en ligne (%)", "part_etranger": "à l'étranger (%)",
                                      "taux_signalement": "signalées (%)"})
    _afficher(
        st.dataframe,
        tableau,
        hide_index=True,
        column_config={
            "transactions": st.column_config.NumberColumn(format="%d"),
            "achat moyen ($)": st.column_config.NumberColumn(format="%.2f"),
            "en ligne (%)": st.column_config.NumberColumn(format="%.2f"),
            "à l'étranger (%)": st.column_config.NumberColumn(format="%.2f"),
            "signalées (%)": st.column_config.NumberColumn(format="%.2f"),
        },
    )


# =============================================================================
# P8-06 : Lieux et catégories
# =============================================================================


def lieux_categories(t: dict, f: dict):
    st.title("Lieux et catégories")
    st.caption(_periode(f))

    lieux = resume_lieux(t, f["annees"], f["canaux"], f["seuil"]).set_index("lieu")
    colonnes = st.columns(3)
    for colonne, lieu in zip(colonnes, LIEUX):
        if lieu in lieux.index:
            ligne = lieux.loc[lieu]
            colonne.metric(lieu, f"{fr(ligne['part_transactions'], 1)} %",
                           help=f"{fr(ligne['transactions'])} transactions")
            colonne.caption(f"des transactions ; signalées : {fr(ligne['taux_signalement'], 2)} %")

    st.subheader("États (achats sur place aux États-Unis)")
    mesure = st.radio("Classer par", ["transactions", "taux_signalement"], horizontal=True,
                      format_func={"transactions": "Transactions", "taux_signalement": "Taux de signalement"}.get)
    etats = classement(t, "etats", "merchant_state_clean", f["annees"], f["seuil"], n=15)
    titre = "transactions" if mesure == "transactions" else "transactions signalées (%)"
    format_valeur = ",.0f" if mesure == "transactions" else ".2f"
    _afficher(st.altair_chart, _barres(etats, "merchant_state_clean", mesure, titre, format_valeur=format_valeur))

    st.subheader("Pays étrangers les plus fréquents")
    pays = classement(t, "pays", "merchant_country", f["annees"], f["seuil"], n=10)
    pays = pays.rename(columns={"merchant_country": "pays", "achats": "achats ($)", "signalees": "signalées",
                                "taux_signalement": "signalées (%)"})
    _afficher(
        st.dataframe,
        pays,
        hide_index=True,
        column_config={
            "achats ($)": st.column_config.NumberColumn(format="%.0f"),
            "signalées (%)": st.column_config.NumberColumn(format="%.2f"),
        },
    )

    st.subheader("Familles de commerçants")
    choix_lieux = st.multiselect("Lieux", LIEUX, default=LIEUX, placeholder="Tous") or LIEUX
    familles = resume_familles(t, f["annees"], choix_lieux, f["seuil"])
    longues = familles.melt(id_vars="mcc_family", value_vars=["part_transactions", "part_achats"],
                            var_name="mesure", value_name="part")
    longues["mesure"] = longues["mesure"].map({"part_transactions": "part des transactions",
                                               "part_achats": "part du montant des achats"})
    graphique = alt.Chart(longues).mark_bar(cornerRadiusEnd=3).encode(
        x=alt.X("part:Q", title="%"),
        y=alt.Y("mcc_family:N", sort=familles["mcc_family"].tolist(), title=None, axis=alt.Axis(labelLimit=320)),
        yOffset="mesure:N",
        color=alt.Color("mesure:N", scale=alt.Scale(range=[BLEU, ORANGE]), legend=alt.Legend(title=None, orient="top")),
        tooltip=[alt.Tooltip("mcc_family:N", title="famille"), "mesure:N", alt.Tooltip("part:Q", format=".2f")],
    )
    _afficher(st.altair_chart, graphique.properties(height=34 * len(familles) + 40))
    tableau = familles[["mcc_family", "transactions", "achats", "taux_signalement"]].rename(
        columns={"mcc_family": "famille", "achats": "achats ($)", "taux_signalement": "signalées (%)"})
    _afficher(
        st.dataframe,
        tableau,
        hide_index=True,
        column_config={
            "achats ($)": st.column_config.NumberColumn(format="%.0f"),
            "signalées (%)": st.column_config.NumberColumn(format="%.2f"),
        },
    )


# =============================================================================
# P8-07 : Transactions signalées
# =============================================================================


def transactions_signalees(t: dict, f: dict):
    st.title("Transactions signalées")
    st.caption(_periode(f) + " Liste triée du score le plus haut au plus bas.")
    toutes = t["signalees"]

    c1, c2, c3 = st.columns([1, 2, 2])
    client = c1.text_input("Client (numéro)", "", help="Exemple : 1098. Laisser vide pour tous les clients.")
    familles = c2.multiselect("Familles de commerçants", sorted(toutes["famille"].unique()), placeholder="Toutes")
    raisons = c3.multiselect("Raison principale", sorted(toutes["raison_principale"].unique()), placeholder="Toutes")
    score_min = st.slider("Score minimal", 0.0, 100.0, 0.0, step=0.5)
    if client and not client.strip().isdigit():
        st.warning("Le numéro de client doit être un nombre entier.")
        client = ""

    liste = liste_signalee(t, f["annees"], f["seuil"], client=client.strip() or None, familles=familles,
                           canaux=f["canaux"], raisons=raisons, score_min=score_min)
    c1, c2, c3 = st.columns(3)
    c1.metric("Transactions signalées", fr(len(liste)))
    c2.metric("Clients concernés", fr(liste["client_id"].nunique()))
    c3.metric("Score médian", fr(liste["score"].median(), 1) if len(liste) else "-")

    evaluation = t["evaluation"].set_index("seuil")
    if f["seuil"] in evaluation.index:
        e = evaluation.loc[f["seuil"]]
        st.info(f"Sur les transactions étiquetées (P7-11), au seuil de {f['seuil']} : précision de "
                f"{fr(e['precision'], 2)} % (part de vraies fraudes parmi les signalées) et rappel de "
                f"{fr(e['rappel'], 2)} % (part des fraudes qui sont signalées).")

    if len(liste) == 0:
        st.warning("Aucune transaction ne correspond aux filtres.")
        return

    courtes = liste["raison_principale"].map(lambda r: f"{r[:3]} : {SHORT_LABELS[r[:3]]}" if r[:3] in SHORT_LABELS else r)
    raisons_compte = courtes.value_counts().rename_axis("raison").reset_index(name="transactions")
    _afficher(st.altair_chart, _barres(raisons_compte, "raison", "transactions", "transactions signalées"))

    colonnes = ["rang", "date", "client_id", "card_id", "montant", "canal", "famille", "ville", "lieu", "score",
                "raison_principale"]
    _afficher(
        st.dataframe,
        liste[colonnes].head(500),
        hide_index=True,
        column_config={
            "date": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm"),
            "montant": st.column_config.NumberColumn("montant ($)", format="%.2f"),
            "score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.1f"),
            "client_id": st.column_config.NumberColumn("client", format="%d"),
            "card_id": st.column_config.NumberColumn("carte", format="%d"),
        },
    )
    st.caption("Les 500 premières lignes sont affichées. Le bouton ci-dessous télécharge toute la liste filtrée.")
    st.download_button("Télécharger la liste filtrée (CSV)", liste[colonnes].to_csv(index=False).encode("utf-8-sig"),
                       file_name="transactions_signalees.csv", mime="text/csv")
