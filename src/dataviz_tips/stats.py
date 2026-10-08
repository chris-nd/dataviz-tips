"""
Module de fonctions d'analyse statistiques.

- Écart interquartile
- Séparation des valeurs extrêmes
"""

import numpy as np
import pandas as pd


def split_extremes(
    df: pd.DataFrame, column: str, k: float = 1.5
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Sépare les lignes extrêmes des autres selon la règle de l'IQR.

    Une valeur est extrême si elle est strictement hors de
    [borne basse, borne haute]. Les NaN vont dans le reste.
    L'index d'origine est conservé.

    :raises KeyError: Si la colonne n'existe pas.
    :raises ValueError: Si k est invalide ou la colonne sans valeur valide.
    :returns: (extrêmes, reste)
    """

    lower, upper = iqr_bounds(df[column], k)
    is_extreme = (df[column] < lower) | (df[column] > upper)

    return df[is_extreme], df[~is_extreme]


def iqr_bounds(series: pd.Series, k: float = 1.5) -> tuple[float, float]:
    """
    Calcule les bornes de l'écart interquartile pour une série donnée et ignore les valeurs NaN.

    :params series: La série de données.
    :type series: pd.Series

    :params k: Le multiplicateur pour déterminer les bornes.
    :type k: float

    :raises ValueError: Si la série ne contient aucune valeur valide ou si k est négatif.

    :returns: Les bornes inférieure et supérieure de l'écart interquartile.
    :rtype: tuple[float, float]
    """

    if series.isna().all():
        raise ValueError("La série ne contient aucune valeur valide.")

    if k < 0:
        raise ValueError("Le paramètre k ne doit pas être un nombre négatif.")

    if np.isnan(k):
        raise ValueError("Le paramètre k ne doit pas être `NaN`.")

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = float(q1 - k * iqr)
    upper_bound = float(q3 + k * iqr)

    return (lower_bound, upper_bound)
