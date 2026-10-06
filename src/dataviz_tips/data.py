"""Module de gestion des données pour le dataset des pourboires."""

import pandas as pd
import seaborn as sns


def drop_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne un nouveau DataFrame sans lignes dupliquées.

    L'index est réinitialisé de 0 à n - 1.

    :param df: Le DataFrame à nettoyer.
    :type df: pd.DataFrame
    :returns: Le DataFrame sans lignes dupliquées.
    :rtype: pd.DataFrame
    """
    return df.drop_duplicates().reset_index(drop=True)


def load_tips() -> pd.DataFrame:
    """
    Charge le dataset des pourboires, dédoublonné.

    :returns: Le dataset des pourboires propre.
    :rtype: pd.DataFrame
    """
    return drop_duplicate_rows(sns.load_dataset("tips"))
