# Guía de exposición — Taller 4, Retail y Aprendizaje No Supervisado

Guía para entender y presentar el notebook `Taller_4_retail_analisis_completo.ipynb`. Pensada para aprender el contenido y exponerlo con fluidez. Cada sección dice qué se hizo, por qué, qué dio y la frase clave para decir en voz alta.

---

## La idea en una frase

Se analizó un año de ventas de una tienda online del Reino Unido para responder quiénes son los mejores clientes y qué productos conviene recomendar o promocionar juntos. La respuesta corta es que el negocio depende de un puñado de clientes, que existe un nicho mayorista muy rentable, y que hay combinaciones de productos no obvias que se pueden aprovechar para vender más.

## La pregunta que guía todo

¿Quiénes son los mejores clientes del retailer y qué productos conviene recomendarles o promocionar juntos para vender más?

## Qué es el aprendizaje no supervisado (para arrancar la charla)

En el aprendizaje supervisado se le enseña al modelo con respuestas conocidas, por ejemplo fotos etiquetadas como perro o gato. En el **no supervisado no hay respuestas**, el modelo descubre patrones por su cuenta. En este taller se usan dos técnicas no supervisadas, el **clustering** para agrupar clientes parecidos sin decirle de antemano cuáles son los grupos, y las **reglas de asociación** para descubrir qué productos se compran juntos.

## El dataset en una frase

Medio millón de transacciones del Reino Unido entre diciembre de 2010 y diciembre de 2011, donde cada fila es un producto dentro de una factura, con su cantidad, precio, fecha y cliente.

---

## Recorrido por secciones

### 1. Exploración inicial
- **Qué se hizo.** Una primera mirada a tipos de datos, nulos, duplicados y valores imposibles.
- **Qué dio.** Aparecieron seis problemas de calidad, entre ellos un 25% de filas sin cliente, cancelaciones y precios negativos.
- **Frase clave.** "Antes de analizar hay que entender qué problemas trae el dato."

### 2. Limpieza
- **Qué se hizo.** Se filtró al Reino Unido, se quitaron cancelaciones, duplicados, valores no positivos y entradas que no son productos como gastos de envío o ajustes manuales. Se conservaron las filas sin cliente para el análisis de productos y se separaron para la segmentación.
- **El punto crítico de los outliers.** Se analizaron con diagramas de caja y se decidió conservarlos, porque las compras enormes no son errores sino clientes mayoristas reales.
- **El balance del dataset.** El coeficiente de Gini de 0.70 muestra que el negocio está muy concentrado en pocos compradores, no es un dataset equilibrado.
- **Frase clave.** "Limpiamos sin borrar lo valioso, los outliers son el mejor negocio."

### 3. Análisis estadístico
- **Qué se hizo.** Se estudiaron las distribuciones del gasto, la estacionalidad, los productos top y la concentración de ingresos.
- **Qué dio.**
  - El gasto por cliente sigue una distribución **log-normal**, lo que permite estimar cuántos clientes de alto valor esperar (ver el bloque dedicado más abajo).
  - El ticket promedio ronda las 490 libras, con su intervalo de confianza.
  - Las ventas tienen una estacionalidad fuerte y estadísticamente significativa, con pico antes de Navidad.
  - El 27% de los clientes genera el 80% de los ingresos, principio de Pareto.
- **Frase clave.** "Pocos clientes y pocos meses concentran casi todo el negocio."

### 4. Segmentación de clientes
- **Qué se hizo.** Se resumió a cada cliente con el modelo RFM, recencia, frecuencia y monto, y se agrupó con K-Means.
- **Qué es RFM.** Tres números por cliente, hace cuánto compró (recencia), cuántas veces (frecuencia) y cuánto gastó (monto). Es el estándar para medir el valor de un cliente.
- **Cómo se eligieron los grupos.** Con el coeficiente de silueta, que mide qué tan separados están, combinado con el criterio de que los grupos fueran útiles para marketing.
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
- **Las tres métricas.** El soporte mide qué tan común es una combinación, la confianza la probabilidad de que se cumpla la recomendación, y el lift cuánto más se compran juntos frente al azar.
- **Qué dio.** Las recomendaciones valiosas son las de venta cruzada entre categorías distintas, como una bolsa con un juguete o un juego de cartas con un dominó, con un lift muy por encima del azar.
- **Frase clave.** "Recomendar lo que el cliente no buscaba pero otros como él sí compraron."

### 7. Tablero resumen
- **Qué se hizo.** Un panel con once vistas que reúne indicadores del negocio, ventas por mes, segmentos, Pareto, productos top, recomendaciones cruzadas y el nicho mayorista con su estacionalidad y su reparto de ingresos.
- **Frase clave.** "Todo el análisis en una sola vista para decidir."

### 8. Conclusiones
- Se presentan **segmentadas por etapa**, limpieza, estadística, segmentación, nicho, reglas y cierre, para mostrar cómo cada una alimentó a la siguiente.
- El negocio depende de una minoría de clientes, identificada y nombrada por la segmentación.
- Existe un nicho mayorista muy rentable con un comportamiento y un surtido propios.
- Las reglas de asociación dan recomendaciones cruzadas accionables.
- Cada etapa alimentó a la siguiente, de la limpieza al tablero final.

---

## Bloque especial, por qué log-normal y no la distribución normal

Esta es una de las partes más importantes de la parte estadística y conviene explicarla bien.

### El problema con la distribución normal

La distribución normal es la clásica campana **simétrica**, donde los datos se reparten parejo a ambos lados del promedio. Funciona para cosas como la estatura o las notas de un examen. Pero el gasto de los clientes **no se comporta así**. La mayoría gasta poco y unos pocos gastan cantidades enormes, lo que genera una distribución muy torcida hacia la derecha, con una cola larga.

