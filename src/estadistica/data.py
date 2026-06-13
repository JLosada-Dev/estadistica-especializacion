"""Carga de datasets."""

from pathlib import Path

import pandas as pd

from estadistica.paths import RAW_DIR

TITANIC_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"


def load_titanic(path: Path | None = None) -> pd.DataFrame:
    """Carga el dataset Titanic desde local con fallback a la URL pública.

    Args:
        path: Ruta opcional al CSV. Si no se da, usa `data/raw/titanic.csv`.
    """
    path = path or RAW_DIR / "titanic.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.read_csv(TITANIC_URL)
