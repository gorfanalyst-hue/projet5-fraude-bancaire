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