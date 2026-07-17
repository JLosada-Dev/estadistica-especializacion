"""Lógica de análisis del dataset de retail, reutilizable por notebooks y dashboards.

Son funciones puras (pandas / sklearn / mlxtend), sin dependencia de Streamlit.
La capa de caché vive en el dashboard; aquí solo está la lógica.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ORDEN_SEGMENTOS = ["Campeones", "Leales", "Ocasionales", "En riesgo"]
COLORES_SEGMENTO = {
    "Campeones": "#2E7D32",
    "Leales": "#378ADD",
    "Ocasionales": "#F9A825",
    "En riesgo": "#E24B4A",
}

# Variables sobre las que se segmenta (RFM enriquecido).
# Antiguedad, TicketMedio y Diversidad agregan comportamiento más allá del RFM básico.
VARIABLES_SEGMENTACION = [
    "Recencia", "Frecuencia", "Monetario", "Antiguedad", "Diversidad", "TicketMedio",
]


# --------------------------------------------------------------------------- #
# Limpieza
# --------------------------------------------------------------------------- #
def limpiar(df: pd.DataFrame, solo_uk: bool = True) -> pd.DataFrame:
    """Aplica la limpieza del Taller 4: ventas reales, productos válidos.

    Por defecto se queda solo con el Reino Unido (el análisis principal). Con
    `solo_uk=False` conserva todos los países, para el análisis regional.
    """
    df = df.copy()
    if solo_uk:
        df = df[df["Country"] == "United Kingdom"]
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df = df.drop_duplicates()
    df = df[~df["InvoiceNo"].str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df = df.dropna(subset=["Description"])
    df = df[df["StockCode"].astype(str).str.match(r"^\d{5}")]
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["Mes"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    return df


def solo_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """Subconjunto con cliente identificado, para la segmentación."""
    dc = df.dropna(subset=["CustomerID"]).copy()
    dc["CustomerID"] = dc["CustomerID"].astype(int)
    return dc


# --------------------------------------------------------------------------- #
# RFM y segmentación
# --------------------------------------------------------------------------- #
def calcular_rfm(dc: pd.DataFrame) -> pd.DataFrame:
    """RFM enriquecido por cliente.

    Además del RFM básico (recencia, frecuencia, monto) agrega tres variables
    de comportamiento: antigüedad (días desde la primera compra), diversidad
    (productos distintos) y ticket medio (gasto por factura).
    """
    ref = dc["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = dc.groupby("CustomerID").agg(
        Recencia=("InvoiceDate", lambda x: (ref - x.max()).days),
        Frecuencia=("InvoiceNo", "nunique"),
        Monetario=("TotalPrice", "sum"),
        Antiguedad=("InvoiceDate", lambda x: (ref - x.min()).days),
        Diversidad=("Description", "nunique"),
    ).reset_index()
    ticket = (dc.groupby(["CustomerID", "InvoiceNo"])["TotalPrice"].sum()
              .groupby("CustomerID").mean())
    rfm["TicketMedio"] = rfm["CustomerID"].map(ticket)
    return rfm


def _nombrar_segmentos(perfil: pd.DataFrame) -> dict:
    nombres: dict = {}
    nombres[perfil["Monetario"].idxmax()] = "Campeones"
    nombres[perfil["Recencia"].idxmax()] = "En riesgo"
    restantes = [g for g in perfil.index if g not in nombres]
    restantes = perfil.loc[restantes].sort_values("Monetario", ascending=False).index.tolist()
    for g, etq in zip(restantes, ["Leales", "Ocasionales", "Grupo 5", "Grupo 6"]):
        nombres[g] = etq
    return nombres


def segmentar(rfm: pd.DataFrame, k: int) -> pd.DataFrame:
    """Agrupa los clientes en k segmentos y proyecta a 2D con PCA (para graficar)."""
    rfm = rfm.copy()
    X = np.log1p(rfm[VARIABLES_SEGMENTACION])
    X_esc = StandardScaler().fit_transform(X)

    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_esc)
    rfm["grupo"] = km.labels_

    perfil = rfm.groupby("grupo").agg(
        Recencia=("Recencia", "mean"),
        Frecuencia=("Frecuencia", "mean"),
        Monetario=("Monetario", "mean"),
    )
    rfm["Segmento"] = rfm["grupo"].map(_nombrar_segmentos(perfil))

    pca = PCA(n_components=2).fit(X_esc)
    coords = pca.transform(X_esc)
    rfm["pca1"], rfm["pca2"] = coords[:, 0], coords[:, 1]
    rfm.attrs["pca_varianza"] = float(pca.explained_variance_ratio_.sum() * 100)
    return rfm


def silueta_por_k(rfm: pd.DataFrame, k_min: int = 2, k_max: int = 6) -> pd.DataFrame:
    X = np.log1p(rfm[VARIABLES_SEGMENTACION])
    X_esc = StandardScaler().fit_transform(X)
    filas = []
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_esc)
        filas.append({"k": k, "silueta": silhouette_score(X_esc, km.labels_)})
    return pd.DataFrame(filas)


# --------------------------------------------------------------------------- #
# Nicho mayorista y reglas de asociación
# --------------------------------------------------------------------------- #
def dataset_valor_futuro(dc: pd.DataFrame, fecha_corte: str = "2011-09-01") -> pd.DataFrame:
    """Construye features (comportamiento pasado) y objetivo (gasto futuro).

    Usa un split temporal para evitar circularidad: las variables se calculan con
    los datos ANTERIORES a `fecha_corte` y el objetivo es el gasto POSTERIOR.
    Así el modelo predice de verdad, no reconstruye una fórmula.
    """
    corte = pd.Timestamp(fecha_corte)
    pasado = dc[dc["InvoiceDate"] < corte]
    futuro = dc[dc["InvoiceDate"] >= corte]

    feat = pasado.groupby("CustomerID").agg(
        Recencia=("InvoiceDate", lambda x: (corte - x.max()).days),
        Frecuencia=("InvoiceNo", "nunique"),
        Monetario=("TotalPrice", "sum"),
        Antiguedad=("InvoiceDate", lambda x: (corte - x.min()).days),
        Diversidad=("Description", "nunique"),
    ).reset_index()
    ticket = (pasado.groupby(["CustomerID", "InvoiceNo"])["TotalPrice"].sum()
              .groupby("CustomerID").mean())
    feat["TicketMedio"] = feat["CustomerID"].map(ticket)

    gasto_futuro = futuro.groupby("CustomerID")["TotalPrice"].sum()
    feat["GastoFuturo"] = feat["CustomerID"].map(gasto_futuro).fillna(0.0)
    return feat


def modelo_valor_futuro(feat: pd.DataFrame) -> dict:
    """Ajusta una regresión múltiple log-log para predecir el gasto futuro.

    Devuelve el modelo, las métricas (R² en train y test) y los datos de test
    para graficar predicho vs real. Trabaja en escala log para domar el sesgo.
    """
    import statsmodels.api as sm
    from sklearn.metrics import r2_score
    from sklearn.model_selection import train_test_split

    cols = VARIABLES_SEGMENTACION
    X = np.log1p(feat[cols])
    y = np.log1p(feat["GastoFuturo"])
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

    modelo = sm.OLS(y_tr, sm.add_constant(X_tr)).fit()
    pred_te = modelo.predict(sm.add_constant(X_te))

    # Coeficientes estandarizados, para comparar la importancia de cada variable
    Xz = (X - X.mean()) / X.std()
    yz = (y - y.mean()) / y.std()
    modelo_z = sm.OLS(yz, sm.add_constant(Xz)).fit()

    return {
        "modelo": modelo,
        "cols": cols,
        "r2_train": float(modelo.rsquared),
        "r2_test": float(r2_score(y_te, pred_te)),
        "coef_estandarizado": modelo_z.params[cols],
        "pvalores": modelo.pvalues[cols],
        "y_test": y_te,
        "pred_test": pred_te,
    }


def modelo_churn(feat: pd.DataFrame) -> dict:
    """Regresión logística para predecir la fuga del cliente.

    Define churn como no haber vuelto a comprar en el período futuro
    (GastoFuturo == 0). Usa el comportamiento pasado como entrada, así que no
    hay fuga de información. Devuelve métricas, coeficientes, la curva ROC y la
    probabilidad de fuga estimada para cada cliente.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
    from sklearn.model_selection import train_test_split

    cols = VARIABLES_SEGMENTACION
    feat = feat.copy()
    feat["churn"] = (feat["GastoFuturo"] == 0).astype(int)

    X = np.log1p(feat[cols])
    Xz = (X - X.mean()) / X.std()
    y = feat["churn"]
    X_tr, X_te, y_tr, y_te = train_test_split(Xz, y, test_size=0.3, random_state=42, stratify=y)

    modelo = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    proba_te = modelo.predict_proba(X_te)[:, 1]
    fpr, tpr, _ = roc_curve(y_te, proba_te)
    feat["prob_churn"] = modelo.predict_proba(Xz)[:, 1]

    return {
        "modelo": modelo,
        "cols": cols,
        "tasa_churn": float(y.mean()),
        "auc": float(roc_auc_score(y_te, proba_te)),
        "accuracy": float(accuracy_score(y_te, (proba_te > 0.5).astype(int))),
        "coef": pd.Series(modelo.coef_[0], index=cols),
        "fpr": fpr,
        "tpr": tpr,
        "feat": feat,
    }


