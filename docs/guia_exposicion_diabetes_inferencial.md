# Guía de exposición — Diabetes, Estadística Inferencial

Guía para entender y presentar el notebook `Taller_3_diabetes_inferencial.ipynb`. Cada sección dice qué se hizo, qué dio y la frase clave para exponer.

---

## La idea en una frase

Queríamos saber **qué factores explican que la diabetes avance rápido o lento** en un paciente. Usamos un conjunto de 442 pacientes y aplicamos las herramientas de estadística inferencial vistas en clase. La respuesta corta es que el avance lo explican principalmente el **peso, los triglicéridos y la presión arterial**, y que el **sexo no influye**.

## El dataset en una frase

442 pacientes con diabetes, 10 medidas clínicas (edad, sexo, peso, presión y seis análisis de sangre) y una variable objetivo `Y` que mide cuánto avanzó la enfermedad un año después.

---

## Recorrido por secciones

### 1. Estadística descriptiva
- **Qué se hizo.** Una tabla con los promedios, la dispersión y la forma de cada variable.
- **Para qué.** Tener una foto general antes de sacar conclusiones.
- **Frase clave.** "Empezamos mirando cómo se comporta cada variable."

### 2. Distribución normal
- **Qué se hizo.** Verificamos si las variables tienen forma de campana, usamos la prueba de Shapiro y los gráficos Q-Q. También aplicamos la regla 68-95-99.7 y la tipificación Z.
- **Qué dio.** Ninguna variable es perfectamente normal. El peso se acerca, la progresión no tanto.
- **Por qué importa.** Algunas pruebas suponen normalidad, así que de aquí en más usamos también pruebas que no la necesitan.
- **Frase clave.** "Los datos no son perfectamente normales, así que tomamos precauciones."

### 3. Probabilidad condicional y Bayes
- **Qué se hizo.** Una tabla que cruza peso alto o bajo con progresión alta o baja.
- **Qué dio.** Sin saber nada, la probabilidad de progresión alta es 50%. Si el peso es alto, sube a **71%**. Si es bajo, baja a **30%**.
- **Frase clave.** "Saber el peso de un paciente cambia mucho lo que podemos esperar de su enfermedad."

### 4. Distribución binomial
- **Qué se hizo.** Modelamos cuántos pacientes con progresión alta esperaríamos en un grupo elegido al azar.
- **Qué dio.** En diez pacientes lo más probable es cinco, encontrar ocho o más es raro.
- **Frase clave.** "Una forma de razonar con probabilidades sobre grupos de pacientes."

### 5. T-Test, progresión por sexo
- **Qué se hizo.** Comparamos la progresión entre hombres y mujeres, con tres pruebas y el tamaño del efecto.
- **Qué dio.** No hay diferencia, y el efecto es prácticamente cero.
- **Frase clave.** "El sexo no influye en cómo avanza la diabetes."

### 6. ANOVA, progresión por peso
- **Qué se hizo.** Dividimos el peso en tres grupos (bajo, medio, alto) y comparamos la progresión, con prueba post-hoc de Tukey.
- **Qué dio.** El peso explica cerca del 30% de la variación, y los tres grupos se diferencian entre sí.
- **Frase clave.** "A más peso, la enfermedad avanza más, de manera escalonada."

### 7. Análisis multivariado y auditoría de la limpieza
- **Qué se hizo.** Un ranking de todos los factores y una regresión que los mira a todos juntos. Además revisamos las decisiones de limpieza del dataset.
- **Qué dio.**
  - Los factores juntos explican cerca del **50%** de la progresión.
  - Mandan tres, **peso y triglicéridos casi empatados, y presión detrás**.
  - Edad y glucosa dejan de importar cuando se considera el resto.
  - Conservar los valores atípicos fue correcto, no distorsionan el modelo.
  - Sobre la limpieza, quitar `S2` estuvo bien, pero quitar `S4` sacrificó un buen predictor.
- **Frase clave.** "La progresión la explica un trío de factores, no uno solo. Y el análisis nos sirvió para revisar la limpieza."

### 8. Comparación visual, sin limpiar y limpio
- **Qué se hizo.** Dos mapas de correlación lado a lado.
- **Qué dio.** El dataset limpio es más fácil de leer, sin las repeticiones de información del crudo.
- **Frase clave.** "Limpiar no cambió las conclusiones, pero las hizo más claras."

### 9. Conclusiones
- El avance de la diabetes lo explica un trío, **peso, triglicéridos y presión**.
- El **sexo no influye**.
- Verificar los supuestos fue clave para confiar en los resultados.
- El análisis sirvió para auditar la limpieza, los dos pasos se retroalimentan.

---

## Mensajes para cerrar la exposición

1. **No es un solo factor.** Al principio parecía que solo el peso importaba, pero el análisis completo mostró que los triglicéridos pesan igual y la presión también.
2. **El sexo no influye**, y lo confirmamos por tres caminos distintos.
3. **Verificar supuestos importa.** Como los datos no eran normales, usamos pruebas de respaldo que confirmaron todo.
4. **Limpieza y análisis van juntos.** El análisis nos hizo ver que una decisión de limpieza, quitar `S4`, fue discutible.

## Posibles preguntas del público

- **¿Por qué no usaron Poisson o la hipergeométrica?** Porque este dataset no tiene conteos por tiempo ni muestreos sin reemplazo donde tendrían sentido. Usarlas sería forzar la herramienta.
- **¿Por qué tantas pruebas para lo mismo?** Porque los datos no son normales. Cada prueba paramétrica se confirma con una no paramétrica para estar seguros.
- **¿Qué significa que explique el 50%?** Que con estos factores podemos dar cuenta de la mitad de por qué unos pacientes avanzan más que otros. La otra mitad depende de cosas que no están en el dataset.
- **¿El peso causa el avance?** El análisis muestra asociación fuerte, no causalidad. Para afirmar causa haría falta un diseño experimental distinto.

## Glosario rápido

- **p-valor.** Si es menor a 0.05, el resultado no es casualidad.
- **Tamaño del efecto.** Mide si una diferencia es grande o trivial, más allá de si es significativa.
- **Correlación.** Qué tan juntas se mueven dos variables, de -1 a 1.
- **R cuadrado.** Qué porcentaje de la variación logra explicar el modelo.
- **Prueba no paramétrica.** Versión de una prueba que no necesita que los datos sean normales.
