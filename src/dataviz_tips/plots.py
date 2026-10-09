"Module de tracé pour les visualisations de données"

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# Fonctions utilitaires


def _get_axes(ax: Axes | None) -> Axes:
    """
    Retourne `ax`, ou crée explicitement une nouvelle figure si `ax` est None.

    :param ax: Axe matplotlib
    :type ax: Axes | None
    :return: Axe matplotlib
    :rtype: Axes
    """

    if ax is None:
        _, ax = plt.subplots()
    return ax


def _set_labels(ax: Axes, title: str, xlabel: str, ylabel: str) -> None:
    """
    Applique le titre et les libellés d'axes.

    :param ax: Axe sur lequel appliquer les labels
    :type ax: Axes
    :param title: Titre du graphique
    :type title: str
    :param xlabel: Libellé de l'axe des abscisses
    :type xlabel: str
    :param ylabel: Libellé de l'axe des ordonnées
    :type ylabel: str
    """

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def _check_column(df: pd.DataFrame, *columns: str) -> None:
    """
    Lève un KeyError explicite si la colonne n'existe pas.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param column: Nom(s) de la colonne à vérifier
    :type column: str
    :raise KeyError: Si la colonne n'existe pas
    """

    for col in columns:
        if col not in df.columns:
            raise KeyError(f"La colonne '{col}' n'existe pas dans le DataFrame.")


def _valid_rows(df: pd.DataFrame, *columns: str) -> pd.DataFrame:
    """
    Lignes sans NaN dans les colonnes données : même comportement mpl et sns.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param columns: Noms des colonnes à vérifier
    :type columns: str
    :return: DataFrame avec les lignes valides
    :rtype: pd.DataFrame
    """
    return df[list(columns)].dropna()


# Histogram


def plot_histogram_mpl(
    df: pd.DataFrame, column: str, *, bins: int = 30, ax: Axes | None = None
) -> Axes:
    """
    Trace un histogramme avec matplotlib.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param column: Nom de la colonne à tracer
    :type column: str
    :param ax: Axe matplotlib sur lequel tracer l'histogramme
    :type ax: Axes | None
    :param bins: Nombre de bins pour l'histogramme
    :type bins: int
    :raise KeyError: Si la colonne n'existe pas
    :return: Axe matplotlib
    :rtype: Axes
    """

    _check_column(df, column)
    ax = _get_axes(ax)
    ax.hist(df[column], bins=bins)
    _set_labels(ax, f"Histogramme de {column}", column, "Fréquence")
    return ax


def plot_histogram_sns(
    df: pd.DataFrame, column: str, *, bins: int = 30, ax: Axes | None = None
) -> Axes:
    """
    Trace un histogramme avec seaborn.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param column: Nom de la colonne à tracer
    :type column: str
    :param ax: Axe seaborn sur lequel tracer l'histogramme
    :type ax: Axes | None
    :param bins: Nombre de bins pour l'histogramme
    :type bins: int | None
    :raise KeyError: Si la colonne n'existe pas
    :return: Axe Matplotlib
    :rtype: Axes
    """

    _check_column(df, column)
    ax = _get_axes(ax)
    sns.histplot(data=df, x=column, bins=bins, ax=ax)
    _set_labels(ax, f"Histogramme de {column}", column, "Fréquence")
    return ax


# Bar


def plot_size_counts_mpl(
    df: pd.DataFrame, column: str, *, ax: Axes | None = None
) -> Axes:
    """
    Trace un graphique de comptage des tailles avec matplotlib.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param column: Nom de la colonne à tracer
    :type column: str
    :param ax: Axe matplotlib sur lequel tracer le graphique
    :type ax: Axes | None
    :return: Axe matplotlib
    :rtype: Axes
    """

    _check_column(df, column)
    ax = _get_axes(ax)
    counts = df[column].value_counts().sort_index()
    ax.bar(counts.index, counts.values)
    _set_labels(ax, f"Comptage des groupes de {column}", column, "Nombre")
    return ax


def plot_size_counts_sns(
    df: pd.DataFrame, column: str, *, ax: Axes | None = None
) -> Axes:
    """
    Trace un graphique de comptage des tailles avec seaborn.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param column: Nom de la colonne à tracer
    :type column: str
    :param ax: Axe seaborn sur lequel tracer le graphique
    :type ax: Axes | None
    :return: Axe seaborn
    :rtype: Axes
    """

    _check_column(df, column)
    ax = _get_axes(ax)
    counts = df[column].value_counts().sort_index()
    sns.countplot(data=df, x=column, order=counts.index, ax=ax)
    _set_labels(ax, f"Comptage des tailles de {column}", column, "Nombre")
    return ax


# Box Plot


def plot_boxplot_mpl(df: pd.DataFrame, column: str, *, ax: Axes | None = None) -> Axes:
    """
    Trace un box plot avec matplotlib.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param column: Nom de la colonne à tracer
    :type column: str
    :param ax: Axe matplotlib sur lequel tracer le box plot
    :type ax: Axes | None
    :return: Axe matplotlib
    :rtype: Axes
    """

    _check_column(df, column)
    ax = _get_axes(ax)
    ax.boxplot(_valid_rows(df, column)[column])
    _set_labels(ax, f"Boîte à moustaches de {column}", "", column)
    return ax


