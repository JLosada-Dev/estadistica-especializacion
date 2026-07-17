"""Las cinco secciones del dashboard de retail."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import datos as proc
from estadistica import retail
from _shared.componentes import encabezado, fig


# --------------------------------------------------------------------------- #
# 1. Resumen
# --------------------------------------------------------------------------- #
def resumen() -> None:
    encabezado("resumen", "Resumen del negocio",
               "Indicadores generales y evolución de las ventas del retailer.")

    df = proc.cargar_datos()
    dc = proc.datos_cliente()

    meses = sorted(df["Mes"].unique())
    rango = st.select_slider("Rango de meses", options=meses, value=(meses[0], meses[-1]))
    df_f = df[(df["Mes"] >= rango[0]) & (df["Mes"] <= rango[1])]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Ingresos", f"£{df_f['TotalPrice'].sum()/1e6:.2f}M")
    c2.metric("Clientes", f"{dc['CustomerID'].nunique():,}")
    c3.metric("Facturas", f"{df_f['InvoiceNo'].nunique():,}")
    c4.metric("Productos", f"{df_f['Description'].nunique():,}")
    c5.metric("Ticket promedio", f"£{df_f.groupby('InvoiceNo')['TotalPrice'].sum().mean():.0f}")

    st.write("")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### Ventas por mes")
        ventas = df_f.groupby("Mes")["TotalPrice"].sum().reset_index()
        f = px.area(ventas, x="Mes", y="TotalPrice", markers=True, color_discrete_sequence=["#3B6FB6"])
        f.update_layout(yaxis_title="Ingresos (£)", xaxis_title="")
        st.plotly_chart(fig(f), use_container_width=True)
    with col_b:
        st.markdown("##### Concentración de ingresos (Pareto)")
        gasto = dc.groupby("CustomerID")["TotalPrice"].sum().sort_values(ascending=False)
        acum = (gasto.cumsum() / gasto.sum() * 100).reset_index(drop=True)
        n80 = int((acum <= 80).sum()) + 1
        f = go.Figure()
        f.add_scatter(y=acum.values, mode="lines", line=dict(color="#3B6FB6", width=2))
        f.add_hline(y=80, line_dash="dash", line_color="#E07A5F")
        f.update_layout(xaxis_title="Clientes ordenados por gasto", yaxis_title="% acumulado")
        st.plotly_chart(fig(f), use_container_width=True)
        st.info(f"**{n80/len(gasto)*100:.0f}% de los clientes genera el 80% de los ingresos.**")

    st.markdown("##### Top 10 productos por ingresos")
    top = df_f.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)
    f = px.bar(top[::-1], orientation="h", color_discrete_sequence=["#2E7D55"])
    f.update_layout(showlegend=False, xaxis_title="Ingresos (£)", yaxis_title="")
    st.plotly_chart(fig(f, 400), use_container_width=True)

    st.divider()
    st.markdown("##### Punto de equilibrio")
    st.caption(
        "El dataset no incluye costos, así que el punto de equilibrio se calcula con tus supuestos. "
        "Es el nivel de ventas mensual donde la utilidad es cero."
    )
    ventas_mes = df_f.groupby("Mes")["TotalPrice"].sum().mean()

    col_ctrl, col_res = st.columns([1, 2])
    with col_ctrl:
        fijos = st.number_input("Costos fijos mensuales (£)", 0, 2_000_000, 200_000, 25_000)
        margen = st.slider("Margen de contribución (%)", 5, 80, 40,
                           help="Porcentaje de cada venta que queda tras los costos variables.")
    eq = retail.punto_equilibrio(fijos, margen, ventas_mes)

    with col_res:
        m1, m2, m3 = st.columns(3)
        m1.metric("Punto de equilibrio", f"£{eq['break_even']/1e3:,.0f}K/mes")
        m2.metric("Ventas mensuales actuales", f"£{ventas_mes/1e3:,.0f}K")
        m3.metric("Margen de seguridad", f"{eq['margen_seguridad']:+.0f}%",
                  "por encima" if eq["margen_seguridad"] >= 0 else "por debajo")

        xs = np.linspace(0, max(ventas_mes, eq["break_even"]) * 1.6, 100)
        costo_total = fijos + (1 - margen / 100) * xs
        f = go.Figure()
        f.add_scatter(x=xs, y=xs, mode="lines", name="Ingresos", line=dict(color="#2E7D55"))
        f.add_scatter(x=xs, y=costo_total, mode="lines", name="Costos totales", line=dict(color="#E24B4A"))
        f.add_vline(x=eq["break_even"], line_dash="dot", line_color="#999")
        f.add_scatter(x=[ventas_mes], y=[ventas_mes], mode="markers", name="Ventas actuales",
                      marker=dict(size=13, color="#222", symbol="diamond"))
        f.update_layout(xaxis_title="Ventas mensuales (£)", yaxis_title="£",
                        legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig(f, 320), use_container_width=True)

    estado = "con ganancia" if eq["utilidad"] >= 0 else "en pérdida"
    st.info(
        f"Con estos supuestos, el negocio necesita vender £{eq['break_even']/1e3:,.0f}K al mes para no "
        f"perder. Hoy vende £{ventas_mes/1e3:,.0f}K, así que opera **{estado}** "
        f"(utilidad estimada £{eq['utilidad']/1e3:,.0f}K/mes)."
    )


# --------------------------------------------------------------------------- #
# 2. Segmentación
# --------------------------------------------------------------------------- #
def segmentacion() -> None:
    encabezado("segmentacion", "Segmentación de clientes",
               "Agrupación por comportamiento con RFM enriquecido y K-Means.")

    col_ctrl, col_info = st.columns([1, 2])
    with col_ctrl:
        k = st.slider("Número de segmentos (k)", min_value=3, max_value=6, value=4)
    with col_info:
        sil = proc.silueta_por_k()
        s_k = sil.loc[sil["k"] == k, "silueta"].iloc[0]
        st.metric("Calidad de la separación (silueta)", f"{s_k:.3f}")

    rfm = proc.segmentar(k)
    presentes = [s for s in proc.ORDEN_SEGMENTOS if s in rfm["Segmento"].unique()]
    presentes += [s for s in rfm["Segmento"].unique() if s not in presentes]

    col_a, col_b = st.columns(2)
    with col_a:
        var = rfm.attrs.get("pca_varianza", 0)
        st.markdown(f"##### Mapa de segmentos · PCA ({var:.0f}% de la información)")
        f = px.scatter(rfm, x="pca1", y="pca2", color="Segmento",
                       color_discrete_map=proc.COLORES_SEGMENTO,
                       hover_data=["Recencia", "Frecuencia", "Monetario"])
        f.update_layout(xaxis_title="Componente principal 1", yaxis_title="Componente principal 2",
                        legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig(f, 400), use_container_width=True)
        st.caption(
            "El PCA resume las tres variables RFM en dos ejes para poder dibujar los grupos en un "
            f"plano. Con un {var:.0f}% de la información conservada, el mapa es fiel a la realidad."
        )
    with col_b:
        st.markdown("##### Ingresos por segmento")
        resumen_seg = rfm.groupby("Segmento").agg(Ingresos=("Monetario", "sum")).reindex(presentes)
        f = px.bar(resumen_seg, y="Ingresos", color=resumen_seg.index,
                   color_discrete_map=proc.COLORES_SEGMENTO)
        f.update_layout(showlegend=False, yaxis_title="Ingresos (£)", xaxis_title="")
        st.plotly_chart(fig(f, 400), use_container_width=True)

    st.markdown("##### Perfil de cada segmento (RFM enriquecido)")
    perfil = rfm.groupby("Segmento").agg(
        Clientes=("CustomerID", "count"),
        Recencia_dias=("Recencia", "mean"),
        Frecuencia=("Frecuencia", "mean"),
        Antiguedad_dias=("Antiguedad", "mean"),
        Diversidad=("Diversidad", "mean"),
        Ticket_medio=("TicketMedio", "mean"),
        Gasto_total=("Monetario", "mean"),
    ).reindex(presentes).round(1)
    st.dataframe(perfil, use_container_width=True)
    st.caption(
        "La antigüedad distingue a los clientes nuevos de los que llevan tiempo. "
        "Los Ocasionales suelen ser clientes recientes con potencial, mientras que los "
        "En riesgo son antiguos que dejaron de comprar."
    )


# --------------------------------------------------------------------------- #
# 3. Nicho mayorista
# --------------------------------------------------------------------------- #
def nicho() -> None:
    encabezado("nicho", "Nicho mayorista",
               "Compradores de gran volumen, un mercado dentro del mercado.")

    umbral = st.slider("Umbral para considerar a un cliente mayorista (unidades en una factura)",
                       min_value=200, max_value=2000, value=1000, step=100)

    dc = proc.datos_cliente().copy()
    ids = proc.clientes_mayoristas(umbral)
    dc["Tipo"] = np.where(dc["CustomerID"].isin(ids), "Mayorista", "Minorista")

    ing_may = dc[dc["Tipo"] == "Mayorista"]["TotalPrice"].sum()
    ing_tot = dc["TotalPrice"].sum()
    gasto_may = dc[dc["Tipo"] == "Mayorista"].groupby("CustomerID")["TotalPrice"].sum().mean()
    gasto_min = dc[dc["Tipo"] == "Minorista"].groupby("CustomerID")["TotalPrice"].sum().mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes mayoristas", f"{len(ids)}", f"{len(ids)/dc['CustomerID'].nunique()*100:.0f}% del total")
    c2.metric("Ingresos que generan", f"{ing_may/ing_tot*100:.0f}%")
    c3.metric("Gasto medio vs minorista", f"£{gasto_may:,.0f}",
              f"{gasto_may/gasto_min:.0f}x más" if gasto_min else "")

    st.write("")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### Reparto de ingresos")
        f = px.pie(names=["Mayoristas", "Resto"], values=[ing_may, ing_tot - ing_may],
                   color_discrete_sequence=["#B7791F", "#E5E9F0"], hole=0.45)
        st.plotly_chart(fig(f), use_container_width=True)
    with col_b:
        st.markdown("##### Productos preferidos por mayoristas")
        top = (dc[dc["Tipo"] == "Mayorista"].groupby("Description")["Quantity"]
               .sum().sort_values(ascending=False).head(8))
        f = px.bar(top[::-1], orientation="h", color_discrete_sequence=["#B7791F"])
        f.update_layout(showlegend=False, xaxis_title="Unidades", yaxis_title="")
        st.plotly_chart(fig(f), use_container_width=True)

    st.info(
        "Los mayoristas compran productos pensados para revender y se abastecen sobre todo "
        "antes de Navidad. Son candidatos a precios por volumen y a un programa B2B dedicado."
    )


# --------------------------------------------------------------------------- #
# 4. Recomendaciones / paquetes
# --------------------------------------------------------------------------- #
def _precio_set(productos, precios: dict) -> float:
    return sum(precios.get(p, 0) for p in productos)


def asociacion() -> None:
    encabezado("recomendaciones", "Paquetes y recomendaciones",
               "Qué productos ofrecer juntos para vender más. Jugá con los controles y los escenarios cambian.")

    c1, c2, c3 = st.columns(3)
    with c1:
        soporte = st.select_slider("Soporte mínimo", options=[0.01, 0.015, 0.02], value=0.01,
                                   help="Qué tan común debe ser una combinación.")
    reglas = proc.reglas_asociacion(soporte)
    with c2:
        min_lift = st.slider("Lift mínimo", 1.0, float(round(reglas["lift"].max())), 2.0, 0.5)
    with c3:
        min_conf = st.slider("Confianza mínima", 0.0, 1.0, 0.2, 0.05)

    n_fact = proc.n_facturas()
    precios = proc.stats_productos().set_index("Description")["precio_medio"].to_dict()

    cross = reglas[(reglas["tipo"] == "Venta cruzada")
                   & (reglas["lift"] >= min_lift)
                   & (reglas["confidence"] >= min_conf)].sort_values("lift", ascending=False)

    tab1, tab2, tab4, tab3 = st.tabs(
        ["Paquetes de promoción", "Explorar por producto", "Tabla cruzada", "Todas las reglas"])

    with tab1:
        st.caption(
            "Cada paquete combina productos que se compran juntos más de lo normal. El alcance es "
            "cuántas facturas ya incluyen el primer producto, a cuántos clientes se podría ofrecer el combo."
        )
        if not len(cross):
            st.warning("Ningún paquete cumple los criterios. Bajá el lift o la confianza.")
        else:
            paq = cross.copy()
            paq["alcance"] = (paq["antecedent support"] * n_fact).round().astype(int)
            paq["copras"] = (paq["alcance"] * paq["confidence"]).round().astype(int)
            paq["valor_potencial"] = paq.apply(
                lambda r: r["copras"] * _precio_set(r["consequents"], precios), axis=1)

            st.metric("Paquetes posibles", len(paq))
            top = paq.head(6).reset_index(drop=True)
            for fila in range(0, len(top), 3):
                cols = st.columns(3)
                for i, col in enumerate(cols):
                    if fila + i >= len(top):
                        break
                    r = top.iloc[fila + i]
                    with col, st.container(border=True):
                        st.markdown(f"**Paquete {fila + i + 1}**")
                        st.markdown(
                            f"<span style='color:#6D4AA6;font-weight:600'>{r['antecedente']}</span>"
                            f"<br><span style='color:#9aa0ab'>+</span><br>"
                            f"<span style='color:#2E7D55;font-weight:600'>{r['consecuente']}</span>",
                            unsafe_allow_html=True)
                        st.caption(f"Confianza {r['confidence']*100:.0f}% · Lift {r['lift']:.1f}")
                        st.caption(f"Alcance: {r['alcance']:,} facturas · Potencial £{r['valor_potencial']:,.0f}")

            st.markdown("##### Todos los paquetes ordenados por potencial")
            tabla = paq.sort_values("valor_potencial", ascending=False)[
                ["antecedente", "consecuente", "confidence", "lift", "alcance", "valor_potencial"]
            ].rename(columns={"antecedente": "Producto gancho", "consecuente": "Producto a sumar",
                              "confidence": "Confianza", "lift": "Lift", "alcance": "Alcance (facturas)",
                              "valor_potencial": "Potencial (£)"})
            st.dataframe(
                tabla.style.format({"Confianza": "{:.0%}", "Lift": "{:.1f}",
                                    "Alcance (facturas)": "{:,}", "Potencial (£)": "£{:,.0f}"}),
                use_container_width=True, height=320, hide_index=True)
            st.download_button("Descargar paquetes (CSV)",
                               tabla.to_csv(index=False).encode("utf-8"),
                               "paquetes_promocion.csv", "text/csv")

    with tab2:
        st.caption("Elegí un producto y mirá con qué conviene combinarlo y cómo se comporta.")
        productos = sorted({p for fs in reglas["antecedents"] for p in fs})
        elegido = st.selectbox("Producto", productos)
        sp = proc.stats_productos()
        info = sp[sp["Description"] == elegido]
        if len(info):
            info = info.iloc[0]
            m1, m2, m3 = st.columns(3)
            m1.metric("Unidades vendidas", f"{int(info['unidades']):,}")
            m2.metric("Facturas que lo incluyen", f"{int(info['facturas']):,}")
            m3.metric("Ingresos", f"£{info['ingresos']:,.0f}")
        socios = reglas[reglas["antecedents"].apply(lambda s: elegido in s)
                        & (reglas["tipo"] == "Venta cruzada")].sort_values("lift", ascending=False)
        st.markdown(f"##### Qué recomendar a quien compra **{elegido}**")
        if len(socios):
            vis = socios.head(10)
            f = px.bar(vis[::-1], x="lift", y="consecuente", orientation="h",
                       color_discrete_sequence=["#6D4AA6"], hover_data={"confidence": ":.0%"})
            f.update_layout(xaxis_title="Lift", yaxis_title="")
            st.plotly_chart(fig(f, 380), use_container_width=True)
        else:
            st.info("Este producto no tiene combinaciones de venta cruzada con los criterios actuales.")

    with tab4:
        st.caption(
            "Tabulación cruzada de afinidad entre los productos más vendidos. Cada celda es el lift "
            "del par, cuánto más se compran juntos frente al azar. Verde intenso (lift mayor a 1) "
            "marca los pares con más afinidad para recomendar o empaquetar."
        )
        n_top = st.slider("Cantidad de productos", 8, 20, 12)
        mat = proc.matriz_lift(n_top)
        etiquetas = [d[:24] for d in mat.index]
        f = px.imshow(mat.values, x=etiquetas, y=etiquetas, text_auto=".1f",
                      color_continuous_scale="RdYlGn", color_continuous_midpoint=1,
                      aspect="auto", labels=dict(color="Lift"))
        f.update_layout(height=560, margin=dict(l=10, r=10, t=10, b=10),
                        xaxis_tickangle=-45)
        st.plotly_chart(f, use_container_width=True)

        st.divider()
        st.markdown("##### Paquetes temáticos armados desde la tabla cruzada")
        st.caption(
            "Agrupando la matriz de afinidad, los productos que van juntos forman bundles de varios "
            "productos. Es el paso de los pares sueltos a un paquete temático completo para promocionar."
        )
        n_temas = st.slider("Cantidad de temas", 3, 8, 5)
        paquetes = proc.paquetes_tematicos(n_top, n_temas)
        if not paquetes:
            st.info("Con estos parámetros no se forman grupos de 2 o más productos. Subí los productos o bajá los temas.")
        for idx, prods in enumerate(paquetes, 1):
            with st.container(border=True):
                st.markdown(f"**Paquete temático {idx}**  ·  {len(prods)} productos")
                st.markdown("  +  ".join(f"<span style='color:#6D4AA6'>{p}</span>" for p in prods),
                            unsafe_allow_html=True)

    with tab3:
        solo_cross = st.toggle("Mostrar solo venta cruzada (recomendaciones no obvias)", value=True)
        filtro = (reglas["lift"] >= min_lift) & (reglas["confidence"] >= min_conf)
        if solo_cross:
            filtro &= reglas["tipo"] == "Venta cruzada"
        sub = reglas[filtro].sort_values("lift", ascending=False)
        st.metric("Reglas que cumplen los criterios", len(sub))
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.dataframe(
                sub[["antecedente", "consecuente", "support", "confidence", "lift", "tipo"]]
                .rename(columns={"antecedente": "Si compra…", "consecuente": "Recomendar…",
                                 "support": "Soporte", "confidence": "Confianza", "lift": "Lift",
                                 "tipo": "Tipo"}).round(3).head(25),
                use_container_width=True, height=430, hide_index=True)
        with col_b:
            if len(sub):
                f = px.scatter(sub, x="support", y="confidence", size="lift", color="tipo",
                               color_discrete_map={"Venta cruzada": "#6D4AA6", "Misma colección": "#C7CCD6"},
                               hover_data=["antecedente", "consecuente", "lift"])
                f.update_layout(xaxis_title="Soporte", yaxis_title="Confianza",
                                legend=dict(orientation="h", y=-0.2))
                st.plotly_chart(fig(f, 430), use_container_width=True)
            else:
                st.warning("Ninguna regla cumple los criterios. Bajá el lift o la confianza.")


# --------------------------------------------------------------------------- #
# Valor del cliente (regresión múltiple)
# --------------------------------------------------------------------------- #
def valor() -> None:
    encabezado("valor", "Valor del cliente",
               "Predicción del gasto futuro de cada cliente con regresión múltiple.")

    corte = st.selectbox(
        "Fecha de corte · el modelo aprende del comportamiento ANTES y predice el gasto DESPUÉS",
        ["2011-08-01", "2011-09-01", "2011-10-01"], index=1)
    feat, res = proc.modelo_valor(corte)
    volvieron = (feat["GastoFuturo"] > 0).mean() * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes modelados", f"{len(feat):,}")
    c2.metric("Volvieron a comprar", f"{volvieron:.0f}%")
    c3.metric("Poder predictivo (R² test)", f"{res['r2_test']:.2f}")

    st.caption(
        "El split temporal evita la circularidad: las variables se calculan con el pasado y el "
        "objetivo es el gasto del futuro. Un R² cercano a 0.27 es razonable, predecir el "
        "comportamiento humano es difícil y la otra parte depende de factores no observados."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### Qué comportamientos predicen el valor futuro")
        coef = res["coef_estandarizado"].sort_values()
        f = px.bar(x=coef.values, y=coef.index, orientation="h",
                   color=["#E24B4A" if v < 0 else "#2E7D55" for v in coef.values],
                   color_discrete_map="identity")
        f.update_layout(xaxis_title="Peso (coeficiente estandarizado)", yaxis_title="")
        st.plotly_chart(fig(f, 380), use_container_width=True)
    with col_b:
        st.markdown("##### Gasto futuro: predicho vs real (test)")
        comp = pd.DataFrame({"Real": res["y_test"].values, "Predicho": res["pred_test"].values})
        f = px.scatter(comp, x="Real", y="Predicho", opacity=0.4,
                       color_discrete_sequence=["#4338CA"])
        lim = float(max(comp["Real"].max(), comp["Predicho"].max()))
        f.add_shape(type="line", x0=0, y0=0, x1=lim, y1=lim, line=dict(color="#999", dash="dash"))
        f.update_layout(xaxis_title="Real (log de gasto futuro)", yaxis_title="Predicho")
        st.plotly_chart(fig(f, 380), use_container_width=True)

    st.info(
        "La frecuencia de compra pasada es el mejor predictor del valor futuro, seguida del monto. "
        "Tiene sentido, quien compró seguido tiende a seguir comprando. La recencia pesa en contra, "
        "cuanto más tiempo sin comprar, menos gasto futuro."
    )


# --------------------------------------------------------------------------- #
# Mercados internacionales
# --------------------------------------------------------------------------- #
def regional() -> None:
    encabezado("regional", "Mercados internacionales",
               "El negocio más allá del Reino Unido, por país.")

    m = proc.metricas_pais()  # ya excluye países con pocos clientes
    fuera = m[m["Country"] != "United Kingdom"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Mercados con datos", f"{len(fuera)} países")
    c2.metric("Ingresos fuera de UK", f"£{fuera['ingresos'].sum()/1e6:.2f}M")
    c3.metric("Mejor mercado (sin UK)", fuera.iloc[0]["Country"])

    tab1, tab2 = st.tabs(["Panorama", "Análisis por país"])

    with tab1:
        incluir_uk = st.toggle("Incluir Reino Unido", value=False,
                               help="UK domina con el 85% de los ingresos; ocultarlo deja ver el resto.")
        datos = m if incluir_uk else fuera

        st.markdown("##### Ingresos por país")
        f = px.choropleth(datos, locations="Country", locationmode="country names",
                          color="ingresos", color_continuous_scale="Teal",
                          scope="europe" if not incluir_uk else "world",
                          hover_data={"clientes": True, "ticket_medio": ":.0f"})
        f.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(f, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("##### Top mercados por ingresos")
            top = fuera.head(8)
            f = px.bar(top[::-1], x="ingresos", y="Country", orientation="h",
                       color_discrete_sequence=["#0E7C86"])
            f.update_layout(xaxis_title="Ingresos (£)", yaxis_title="")
            st.plotly_chart(fig(f, 360), use_container_width=True)
        with col_b:
            st.markdown("##### Oportunidad: consumo vs mayorista")
            f = px.scatter(fuera, x="clientes", y="ingreso_por_cliente", text="Country",
                           size="ingresos", color_discrete_sequence=["#0E7C86"])
            f.update_traces(textposition="top center")
            f.update_layout(xaxis_title="Clientes", yaxis_title="Ingreso por cliente (£)")
            st.plotly_chart(fig(f, 360), use_container_width=True)

        st.info(
            "Arriba a la izquierda, pocos clientes con alto gasto por cliente, están los mercados "
            "de perfil mayorista como Noruega o Suiza, candidatos a gestión de cuentas clave. Abajo "
            "a la derecha, muchos clientes, los de consumo como Alemania y Francia, para marketing masivo."
        )

    with tab2:
        st.caption(
            "Los clientes de cada país compran productos distintos (verificado con una prueba "
            "estadística). Esto abre la puerta a un catálogo y recomendaciones localizados."
        )
        pais = st.selectbox("País", fuera["Country"].tolist())
        info = fuera[fuera["Country"] == pais].iloc[0]
        m1, m2, m3 = st.columns(3)
        m1.metric("Clientes", f"{int(info['clientes'])}")
        m2.metric("Ingresos", f"£{info['ingresos']/1e3:,.0f}K")
        m3.metric("Gasto por cliente", f"£{info['ingreso_por_cliente']:,.0f}")

        top, distintivos = proc.perfil_pais(pais)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"##### Productos más vendidos en {pais}")
            f = px.bar(top[::-1], orientation="h", color_discrete_sequence=["#0E7C86"])
            f.update_layout(showlegend=False, xaxis_title="Unidades", yaxis_title="")
            st.plotly_chart(fig(f, 360), use_container_width=True)
        with col_b:
            st.markdown(f"##### Productos distintivos de {pais}")
            st.caption("Lo que este país compra mucho más que el promedio (índice de especialización).")
            f = px.bar(distintivos[::-1], orientation="h", color_discrete_sequence=["#7C3AED"])
            f.update_layout(showlegend=False, xaxis_title="Veces sobre el promedio", yaxis_title="")
            st.plotly_chart(fig(f, 360), use_container_width=True)

        st.info(
            f"Los productos distintivos de {pais} son los que conviene destacar en su tienda y "
            "ofrecer en promociones locales, en vez de aplicar el mismo catálogo del Reino Unido."
        )


# --------------------------------------------------------------------------- #
# Fuga de clientes (regresión logística)
# --------------------------------------------------------------------------- #
def churn() -> None:
    encabezado("churn", "Fuga de clientes",
               "Probabilidad de que cada cliente no vuelva a comprar (regresión logística).")

    corte = st.selectbox(
        "Fecha de corte · se aprende del pasado y se predice si el cliente vuelve después",
        ["2011-08-01", "2011-09-01", "2011-10-01"], index=1)
    res = proc.modelo_churn(corte)

    c1, c2, c3 = st.columns(3)
    c1.metric("Tasa de fuga", f"{res['tasa_churn']*100:.0f}%")
    c2.metric("Capacidad del modelo (AUC)", f"{res['auc']:.2f}")
    c3.metric("Aciertos (accuracy)", f"{res['accuracy']*100:.0f}%")

    st.caption(
        "Churn = el cliente no volvió a comprar en el período futuro. El modelo usa solo el "
        "comportamiento pasado, así que la predicción es honesta. Un AUC de 0.74 indica que "
        "distingue bien a quién se va de quién se queda."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### Qué comportamientos predicen la fuga")
        coef = res["coef"].sort_values()
        f = px.bar(x=coef.values, y=coef.index, orientation="h",
                   color=["#E24B4A" if v > 0 else "#2E7D55" for v in coef.values],
                   color_discrete_map="identity")
        f.update_layout(xaxis_title="Efecto sobre la probabilidad de fuga", yaxis_title="")
        st.plotly_chart(fig(f, 360), use_container_width=True)
        st.caption("Verde reduce la fuga, rojo la aumenta. La frecuencia es el mayor escudo.")
    with col_b:
        st.markdown("##### Curva ROC")
        f = go.Figure()
        f.add_scatter(x=res["fpr"], y=res["tpr"], mode="lines",
                      line=dict(color="#B91C1C", width=2), name=f"AUC {res['auc']:.2f}")
        f.add_shape(type="line", x0=0, y0=0, x1=1, y1=1, line=dict(color="#999", dash="dash"))
        f.update_layout(xaxis_title="Falsos positivos", yaxis_title="Verdaderos positivos",
                        legend=dict(x=0.5, y=0.1))
        st.plotly_chart(fig(f, 360), use_container_width=True)

    st.markdown("##### Clientes valiosos en riesgo de fuga")
    st.caption("Prioridad de retención: alta probabilidad de fuga y alto gasto pasado.")
    feat = res["feat"]
    riesgo = st.slider("Probabilidad de fuga mínima", 0.5, 0.95, 0.7, 0.05)
    lista = feat[feat["prob_churn"] >= riesgo].sort_values("Monetario", ascending=False)
    lista = lista[["CustomerID", "prob_churn", "Recencia", "Frecuencia", "Monetario"]].head(20)
    st.dataframe(
        lista.rename(columns={"prob_churn": "Prob. fuga", "Monetario": "Gasto pasado (£)",
                              "Recencia": "Recencia (días)"})
        .style.format({"Prob. fuga": "{:.0%}", "Gasto pasado (£)": "£{:,.0f}"}),
        use_container_width=True, hide_index=True, height=320)
    st.download_button("Descargar lista de retención (CSV)",
                       lista.to_csv(index=False).encode("utf-8"),
                       "clientes_en_riesgo.csv", "text/csv")


# --------------------------------------------------------------------------- #
# Lealtad / NPS (datos simulados)
# --------------------------------------------------------------------------- #
def lealtad() -> None:
    encabezado("nps", "Lealtad de clientes (NPS)",
               "Net Promoter Score por segmento, con datos de encuesta simulados.")

    st.warning(
        "⚠️ Datos simulados. El dataset no contiene encuestas reales. Los puntajes se generan "
        "según el comportamiento de cada cliente para demostrar cómo se calcula y se lee el NPS.",
        icon="⚠️",
    )

    nps_df = proc.nps_simulado()
    nps_global = retail.calcular_nps(nps_df)

    c1, c2, c3 = st.columns(3)
    c1.metric("NPS global (simulado)", f"{nps_global:+.0f}")
    c2.metric("Promotores", f"{(nps_df['nps_cat']=='Promotor').mean()*100:.0f}%")
    c3.metric("Detractores", f"{(nps_df['nps_cat']=='Detractor').mean()*100:.0f}%")

    st.caption(
        "El NPS pregunta del 0 al 10 qué tan probable es recomendar la tienda. Los que responden "
        "9-10 son promotores, 7-8 pasivos y 0-6 detractores. El NPS es el % de promotores menos el "
        "% de detractores, va de -100 a 100."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### NPS por segmento")
        filas = []
        for seg in proc.ORDEN_SEGMENTOS:
            sub = nps_df[nps_df["Segmento"] == seg]
            if len(sub):
                filas.append({"Segmento": seg, "NPS": retail.calcular_nps(sub)})
        dnps = pd.DataFrame(filas)
        f = px.bar(dnps, x="Segmento", y="NPS",
                   color="Segmento", color_discrete_map=proc.COLORES_SEGMENTO)
        f.add_hline(y=0, line_color="#999")
        f.update_layout(showlegend=False, yaxis_title="NPS")
        st.plotly_chart(fig(f, 360), use_container_width=True)
    with col_b:
        st.markdown("##### Distribución de respuestas")
        dist = nps_df["nps_cat"].value_counts().reindex(["Promotor", "Pasivo", "Detractor"])
        f = px.pie(names=dist.index, values=dist.values, hole=0.45,
                   color=dist.index,
                   color_discrete_map={"Promotor": "#2E7D55", "Pasivo": "#F9A825", "Detractor": "#E24B4A"})
        st.plotly_chart(fig(f, 360), use_container_width=True)

    st.info(
        "El patrón simulado es coherente con el comportamiento, los Campeones son promotores netos "
        "y los clientes En riesgo, detractores. En la práctica, una encuesta real confirmaría o "
        "ajustaría esta lectura, y permitiría actuar sobre los detractores antes de perderlos."
    )


# --------------------------------------------------------------------------- #
# Pronóstico de ventas (Monte Carlo)
# --------------------------------------------------------------------------- #
def pronostico() -> None:
    encabezado("pronostico", "Pronóstico de ventas",
               "Proyección de ventas semanales con simulación de Monte Carlo.")

    c1, c2 = st.columns(2)
    with c1:
        horizonte = st.slider("Semanas a pronosticar", 4, 16, 12)
    with c2:
        n_sim = st.select_slider("Escenarios simulados", [500, 1000, 2000, 5000], 2000)

    serie = proc.serie_semanal()
    res = proc.pronostico(horizonte, n_sim)
    fut = res["futuro"]
    n = res["n_historia"]

    st.caption(
        "Monte Carlo genera miles de escenarios futuros sintéticos, sumándole a la tendencia un "
        "ruido tomado de la variación real observada. De esa nube de escenarios sale el valor "
        "esperado y las bandas de incertidumbre."
    )

    st.markdown("##### Ventas semanales, historia y pronóstico")
    f = go.Figure()
    f.add_scatter(x=list(range(n)), y=serie.values, mode="lines",
                  line=dict(color="#3B6FB6"), name="Historia")
    fx = list(range(n, n + horizonte))
    f.add_scatter(x=fx, y=fut["p90"], mode="lines", line=dict(width=0), showlegend=False)
    f.add_scatter(x=fx, y=fut["p10"], mode="lines", line=dict(width=0), fill="tonexty",
                  fillcolor="rgba(124,58,237,0.18)", name="Banda 80%")
    f.add_scatter(x=fx, y=fut["media"], mode="lines",
                  line=dict(color="#7C3AED", dash="dash"), name="Esperado")
    f.update_layout(xaxis_title="Semana", yaxis_title="Ventas (£)",
                    legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig(f, 380), use_container_width=True)

    st.markdown(f"##### Distribución del total de las próximas {horizonte} semanas")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        f = px.histogram(x=res["totales"] / 1e6, nbins=40, color_discrete_sequence=["#7C3AED"])
        f.add_vline(x=res["esperado_total"] / 1e6, line_color="#222", line_dash="dash")
        f.update_layout(xaxis_title="Ventas totales (£M)", yaxis_title="Escenarios")
        st.plotly_chart(fig(f, 320), use_container_width=True)
    with col_b:
        st.metric("Valor esperado", f"£{res['esperado_total']/1e6:.2f}M")
        st.metric("Desviación (incertidumbre)", f"£{res['desviacion_total']/1e3:,.0f}K")
        objetivo = st.number_input("Meta de ventas (£M)", 1.0, 6.0, 2.5, 0.5)
        prob = (res["totales"] > objetivo * 1e6).mean() * 100
        st.metric(f"Prob. de superar £{objetivo:.1f}M", f"{prob:.0f}%")

    st.info(
        "Como solo hay un año de datos, el pronóstico es de horizonte corto y no captura la caída "
        "post-navideña. Su valor está en mostrar el rango de incertidumbre, no un número exacto."
    )


# --------------------------------------------------------------------------- #
# 5. Simulador
# --------------------------------------------------------------------------- #
def simulador() -> None:
    encabezado("simulador", "Simulador de escenarios",
               "Proyectá el impacto de distintas estrategias sobre los ingresos.")

    dc = proc.datos_cliente()
    rfm = proc.segmentar(4)
    base = dc["TotalPrice"].sum()

    champ = rfm[rfm["Segmento"] == "Campeones"]
    ids_may = proc.clientes_mayoristas(1000)

    st.markdown("##### Palancas de la estrategia")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Fidelizar campeones**")
        uplift_champ = st.slider("Aumento de gasto de campeones (%)", 0, 50, 10, key="champ")
    with col2:
        st.markdown("**Captar mayoristas**")
        nuevos_may = st.slider("Nuevos clientes mayoristas", 0, 100, 20, key="may")
    with col3:
        st.markdown("**Promoción cruzada**")
        conv_cross = st.slider("Conversión de recomendaciones (%)", 0, 30, 10, key="cross")

    # Monte Carlo: cada palanca es incierta, se simulan miles de escenarios
    gastos_may = (dc[dc["CustomerID"].isin(ids_may)].groupby("CustomerID")["TotalPrice"]
                  .sum().values)
    ticket = dc.groupby("InvoiceNo")["TotalPrice"].sum().mean()
    sim = retail.simular_negocio_montecarlo(
        base=base, ingreso_campeones=champ["Monetario"].sum(), gastos_mayoristas=gastos_may,
        n_facturas=dc["InvoiceNo"].nunique(), ticket_medio=ticket,
        uplift_champ=uplift_champ, nuevos_mayoristas=nuevos_may, conversion_cross=conv_cross,
    )
    p10, p50, p90 = np.percentile(sim, [10, 50, 90])
    crecimiento = (sim.mean() - base) / base * 100

    st.write("")
    st.caption(
        "Cada palanca tiene un resultado incierto, no un número fijo. Monte Carlo simula miles de "
        "escenarios para mostrar el rango probable, no una falsa precisión."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos actuales", f"£{base/1e6:.2f}M")
    c2.metric("Ingresos proyectados (esperado)", f"£{sim.mean()/1e6:.2f}M", f"+{crecimiento:.1f}%")
    c3.metric("Rango probable (80%)", f"£{p10/1e6:.2f}M – £{p90/1e6:.2f}M")

    st.write("")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown("##### Distribución de los ingresos proyectados")
        f = px.histogram(x=sim / 1e6, nbins=40, color_discrete_sequence=["#0E7C86"])
        f.add_vline(x=base / 1e6, line_color="#999", line_dash="dash",
                    annotation_text="actual", annotation_position="top")
        f.add_vline(x=sim.mean() / 1e6, line_color="#222", line_dash="dash",
                    annotation_text="esperado", annotation_position="top")
        f.update_layout(xaxis_title="Ingresos proyectados (£M)", yaxis_title="Escenarios")
        st.plotly_chart(fig(f, 340), use_container_width=True)
    with col_b:
        st.metric("Ingreso adicional esperado", f"£{(sim.mean()-base)/1e3:,.0f}K")
        st.metric("Incertidumbre (desviación)", f"£{sim.std()/1e3:,.0f}K")
        meta = st.number_input("Meta de crecimiento (%)", 0.0, 30.0, 5.0, 1.0)
        prob = (sim > base * (1 + meta / 100)).mean() * 100
        st.metric(f"Prob. de crecer más de {meta:.0f}%", f"{prob:.0f}%")

    st.caption(
        "Fidelizar campeones aplica el aumento sobre su gasto actual, captar mayoristas suma clientes "
        "con gasto muestreado de los mayoristas reales, y la promoción cruzada estima ventas extra "
        "sobre las facturas. La variabilidad de cada palanca alimenta la incertidumbre del total."
    )
