"Module de test pour les fonctions de statistiques."

import numpy as np
import pandas as pd
import pytest

from dataviz_tips.stats import iqr_bounds, split_extremes


# Test iqr_bounds()


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


# Tests split_extremes()


@pytest.fixture(name="df")
def fixture_df():
    "Crée un DataFrame de test."
    return pd.DataFrame({"x": [1, 2, 3, 4, 100], "y": list("abcde")})


def test_splits_extreme_rows(df):
    "Teste la séparation des lignes extrêmes."
    extremes, rest = split_extremes(df, "x")

    pd.testing.assert_frame_equal(extremes, df.iloc[[4]])
    pd.testing.assert_frame_equal(rest, df.iloc[[0, 1, 2, 3]])


def test_keeps_all_rows(df):
    "Teste que toutes les lignes sont conservées."
    extremes, rest = split_extremes(df, "x")

    assert len(extremes) + len(rest) == len(df)
    pd.testing.assert_frame_equal(pd.concat([extremes, rest]).sort_index(), df)


@pytest.mark.parametrize("values", [[1, 2, 3, 4, 7], [-1, 2, 3, 4, 5]])
def test_value_on_bound_is_not_extreme(values):
    "Teste que les valeurs sur les bornes ne sont pas considérées comme extrêmes."
    df = pd.DataFrame({"x": values})

    extremes, rest = split_extremes(df, "x")

    assert extremes.empty
    pd.testing.assert_frame_equal(rest, df)


def test_nan_goes_to_rest():
    "Teste que les valeurs NaN vont dans le reste."
    df = pd.DataFrame({"x": [1, 2, 3, 4, 100, np.nan]})

    extremes, rest = split_extremes(df, "x")

    pd.testing.assert_frame_equal(extremes, df.iloc[[4]])
    pd.testing.assert_frame_equal(rest, df.iloc[[0, 1, 2, 3, 5]])


def test_no_extreme_returns_empty_frame_with_columns():
    "Teste qu'aucune ligne n'est considérée comme extrême."
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": list("abcde")})

    extremes, rest = split_extremes(df, "x")

    pd.testing.assert_frame_equal(extremes, df.iloc[0:0])
    pd.testing.assert_frame_equal(rest, df)


def test_does_not_df_mutate_input():
    "Teste que le DataFrame d'entrée n'est pas modifié."
    df = pd.DataFrame({"x": [1, 2, 3, 4, 100, np.nan]})
    original = df.copy()

    _ = split_extremes(df, "x")

    pd.testing.assert_frame_equal(df, original)


def test_unknown_column_raises_key_error(df):
    "Teste que la levée d'une erreur est attendue pour une colonne inconnue."
    with pytest.raises(KeyError):
        split_extremes(df, "missing")


def test_negative_k_raises_value_error(df):
    "Teste que la levée d'une erreur est attendue pour un paramètre k négatif."
    with pytest.raises(ValueError, match="négatif"):
        split_extremes(df, "x", k=-1)
