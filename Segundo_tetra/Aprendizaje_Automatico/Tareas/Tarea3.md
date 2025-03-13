### Tarea 3
### Jorge Ramon Flores Portilla 1550162

## Diseño del experimento con 5 Umbrales
Se probaron los siguientes umbrales:
- **-1000, -500, 0, 500, 1000**

## Tendencia observada:
- La **precisión aumenta** a medida que el umbral sube.
- El **recall disminuye** conforme el umbral es más alto.

Esto ocurre porque al elevar el umbral, el modelo se vuelve más estricto al clasificar un dígito como "5", lo que reduce los falsos positivos (**aumentando la precisión**), pero también hace que pierda más casos reales (**disminuyendo el recall**).

---

## Prueba estadística sobre el impacto del umbral

El error en la prueba ANOVA (`NaN`) nos permite ver que todos los grupos analizados tienen un solo valor, lo cual impide realizar la comparación estadística.

---

## ¿Existe un Dígito Más Fácil de Clasificar?
- **Dígito "1" tiene la mayor precisión y recall.**
- Para los demás dígitos, los valores de precisión y recall son **0.0**, indicando que no fueron correctamente clasificados bajo los umbrales probados.

### 🔹 Prueba Kruskal-Wallis (p-valor = 0.4372)
El resultado de **p = 0.4372** indica que **no hay suficiente evidencia estadística para afirmar que un dígito es significativamente más fácil de clasificar que otros**. Esto implica que el **dígito "1"** es el más fácil de clasificar, pero **no hay evidencia estadística fuerte** para confirmarlo.

Link del código: https://colab.research.google.com/drive/1TqjVHyq1mFF4mbQVCKuoMbxkaAjGuOPJ?usp=sharing