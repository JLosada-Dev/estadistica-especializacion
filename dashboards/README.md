# Dashboards

Aplicaciones interactivas de Streamlit. Cada análisis vive en su propia carpeta y
es **independiente**: construir o modificar uno no afecta a los demás.

## Estructura

```
dashboards/
├── _shared/            # tema y componentes visuales comunes a todos
│   ├── tema.py         # CSS, paleta light, logo
│   └── componentes.py  # encabezado de sección, estilo de gráficos, íconos SVG
└── retail/             # dashboard del análisis de retail (Taller 4)
    ├── app.py          # punto de entrada y navegación
    ├── datos.py        # capa de caché (envuelve estadistica.retail)
    └── secciones.py    # las pantallas
```

La **lógica de análisis** (limpieza, RFM, clustering, reglas) no vive aquí, sino en
`src/estadistica/` (por ejemplo `estadistica.retail`), para que la compartan los
notebooks y los dashboards sin duplicarla.

## Cómo ejecutar (local)

Desde la raíz del proyecto:

```bash
uv run streamlit run dashboards/retail/app.py
```

Se abre en `http://localhost:8501`. La primera carga tarda unos segundos (lee el
dataset y lo limpia); después todo es instantáneo gracias al caché.

## Cómo agregar un dashboard nuevo

1. Crear una carpeta `dashboards/mi_analisis/` con `app.py`, `datos.py` y `secciones.py`.
2. Poner la lógica de análisis reutilizable en `src/estadistica/` (no en el dashboard).
3. Reusar el tema y los componentes con `from _shared import tema, componentes`.
4. Copiar el bloque de *bootstrap de rutas* del `app.py` de retail (hace importable
   `estadistica` y `_shared`).

No hay que tocar ningún otro dashboard.

## Desplegar en Streamlit Community Cloud

1. Subir el repo a GitHub.
2. En share.streamlit.io, crear una app apuntando al archivo principal, por ejemplo
   `dashboards/retail/app.py`. Para un segundo dashboard, se crea otra app apuntando
   a `dashboards/mi_analisis/app.py`. Cada una tiene su propia URL.
3. Las dependencias se leen de `requirements.txt` (en la raíz del repo).
4. Los datos pesados no se versionan: `estadistica.load_retail()` los descarga desde
   su URL pública la primera vez.
