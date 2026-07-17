# Guía de exposición — Dashboard de retail

Guía para presentar el dashboard interactivo de análisis de retail. Cada sección dice qué muestra, qué mover en vivo para impresionar, y el mensaje de negocio para el cliente.

---

## Qué es

Un dashboard interactivo que reúne todo el análisis de una tienda online del Reino Unido, de la descripción del negocio a la predicción y la simulación. Responde una pregunta central.

> **¿Quiénes son los mejores clientes y qué conviene venderles para crecer?**

Tiene **10 secciones**, agrupadas en tres bloques: entender el negocio, conocer a los clientes y proyectar el futuro.

## Cómo lanzarlo

Desde la raíz del proyecto:

```bash
uv run streamlit run dashboards/retail/app.py
```

Se abre en el navegador. La primera carga tarda unos segundos (lee y limpia los datos), después todo es instantáneo.

## Antes de empezar, dos advertencias de honestidad

Para presentar con transparencia, hay dos cosas que conviene aclarar de entrada.

- La sección de **Lealtad (NPS)** usa **datos de encuesta simulados**, porque el dataset no tiene encuestas. Está marcado en pantalla.
- El **punto de equilibrio** y el **simulador** usan **supuestos del usuario** (costos, conversiones), no datos reales. También están marcados.

Todo lo demás son datos reales del negocio.

---

## Recorrido por las secciones

### 1. Resumen
- **Qué muestra.** Los indicadores del negocio, ventas por mes, concentración de ingresos (Pareto) y top de productos. Al final, una calculadora de punto de equilibrio.
- **En vivo.** Mové el rango de meses y mirá cómo cambian los KPIs. En el punto de equilibrio, ingresá un costo fijo y un margen, y mostrá cómo el gráfico marca a partir de cuánto el negocio gana.
- **Mensaje.** "El negocio factura millones, pero depende de pocos clientes, y acá vemos a partir de qué nivel de ventas deja ganancia."

### 2. Segmentación de clientes
- **Qué muestra.** Los clientes agrupados por comportamiento (RFM enriquecido) en cuatro segmentos: Campeones, Leales, Ocasionales y En riesgo. Incluye el mapa PCA y el perfil de cada grupo.
- **En vivo.** Mové el slider del número de grupos y mostrá cómo se reorganizan los clientes y cambia la calidad de la separación.
- **Mensaje.** "No todos los clientes son iguales. Estos cuatro tipos piden estrategias distintas, y la antigüedad nos deja distinguir a un cliente nuevo con potencial de uno que se está yendo."

### 3. Valor del cliente
- **Qué muestra.** Una regresión que predice cuánto gastará cada cliente en el futuro, con su poder predictivo y qué comportamientos lo anticipan.
- **En vivo.** Cambiá la fecha de corte y mostrá que el modelo aprende del pasado para predecir el futuro, sin trampa.
- **Mensaje.** "Podemos estimar cuánto vale cada cliente a futuro. La frecuencia de compra es la mejor señal, lo que confirma que hay que mantener a la gente comprando seguido."

### 4. Fuga de clientes
- **Qué muestra.** Una regresión logística que estima la probabilidad de que cada cliente no vuelva a comprar, con la curva ROC y una lista de clientes valiosos en riesgo.
- **En vivo.** Mové el slider de probabilidad de fuga y mostrá cómo aparece la lista de retención. Descargá el CSV.
- **Mensaje.** "Sabemos con anticipación a quién estamos por perder. Esta lista, clientes valiosos a punto de irse, es donde una campaña de retención rinde más."

### 5. Mercados internacionales
- **Qué muestra.** El negocio más allá del Reino Unido. En la pestaña Panorama, un mapa y los mercados por perfil. En Análisis por país, los productos preferidos y distintivos de cada país.
- **En vivo.** En el mapa, pasá el mouse por los países. En la segunda pestaña, elegí un país y mostrá qué productos compra de más respecto al promedio.
- **Mensaje.** "Cada país compra distinto, lo confirmamos con una prueba estadística. Eso abre la puerta a un catálogo localizado, y a detectar mercados de alto valor como Irlanda para expandirse."

### 6. Lealtad (NPS)
- **Qué muestra.** El Net Promoter Score por segmento. **Datos simulados.**
- **En vivo.** Mostrá que los Campeones son promotores y los clientes En riesgo, detractores.
- **Mensaje.** "Con datos de encuesta, mediríamos la lealtad así. La simulación muestra el patrón esperable, los mejores clientes recomiendan y los que se van están descontentos."

