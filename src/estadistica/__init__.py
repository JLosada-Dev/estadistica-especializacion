__version__ = "0.1.0"

from estadistica.data import load_titanic
from estadistica.paths import PROJECT_ROOT, RAW_DIR

__all__ = ["PROJECT_ROOT", "RAW_DIR", "__version__", "load_titanic"]
