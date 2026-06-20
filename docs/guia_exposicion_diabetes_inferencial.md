# Guía de exposición — Taller 3, Diabetes y Estadística Inferencial

Guía para entender y presentar el notebook `Taller_3_diabetes_inferencial.ipynb`. Pensada para aprender el contenido y exponerlo con fluidez. Cada sección dice qué se hizo, por qué, qué dio y la frase clave para decir en voz alta.

---

## La idea en una frase

El objetivo fue descubrir **qué factores hacen que la diabetes avance más rápido o más lento** en un paciente. Se trabajó con 442 pacientes y se aplicaron las herramientas de estadística inferencial vistas en clase. La respuesta corta es que el avance lo explican sobre todo el **peso, los triglicéridos y la presión arterial**, y que el **sexo no influye**.

## Qué es la estadística inferencial (para arrancar la charla)

La estadística descriptiva solo resume lo que se ve, promedios y gráficos. La **inferencial va un paso más allá**, saca conclusiones y mide si son confiables o producto del azar. La herramienta central es la **prueba de hipótesis**, que funciona así, se plantea una afirmación a refutar (la hipótesis nula, por ejemplo "el sexo no influye"), se calcula un **p-valor**, y si ese valor es menor a 0.05 se concluye que el resultado no es casualidad.

## El dataset en una frase

442 pacientes con diabetes, 10 medidas clínicas (edad, sexo, peso o BMI, presión y seis análisis de sangre llamados S1 a S6) y una variable objetivo `Y` que mide cuánto avanzó la enfermedad un año después.

---

## Recorrido por secciones

### 1. Estadística descriptiva
- **Qué se hizo.** Una tabla con el promedio, la dispersión y la forma de cada variable.
- **Por qué.** Antes de inferir nada conviene conocer cómo se comporta cada variable, es la foto de partida.
- **Dato útil.** La asimetría de `Y` ya anticipa que no será una distribución normal, tiene una cola hacia la derecha.
- **Frase clave.** "Primero miramos cómo se comporta cada variable."

### 2. Distribución normal
- **Qué se hizo.** Se verificó si las variables tienen forma de campana, con la prueba de Shapiro y los gráficos Q-Q. Se aplicó la regla 68-95-99.7 y la tipificación Z.
- **Qué significa la tipificación Z.** Es transformar una variable para expresarla en "cuántas desviaciones estándar se aleja del promedio", lo que permite comparar y calcular probabilidades.
- **Qué dio.** Ninguna variable es perfectamente normal. El peso se acerca bastante, la progresión menos.
- **Por qué importa.** El T-Test y el ANOVA suponen normalidad, así que de aquí en más cada prueba se acompaña con una alternativa que no la necesita.
- **Frase clave.** "Los datos no son perfectamente normales, así que tomamos precauciones."

### 3. Probabilidad condicional y Bayes
- **Qué se hizo.** Una tabla que cruza peso alto o bajo con progresión alta o baja, y se calcularon probabilidades condicionales.
- **Qué es una probabilidad condicional.** Es la probabilidad de algo **sabiendo** otra cosa, por ejemplo la probabilidad de progresión alta sabiendo que el paciente tiene peso alto.
- **Qué dio.** Sin saber nada, la probabilidad de progresión alta es 50%. Si el peso es alto, sube a **71%**. Si es bajo, baja a **30%**. El chi-cuadrado confirma que la relación no es casualidad.
- **Frase clave.** "Saber el peso de un paciente cambia mucho lo que podemos esperar de su enfermedad."

### 4. Distribución binomial
- **Qué se hizo.** Se modeló cuántos pacientes con progresión alta se esperarían en un grupo elegido al azar.
- **Cuándo aplica la binomial.** Cuando algo tiene solo dos resultados posibles (alto o no alto) y se repite varias veces de forma independiente.
- **Qué dio.** En diez pacientes lo más probable es cinco, encontrar ocho o más es raro.
- **Frase clave.** "Una forma de razonar con probabilidades sobre grupos de pacientes."

### 5. T-Test, progresión por sexo
- **Qué se hizo.** Se comparó la progresión entre hombres y mujeres con tres pruebas, más el tamaño del efecto.
- **Por qué tres pruebas.** El T-Test es la clásica, Mann-Whitney es la versión que no exige normalidad, y el d de Cohen mide si la diferencia, aunque exista, es grande o trivial.
- **Qué dio.** No hay diferencia, y el tamaño del efecto es prácticamente cero.
- **Frase clave.** "El sexo no influye en cómo avanza la diabetes."

### 6. ANOVA, progresión por peso
- **Qué se hizo.** Se dividió el peso en tres grupos, bajo, medio y alto, y se comparó la progresión entre ellos, con prueba post-hoc de Tukey.
- **Qué es el ANOVA y qué agrega Tukey.** El ANOVA dice si **al menos un grupo** difiere de los demás, pero no cuál. Tukey completa el análisis indicando **entre qué grupos** está la diferencia.
- **Qué dio.** El peso explica cerca del 30% de la variación, y los tres grupos se diferencian entre sí de forma escalonada.
- **Frase clave.** "A más peso, la enfermedad avanza más, paso a paso."

