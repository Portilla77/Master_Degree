## Rendimiento de estudiantes

Se utilizó regresión lineal múltiple para modelar la relación entre el **GPA** y el resto de las variables disponibles en el conjunto de datos.

Las variables incluidas en el modelo fueron:
- **Variables continuas:** StudyTimeWeekly, Absences
- **Variables categóricas:** Tutoring, ParentalSupport, Extracurricular, Sports, Music, Volunteering

### Resultados:
- **Error Cuadrático Medio (MSE):** 0.03570652030968603
- **Coeficiente de Determinación (R²):** 0.9568205199526371

El modelo muestra un **R² de 0.95**, lo que indica que el 95.6% de la variabilidad del GPA es explicada por las variables predictoras.
Realizamos una predicción del **GPA** considerando un incremento del 10% en el tiempo de estudio semanal según el modelo entrenado.

- **GPA predicho con 10% más de estudio:** 1.5855753471668976
Así mismo, el resultado de la predicción se envió a través de un bot de Telegram con token hardcodeado utilizando la API de Telegram.

El modelo se utilizó para hacer la predicción de un nuevo estudiante con los siguientes datos supuestos:

Datos del Estudiante
- StudyTimeWeekly: 15
- Absences: 2
- Tutoring: 1
- ParentalSupport: 1
- Extracurricular: 1
- Sports: 0
- Music: 1


Esto significa que, con las características ingresadas (StudyTimeWeekly = 15, Absences = 2, etc.), el modelo estima que el estudiante tendrá un GPA de aproximadamente 3.58 puntos.

Link del código: https://colab.research.google.com/drive/1YyYp5aRof1h2H35-pht0WV8utCUY26Fi?usp=sharing