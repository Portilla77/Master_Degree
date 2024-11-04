# Métodos Estadísticos Básicos
**MET. Alejandra Cerda**  
**Jorge Ramón Flores Portilla**  
**Evidencia 2**

---

## Problema 1

### a) Número de modelos de regresión con 5 variables
Si consideramos un total de 8 variables, la cantidad de modelos de regresión que se pueden formar incluyendo exactamente 5 variables es:

$C(8, 5) = \frac{8!}{5! (8-5)!} = 56$

Es decir, se pueden revisar un total de **56 modelos**.

### b) Número total de modelos de regresión
Con 10 variables predictoras, se revisan todos los posibles modelos:
$C(10, 1) + C(10, 2) + ... + C(10, 10) = 10 + 45 + 120 + 210 + 252 + 210 + 120 + 45 + 10 + 1 = 1023$
Por lo tanto, se revisan un total de **1023 modelos de regresión**.

### c) Probabilidad de elegir un modelo con exactamente 2 variables
La probabilidad de elegir un modelo con exactamente 2 variables es:
$
P(\text{2 variables}) = \frac{C(10, 2)}{\text{Total modelos}} = \frac{45}{1023} \approx 0.04398 = 4.39\%
$

Por lo tanto, **la probabilidad de elegir un modelo de exactamente 2 variables es del $4.39\%$**

### d) Probabilidad de elegir un modelo con a lo más 5 variables

Calculando el número de modelos con a lo más 5 variables:
$C(10, 1) + C(10, 2) + C(10, 3) + C(10, 4) + C(10, 5) = 10 + 45 + 120 + 210 + 252 = 637$

La probabilidad es:
$P(\text{A lo más 5 variables}) = \frac{637}{1023} \approx 0.62267 = 62.26\%$

Por lo tanto, **la probabilidad de elegir un modelo de a lo más 5 variables es del $62.26\%$**

---

## Problema 2

En una gasolinera:
- 45% de los clientes usan gasolina regular.
- 30% usan gasolina plus.
- 25% usan gasolina premium.
Además, las probabilidades de llenar el tanque son:
- 20% para regular, 75% para plus, 60% para premium.

### a) ¿Cuál es la probabilidad de que el siguiente cliente pida gasolina premium y llene el tanque?

$P(\text{Premium y llenar}) = 0.25 \times 0.60 = 0.15 = 15\%$

Por tanto, **la probabilidad de que el siguiente cliente pida gasolina premium y llene el tanque es del $15\%$**

### b) ¿Cuál es la probabilidad de que el siguiente cliente llene el tanque?
$
P(\text{Llenar tanque}) = (0.20 \times 0.45) + (0.75 \times 0.30) + (0.60 \times 0.25) = 0.09 + 0.225 + 0.15 = 0.465 = 46.5\%
$
Por lo tanto, **la probabilidad de que el siguiente cliente llene su tanque es del 46.5\%**

### c) Si el siguiente cliente llena el tanque ¿Cuál es la probabilidad de que pida gasolina regular?

Usando el teorema de Bayes:
$
P(\text{Regular} \mid \text{Llenar tanque}) = \frac{P(\text{Llenar tanque} \mid \text{Regular}) \times P(\text{Regular})}{P(\text{Llenar tanque})} = \frac{(0.20 \times 0.45)}{0.465} \approx 0.1935 = 19.35\%
$

Entonces, si el siguiente cliente llena el tanque, **la probabilidad de que el cliente pida gasolina regular es del $19.35\%$**

---

## Problema 3

| Sexo      | Aprobados | No aprobados | Total |
|-----------|-----------|--------------|-------|
| Hombres   | 200       | 30           | 230   |
| Mujeres   | 414       | 56           | 470   |
| **Total** | **614**   | **86**       | **700** |

### a) Probabilidad de que un empleado sea mujer
$
P(\text{Mujer}) = \frac{470}{700} = 0.6714 = 67.14\%
$

Entonces, **la probabilidad de que un empleado sea mujer es del $67.14\%$**

### b) Probabilidad de que sea mujer y no apruebe
$P(\text{Mujer y no aprueba}) = \frac{56}{700} = 0.08 = 8\%$

Es decir, **la probabilidad de que sea mujer y no apruebe es del $8\%$**

### c) Probabilidad de que el desempeño sea aprobatorio dado que es mujer
$P(\text{Aprobatorio} \mid \text{Mujer}) = \frac{414}{470} = 0.8809 = 88.09\%$

Es decir, **la probabilidad de que sea mujer y no apruebe es del $88.09\%$**

### d) Probabilidad de que sea hombre dado que el desempeño es aprobatorio
$P(\text{Hombre} \mid \text{Aprobatorio}) = \frac{200}{614} = 0.3257 = 32.57\%$

**La probabilidad de que sea hombre dado que el desempeño es aprobatorio es del $32.57\%$**

---

## Problema 4

### a) $P(B)$:
$P(B) = \frac{30}{100} = 0.3 = 30\%$


Por lo tanto, **la probabilidad de B es del $30\%$**

### b) $P(A \cup B)$:
$P(A \cup B) = \frac{50}{100} = 0.5 = 50\%$

**Por lo tanto, la probabilidad de P(A∪B) es del $50\%$**

### c) $P(F')$:
Valores fuera de \( F \): \( 13, 20, 5 \)
$P(F') = \frac{38}{100} = 0.38 = 38\%$

**Por lo tanto, la probabilidad de P(F´) es del $38\%$**

### d) $P(B \cap F)$:
Valores de la intersección: \( 2, 3 \)
$P(B \cap F) = \frac{5}{100} = 0.05 = 5\%$

**Por lo tanto, la probabilidad de P(B∩F) es del $5\%$**