def punto_equilibrio(costos_fijos: float, margen_pct: float, ventas: float) -> dict:
    """Punto de equilibrio del negocio a partir de supuestos de costo.

    El dataset no tiene costos, así que se calculan con parámetros que ingresa
    el usuario. El equilibrio es el nivel de ventas donde la utilidad es cero:
    ventas = costos_fijos / margen_de_contribución.
    """
    margen = margen_pct / 100
    be = costos_fijos / margen if margen > 0 else float("inf")
    utilidad = ventas * margen - costos_fijos
    seguridad = (ventas - be) / ventas * 100 if ventas > 0 else 0.0
    return {"break_even": be, "utilidad": utilidad, "margen_seguridad": seguridad}


def serie_semanal(df: pd.DataFrame) -> pd.Series:
    """Ventas totales por semana (descarta la última, incompleta)."""
    s = df.groupby(df["InvoiceDate"].dt.to_period("W"))["TotalPrice"].sum()
    return s.iloc[:-1]


def pronostico_montecarlo(serie: pd.Series, horizonte: int = 12,
                          n_sim: int = 2000, semilla: int = 42) -> dict:
    """Pronóstico de ventas con simulación de Monte Carlo.

    Ajusta una tendencia lineal y simula `n_sim` escenarios futuros sintéticos,
    sumándole a la tendencia un ruido remuestreado de los residuos reales. De
    esos miles de escenarios sale el valor esperado y las bandas de incertidumbre.
    """
    rng = np.random.default_rng(semilla)
    y = serie.values
    n = len(y)
    t = np.arange(n)

    pendiente, intercepto = np.polyfit(t, y, 1)
    resid = y - (intercepto + pendiente * t)

    tf = np.arange(n, n + horizonte)
    base = intercepto + pendiente * tf
    paths = np.clip(base[None, :] + rng.choice(resid, size=(n_sim, horizonte)), 0, None)

    p10, p50, p90 = np.percentile(paths, [10, 50, 90], axis=0)
    futuro = pd.DataFrame({
        "semana": np.arange(1, horizonte + 1),
        "media": paths.mean(axis=0),
        "p10": p10, "p50": p50, "p90": p90,
    })
    totales = paths.sum(axis=1)
    return {
        "futuro": futuro,
        "totales": totales,
        "esperado_total": float(totales.mean()),
        "desviacion_total": float(totales.std()),
        "tendencia_semanal": float(pendiente),
        "n_historia": n,
    }


