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

# =============================================================================
# P3-06 : Transformation de la colonne errors
# =============================================================================
 
# Liste standard des erreurs simples et sous-ensemble des échecs d'authentification (cf. P4-06)
ALL_ERROR_TYPES = [
    "Bad PIN",
    "Bad CVV",
    "Bad Card Number",
    "Bad Expiration",
    "Bad Zipcode",
    "Insufficient Balance",
    "Technical Glitch",
]
 
AUTH_ERROR_TYPES = [
    "Bad PIN",
    "Bad CVV",
    "Bad Card Number",
    "Bad Expiration",
    "Bad Zipcode",
]
 
 
def _slugify_error_name(err_name: str) -> str:
    """Transforme 'Bad Card Number' en 'err_bad_card_number'."""
    return "err_" + err_name.lower().replace(" ", "_")
 
 
def transform_errors_column(
    df: pd.DataFrame, error_col: str = "errors"
) -> pd.DataFrame:
    """
    P3-06 : Transforme la colonne 'errors' en :
    - Une colonne binaire (int8 : 0/1) par type d'erreur simple
    - Un indicateur 'has_error' (au moins une erreur)
    - Un indicateur 'has_auth_error' (échec d'authentification : PIN, CVV, numéro, expiration, zip)
    """
    s_err = df[error_col].astype("string").fillna("")
 
    # 1. Indicateur "au moins une erreur"
    df["has_error"] = (s_err != "").astype("int8")
 
    # 2. Une colonne oui/non (int8) par type d'erreur
    # Astuce mémoire/vitesse : calculer sur les modalités uniques puis mapper
    unique_vals = s_err.unique()
    for err_type in ALL_ERROR_TYPES:
        col_name = _slugify_error_name(err_type)
        # On vérifie la présence exacte du jeton d'erreur dans la chaîne séparée par des virgules
        mapping = {
            val: int(err_type in [token.strip() for token in val.split(",")])
            for val in unique_vals
        }
        df[col_name] = s_err.map(mapping).astype("int8")
 
    # 3. Indicateur "échec d'authentification"
    auth_cols = [_slugify_error_name(e) for e in AUTH_ERROR_TYPES]
    df["has_auth_error"] = (df[auth_cols].sum(axis=1) > 0).astype("int8")
 
    return df
 
 
def check_errors_transformation(df: pd.DataFrame, error_col: str = "errors"):
    """
    Vérifie le critère de fin de P3-06 :
    Compare les totaux des nouvelles colonnes binaires avec le comptage direct (P2-13).
    """
    print("=== Contrôle P3-06 : Transformation de la colonne 'errors' ===")
    s_err = df[error_col].dropna().astype(str)
 
    # Comptage de référence façon P2-13 (explosion des chaînes séparées par virgule)
    ref_counts = (
        s_err.str.split(",")
        .explode()
        .str.strip()
        .value_counts()
    )
 
    all_match = True
    for err_type in ALL_ERROR_TYPES:
        col_name = _slugify_error_name(err_type)
        col_total = int(df[col_name].sum()) if col_name in df.columns else 0
        ref_total = int(ref_counts.get(err_type, 0))
        match = col_total == ref_total
        all_match = all_match and match
        statut = "OK" if match else "ÉCART !"
        print(f"  - {err_type:<22} ({col_name:<25}) : {col_total:>8} | Réf P2-13 : {ref_total:>8} [{statut}]")

    inconnus = sorted(set(ref_counts.index) - set(ALL_ERROR_TYPES))
    print(f"  - Types d'erreur absents de ALL_ERROR_TYPES : {inconnus}")
    all_match = all_match and not inconnus

    print(f"  - Transactions avec >= 1 erreur (has_error)      : {int(df['has_error'].sum()):>8}")
    print(f"  - Transactions avec échec auth (has_auth_error)  : {int(df['has_auth_error'].sum()):>8}")
    print(f"Critère de fin P3-06 validé : {all_match}\n")
 
    print(f"  - Transactions avec >= 1 erreur (has_error)      : {int(df['has_error'].sum()):>8}")
    print(f"  - Transactions avec échec auth (has_auth_error)  : {int(df['has_auth_error'].sum()):>8}")
    print(f"Critère de fin P3-06 validé : {all_match}\n")
 
 
# =============================================================================
# P3-07 : Structuration du lieu des transactions
# =============================================================================
 
