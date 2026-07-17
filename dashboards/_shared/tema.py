"""Tema visual compartido por todos los dashboards (paleta light y elegante)."""

import streamlit as st

LOGO_BARRAS = """
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3B6FB6"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 21h18"/>
  <rect x="5" y="11" width="3.2" height="7" rx="1" fill="#3B6FB6" stroke="none"/>
  <rect x="10.4" y="6.5" width="3.2" height="11.5" rx="1" fill="#6FA0DA" stroke="none"/>
  <rect x="15.8" y="13.5" width="3.2" height="4.5" rx="1" fill="#A9C6EC" stroke="none"/>
</svg>
"""

_CSS = """
<style>
  .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1320px; }
  header[data-testid="stHeader"] { background: transparent; }

  .sec-header {
    display: flex; align-items: center; gap: 16px;
    margin: 0.1rem 0 1.5rem 0; padding-bottom: 1.1rem;
    border-bottom: 1px solid #EAEDF2;
  }
  .sec-icon {
    width: 48px; height: 48px; border-radius: 13px; flex: none;
    display: flex; align-items: center; justify-content: center;
  }
  .sec-title { font-size: 1.55rem; font-weight: 700; color: #1E2A3A; line-height: 1.15; }
  .sec-desc  { color: #6B7280; font-size: 0.93rem; margin-top: 2px; }

  div[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #E6EAF1; border-radius: 14px;
    padding: 16px 18px; box-shadow: 0 1px 2px rgba(16,24,40,0.04);
  }
  div[data-testid="stMetricLabel"] p { color: #6B7280; font-size: 0.8rem; }

  section[data-testid="stSidebar"] { background: #F7F9FC; border-right: 1px solid #EAEDF2; }
  .logo-wrap { display: flex; align-items: center; gap: 12px; padding: 4px 0 2px 0; }
  .logo-title { font-size: 1.15rem; font-weight: 700; color: #1E2A3A; line-height: 1.1; }
  .logo-sub { font-size: 0.78rem; color: #8A93A2; }
  .guia-box {
    background: #FFFFFF; border: 1px solid #E6EAF1; border-radius: 12px;
    padding: 12px 14px; font-size: 0.85rem; color: #465061;
  }
  .guia-box b { color: #3B6FB6; }
</style>
"""


def aplicar() -> None:
    """Inyecta el CSS del tema. Llamar una vez al inicio de cada app."""
    st.markdown(_CSS, unsafe_allow_html=True)


def logo(titulo: str, subtitulo: str) -> None:
    st.markdown(
        f'<div class="logo-wrap">{LOGO_BARRAS}'
        f'<div><div class="logo-title">{titulo}</div>'
        f'<div class="logo-sub">{subtitulo}</div></div></div>',
        unsafe_allow_html=True,
    )
