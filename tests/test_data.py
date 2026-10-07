"""
Teste le chargement des données, la suppression des lignes dupliquées,
la non mutation du jeu de données et la réinitialisation des index.
"""

import pandas as pd
import pytest
import seaborn as sns

from dataviz_tips.data import drop_duplicate_rows, load_tips


@pytest.fixture(name="df_duplicate")
def fixture_tips_duplicate():
    "Fixture pour créer un DataFrame de test"
    return pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})


@pytest.mark.parametrize(
    "df, expected",
    [
        (
            pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]}),
            pd.DataFrame({"a": [1, 2], "b": ["x", "y"]}),
        ),
        (
            pd.DataFrame({"a": [0, 1, 1], "b": ["x", "y", "y"]}),
            pd.DataFrame({"a": [0, 1], "b": ["x", "y"]}),
        ),
    ],
)
def test_load_tips(df, expected, monkeypatch):
    "Vérifie que le dataset des pourboires est chargé correctement"

    def mock_df(name):
        assert name == "tips"
        return df

    monkeypatch.setattr(sns, "load_dataset", mock_df)

    pd.testing.assert_frame_equal(load_tips(), expected)


@pytest.mark.parametrize(
    "df, expected",
    [
        (
            pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]}),
            pd.DataFrame({"a": [1, 2], "b": ["x", "y"]}),
        ),
        (
            pd.DataFrame({"a": [1, 2, 1], "b": ["x", "y", "x"]}),
            pd.DataFrame({"a": [1, 2], "b": ["x", "y"]}),
        ),
    ],
)
def test_removes_identical_rows(df, expected):
    "Vérifie que les lignes identiques sont supprimées"
    result = drop_duplicate_rows(df)

    pd.testing.assert_frame_equal(result, expected)


def test_does_not_mutate_input(df_duplicate):
    "Vérifie que le DataFrame source n'est pas modifié"
    df_original = df_duplicate.copy()
    drop_duplicate_rows(df_duplicate)

    pd.testing.assert_frame_equal(df_original, df_duplicate)


@pytest.mark.parametrize(
    "df",
    [
        pd.DataFrame({"a": [0, 1, 2], "b": ["x", "y", "z"]}),
        pd.DataFrame({"a": [1, 2, 3], "b": ["x", "x", "z"]}),
    ],
)
def test_keeps_frame_without_duplicates(df):
    "Vérifie que l'absence de doublons ne modifie pas le DataFrame"

    result = drop_duplicate_rows(df)

    pd.testing.assert_frame_equal(result, df)


def test_all_identical_rows():
    "Vérifie que toutes les lignes identiques sont supprimées sauf la première"
    df = pd.DataFrame({"a": [1, 1, 1], "b": ["x", "x", "x"]})
    expected = pd.DataFrame({"a": [1], "b": ["x"]})

    result = drop_duplicate_rows(df)

    pd.testing.assert_frame_equal(result, expected)


def test_empty_df():
    "Vérifie qu'un DataFrame vide est géré correctement"
    df = pd.DataFrame(columns=["a", "b"])

    result = drop_duplicate_rows(df)

    pd.testing.assert_frame_equal(result, df)


def test_reset_index(df_duplicate):
    "Vérifie que l'index est réinitialisé"

    result = drop_duplicate_rows(df_duplicate)

    pd.testing.assert_index_equal(result.index, pd.RangeIndex(len(result)))
