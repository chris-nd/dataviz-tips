"Module de test pour les fonctions de tracé"

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.axes import Axes

from dataviz_tips.plots import (
    plot_boxplot_mpl,
    plot_boxplot_sns,
    plot_correlation_heatmap_mpl,
    plot_correlation_heatmap_sns,
    plot_histogram_mpl,
    plot_histogram_sns,
    plot_scatter_mpl,
    plot_scatter_sns,
    plot_size_counts_mpl,
    plot_size_counts_sns,
    save_figure,
)

HISTOGRAM = [plot_histogram_mpl, plot_histogram_sns]
SCATTER = [plot_scatter_mpl, plot_scatter_sns]
BOXPLOT = [plot_boxplot_mpl, plot_boxplot_sns]
COUNTER = [plot_size_counts_mpl, plot_size_counts_sns]
HEATMAP = [plot_correlation_heatmap_mpl, plot_correlation_heatmap_sns]

CASES = [
    pytest.param(plot_histogram_mpl, ("tip",), id="hist_mpl"),
    pytest.param(plot_histogram_sns, ("tip",), id="hist_sns"),
    pytest.param(plot_size_counts_mpl, ("tip",), id="bar_mpl"),
    pytest.param(plot_size_counts_sns, ("tip",), id="bar_sns"),
    pytest.param(plot_boxplot_mpl, ("tip",), id="box_mpl"),
    pytest.param(plot_boxplot_sns, ("tip",), id="box_sns"),
    pytest.param(plot_scatter_mpl, ("tip", "total_bill"), id="scatter_mpl"),
    pytest.param(plot_scatter_sns, ("tip", "total_bill"), id="scatter_sns"),
]


@pytest.fixture(name="df")
def fixture_scatter_df():
    "Fixture pour créer un DataFrame de test"
    return pd.DataFrame(
        {"tip": [1, 2, 2, 3], "total_bill": [10, 20, 20, 30], "size": [2, 3, 3, 4]}
    )


# Test Helpers


@pytest.mark.parametrize("plot_func, columns", CASES)
def test_creates_a_new_axes_each_call(plot_func, columns, df):
    "Teste qu'un nouvel axe est créé à chaque appel"
    assert plot_func(df, *columns) is not plot_func(df, *columns)


@pytest.mark.parametrize("plot_func, columns", CASES)
def test_draws_on_given_axes(plot_func, columns, df):
    "Teste que le graphique est dessiné sur l'axe donné"
    _, given_ax = plt.subplots()

    assert plot_func(df, *columns, ax=given_ax) is given_ax


@pytest.mark.parametrize("plot_func, columns", CASES)
def test_has_a_title(plot_func, columns, df):
    "Teste que le graphique a un titre"
    assert plot_func(df, *columns).get_title() != ""


@pytest.mark.parametrize("plot_func, columns", CASES)
def test_missing_column_raises_without_orphan_figure(plot_func, columns, df):
    "Teste que lève une erreur lorsqu'une colonne manquante est spécifiée"
    for i in range(len(columns)):  # on teste chaque colonne, x puis y
        bad = list(columns)
        bad[i] = "missing"

        with pytest.raises(KeyError, match="missing"):
            plot_func(df, *bad)

        assert plt.get_fignums() == []


# Test histogramme


@pytest.mark.parametrize("plot_func", HISTOGRAM)
def test_histogram_counts_every_row(plot_func, df):
    "Teste que l'histogramme compte chaque ligne du DataFrame"
    ax = plot_func(df, "tip")

    assert isinstance(ax, Axes)
    assert sum(patch.get_height() for patch in ax.patches) == len(df)


@pytest.mark.parametrize("plot_func", HISTOGRAM)
def test_histogram_title_and_labels(plot_func, df):
    "Teste que l'histogramme a le bon titre et les bonnes étiquettes"
    ax = plot_func(df, "tip")

    assert ax.get_title() == "Histogramme de tip"
    assert ax.get_xlabel() == "tip"
    assert ax.get_ylabel() == "Fréquence"


@pytest.mark.parametrize("plot_func", HISTOGRAM)
def test_bins_sets_number_of_bars(plot_func, df):
    "Teste que le nombre de bins définis le nombre de barres"
    ax = plot_func(df, "tip", bins=5)

    assert len(ax.patches) == 5


@pytest.mark.parametrize("plot_func", HISTOGRAM)
def test_ignore_nan(plot_func, df):
    "Teste que les valeurs NaN sont ignorées"
    df = pd.DataFrame({"tip": [1, 2, 2, 3, np.nan]})

    ax = plot_func(df, "tip")

    assert sum(patch.get_height() for patch in ax.patches) == 4


@pytest.mark.parametrize("plot_func", HISTOGRAM)
def test_column_not_exists(plot_func, df):
    "Teste que l'histogramme gère correctement une colonne non existante"

    with pytest.raises(KeyError, match="bill"):
        plot_func(df, "bill")

    assert plt.get_fignums() == []  # aucune figure orpheline


# Test scatter plot


@pytest.mark.parametrize("plot_func", SCATTER)
def test_scatter_plots_every_row(plot_func, df):
    "Teste que le graphique de dispersion dessine chaque ligne du DataFrame"
    ax = plot_func(df, "tip", "total_bill")

    assert isinstance(ax, Axes)
    assert len(ax.collections[0].get_offsets()) == len(df)


