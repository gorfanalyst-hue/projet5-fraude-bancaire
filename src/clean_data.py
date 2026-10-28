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