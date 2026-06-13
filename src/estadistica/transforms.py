"""Transformaciones genéricas sobre DataFrames.

NO dependen del dominio (titanic, clientes, ventas, etc.).
Operan sobre cualquier DataFrame que tenga las columnas indicadas.

Estas son las funciones candidatas a moverse a una librería compartida
si las necesitás en otros proyectos.
"""

from collections.abc import Iterable

import pandas as pd


def imputar_mediana(df: pd.DataFrame, columnas: Iterable[str]) -> pd.DataFrame:
    """Rellena NaN de columnas numéricas con su mediana."""
    df = df.copy()
    for col in columnas:
        df[col] = df[col].fillna(df[col].median())
    return df


def imputar_moda(df: pd.DataFrame, columnas: Iterable[str]) -> pd.DataFrame:
    """Rellena NaN de columnas categóricas con su moda."""
    df = df.copy()
    for col in columnas:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df


def detectar_outliers_iqr(df: pd.DataFrame, columna: str, k: float = 1.5) -> pd.Series:
    """Devuelve una máscara booleana marcando outliers según el método IQR."""
    q1, q3 = df[columna].quantile([0.25, 0.75])
    iqr = q3 - q1
    return (df[columna] < q1 - k * iqr) | (df[columna] > q3 + k * iqr)


def reporte_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen de valores nulos por columna."""
    nulos = df.isna().sum()
    return pd.DataFrame(
        {
            "nulos": nulos,
            "pct": (nulos / len(df) * 100).round(2),
            "dtype": df.dtypes.astype(str),
        }
    ).sort_values("nulos", ascending=False)
