import pandas as pd

def convert_currency_column(series: pd.Series) -> pd.Series:
    """
    Convertit une colonne texte du type '$1,234.56' ou '$-77.00'
    en float. Retourne NaN pour toute valeur non convertible.
    """
    cleaned = (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def report_conversion_issues(original: pd.Series, converted: pd.Series, label: str):
    """
    Liste les valeurs qui n'ont pas pu être converties (critère de fin de P3-02).
    """
    failed_mask = converted.isna() & original.notna()
    n_failed = failed_mask.sum()
    print(f"{label}: {n_failed} valeur(s) non convertie(s)")
    if n_failed > 0:
        print(original[failed_mask].unique()[:10])

# Conversion des dates
def convert_month_year_column(series: pd.Series, end_of_month: bool = False) -> pd.Series:
    """
    Convertit une colonne texte 'mm/aaaa' en datetime.
    Par défaut : 1er jour du mois. Avec end_of_month=True : dernier jour du mois.
    Retourne NaT pour toute valeur non convertible.
    """
    dates = pd.to_datetime(series, format="%m/%Y", errors="coerce")
    if end_of_month:
        dates = dates + pd.offsets.MonthEnd(0)
    return dates


def check_datetime_column(series: pd.Series, label: str):
    """
    Affiche le type, le nombre de dates manquantes et la plage de dates.
    """
    print(f"{label}: type={series.dtype}, "
          f"manquantes={series.isna().sum()}, "
          f"min={series.min()}, max={series.max()}")


def build_mcc_table(df_mcc: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie la table des codes MCC : espaces retirés, tri par code,
    unicité des codes vérifiée.
    """
    table = df_mcc.copy()
    table["description"] = table["description"].str.strip()
    table = table.sort_values("mcc_code").reset_index(drop=True)
    n_dup = table["mcc_code"].duplicated().sum()
    if n_dup:
        raise ValueError(f"{n_dup} code(s) MCC en double")
    return table


def check_mcc_join(df_transaction: pd.DataFrame, df_mcc: pd.DataFrame) -> bool:
    """
    Joint transactions et catégories MCC, puis vérifie qu'aucune ligne
    n'est perdue ou dupliquée et qu'aucune transaction n'est sans catégorie.
    """
    n_before = len(df_transaction)
    joined = df_transaction[["id", "mcc"]].merge(
        df_mcc, left_on="mcc", right_on="mcc_code",
        how="left", validate="many_to_one"
    )
    n_after = len(joined)
    orphan_mask = joined["description"].isna()
    n_orphan = orphan_mask.sum()

    print(f"Lignes avant : {n_before:,} | après : {n_after:,}")
    print(f"Transactions sans catégorie : {n_orphan:,}")
    if n_orphan:
        print("Codes MCC sans correspondance :",
              sorted(joined.loc[orphan_mask, "mcc"].unique()))
    return n_before == n_after and n_orphan == 0


from src.mcc_families import MCC_TO_FAMILLE, MCC_DESCRIPTIONS_FR

def add_mcc_families(df_mcc: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la famille et la description française à la table MCC."""
    table = df_mcc.copy()
    table["famille"] = table["mcc_code"].map(MCC_TO_FAMILLE)
    table["description_fr"] = table["mcc_code"].map(MCC_DESCRIPTIONS_FR)
    return table


def check_mcc_families(df_mcc: pd.DataFrame, df_transaction: pd.DataFrame) -> bool:
    """
    Vérifie que chaque code a une famille et une description française,
    puis résume les familles (codes et transactions).
    """
    missing_family = df_mcc.loc[df_mcc["famille"].isna(), "mcc_code"].tolist()
    missing_fr = df_mcc.loc[df_mcc["description_fr"].isna(), "mcc_code"].tolist()
    extra = sorted(set(MCC_TO_FAMILLE) - set(df_mcc["mcc_code"]))
    print(f"Codes sans famille : {missing_family}")
    print(f"Codes sans description française : {missing_fr}")
    print(f"Codes du dictionnaire absents de la table : {extra}")

    n_tx = df_transaction["mcc"].value_counts().rename("n_transactions")
    resume = (
        df_mcc.merge(n_tx, left_on="mcc_code", right_index=True, how="left")
        .groupby("famille")
        .agg(n_codes=("mcc_code", "count"), n_transactions=("n_transactions", "sum"))
        .sort_values("n_transactions", ascending=False)
    )
    resume["part_%"] = (100 * resume["n_transactions"] / resume["n_transactions"].sum()).round(1)
    print(resume)
    return not (missing_family or missing_fr or extra)