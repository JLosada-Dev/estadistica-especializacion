# Guía de exposición — Análisis completo de un retailer online

Guía para entender y presentar el notebook `Taller_4_retail_analisis_completo.ipynb`. Cada sección dice qué se hizo, qué dio y la frase clave para exponer.

---

## La idea en una frase

Se analiza un año de ventas de una tienda online del Reino Unido para responder quiénes son los mejores clientes y qué productos conviene recomendar o promocionar juntos. La respuesta corta es que el negocio depende de un puñado de clientes, que existe un nicho mayorista muy rentable, y que hay combinaciones de productos no obvias que se pueden aprovechar para vender más.

## La pregunta que guía todo

¿Quiénes son los mejores clientes del retailer y qué productos conviene recomendarles o promocionar juntos para vender más?

## El dataset en una frase

Medio millón de transacciones del Reino Unido entre diciembre de 2010 y diciembre de 2011, donde cada fila es un producto dentro de una factura, con su cantidad, precio, fecha y cliente.

---

## Recorrido por secciones

### 1. Exploración inicial
- **Qué se hizo.** Una primera mirada a tipos de datos, nulos, duplicados y valores imposibles.
- **Qué dio.** Aparecieron seis problemas de calidad, entre ellos un 25% de filas sin cliente, cancelaciones y precios negativos.
- **Frase clave.** "Antes de analizar hay que entender qué problemas trae el dato."

### 2. Limpieza
- **Qué se hizo.** Se filtró al Reino Unido, se quitaron cancelaciones, duplicados, valores no positivos y entradas que no son productos como gastos de envío. Se conservaron las filas sin cliente para el análisis de productos y se separaron para la segmentación.
- **Punto crítico de los outliers.** Se analizaron con boxplots y se decidió conservarlos, porque las compras enormes no son errores sino clientes mayoristas reales.
- **El balance.** El coeficiente de Gini de 0.70 muestra que el negocio está muy concentrado en pocos compradores, no es un dataset equilibrado.
- **Frase clave.** "Limpiamos sin borrar lo valioso, los outliers son el mejor negocio."

### 3. Análisis estadístico
- **Qué se hizo.** Se estudiaron las distribuciones, la estacionalidad, los productos top y la concentración de ingresos.
- **Qué dio.**
  - El gasto por cliente sigue una distribución log-normal, lo que permite estimar cuántos clientes de alto valor esperar.
  - El ticket promedio ronda las 490 libras.
  - Las ventas tienen una estacionalidad fuerte y significativa, con pico antes de Navidad.
  - El 27% de los clientes genera el 80% de los ingresos, principio de Pareto.
- **Frase clave.** "Pocos clientes y pocos meses concentran casi todo el negocio."

### 4. Segmentación de clientes
- **Qué se hizo.** Se resumió a cada cliente con el modelo RFM, recencia, frecuencia y monto, y se agrupó con K-Means.
- **Qué dio.** Cuatro segmentos claros, Campeones, Leales, Ocasionales y En riesgo, validados con un mapa visual y con una prueba estadística que confirma que difieren de verdad.
- **Frase clave.** "Cuatro tipos de cliente, cada uno con su estrategia."

### 5. Detección del nicho mayorista
- **Qué se hizo.** Se aislaron los compradores de gran volumen y se comprobó si son un mercado aparte.
- **Qué dio.**
  - 163 clientes, apenas un 4%, generan más de un tercio de los ingresos y gastan trece veces más que un minorista.
  - Una prueba de chi-cuadrado confirma que compran productos distintos, artículos para revender en vez de decoración.
- **Frase clave.** "Hay un mercado mayorista escondido que vale oro y necesita su propia estrategia."

### 6. Reglas de asociación
- **Qué se hizo.** Se buscaron productos que se compran juntos para generar recomendaciones, separando las combinaciones obvias de las realmente útiles.
- **Qué dio.** Las recomendaciones valiosas son las de venta cruzada entre categorías distintas, como una bolsa con un juguete o un juego de cartas con un dominó, con una asociación muy por encima del azar.
- **Frase clave.** "Recomendar lo que el cliente no buscaba pero otros como él sí compraron."

### 7. Tablero resumen
- **Qué se hizo.** Un panel único que reúne indicadores del negocio, segmentos, Pareto, productos top y recomendaciones.
- **Frase clave.** "Todo el análisis en una sola vista para decidir."

### 8. Conclusiones
- El negocio depende de una minoría de clientes, identificada y nombrada por la segmentación.
- Existe un nicho mayorista muy rentable con un comportamiento y un surtido propios.
- Las reglas de asociación dan recomendaciones cruzadas accionables.
- Cada etapa alimentó a la siguiente, de la limpieza al tablero final.

---

## Mensajes para cerrar la exposición

1. **El negocio se sostiene sobre pocos.** Un 27% de clientes hace el 80% de las ventas, y un 4% mayorista aporta más de un tercio. Retenerlos es la prioridad.
2. **El nicho mayorista es la gran oportunidad.** Compra distinto, gasta trece veces más y se abastece antes de Navidad. Merece precios por volumen y atención dedicada.
3. **Las recomendaciones útiles son las no obvias.** El valor no está en sugerir el plato que va con la taza, sino en cruzar categorías distintas.
4. **La estadística guió cada decisión.** Distribuciones, pruebas de hipótesis y segmentación validada convierten intuiciones en conclusiones con respaldo.

## Posibles preguntas del público

- **¿Por qué se quedaron solo con el Reino Unido?** Concentra el 91% de las ventas y evita mezclar mercados de tamaños muy distintos.
- **¿Por qué no eliminaron los outliers?** Porque son compras mayoristas reales que aportan casi la mitad de los ingresos. Borrarlos destruiría el mejor segmento.
- **¿Por qué cuatro grupos de clientes y no dos?** La medida de calidad prefería dos, pero cuatro grupos son más accionables para marketing, distinguen campeones, leales, ocasionales y en riesgo.
- **¿Las reglas de asociación predicen el futuro?** No, describen patrones de compra conjunta observados. Sirven para recomendar, no para pronosticar.
- **¿El nicho mayorista causa la estacionalidad?** Contribuye, ya que se abastece en otoño, pero la estacionalidad también viene del consumidor final que compra para Navidad.

## Glosario rápido

- **RFM.** Resumen de un cliente en tres números, hace cuánto compró, cuántas veces y cuánto gastó.
- **K-Means.** Algoritmo que agrupa clientes parecidos sin que se le diga de antemano cuáles son los grupos.
- **Lift.** Cuánto más se compran dos productos juntos frente a lo esperable por azar. Un lift de 10 es diez veces más.
- **Soporte y confianza.** Qué tan común es una combinación, y qué tan seguido se cumple la recomendación.
- **Pareto.** La idea de que una minoría concentra la mayoría del resultado, el clásico 80-20.
- **Gini.** Mide concentración, de 0 reparto perfecto a 1 todo en pocas manos.
- **Distribución log-normal.** Cuando una variable no es normal pero su logaritmo sí, típico del gasto en consumo.
- **PCA.** Técnica que resume varias variables en dos para poder dibujar los grupos en un plano.
