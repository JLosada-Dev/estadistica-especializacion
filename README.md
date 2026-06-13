# estadistica

Proyecto de análisis de datos y estadística usando Python, gestionado con [uv](https://docs.astral.sh/uv/) y trabajado en Jupyter Notebook desde Visual Studio Code.

## Requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/) >= 0.4
- Python 3.12 (uv lo instalará automáticamente si no lo tienes)
- Visual Studio Code con las extensiones:
  - **Python** (Microsoft)
  - **Jupyter** (Microsoft)

## Setup

Clona el repo y desde la raíz del proyecto:

```bash
uv sync
```

Esto crea el entorno virtual `.venv` e instala todas las dependencias (producción y desarrollo) definidas en `pyproject.toml`.

## Usar el notebook en VS Code

1. Abre la carpeta del proyecto en VS Code.
2. Abre cualquier archivo `.ipynb` dentro de `notebooks/`.
3. En la esquina superior derecha del notebook, en **"Select Kernel"**, elige el intérprete `.venv/bin/python` del proyecto.
4. Ejecuta las celdas con `Shift + Enter`.

## Estructura del proyecto

```
estadistica/
├── data/
│   ├── raw/           # Datos originales sin modificar (no se versionan)
│   ├── interim/       # Datos en transformación
│   ├── processed/     # Datos finales listos para análisis
│   └── external/      # Fuentes externas
├── notebooks/         # Notebooks de exploración y análisis
├── src/
│   └── estadistica/   # Código reutilizable (funciones, módulos)
├── reports/
│   └── figures/       # Gráficos generados
├── references/        # Diccionarios de datos, manuales, papers
├── pyproject.toml     # Dependencias y configuración del proyecto
├── uv.lock            # Lockfile reproducible
└── .gitignore
```

## Comandos útiles

```bash
# Instalar/sincronizar dependencias
uv sync

# Agregar una nueva librería
uv add nombre-libreria

# Agregar una librería solo de desarrollo
uv add --dev nombre-libreria

# Correr un script con el entorno
uv run python src/estadistica/script.py

# Abrir JupyterLab (opcional, si no usas VS Code)
uv run jupyter lab

# Formatear / linter
uv run ruff check .
uv run ruff format .
```

## Convenciones para notebooks

- Numerar los notebooks por orden: `01-exploracion.ipynb`, `02-limpieza.ipynb`, etc.
- No commitear datos crudos pesados (ya están en `.gitignore`).
- Mover funciones reutilizables a `src/estadistica/` y llamarlas desde el notebook.
