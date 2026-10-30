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