### 7. Pronóstico de ventas
- **Qué muestra.** Una proyección de ventas con simulación de Monte Carlo, con bandas de incertidumbre y la distribución de resultados.
- **En vivo.** Mové el horizonte y la cantidad de escenarios. Cambiá la meta de ventas y mostrá la probabilidad de alcanzarla.
- **Mensaje.** "Un buen pronóstico no da un número, da un rango. Monte Carlo simula miles de futuros posibles y nos dice no solo cuánto esperamos vender, sino con qué probabilidad superamos una meta."

### 8. Nicho mayorista
- **Qué muestra.** El grupo de compradores de gran volumen, su peso en los ingresos y los productos que prefieren.
- **En vivo.** Mové el umbral de unidades que define a un mayorista.
- **Mensaje.** "Dentro de los datos hay un mercado escondido. Pocos clientes mayoristas generan más de un tercio de los ingresos. Merecen un trato y un catálogo propios."

### 9. Recomendaciones
- **Qué muestra.** Cuatro pestañas. Paquetes de promoción listos, explorador por producto, la tabla cruzada de afinidad con paquetes temáticos, y todas las reglas.
- **En vivo.** Mové los sliders de lift y confianza y mirá cómo cambian las recomendaciones. En la tabla cruzada, mostrá el heatmap y los paquetes temáticos que arma solo.
- **Mensaje.** "Sabemos qué productos se compran juntos. Esto se traduce en paquetes de promoción concretos, desde pares hasta combos temáticos de varios productos, para vender más por venta cruzada."

### 10. Simulador
- **Qué muestra.** Un simulador de escenarios con Monte Carlo. Tres palancas de estrategia y la distribución de ingresos proyectados.
- **En vivo.** Mové las palancas, fidelizar campeones, captar mayoristas, promoción cruzada, y mostrá cómo cambia el ingreso esperado y la probabilidad de cumplir una meta de crecimiento.
- **Mensaje.** "Acá el cliente juega con su estrategia. Como cada palanca es incierta, no damos un número falso sino un rango probable, que es como se decide en la realidad."

---

## Flujo narrativo sugerido (10-15 min)

Un orden que cuenta una historia.

1. **Resumen** — "Este es el negocio: tamaño, estacionalidad y a partir de cuánto gana."
2. **Segmentación** — "Sus clientes no son uno solo, son cuatro tipos."
3. **Valor y Fuga** — "De cada cliente sabemos cuánto vale y qué riesgo hay de perderlo."
4. **Nicho mayorista y Mercados** — "Hay oro escondido: un nicho mayorista y mercados internacionales que compran distinto."
5. **Recomendaciones** — "Y sabemos exactamente qué ofrecerles para vender más."
6. **Pronóstico y Simulador** — "Por último, proyectamos el futuro y simulamos estrategias con su incertidumbre."

Cierre: "De entender el negocio a decidir qué hacer, todo en una herramienta interactiva."

---

## Las técnicas detrás (por si preguntan)

| Sección | Técnica |
|---|---|
| Segmentación | RFM enriquecido + K-Means + PCA |
| Valor del cliente | Regresión lineal múltiple con split temporal |
| Fuga | Regresión logística |
| Mercados | Chi-cuadrado de independencia |
| Pronóstico y Simulador | Simulación de Monte Carlo |
| Recomendaciones | Reglas de asociación (FP-Growth) + clustering jerárquico |
| Nicho | Chi-cuadrado |

## Preguntas frecuentes

- **¿Los datos son reales?** Sí, son transacciones reales de un retailer. Las únicas partes simuladas, la encuesta de NPS y los supuestos de costos del punto de equilibrio y el simulador, están marcadas en pantalla.
- **¿Por qué el pronóstico no es un solo número?** Porque predecir con certeza es imposible. Monte Carlo da el rango realista de lo que puede pasar.
- **¿Por qué no incluyeron el país en el modelo de fuga?** Lo probamos y la geografía no influía de forma significativa en la fuga, así que no lo agregamos para no meter ruido.
- **¿Se puede publicar online?** Sí, está preparado para subir a Streamlit Community Cloud y compartir por un link.

## Glosario rápido

- **RFM.** Resumen de un cliente en recencia, frecuencia y monto.
- **Lift.** Cuánto más se compran dos productos juntos frente al azar.
- **AUC.** Qué tan bien un modelo distingue dos grupos, de 0.5 (azar) a 1 (perfecto).
- **Monte Carlo.** Simular miles de escenarios al azar para obtener una distribución de resultados.
- **NPS.** Net Promoter Score, mide la lealtad de 0 a 100 según promotores menos detractores.
- **Punto de equilibrio.** El nivel de ventas donde la utilidad es cero.
