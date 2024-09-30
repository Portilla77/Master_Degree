### Problema 1
#a)
combinaciones <- choose(8, 5)
print(combinaciones)

#b)

combinaciones_totales <- sum(sapply(1:10, function(k) choose(10, k)))
cat("Número total de modelos de regresión a revisar:", combinaciones_totales, "\n")


#c)

combinaciones_2_variables <- choose(10, 2)
cat("Número de modelos con exactamente 2 variables:", combinaciones_2_variables, "\n")

probabilidad_2_variables <- combinaciones_2_variables / combinaciones_totales
cat("Probabilidad de elegir un modelo con exactamente 2 variables:", probabilidad_2_variables * 100, "%\n")


#d)


combinaciones_1_5 <- sum(sapply(1:5, function(k) choose(10, k)))

combinaciones_totales <- sum(sapply(1:10, function(k) choose(10, k)))

probabilidad_1_5 <- combinaciones_1_5 / combinaciones_totales

cat("Número total de modelos con a lo más 5 variables:", combinaciones_1_5, "\n")
cat("Probabilidad de elegir un modelo con a lo más 5 variables:", probabilidad_1_5 * 100, "%\n")


## Problema 2

# a)

prob_premium <- 0.25
prob_llena_premium <- 0.60

prob_premium_y_llena <- prob_premium * prob_llena_premium
cat("Probabilidad de que un cliente pida gasolina premium y llene el tanque:", prob_premium_y_llena * 100, "%\n")

# b)
prob_regular <- 0.45
prob_plus <- 0.30
prob_llena_regular <- 0.20
prob_llena_plus <- 0.75

# Probabilidad total de llenar el tanque
prob_llena_tanque <- (prob_llena_regular * prob_regular) + 
                     (prob_llena_plus * prob_plus) + 
                     (prob_llena_premium * prob_premium)

cat("Probabilidad de que un cliente llene su tanque:", prob_llena_tanque * 100, "%\n")

# c)
prob_regular_given_llena <- (prob_llena_regular * prob_regular) / prob_llena_tanque
prob_plus_given_llena <- (prob_llena_plus * prob_plus) / prob_llena_tanque
prob_premium_given_llena <- (prob_llena_premium * prob_premium) / prob_llena_tanque

cat("Probabilidad de usar gasolina regular dado que llenó el tanque:", prob_regular_given_llena * 100, "%\n")

### Problema 3

total_empleados <- 700
hombres_aprobados <- 200
hombres_no_aprobados <- 30
mujeres_aprobadas <- 414
mujeres_no_aprobadas <- 56

total_mujeres <- mujeres_aprobadas + mujeres_no_aprobadas

total_aprobados <- hombres_aprobados + mujeres_aprobadas
total_no_aprobados <- hombres_no_aprobados + mujeres_no_aprobadas

#a)

prob_mujer <- total_mujeres / total_empleados
print(prob_mujer)

#b)

prob_mujer_no_aprueba <- mujeres_no_aprobadas / total_empleados
prob_mujer_no_aprueba
print(prob_mujer_no_aprueba)

#c)

prob_aprobatorio_dado_mujer <- mujeres_aprobadas / total_mujeres
print(prob_aprobatorio_dado_mujer)

#d)

prob_hombre_dado_aprobatorio <- hombres_aprobados / total_aprobados
print(prob_hombre_dado_aprobatorio)