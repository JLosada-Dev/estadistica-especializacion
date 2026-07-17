"""Capa de caché del dashboard de retail.

Envuelve la lógica pura de `estadistica.retail` con `st.cache_data`, de modo que
cada cálculo pesado se hace una sola vez por sesión.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from estadistica import load_retail, retail

ORDEN_SEGMENTOS = retail.ORDEN_SEGMENTOS
COLORES_SEGMENTO = retail.COLORES_SEGMENTO


@st.cache_data(show_spinner="Cargando y limpiando los datos…")
def cargar_datos() -> pd.DataFrame:
    return retail.limpiar(load_retail())


@st.cache_data(show_spinner=False)
def datos_cliente() -> pd.DataFrame:
    return retail.solo_clientes(cargar_datos())


@st.cache_data(show_spinner=False)
def datos_global() -> pd.DataFrame:
    return retail.limpiar(load_retail(), solo_uk=False)


@st.cache_data(show_spinner=False)
def metricas_pais() -> pd.DataFrame:
    return retail.metricas_pais(datos_global())


@st.cache_data(show_spinner=False)
def perfil_pais(pais: str):
    return retail.perfil_pais(datos_global(), pais)


@st.cache_data(show_spinner=False)
def calcular_rfm() -> pd.DataFrame:
    return retail.calcular_rfm(datos_cliente())


@st.cache_data(show_spinner=False)
def segmentar(k: int) -> pd.DataFrame:
    return retail.segmentar(calcular_rfm(), k)


@st.cache_data(show_spinner=False)
def silueta_por_k() -> pd.DataFrame:
    return retail.silueta_por_k(calcular_rfm())


@st.cache_data(show_spinner=False)
def clientes_mayoristas(umbral: int):
    return retail.clientes_mayoristas(datos_cliente(), umbral)


@st.cache_data(show_spinner=False)
def nps_simulado(semilla: int = 42):
    rfm = retail.segmentar(calcular_rfm(), 4)
    return retail.nps_simulado(rfm, semilla)


@st.cache_data(show_spinner=False)
def serie_semanal():
    return retail.serie_semanal(cargar_datos())


@st.cache_data(show_spinner="Simulando escenarios…")
def pronostico(horizonte: int, n_sim: int):
    return retail.pronostico_montecarlo(serie_semanal(), horizonte, n_sim)


@st.cache_data(show_spinner="Entrenando el modelo de valor…")
def modelo_valor(fecha_corte: str):
    feat = retail.dataset_valor_futuro(datos_cliente(), fecha_corte)
    return feat, retail.modelo_valor_futuro(feat)


@st.cache_data(show_spinner="Entrenando el modelo de fuga…")
def modelo_churn(fecha_corte: str):
    feat = retail.dataset_valor_futuro(datos_cliente(), fecha_corte)
    return retail.modelo_churn(feat)


@st.cache_data(show_spinner="Calculando combinaciones de productos…")
def reglas_asociacion(min_support: float) -> pd.DataFrame:
    return retail.reglas_asociacion(cargar_datos(), min_support)


@st.cache_data(show_spinner=False)
def stats_productos() -> pd.DataFrame:
    return retail.stats_productos(cargar_datos())


@st.cache_data(show_spinner=False)
def matriz_lift(n_top: int):
    return retail.matriz_lift_top(cargar_datos(), n_top)


@st.cache_data(show_spinner=False)
def paquetes_tematicos(n_top: int, n_temas: int):
    return retail.paquetes_tematicos(matriz_lift(n_top), n_temas)


@st.cache_data(show_spinner=False)
def n_facturas() -> int:
    return cargar_datos()["InvoiceNo"].nunique()
