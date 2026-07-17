"""Componentes visuales reutilizables por todos los dashboards."""

import plotly.io as pio
import streamlit as st

pio.templates.default = "plotly_white"

# Íconos SVG por tipo de sección (stroke = currentColor para tomar el acento)
SVG = {
    "resumen": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/>
        <rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>""",
    "segmentacion": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="8" cy="9" r="3"/><circle cx="17" cy="10" r="2.3"/>
        <path d="M3 19c0-2.8 2.2-4.5 5-4.5s5 1.7 5 4.5"/><path d="M15 18.5c0-2 1.3-3.2 3-3.2"/></svg>""",
    "nicho": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2.5 14.7 8.6 21 9.2 16.2 13.5 17.8 20 12 16.6 6.2 20 7.8 13.5 3 9.2 9.3 8.6"/></svg>""",
    "recomendaciones": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.5 12.5l-8 8L3 11V3.5h7.5z"/><circle cx="7.5" cy="7.5" r="1.4"/></svg>""",
    "simulador": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/>
        <circle cx="9" cy="7" r="2.3" fill="white"/><circle cx="15" cy="12" r="2.3" fill="white"/>
        <circle cx="8" cy="17" r="2.3" fill="white"/></svg>""",
    "generico": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/></svg>""",
    "valor": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 17l6-6 4 4 7-7"/><path d="M14 7h7v7"/></svg>""",
    "churn": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/></svg>""",
    "regional": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>
        <path d="M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18"/></svg>""",
    "nps": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M7 10v11"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a2.5 2.5 0 0 1 3 3z"/></svg>""",
    "pronostico": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 3v18h18"/><path d="M7 14l3-3 3 3 5-6"/><path d="M18 8h2v2"/></svg>""",
}
COLOR = {
    "resumen": "#3B6FB6",
    "segmentacion": "#2E7D55",
    "nicho": "#B7791F",
    "recomendaciones": "#6D4AA6",
    "simulador": "#0E7C86",
    "valor": "#4338CA",
    "churn": "#B91C1C",
    "regional": "#0E7C86",
    "nps": "#BE185D",
    "pronostico": "#7C3AED",
    "generico": "#3B6FB6",
}


def encabezado(clave: str, titulo: str, descripcion: str) -> None:
    """Header de sección con ícono SVG y color de acento."""
    color = COLOR.get(clave, COLOR["generico"])
    svg = SVG.get(clave, SVG["generico"])
    st.markdown(
        f'<div class="sec-header">'
        f'<div class="sec-icon" style="background:{color}1A; color:{color};">{svg}</div>'
        f'<div><div class="sec-title">{titulo}</div>'
        f'<div class="sec-desc">{descripcion}</div></div></div>',
        unsafe_allow_html=True,
    )


def fig(figura, height: int = 360):
    """Aplica un layout consistente a un gráfico de Plotly."""
    figura.update_layout(
        height=height, margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="sans-serif", size=12, color="#1E2A3A"),
    )
    return figura
