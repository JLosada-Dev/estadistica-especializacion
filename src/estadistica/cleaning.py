"""Limpieza ESPECÍFICA del dataset Titanic.

Esto NO se reutiliza en otros proyectos — vive acá porque conoce las columnas
de este dataset (deck, alive, class, embark_town, ...).

Se apoya en `transforms.py` para las operaciones genéricas.
"""

import pandas as pd

from estadistica.transforms import imputar_mediana, imputar_moda

COLUMNAS_REDUNDANTES = ["alive", "class", "embark_town"]
COLUMNAS_DERIVADAS = ["adult_male", "who", "alone"]
COLUMNAS_DEMASIADOS_NULOS = ["deck"]


def limpiar_titanic(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline de limpieza del Titanic.

    Decisiones específicas de este dataset:
    - `age` se imputa con mediana (sesgo por outliers).
    - `embarked` se imputa con moda (solo 2 nulos).
    - `deck` se elimina (688 nulos de 891).
    - Se eliminan columnas redundantes y derivadas (`alive`, `class`, etc.).
    """
    return (
        df.pipe(imputar_mediana, columnas=["age"])
        .pipe(imputar_moda, columnas=["embarked"])
        .drop(
            columns=[
                *COLUMNAS_DEMASIADOS_NULOS,
                *COLUMNAS_REDUNDANTES,
                *COLUMNAS_DERIVADAS,
            ]
        )
    )
