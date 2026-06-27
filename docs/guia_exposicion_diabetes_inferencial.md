# Guía de exposición — Taller 3, Diabetes y Estadística Inferencial

Guía pensada para **entender de verdad** cada parte del notebook `Taller_3_diabetes_inferencial.ipynb` y poder exponerlo con tranquilidad, sin tecnicismos. Cada concepto se explica primero con palabras simples y un ejemplo, y después se conecta con lo que hicimos.

---

## La historia en una frase

Teníamos 442 pacientes con diabetes y queríamos saber **qué hace que la enfermedad avance rápido o lento**. Después de aplicar varias herramientas estadísticas, la respuesta fue clara: lo que más influye es el **peso, los triglicéridos y la presión arterial**, mientras que el **sexo no tiene nada que ver**.

## Antes de empezar, dos ideas que se repiten todo el tiempo

Si entendés estas dos cosas, entendés el 80% del taller.

**1. ¿Qué es la estadística inferencial?**
Imaginá que probás una cucharada de sopa para saber si le falta sal. No te tomás toda la olla, con una cucharada **inferís** cómo está el resto. Eso es la estadística inferencial: sacar conclusiones generales a partir de una muestra, y además decir **qué tan confiable** es esa conclusión.

**2. ¿Qué es el p-valor?**
Es el número que nos dice si un resultado es **real o pura casualidad**. La regla es simple:
- **p menor a 0.05** → el resultado es real, no es suerte. "Esto significa algo."
- **p mayor a 0.05** → podría ser casualidad. "No hay evidencia suficiente."

Pensalo como un detector de coincidencias. Si tirás una moneda 3 veces y salen 3 caras, podría ser suerte (p alto). Si salen 20 caras seguidas, ya no es suerte, la moneda está cargada (p bajo).

## Los datos en una frase

Cada paciente tiene 10 medidas (edad, sexo, peso o BMI, presión y seis análisis de sangre llamados S1 a S6) y un número final `Y` que mide **cuánto avanzó su diabetes un año después**. Ese `Y` es lo que queremos explicar.

---

## Recorrido por el notebook, sección por sección

### 1. Estadística descriptiva — la foto inicial
- **Qué hicimos.** Calculamos promedios y vimos cómo se reparte cada variable.
- **Por qué.** Es como mirar el paisaje antes de salir a caminar. Necesitamos conocer los datos antes de sacar conclusiones.
- **Para decir.** "Arrancamos conociendo cómo se comporta cada medida."

### 2. Distribución normal — ¿los datos tienen forma de campana?
- **La idea simple.** Muchas cosas en la naturaleza se reparten en forma de **campana**: la mayoría de los valores en el medio y pocos en los extremos. La estatura, por ejemplo. A eso se le llama distribución normal.
- **Qué hicimos.** Revisamos si nuestras variables tenían esa forma de campana, con un gráfico (el Q-Q plot) y una prueba (la de Shapiro).
- **Qué encontramos.** Ninguna tiene forma de campana perfecta. El peso se acerca, la progresión no tanto.
- **Por qué importa.** Algunas pruebas que vienen después **suponen** que los datos son normales. Como no lo son del todo, decidimos acompañar cada prueba con una versión de respaldo que no necesita esa forma de campana.
- **Para decir.** "Los datos no son una campana perfecta, así que tomamos precauciones en todo el análisis."

### 3. Probabilidad condicional y Bayes — ¿saber el peso cambia algo?
- **La idea simple.** Una probabilidad condicional es la chance de algo **sabiendo otra cosa**. Por ejemplo, la chance de que llueva en general es una, pero la chance de que llueva **sabiendo que el cielo está negro** es otra mucho mayor.
- **Qué hicimos.** Comparamos la chance de progresión alta en general contra la chance sabiendo que el paciente tiene peso alto.
- **Qué encontramos.** Sin saber nada, la chance de progresión alta es **50%**. Pero si el paciente tiene peso alto, sube a **71%**, y si tiene peso bajo, baja a **30%**.
- **Para decir.** "Saber el peso de un paciente cambia bastante lo que podemos esperar de su enfermedad."

### 4. Distribución binomial — contar casos en un grupo
- **La idea simple.** La binomial sirve para situaciones de **sí o no** que se repiten. Como tirar una moneda 10 veces y preguntarse cuántas caras saldrán.
- **Qué hicimos.** Calculamos, si tomamos pacientes al azar, cuántos esperaríamos que tengan progresión alta.
- **Qué encontramos.** En un grupo de 10, lo más probable es que 5 tengan progresión alta. Encontrar 8 o más sería raro.
- **Para decir.** "Una forma de razonar con probabilidades sobre grupos de pacientes."

### 5. T-Test — ¿hombres y mujeres avanzan distinto?
- **La idea simple.** El T-Test sirve para responder **¿estos dos grupos son realmente distintos, o la diferencia es casualidad?** Compara los promedios de dos grupos.
- **Qué hicimos.** Comparamos la progresión entre hombres y mujeres. Y para estar seguros, lo confirmamos con otra prueba (Mann-Whitney) y medimos el **tamaño de la diferencia** (el d de Cohen).
- **Por qué tres cosas.** El T-Test dice si hay diferencia. Mann-Whitney lo confirma sin depender de la forma de campana. Y el tamaño del efecto dice si esa diferencia, aunque exista, es **grande o insignificante**.
- **Qué encontramos.** No hay diferencia, y el tamaño es prácticamente cero. El sexo no importa.
- **Para decir.** "El sexo no influye en cómo avanza la diabetes, lo confirmamos por tres caminos distintos."