def simular_negocio_montecarlo(
    base: float, ingreso_campeones: float, gastos_mayoristas: np.ndarray,
    n_facturas: int, ticket_medio: float,
    uplift_champ: float, nuevos_mayoristas: int, conversion_cross: float,
    n_sim: int = 5000, semilla: int = 42,
) -> np.ndarray:
    """Simula el ingreso total proyectado bajo incertidumbre (Monte Carlo).

    Cada palanca tiene un resultado incierto, no un valor fijo. El uplift de
    campeones y la conversión de la promoción se realizan alrededor de su
    objetivo con variabilidad, y cada mayorista nuevo gasta un monto muestreado
    de los mayoristas reales. Devuelve un arreglo con el ingreso total simulado.
    """
    rng = np.random.default_rng(semilla)

    # Fidelizar campeones: el aumento realizado varía alrededor del objetivo
    uplift = np.clip(rng.normal(uplift_champ / 100, (uplift_champ / 100) * 0.4 + 1e-9, n_sim), 0, None)
    delta_champ = ingreso_campeones * uplift

    # Captar mayoristas: cada nuevo cliente gasta un monto tomado de los reales
    if nuevos_mayoristas > 0 and len(gastos_mayoristas):
        delta_may = rng.choice(gastos_mayoristas, size=(n_sim, nuevos_mayoristas)).sum(axis=1)
    else:
        delta_may = np.zeros(n_sim)

    # Promoción cruzada: la conversión realizada varía alrededor del objetivo
    conv = np.clip(rng.normal(conversion_cross / 100, (conversion_cross / 100) * 0.4 + 1e-9, n_sim), 0, None)
    delta_cross = n_facturas * conv * ticket_medio * 0.05

    return base + delta_champ + delta_may + delta_cross


