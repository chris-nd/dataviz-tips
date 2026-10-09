"Module de configuration pour le backend matplotlib"

import matplotlib
import matplotlib.pyplot as plt
import pytest

matplotlib.use("Agg")  # backend sans fenêtre, chargé avant tous les tests


@pytest.fixture(autouse=True)
def close_figures():
    "Ferme toutes les figures après chaque test."
    yield
    plt.close("all")