### 6. ANOVA — ¿el peso marca una diferencia?
- **La idea simple.** El ANOVA es como el T-Test pero para **más de dos grupos**. Divide a los pacientes en grupos (peso bajo, medio y alto) y pregunta si avanzan distinto.
- **Qué agrega Tukey.** El ANOVA dice "al menos un grupo es distinto" pero no cuál. La prueba de Tukey completa la frase y dice **exactamente entre qué grupos** está la diferencia.
- **Qué encontramos.** El peso explica cerca del **30%** de por qué unos avanzan más que otros, y los tres grupos se diferencian claramente. A más peso, más rápido avanza.
- **Para decir.** "A más peso, la diabetes avanza más, de manera escalonada."

### 7. Análisis multivariado — mirar todos los factores juntos
- **La idea simple.** Hasta acá miramos un factor por vez. Pero en la realidad todos actúan al mismo tiempo. La **regresión** mira todos los factores juntos y dice cuáles siguen importando cuando se consideran los demás.
- **Una analogía.** Es como un equipo de fútbol. Mirar a un jugador solo engaña, porque su rendimiento depende de los compañeros. La regresión mira a todo el equipo a la vez.
- **Qué encontramos.**
  - Todos los factores juntos explican cerca del **50%** del avance.
  - Los tres que más pesan son **peso y triglicéridos casi empatados, y la presión detrás**.
  - La edad y la glucosa dejan de importar cuando se considera el resto.
- **Bonus, auditoría de la limpieza.** Aprovechamos para revisar decisiones que se habían tomado al limpiar los datos. Descubrimos que eliminar la variable `S4` fue discutible, porque en realidad era un buen predictor.
- **Para decir.** "El avance lo explica un equipo de factores, no uno solo. Y de paso revisamos nuestra propia limpieza."

### 8. Comparación, datos sin limpiar y limpios
- **Qué hicimos.** Pusimos lado a lado dos mapas de correlación, antes y después de limpiar.
- **Qué encontramos.** El limpio es más fácil de leer, sin información repetida.
- **Para decir.** "Limpiar no cambió las conclusiones, pero las hizo más claras."

### 9. Tablero resumen — todo en una imagen
- **Qué es.** Un panel que junta lo principal del análisis en una sola vista, los indicadores, qué factores importan, las comparaciones por sexo y por peso, y el peso final de cada factor.
- **Para qué.** Es la diapositiva ideal para cerrar la exposición.
- **Para decir.** "Todo el análisis condensado en una imagen."

### 10. Conclusiones — organizadas por hipótesis
- Las conclusiones están armadas como una **lista de preguntas que nos hicimos y qué respondió cada prueba** (ver la tabla más abajo).
- En resumen: el avance lo explican **peso, triglicéridos y presión**, el **sexo no influye**, y verificar los supuestos fue clave para confiar en los resultados.

---

## La tabla de hipótesis (lo más importante para exponer)

Esta tabla resume todo el método. Si la entendés, podés explicar el taller entero.

| Lo que nos preguntamos | Cómo lo probamos | Qué salió |
|---|---|---|
| ¿Los datos tienen forma de campana? | Shapiro y Q-Q plot | No, ninguno |
| ¿El peso se relaciona con el avance? | Chi-cuadrado | Sí, relación real |
| ¿El sexo influye en el avance? | T-Test y Mann-Whitney | No influye |
| ¿El peso influye en el avance? | ANOVA y Tukey | Sí, y bastante |
| ¿Un solo factor explica todo? | Regresión múltiple | No, son varios |

---

## Las 4 frases para cerrar

1. **No es un solo culpable.** Parecía que solo el peso importaba, pero también pesan los triglicéridos y la presión.
2. **El sexo no influye**, y lo confirmamos tres veces para estar seguros.
3. **Desconfiar y verificar dio resultado.** Como los datos no eran normales, usamos pruebas de respaldo que confirmaron todo.
4. **Limpiar y analizar van de la mano.** El análisis nos hizo ver que una decisión de limpieza fue discutible.

## Preguntas que te pueden hacer (y cómo responder)

- **¿Por qué no usaron otras distribuciones como Poisson?** Porque no encajan con estos datos. Usarlas sería forzar la herramienta solo para lucirla.
- **¿Por qué tantas pruebas para lo mismo?** Porque los datos no eran perfectos, así que cada resultado lo confirmamos con una segunda prueba para estar seguros.
- **¿Qué significa que expliquen el 50%?** Que con estos factores entendemos la mitad de por qué unos pacientes avanzan más. La otra mitad depende de cosas que no estaban en los datos.
- **¿El peso causa el avance?** Mostramos que están fuertemente relacionados, pero relación no es lo mismo que causa. Para afirmar que lo causa haría falta otro tipo de estudio.

## Mini diccionario (en palabras simples)

- **p-valor.** El detector de casualidad. Menor a 0.05 significa "esto es real".
- **Hipótesis nula.** La afirmación aburrida que intentamos refutar, normalmente "no pasa nada / no hay efecto".
- **Distribución normal.** La famosa campana, la mayoría de los valores en el medio y pocos en los extremos.
- **Tamaño del efecto.** No solo si hay diferencia, sino si es grande o insignificante.
- **Correlación.** Qué tan de la mano se mueven dos cosas.
- **R cuadrado.** El porcentaje de algo que el modelo logra explicar.
- **Prueba no paramétrica.** Una prueba que funciona aunque los datos no tengan forma de campana.
- **Regresión.** Mira todos los factores juntos y dice cuánto pesa cada uno.