def nps_simulado(rfm_segmentado: pd.DataFrame, semilla: int = 42) -> pd.DataFrame:
    """Simula respuestas de una encuesta NPS (0 a 10) por cliente.

    DATOS SINTÉTICOS. El dataset real no tiene encuestas, así que se simulan
    puntajes calibrados por segmento (los campeones puntúan alto, los clientes
    en riesgo bajo) para demostrar cómo se calcula el NPS. No son datos reales.
    """
    rng = np.random.default_rng(semilla)
    medias = {"Campeones": 9.0, "Leales": 7.8, "Ocasionales": 7.0, "En riesgo": 5.5}
    df = rfm_segmentado.copy()
    base = df["Segmento"].map(medias).fillna(7.0)
    df["nps_score"] = np.clip(np.round(base + rng.normal(0, 1.2, len(df))), 0, 10).astype(int)
    df["nps_cat"] = pd.cut(df["nps_score"], bins=[-1, 6, 8, 10],
                           labels=["Detractor", "Pasivo", "Promotor"])
    return df


def calcular_nps(df_nps: pd.DataFrame) -> float:
    """NPS = porcentaje de promotores menos porcentaje de detractores."""
    prom = (df_nps["nps_cat"] == "Promotor").mean()
    detr = (df_nps["nps_cat"] == "Detractor").mean()
    return float((prom - detr) * 100)


def clientes_mayoristas(dc: pd.DataFrame, umbral_unidades: int) -> np.ndarray:
    uf = dc.groupby(["CustomerID", "InvoiceNo"])["Quantity"].sum().reset_index()
    return uf[uf["Quantity"] >= umbral_unidades]["CustomerID"].unique()


def metricas_pais(df: pd.DataFrame, min_clientes: int = 10) -> pd.DataFrame:
    """Métricas de negocio por país, filtrando los que tienen pocos clientes.

    `df` debe venir de `limpiar(..., solo_uk=False)`. El ingreso por cliente
    revela qué mercados son mayoristas (pocos clientes, mucho gasto) frente a
    los de consumo (muchos clientes).
    """
    m = df.groupby("Country").agg(
        ingresos=("TotalPrice", "sum"),
        clientes=("CustomerID", "nunique"),
        facturas=("InvoiceNo", "nunique"),
    ).reset_index()
    ticket = (df.groupby(["Country", "InvoiceNo"])["TotalPrice"].sum()
              .groupby("Country").mean())
    m["ticket_medio"] = m["Country"].map(ticket)
    m["ingreso_por_cliente"] = m["ingresos"] / m["clientes"].replace(0, np.nan)
    return m[m["clientes"] >= min_clientes].sort_values("ingresos", ascending=False)


def perfil_pais(df_global: pd.DataFrame, pais: str, n: int = 8) -> tuple:
    """Productos más vendidos de un país y los que sobre-consume frente al promedio.

    Devuelve dos Series: los top productos por unidades, y los productos
    "distintivos", aquellos que el país compra en mucha mayor proporción que el
    promedio global (índice de especialización). Revela oportunidades de
    localización del catálogo.
    """
    pdf = df_global[df_global["Country"] == pais]
    loc = pdf.groupby("Description")["Quantity"].sum()
    top = loc.sort_values(ascending=False).head(n)

    loc_share = loc / loc.sum()
    glob = df_global.groupby("Description")["Quantity"].sum()
    glob_share = glob / glob.sum()
    indice = (loc_share / glob_share.reindex(loc_share.index)).dropna()
    # Solo productos con volumen local relevante, para no inflar el índice con la cola larga
    relevantes = loc[loc >= loc.quantile(0.6)].index
    distintivos = indice[indice.index.isin(relevantes)].sort_values(ascending=False).head(n)
    return top, distintivos


