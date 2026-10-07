"Module de test pour les fonctions de statistiques."

import numpy as np
import pandas as pd
import pytest

from dataviz_tips.stats import iqr_bounds


@pytest.fixture(name="series")
def fixture_series():
    "Crée une série de données pour les tests."
    return pd.Series([1, 2, 3, 4, 100])


def test_iqr_bounds(series):
    "Vérifie les bornes de l'écart interquartile d'une série avec K=1.5"

    assert iqr_bounds(series) == pytest.approx((-1, 7))


def test_series_with_two_values():
    "Vérifie les bornes pour une série avec deux valeurs."
    s = pd.Series([1, 3])

    assert iqr_bounds(s) == pytest.approx((0, 4))


def test_series_with_unique_value():
    "Vérifie les bornes pour une série avec une seule valeur."
    s = pd.Series([7])

    assert iqr_bounds(s) == pytest.approx((7, 7))


def test_series_with_constant_values():
    "Vérifie les bornes pour une série avec des valeurs constantes."
    s = pd.Series([5, 5, 5, 5])

    assert iqr_bounds(s) == pytest.approx((5, 5))


def test_series_with_nan_ignored():
    "Vérifie les bornes pour une série avec des valeurs NaN."
    s = pd.Series([1, 2, 3, 4, 100, np.nan])

    assert iqr_bounds(s) == pytest.approx((-1, 7))


@pytest.mark.parametrize(
    "k, expected", [(0, (2, 4)), (3, (-4, 10))], ids=["k=0", "k=3"]
)
def test_series_with_different_k(series, k, expected):
    "Vérifie les bornes pour une série avec un paramètre k différent."

    assert iqr_bounds(series, k=k) == pytest.approx(expected)


@pytest.mark.parametrize(
    "s",
    [(pd.Series([], dtype=float)), (pd.Series([np.nan], dtype=float))],
    ids=["empty", "only_nan"],
)
def test_empty_or_nan_series(s):
    "Lève une erreur pour une série vide ou ne contenant que des NaN »"

    with pytest.raises(ValueError, match="La série ne contient aucune valeur valide."):
        iqr_bounds(s)


def test_series_with_negative_k(series):
    "Lève une erreur pour une série avec un paramètre k négatif."

    with pytest.raises(
        ValueError, match="Le paramètre k ne doit pas être un nombre négatif."
    ):
        iqr_bounds(series, k=-1)


def test_series_with_decimal_k(series, k=0.5):
    "Vérifie les bornes pour une série avec un paramètre k décimal."

    assert iqr_bounds(series, k=k) == pytest.approx((1, 5))


def test_series_with_k_nan(series, k=np.nan):
    "Lève une erreur pour une série avec un paramètre k égal à NaN."

    with pytest.raises(ValueError, match="Le paramètre k ne doit pas être `NaN`."):
        iqr_bounds(series, k=k)


def test_does_not_mutate_input():
    "Ne modifie pas la série d'entrée."

    original_series = pd.Series([1, 2, 3, 4, 100, np.nan])
    series = original_series.copy()
    iqr_bounds(series)

    pd.testing.assert_series_equal(series, original_series)
