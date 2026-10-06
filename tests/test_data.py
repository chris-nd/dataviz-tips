"""
Teste la suppression des lignes dupliquées, la conservation des index
et la mutabilité du dataset.
"""

import pandas as pd

from dataviz_tips.data import drop_duplicate_rows, load_tips


def test_load_tips():
    "Vérifie que le dataset des pourboires est chargé correctement"
    tips = load_tips()
    assert isinstance(tips, pd.DataFrame)


def test_removes_identical_rows():
    "Vérifie que les lignes identiques sont supprimées"
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})

    result = drop_duplicate_rows(df)

    assert len(result) == 2


def test_non_mutability_df():
    "Vérifie que le DataFrame source n'est pas modifié"
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    df_original = df.copy()

    drop_duplicate_rows(df)

    pd.testing.assert_frame_equal(df_original, df)


def test_non_duplicate_rows():
    "Vérifie que l'absence de doublons ne modifie pas le DataFrame"
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "x", "y"]})

    result = drop_duplicate_rows(df)

    pd.testing.assert_index_equal(result.index, df.index)


def test_reset_index():
    "Vérifie que l'index est réinitialisé"
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})

    result = drop_duplicate_rows(df)

    pd.testing.assert_index_equal(result.index, pd.RangeIndex(len(result)))