def stats_productos(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("Description").agg(
        unidades=("Quantity", "sum"),
        facturas=("InvoiceNo", "nunique"),
        ingresos=("TotalPrice", "sum"),
        precio_medio=("UnitPrice", "mean"),
    ).reset_index()


def matriz_lift_top(df: pd.DataFrame, n_top: int = 12) -> pd.DataFrame:
    """Tabulación cruzada de afinidad (lift) entre los productos más vendidos.

    Cada celda es el lift del par, cuánto más se compran juntos esos dos
    productos frente a lo esperable por azar. Un lift mayor a 1 indica afinidad.
    La diagonal queda vacía (un producto consigo mismo no aporta).
    """
    top = list(df.groupby("Description")["Quantity"].sum()
               .sort_values(ascending=False).head(n_top).index)
    n_facturas = df["InvoiceNo"].nunique()
    facturas = {p: set(df[df["Description"] == p]["InvoiceNo"]) for p in top}
    conteo = {p: len(facturas[p]) for p in top}

    mat = np.full((n_top, n_top), np.nan)
    for i, a in enumerate(top):
        for j, b in enumerate(top):
            if i != j and conteo[a] and conteo[b]:
                co = len(facturas[a] & facturas[b])
                mat[i, j] = co * n_facturas / (conteo[a] * conteo[b])
    return pd.DataFrame(mat, index=top, columns=top)


def paquetes_tematicos(matriz_lift: pd.DataFrame, n_temas: int = 5) -> list:
    """Arma paquetes de varios productos agrupando la tabla cruzada de afinidad.

    Convierte el lift en distancia (más afinidad, menos distancia) y aplica
    clustering jerárquico. Cada grupo de productos mutuamente afines es un
    paquete temático, algo que las reglas par a par no entregan directamente.
    """
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import squareform

    L = matriz_lift.values.copy()
    np.fill_diagonal(L, np.nanmax(L))
    L = np.nan_to_num(L, nan=0.0)
    dist = 1.0 / (L + 0.1)
    np.fill_diagonal(dist, 0.0)
    dist = (dist + dist.T) / 2

    Z = linkage(squareform(dist, checks=False), method="average")
    grupos = fcluster(Z, t=n_temas, criterion="maxclust")

    paquetes = []
    for g in sorted(set(grupos)):
        prods = [matriz_lift.index[i] for i in range(len(grupos)) if grupos[i] == g]
        if len(prods) >= 2:
            paquetes.append(prods)
    return paquetes


def reglas_asociacion(df: pd.DataFrame, min_support: float) -> pd.DataFrame:
    """Reglas a un soporte dado, deduplicadas y clasificadas en cruzada / colección."""
    cesta = df.groupby(["InvoiceNo", "Description"])["Quantity"].sum().unstack().fillna(0) > 0
    frecuentes = fpgrowth(cesta, min_support=min_support, use_colnames=True)
    reglas = association_rules(frecuentes, metric="lift", min_threshold=1)

    reglas["par"] = reglas.apply(
        lambda r: tuple(sorted([tuple(sorted(r["antecedents"])), tuple(sorted(r["consequents"]))])),
        axis=1,
    )
    reglas = reglas.sort_values("lift", ascending=False).drop_duplicates("par").reset_index(drop=True)

    def es_cross_sell(r):
        pa = set(" ".join(r["antecedents"]).split())
        pc = set(" ".join(r["consequents"]).split())
        return len(pa & pc) == 0

    reglas["tipo"] = np.where(reglas.apply(es_cross_sell, axis=1), "Venta cruzada", "Misma colección")
    reglas["antecedente"] = reglas["antecedents"].apply(lambda s: ", ".join(s))
    reglas["consecuente"] = reglas["consequents"].apply(lambda s: ", ".join(s))
    return reglas