def plot_boxplot_sns(df: pd.DataFrame, column: str, *, ax: Axes | None = None) -> Axes:
    """
    Trace un box plot avec seaborn.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param column: Nom de la colonne à tracer
    :type column: str
    :param ax: Axe seaborn sur lequel tracer le box plot
    :type ax: Axes | None
    :return: Axe seaborn
    :rtype: Axes
    """

    _check_column(df, column)
    ax = _get_axes(ax)
    sns.boxplot(data=_valid_rows(df, column), y=column, ax=ax)
    _set_labels(ax, f"Boîte à moustaches de {column}", "", column)
    return ax


# Scatter


def plot_scatter_mpl(
    df: pd.DataFrame, x: str, y: str, *, ax: Axes | None = None
) -> Axes:
    """
    Trace un graphique de dispersion avec matplotlib.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param x: Nom de la colonne à tracer sur l'axe des x
    :type x: str
    :param y: Nom de la colonne à tracer sur l'axe des y
    :type y: str
    :param ax: Axe matplotlib sur lequel tracer le graphique
    :type ax: Axes | None
    :return: Axe matplotlib
    :rtype: Axes
    """

    _check_column(df, x, y)
    ax = _get_axes(ax)
    data = _valid_rows(df, x, y)
    ax.scatter(data[x], data[y])
    _set_labels(ax, f"Graphique de dispersion de {x} vs {y}", x, y)
    return ax


def plot_scatter_sns(
    df: pd.DataFrame, x: str, y: str, *, ax: Axes | None = None
) -> Axes:
    """
    Trace un graphique de dispersion avec seaborn.

    :param df: DataFrame contenant les données
    :type df: pd.DataFrame
    :param x: Nom de la colonne à tracer sur l'axe des x
    :type x: str
    :param y: Nom de la colonne à tracer sur l'axe des y
    :type y: str
    :param ax: Axe seaborn sur lequel tracer le graphique
    :type ax: Axes | None
    :return: Axe seaborn
    :rtype: Axes
    """

    _check_column(df, x, y)
    ax = _get_axes(ax)
    data = _valid_rows(df, x, y)
    sns.scatterplot(data=data, x=x, y=y, ax=ax)
    _set_labels(ax, f"{y} en fonction de {x}", x, y)
    return ax


# Heatmap


def _check_corr_matrix(corr_matrix: pd.DataFrame) -> None:
    """
    Vérifie que la matrice de corrélation est valide.

    :param corr_matrix: Matrice de corrélation
    :type corr_matrix: pd.DataFrame
    :raises ValueError: Si la matrice n'est pas carrée ou est vide.
    """

    if corr_matrix.empty or corr_matrix.shape[0] != corr_matrix.shape[1]:
        raise ValueError("La matrice de corrélation doit être carrée et non vide.")


def plot_correlation_heatmap_mpl(corr_matrix, *, ax=None):
    """
    Trace une carte thermique de corrélation avec matplotlib.

    :param corr_matrix: Matrice de corrélation
    :type corr_matrix: pd.DataFrame
    :param ax: Axe matplotlib sur lequel tracer le graphique
    :type ax: Axes | None
    :return: Axe matplotlib
    :rtype: Axes
    """

    _check_corr_matrix(corr_matrix)  # valider avant de créer la figure
    ax = _get_axes(ax)
    image = ax.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(corr_matrix.shape[1]), labels=list(corr_matrix.columns))
    ax.set_yticks(range(corr_matrix.shape[0]), labels=list(corr_matrix.index))
    for i in range(corr_matrix.shape[0]):
        for j in range(corr_matrix.shape[1]):
            ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha="center", va="center")
    ax.figure.colorbar(image, ax=ax)
    _set_labels(ax, "Carte thermique de corrélation", "", "")
    return ax


def plot_correlation_heatmap_sns(corr_matrix, *, ax=None):
    """
    Trace une carte thermique de corrélation avec seaborn.

    :param corr_matrix: Matrice de corrélation
    :type corr_matrix: pd.DataFrame
    :param ax: Axe seaborn sur lequel tracer le graphique
    :type ax: Axes | None
    :return: Axe seaborn
    :rtype: Axes
    """

    _check_corr_matrix(corr_matrix)
    ax = _get_axes(ax)
    sns.heatmap(
        corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax
    )
    _set_labels(ax, "Carte thermique de corrélation", "", "")
    return ax


# Sauvegarde des figures


def save_figure(fig: Figure, path: str | Path, *, dpi: int = 300) -> Path:
    """
    Exporte une figure et retourne le chemin du fichier écrit.

    Les dossiers manquants sont créés, un fichier existant est écrasé.

    :param fig: Figure à exporter
    :type fig: Figure
    :param path: Chemin du fichier à créer
    :type path: str | Path
    :param dpi: Résolution de la figure exportée
    :type dpi: int
    :raises ValueError: Si l'extension est absente ou non supportée.
    :return: Chemin du fichier créé
    :rtype: Path
    """

    path = Path(path)
    extension = path.suffix.lstrip(".").lower()
    supported = fig.canvas.get_supported_filetypes()
    if extension not in supported:
        raise ValueError(
            f"Format '{path.suffix}' non supporté. "
            f"Formats disponibles : {', '.join(sorted(supported))}"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi)

    return path
