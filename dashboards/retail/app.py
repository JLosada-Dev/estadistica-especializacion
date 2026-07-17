"""Dashboard interactivo del análisis de retail.

Ejecutar desde la raíz del proyecto con:
    uv run streamlit run dashboards/retail/app.py
"""

# --- Bootstrap de rutas: hace importable `estadistica` (src/) y `_shared`
# tanto en local como en Streamlit Cloud, sin depender de la instalación. ---
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
for ruta in (RAIZ / "src", RAIZ / "dashboards"):
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))

import streamlit as st  # noqa: E402

from _shared import tema  # noqa: E402

st.set_page_config(
    page_title="Retail · Dashboard de análisis",
    layout="wide",
    initial_sidebar_state="expanded",
)
tema.aplicar()

import secciones  # noqa: E402

SECCIONES = {
    "Resumen": secciones.resumen,
    "Segmentación de clientes": secciones.segmentacion,
    "Valor del cliente": secciones.valor,
    "Fuga de clientes": secciones.churn,
    "Mercados internacionales": secciones.regional,
    "Lealtad (NPS)": secciones.lealtad,
    "Pronóstico de ventas": secciones.pronostico,
    "Nicho mayorista": secciones.nicho,
    "Recomendaciones": secciones.asociacion,
    "Simulador": secciones.simulador,
}

with st.sidebar:
    tema.logo("Análisis de retail", "Reino Unido · 2010-2011")
    st.write("")
    eleccion = st.radio("Secciones", list(SECCIONES.keys()), label_visibility="collapsed")
    st.write("")
    st.markdown(
        '<div class="guia-box"><b>Pregunta guía</b><br>'
        "¿Quiénes son los mejores clientes y qué productos conviene "
        "recomendar o promocionar juntos para vender más?</div>",
        unsafe_allow_html=True,
    )

SECCIONES[eleccion]()