# Codes officiels à 2 lettres des 50 États américains + DC + territoires US
US_STATES_AND_TERRITORIES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC", "PR", "GU", "VI", "AS", "MP", "AA"
}
 
 
def structurer_lieu_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    P3-07 : Structure les colonnes géographiques des transactions :
    - Crée l'indicateur 'is_online' (int8 : 0/1)
    - Sépare 'merchant_country' et 'merchant_state_clean' avec valeurs explicites
    - Crée l'indicateur 'is_foreign' (int8 : 0/1)
    - Remplace les valeurs manquantes de ville/état/pays par des modalités explicites
    """
    city_str = df["merchant_city"].astype("string").str.strip().fillna("UNKNOWN")
    state_str = df["merchant_state"].astype("string").str.strip()
    chip_str = df["use_chip"].astype("string").str.strip().fillna("")
 
    # 1. Indicateur "en ligne" (concordance entre merchant_city == ONLINE et use_chip)
    is_online_mask = (city_str.str.upper() == "ONLINE") | (chip_str == "Online Transaction")
    df["is_online"] = is_online_mask.astype("int8")

        # Désaccord ville ONLINE / canal (P2-07) : conservé et marqué, pas supprimé
    df["online_channel_mismatch"] = (is_online_mask & (chip_str != "Online Transaction")).astype("int8")
 
    # 2. Identification des États américains vs Pays étrangers
    is_us_state_mask = (~is_online_mask) & state_str.isin(US_STATES_AND_TERRITORIES)
    is_foreign_mask = (~is_online_mask) & state_str.notna() & (~state_str.isin(US_STATES_AND_TERRITORIES))
 
    # 3. Construction de la colonne 'merchant_country'
    country = pd.Series("UNKNOWN", index=df.index, dtype="string")
    country = country.mask(is_online_mask, "ONLINE")
    country = country.mask(is_us_state_mask, "USA")
    country = country.mask(is_foreign_mask, state_str)
    df["merchant_country"] = country.astype("category")
 
    # 4. Construction de la colonne 'merchant_state_clean' (sans aucun NaN)
    state_clean = pd.Series("UNKNOWN", index=df.index, dtype="string")
    state_clean = state_clean.mask(is_online_mask, "ONLINE")
    state_clean = state_clean.mask(is_us_state_mask, state_str)
    state_clean = state_clean.mask(is_foreign_mask, "FOREIGN_NO_STATE")
    df["merchant_state_clean"] = state_clean.astype("category")
 
    # 5. Nettoyage explicite de 'merchant_city'
    city_clean = city_str.mask(is_online_mask, "ONLINE")
    df["merchant_city"] = city_clean.astype("category")
 
    # 6. Indicateur "à l'étranger" (transactions physiques hors USA)
    df["is_foreign"] = is_foreign_mask.astype("int8")
 
    # 7. Traitement explicite du code postal (zip) s'il est présent
    if "zip" in df.columns:
        zip_str = (
            df["zip"]
            .astype("string")
            .str.replace(r"\.0$", "", regex=True)
            .str.strip()
            .str.zfill(5)
        )
        zip_clean = zip_str.fillna("UNKNOWN")
        zip_clean = zip_clean.mask(is_online_mask, "ONLINE")
        zip_clean = zip_clean.mask(is_foreign_mask & df["zip"].isna(), "FOREIGN_NO_ZIP")
        df["zip_clean"] = zip_clean.astype("category")
 
    return df
 
 
def check_location_structuration(df: pd.DataFrame):
    """
    Vérifie le critère de fin de P3-07 :
    Plus aucun manquant inexpliqué dans les colonnes de lieu.
    """
    print("=== Contrôle P3-07 : Structuration du lieu des transactions ===")
    loc_cols = ["merchant_city", "merchant_state_clean", "merchant_country", "is_online", "is_foreign"]
    if "zip_clean" in df.columns:
        loc_cols.append("zip_clean")

    for col in loc_cols:
        n_na = int(df[col].isna().sum())
        n_unk = 0 if col in ("is_online", "is_foreign") else int((df[col] == "UNKNOWN").sum())
        print(f"  - {col:<22} : NaN = {n_na:>6} | 'UNKNOWN' (inexpliqués) = {n_unk:>6}")

    print("\nRépartition par type de localisation :")
    print(f"  - En ligne (is_online=1)      : {int(df['is_online'].sum()):>10}")
    print(f"  - À l'étranger (is_foreign=1) : {int(df['is_foreign'].sum()):>10}")
    print(f"  - Aux USA (physique)          : {int((df['merchant_country'] == 'USA').sum()):>10}\n")
    print(f"  - Désaccord ville/canal (online_channel_mismatch=1) : {int(df['online_channel_mismatch'].sum()):>10}")
 