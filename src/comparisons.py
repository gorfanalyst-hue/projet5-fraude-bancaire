"""
Comparaisons chiffrées et tests statistiques (phases 6 et 7).

Avec des millions de lignes, presque tout écart devient « significatif ».
Chaque comparaison donne donc aussi la taille de l'écart (taille d'effet),
qui dit si l'écart compte en pratique.
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, mannwhitneyu


def rate_table(df: pd.DataFrame, by, flag: str) -> pd.DataFrame:
    """
    Taux d'une colonne 0/1 (erreur, signalement...) pour chaque valeur de `by`.
    - écart_points : différence avec le taux global, en points de pourcentage ;
    - rapport : taux du groupe divisé par le taux global (2 = deux fois plus).
    """
    table = df.groupby(by, observed=True)[flag].agg(["size", "sum"])
    table.columns = ["transactions", "cas"]
    global_rate = 100 * df[flag].mean()
    table["taux_%"] = 100 * table["cas"] / table["transactions"]
    table["écart_points"] = table["taux_%"] - global_rate
    table["rapport"] = table["taux_%"] / global_rate
    return table.round({"taux_%": 3, "écart_points": 3, "rapport": 2})


def effect_label(value: float) -> str:
    """Lecture d'une taille d'effet (V de Cramér ou corrélation rang-bisériale), en valeur absolue."""
    v = abs(value)
    if v < 0.1:
        return "négligeable"
    if v < 0.3:
        return "faible"
    if v < 0.5:
        return "moyen"
    return "fort"


def chi2_test(df: pd.DataFrame, col: str, flag: str) -> dict:
    """
    Test du khi-deux d'indépendance entre une variable catégorielle et une colonne 0/1.
    Taille d'effet : V de Cramér (0 = aucun lien, 1 = lien parfait).
    """
    table = pd.crosstab(df[col], df[flag])
    chi2, p, dof, _ = chi2_contingency(table, correction=False)
    n = table.to_numpy().sum()
    v = float(np.sqrt(chi2 / (n * (min(table.shape) - 1))))
    return {"variable": col, "test": "khi-deux", "statistique": round(chi2, 1), "ddl": int(dof),
            "p_valeur": p, "taille d'effet": round(v, 3), "mesure": "V de Cramér", "lecture": effect_label(v)}


def mann_whitney_test(values: pd.Series, flag: pd.Series, name: str) -> dict:
    """
    Test de Mann-Whitney entre les lignes où flag = 1 et les autres.
    Taille d'effet : corrélation rang-bisériale r, de -1 à 1.
    r > 0 : les valeurs du groupe flag = 1 sont plutôt plus élevées.
    """
    a = values[flag == 1].dropna().to_numpy()
    b = values[flag == 0].dropna().to_numpy()
    u, p = mannwhitneyu(a, b, alternative="two-sided", method="asymptotic")
    r = 2 * u / (len(a) * len(b)) - 1
    return {"variable": name, "test": "Mann-Whitney", "statistique": round(float(u), 1), "ddl": np.nan,
            "p_valeur": p, "taille d'effet": round(float(r), 3), "mesure": "rang-bisériale",
            "lecture": effect_label(r), "médiane groupe 1": float(np.median(a)),
            "médiane groupe 0": float(np.median(b))}


def holm_correction(pvalues) -> np.ndarray:
    """
    Correction de Holm : quand on fait m tests, la plus petite p-valeur est
    multipliée par m, la suivante par m - 1, etc. Les valeurs restent croissantes
    et ne dépassent pas 1.
    """
    p = np.asarray(pvalues, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adjusted = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[idx]))
        adjusted[idx] = running
    return adjusted