Si se intentara describir el gasto con una normal, el modelo fallaría feo. Predeciría incluso gastos negativos, que son imposibles, y subestimaría por completo a los grandes compradores.

### Qué es la distribución log-normal

Una variable es log-normal cuando **no es normal, pero su logaritmo sí lo es**. En otras palabras, si en lugar del gasto se mira el logaritmo del gasto, esa nueva variable sí forma una campana simétrica.

Aplicar el logaritmo tiene el efecto de **comprimir la cola larga**, acerca los valores gigantes al resto y simétriza la distribución. En el notebook se vio que la asimetría del gasto cae de más de 20 a casi cero al tomar el logaritmo, y que la regla 68-95-99.7 se cumple con mucha precisión sobre el log del gasto.

### Por qué el gasto tiende a ser log-normal

La intuición es la siguiente. Una distribución normal aparece cuando muchos factores **se suman**. Una log-normal aparece cuando muchos factores **se multiplican**. El gasto de un cliente es un producto de varios factores, cuántas veces visita la tienda, cuántos productos lleva por visita y el precio de cada uno. Como esos factores se multiplican, el resultado tiende naturalmente a una log-normal. Es un patrón típico en consumo, ingresos y precios.

### Para qué sirve saberlo

Tiene tres beneficios concretos.

Primero, permite **calcular probabilidades** de negocio. Una vez que se sabe que el gasto es log-normal, se puede estimar qué porcentaje de clientes superará cierto monto. En el notebook el modelo estimó que cerca del 6% supera las 5.000 libras y un 2% las 10.000, valores casi idénticos a los reales.

Segundo, da un criterio **objetivo** para definir a un cliente premium, en lugar de elegir un umbral a dedo.

Tercero, **justifica una decisión técnica**. En la segmentación se transforman las variables con logaritmo antes de agrupar, precisamente para que los pocos clientes de gasto enorme no aplasten al resto y el algoritmo encuentre grupos sensatos.

### Cómo decirlo en una frase

"El gasto no es una campana normal porque casi todos gastan poco y unos pocos gastan muchísimo. Pero el logaritmo del gasto sí es normal, eso se llama log-normal, y nos sirve para estimar cuántos clientes de alto valor esperar y para que el algoritmo de segmentación no se desbalancee."

---

## Mensajes para cerrar la exposición

1. **El negocio se sostiene sobre pocos.** Un 27% de clientes hace el 80% de las ventas, y un 4% mayorista aporta más de un tercio. Retenerlos es la prioridad.
2. **El nicho mayorista es la gran oportunidad.** Compra distinto, gasta trece veces más y se abastece antes de Navidad. Merece precios por volumen y atención dedicada.
3. **Las recomendaciones útiles son las no obvias.** El valor no está en sugerir el plato que va con la taza, sino en cruzar categorías distintas.
4. **La estadística guió cada decisión.** Distribuciones, pruebas de hipótesis y segmentación validada convierten intuiciones en conclusiones con respaldo.

## Posibles preguntas del público

- **¿Por qué se quedaron solo con el Reino Unido?** Concentra el 91% de las ventas y evita mezclar mercados de tamaños muy distintos.
- **¿Por qué no eliminaron los outliers?** Porque son compras mayoristas reales que aportan casi la mitad de los ingresos. Borrarlos destruiría el mejor segmento.
- **¿Por qué log-normal y no normal?** Porque el gasto está muy torcido, casi todos gastan poco y pocos gastan muchísimo. Su logaritmo sí es una campana, y eso permite calcular probabilidades y evitar que los grandes compradores desbalanceen la segmentación.
- **¿Por qué cuatro grupos de clientes y no dos?** La medida de calidad prefería dos, pero cuatro grupos son más accionables para marketing, distinguen campeones, leales, ocasionales y en riesgo.
- **¿Las reglas de asociación predicen el futuro?** No, describen patrones de compra conjunta observados. Sirven para recomendar, no para pronosticar.
- **¿El nicho mayorista causa la estacionalidad?** Contribuye, ya que se abastece en otoño, pero la estacionalidad también viene del consumidor final que compra para Navidad.

## Glosario rápido

- **Aprendizaje no supervisado.** El modelo descubre patrones sin que se le den respuestas de antemano.
- **RFM.** Resumen de un cliente en tres números, hace cuánto compró, cuántas veces y cuánto gastó.
- **K-Means.** Algoritmo que agrupa clientes parecidos sin que se le diga cuáles son los grupos.
- **Coeficiente de silueta.** Mide qué tan bien separados quedaron los grupos, de -1 a 1.
- **Lift.** Cuánto más se compran dos productos juntos frente a lo esperable por azar. Un lift de 10 es diez veces más.
- **Soporte y confianza.** Qué tan común es una combinación, y qué tan seguido se cumple la recomendación.
- **Pareto.** La idea de que una minoría concentra la mayoría del resultado, el clásico 80-20.
- **Gini.** Mide concentración, de 0 reparto perfecto a 1 todo en pocas manos.
- **Distribución normal.** La campana simétrica clásica, sirve cuando los datos se reparten parejo alrededor del promedio.
- **Distribución log-normal.** Cuando una variable no es normal pero su logaritmo sí, típico del gasto, los ingresos y los precios.
- **PCA.** Técnica que resume varias variables en dos para poder dibujar los grupos en un plano.
- **Chi-cuadrado.** Prueba que verifica si dos cosas están relacionadas o son independientes.