@pytest.mark.parametrize("plot_func", SCATTER)
def test_scatter_ignores_nan(plot_func):
    "Teste que le graphique de dispersion ignore les valeurs NaN"
    df = pd.DataFrame({"tip": [1, 2, 3, np.nan], "total_bill": [10, 20, 30, 40]})

    assert len(plot_func(df, "tip", "total_bill").collections[0].get_offsets()) == 3


# Test box plots


@pytest.mark.parametrize("plot_func", BOXPLOT)
def test_boxplot_is_vertical_and_ignores_nan(plot_func):
    "Teste que le boxplot est vertical et ignore les valeurs NaN"
    df = pd.DataFrame({"tip": [1, 2, 3, np.nan]})

    ax = plot_func(df, "tip")

    assert ax.get_ylabel() == "tip"  # verticale : la colonne est sur l'axe y
    medians = [
        line.get_ydata()
        for line in ax.lines
        if len(line.get_ydata()) == 2 and line.get_ydata()[0] == line.get_ydata()[1]
    ]
    assert any(np.isclose(m[0], 2.0) for m in medians)  # médiane de [1, 2, 3]


# Test bar plots


@pytest.mark.parametrize("plot_func", COUNTER)
def test_size_counts_heights(plot_func, df):  # tip = [1, 2, 2, 3]
    "Teste que le graphique de comptage affiche les bonnes hauteurs"
    ax = plot_func(df, "tip")

    assert [patch.get_height() for patch in ax.patches] == [1, 2, 1]


# Test heatmap


def _artist(ax):
    "Image (Matplotlib) ou maillage (Seaborn) qui porte la matrice."
    return ax.images[0] if ax.images else ax.collections[0]


@pytest.fixture(name="corr_matrix")
def fixture_corr_matrix():  # écrite à la main : pas de df.corr() dans un test
    return pd.DataFrame(
        [[1, 0.5, -0.2], [0.5, 1, 0.3], [-0.2, 0.3, 1]],
        index=list("abc"),
        columns=list("abc"),
    )


@pytest.mark.parametrize("func", HEATMAP)
def test_heatmap_draws_every_cell(func, corr_matrix):
    ax = func(corr_matrix)

    np.testing.assert_allclose(np.asarray(_artist(ax).get_array()), corr_matrix.values)


@pytest.mark.parametrize("func", HEATMAP)
def test_heatmap_scale_is_fixed_to_minus_one_one(func, corr_matrix):
    assert _artist(func(corr_matrix)).get_clim() == (-1, 1)


@pytest.mark.parametrize("func", HEATMAP)
def test_heatmap_labels_and_values(func, corr_matrix):
    ax = func(corr_matrix)

    assert [t.get_text() for t in ax.get_xticklabels()] == list("abc")
    assert [t.get_text() for t in ax.get_yticklabels()] == list("abc")
    assert [t.get_text() for t in ax.texts] == [
        "1.00",
        "0.50",
        "-0.20",
        "0.50",
        "1.00",
        "0.30",
        "-0.20",
        "0.30",
        "1.00",
    ]


@pytest.mark.parametrize("func", HEATMAP)
def test_heatmap_has_colorbar(func, corr_matrix):
    assert len(func(corr_matrix).figure.axes) == 2  # axe principal + barre de couleurs


@pytest.mark.parametrize("func", HEATMAP)
@pytest.mark.parametrize("bad", [pd.DataFrame(), pd.DataFrame([[1, 2, 3], [4, 5, 6]])])
def test_heatmap_rejects_non_square_without_orphan_figure(func, bad):
    with pytest.raises(ValueError, match="carrée"):
        func(bad)

    assert plt.get_fignums() == []


# Test sauvegarde des figures


@pytest.fixture(name="fig")
def fixture_fig():
    return plt.figure(figsize=(2, 1))


def test_save_figure_writes_a_valid_png(fig, tmp_path):
    target = tmp_path / "a.png"

    result = save_figure(fig, target, dpi=100)

    assert result == target
    assert target.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_save_figure_respects_dpi(fig, tmp_path):
    save_figure(fig, tmp_path / "a.png", dpi=100)

    assert plt.imread(tmp_path / "a.png").shape[:2] == (100, 200)  # hauteur, largeur


def test_save_figure_creates_missing_folders(fig, tmp_path):
    target = tmp_path / "reports" / "figures" / "a.png"

    save_figure(fig, target)

    assert target.exists()


def test_save_figure_overwrites_existing_file(fig, tmp_path):
    target = tmp_path / "a.png"

    save_figure(fig, target)
    save_figure(fig, target)  # ne doit pas lever d'erreur

    assert target.exists()


@pytest.mark.parametrize("name", ["no_extension", "figure.xyz"])
def test_save_figure_rejects_unknown_format_without_side_effect(fig, tmp_path, name):
    target = tmp_path / "new_folder" / name

    with pytest.raises(ValueError, match="non supporté"):
        save_figure(fig, target)

    assert not target.parent.exists()  # aucun dossier créé malgré l'erreur