### 7. Análisis multivariado y auditoría de la limpieza
- **Qué se hizo.** Un ranking de todos los factores y una regresión que los mira a todos juntos. Además se revisaron las decisiones de limpieza del dataset.
- **Por qué la regresión es la clave.** Las secciones anteriores miran un factor por vez. La regresión múltiple los considera **simultáneamente**, y revela cuáles siguen importando cuando se controla por el resto.
- **Qué dio.**
  - Los factores juntos explican cerca del **50%** de la progresión.
  - Mandan tres, **peso y triglicéridos casi empatados, y presión detrás**.
  - Edad y glucosa dejan de importar al considerar el resto.
  - Conservar los valores atípicos fue correcto, no distorsionan el modelo.
  - Sobre la limpieza, quitar `S2` estuvo bien, pero quitar `S4` sacrificó un buen predictor.
- **Frase clave.** "La progresión la explica un trío de factores, no uno solo. Y el análisis nos sirvió para revisar la limpieza."

### 8. Comparación visual, sin limpiar y limpio
- **Qué se hizo.** Dos mapas de correlación lado a lado, el dataset crudo y el limpio.
- **Qué dio.** El limpio es más fácil de leer, sin las repeticiones de información del crudo, como la correlación de 0.90 entre `S1` y `S2`.
- **Frase clave.** "Limpiar no cambió las conclusiones, pero las hizo más claras."

### 9. Tablero resumen
- **Qué se hizo.** Un panel único que reúne lo principal, los indicadores, el ranking de factores, la probabilidad condicional por peso, las comparaciones por sexo y por peso, y el peso final de cada factor en el modelo.
- **Para qué sirve en la exposición.** Es la diapositiva ideal para cerrar, muestra todo el análisis de un vistazo.
- **Frase clave.** "Todo el análisis condensado en una imagen."

### 10. Conclusiones
- Se presentan como una **tabla de hipótesis**, cada afirmación con su prueba y su resultado, más conclusiones por tema.
- El avance de la diabetes lo explica un trío, **peso, triglicéridos y presión**.
- El **sexo no influye**.
- Verificar los supuestos fue clave para confiar en los resultados.
- El análisis sirvió para auditar la limpieza, los dos pasos se retroalimentan.

---

## La tabla de hipótesis (el corazón de la exposición)

Conviene tener esta tabla a mano, resume todo el método de un golpe.

| Hipótesis planteada | Prueba aplicada | Resultado |
|---|---|---|
| Las variables son normales | Shapiro-Wilk, Q-Q | Rechazada, ninguna lo es |
| El BMI se asocia a la progresión | Chi-cuadrado | Confirmada |
| El sexo influye en la progresión | T-Test, Mann-Whitney | Rechazada |
| El BMI influye en la progresión | ANOVA, Tukey | Confirmada, efecto grande |
| Un solo factor explica la progresión | Regresión múltiple | Rechazada, son varios |

---

## Mensajes para cerrar la exposición

1. **No es un solo factor.** Al principio parecía que solo el peso importaba, pero el análisis completo mostró que los triglicéridos pesan igual y la presión también.
2. **El sexo no influye**, y se confirmó por tres caminos distintos.
3. **Verificar supuestos importa.** Como los datos no eran normales, se usaron pruebas de respaldo que confirmaron todo.
4. **Limpieza y análisis van juntos.** El análisis hizo ver que una decisión de limpieza, quitar `S4`, fue discutible.

## Posibles preguntas del público

- **¿Por qué no usaron Poisson o la hipergeométrica?** Porque este dataset no tiene conteos por tiempo ni muestreos sin reemplazo donde tendrían sentido. Usarlas sería forzar la herramienta.
- **¿Por qué tantas pruebas para lo mismo?** Porque los datos no son normales. Cada prueba paramétrica se confirma con una no paramétrica para estar seguros.
- **¿Qué significa que explique el 50%?** Que con estos factores se da cuenta de la mitad de por qué unos pacientes avanzan más que otros. La otra mitad depende de cosas que no están en el dataset.
- **¿El peso causa el avance?** El análisis muestra asociación fuerte, no causalidad. Para afirmar causa haría falta un diseño experimental distinto.

## Glosario rápido

- **p-valor.** Si es menor a 0.05, el resultado no es casualidad.
- **Hipótesis nula.** La afirmación que se intenta refutar, por defecto "no hay efecto".
- **Tamaño del efecto (d de Cohen).** Mide si una diferencia es grande o trivial, más allá de si es significativa.
- **Correlación.** Qué tan juntas se mueven dos variables, de -1 a 1.
- **R cuadrado.** Qué porcentaje de la variación logra explicar el modelo.
- **Prueba no paramétrica.** Versión de una prueba que no necesita que los datos sean normales.
- **Tipificación Z.** Expresar un valor en cuántas desviaciones estándar se aleja del promedio.
