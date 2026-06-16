"""Carga de datasets."""

from pathlib import Path

import pandas as pd

from estadistica.paths import RAW_DIR

TITANIC_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
DIABETES_URL = "https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt"


def load_titanic(path: Path | None = None) -> pd.DataFrame:
    """Carga el dataset Titanic desde local con fallback a la URL pública.

    Args:
        path: Ruta opcional al CSV. Si no se da, usa `data/raw/titanic.csv`.
    """
    path = path or RAW_DIR / "titanic.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.read_csv(TITANIC_URL)


def load_diabetes(path: Path | None = None) -> pd.DataFrame:
    """Carga el dataset Diabetes (Efron et al., 2004) separado por tabs.

    442 pacientes × 10 features clínicas + target `Y` (progresión a 1 año).

    Args:
        path: Ruta opcional al archivo. Si no se da, usa `data/raw/diabetes.tab.txt`.
    """
    path = path or RAW_DIR / "diabetes.tab.txt"
    if path.exists():
        return pd.read_csv(path, sep="\t")
    return pd.read_csv(DIABETES_URL, sep="\t")
