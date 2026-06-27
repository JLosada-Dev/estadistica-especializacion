"""Carga de datasets."""

from pathlib import Path

import pandas as pd

from estadistica.paths import EXTERNAL_DIR, RAW_DIR

TITANIC_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
DIABETES_URL = "https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt"
RETAIL_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"


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


def load_retail(path: Path | None = None, cache: bool = True) -> pd.DataFrame:
    """Carga el dataset Online Retail (UCI) con fallback a la URL pública.

    ~541k transacciones de un retailer online del Reino Unido (2010-2011).
    El archivo (~23 MB) NO se versiona en git: si no existe localmente se
    descarga desde UCI y, por defecto, se cachea en `data/external/`.

    Args:
        path: Ruta opcional al .xlsx. Si no se da, usa
            `data/external/Online_Retail.xlsx`.
        cache: Si descarga desde la URL, guarda una copia local para que
            las siguientes cargas sean rápidas.
    """
    path = path or EXTERNAL_DIR / "Online_Retail.xlsx"
    if path.exists():
        return pd.read_excel(path)

    df = pd.read_excel(RETAIL_URL)
    if cache:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(path, index=False)
    return df
