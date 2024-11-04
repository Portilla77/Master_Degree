library(stats)

# a)
pacientes_alvarez <- c(72, 92, 108, 97, 72, 69, 117, 87, 94, 109, 94, 96, 112, 80, 100, 81, 86, 113, 107,
                      77, 84, 99, 73, 69, 103, 103, 117, 100, 66, 66, 84)

media_alvarez <- mean(pacientes_alvarez)
print(media_alvarez)
desviacion_alvarez <- sd(pacientes_alvarez)
print(desviacion_alvarez)

mu_0 <- 130
t_test_a <- t.test(pacientes_alvarez, mu = mu_0, alternative = "less")
print(t_test_a$statistic)
print(t_test_a$p.value / 2)

alpha_confianza <- 0.05
n <- length(pacientes_alvarez)
gl <- n - 1
t_critico_confianza <- qt(1 - alpha_confianza / 2, gl)

margen_error <- t_critico_confianza * (desviacion_alvarez / sqrt(n))
limite_inferior <- media_alvarez - margen_error
limite_superior <- media_alvarez + margen_error
print(c(limite_inferior, limite_superior))

# b)
pacientes_casas <- c(73, 70, 117, 114, 111, 109, 92, 89, 80, 111, 122, 69, 72, 90, 69, 87, 111, 85, 82, 70)
pacientes_dominguez <- c(119, 76, 94, 74, 107, 115, 66, 94, 122, 68, 95, 88, 82, 114, 109, 105, 97, 95, 88, 101,
                         114, 110, 116, 124, 72, 120, 106)

desviacion_casas <- sd(pacientes_casas)
desviacion_dominguez <- sd(pacientes_dominguez)
print(c("Pacientes Casas:", desviacion_casas, "Pacientes Dominguez:", desviacion_dominguez))

t_test_b <- t.test(pacientes_casas, pacientes_dominguez, alternative = "less", var.equal = FALSE)
media_casas <- mean(pacientes_casas)
media_dominguez <- mean(pacientes_dominguez)

n_casas <- length(pacientes_casas)
n_dominguez <- length(pacientes_dominguez)

mean_diff <- media_casas - media_dominguez

numerador_df <- (desviacion_casas^2 / n_casas + desviacion_dominguez^2 / n_dominguez)^2
denominador_df <- ((desviacion_casas^2 / n_casas)^2 / (n_casas - 1)) + ((desviacion_dominguez^2 / n_dominguez)^2 / (n_dominguez - 1))
df <- numerador_df / denominador_df
alpha <- 0.05
t_critical <- qt(1 - alpha/2, df)

margin_of_error <- t_critical * sqrt(desviacion_casas^2 / n_casas + desviacion_dominguez^2 / n_dominguez)

ci_lower <- mean_diff - margin_of_error
ci_upper <- mean_diff + margin_of_error

print(c("Media de Pacientes Casas:", media_casas))
print(c("Media de Pacientes Dominguez:", media_dominguez))
print(c("Desviación Estándar de Pacientes Casas:", desviacion_casas))
print(c("Desviación Estándar de Pacientes Dominguez:", desviacion_dominguez))
print(t_test_b$statistic)
print(t_test_b$p.value)
print(c(ci_lower, ci_upper))

# c)
p_0 <- 0.15
n <- length(pacientes_dominguez)
no_controlados <- sum(pacientes_dominguez < 80 | pacientes_dominguez > 130)
p_muestral <- no_controlados / n
z <- (p_muestral - p_0) / sqrt((p_0 * (1 - p_0)) / n)
p_value <- 1 - pnorm(z)
z_critical <- qnorm(1 - alpha / 2)

margin_of_error <- z_critical * sqrt((p_muestral * (1 - p_muestral)) / n)

ci_lower <- p_muestral - margin_of_error
ci_upper <- p_muestral + margin_of_error

print(c("Número de pacientes 'no controlados':", no_controlados))
print(c("Proporción muestral de pacientes no controlados:", round(p_muestral, 3)))
print(c("Estadístico z:", round(z, 3)))
print(c("Valor p:", round(p_value, 3)))
print(c("Intervalo de confianza del 95% para la proporción muestral:", ci_lower, ci_upper))

# d)
pacientes_benitez <- c(112,123,122,122,112,85,98,105,110,112,69,86,78,117,114,84,74,103,109,100)

media_benitez <- mean(pacientes_benitez)
desviacion_benitez <- sd(pacientes_benitez)

media_diff <- media_casas - media_benitez

numerador_df <- (desviacion_casas^2 / n_casas + desviacion_benitez^2 / n_benitez)^2
denominador_df <- ((desviacion_casas^2 / n_casas)^2 / (n_casas - 1)) + ((desviacion_benitez^2 / n_benitez)^2 / (n_benitez - 1))
df <- numerador_df / denominador_df

t_critical <- qt(1 - alpha/2, df)

margin_of_error <- t_critical * sqrt((desviacion_casas^2 / n_casas) + (desviacion_benitez^2 / n_benitez))

ci_lower <- media_diff - margin_of_error
ci_upper <- media_diff + margin_of_error

t_test_d <- t.test(pacientes_casas, pacientes_benitez, alternative = "greater", var.equal = FALSE)

print(c("Media Dr. Casas:", media_casas, "Desviación estándar Dr. Casas:", desviacion_casas))
print(c("Media Dr. Benítez:", media_benitez, "Desviación estándar Dr. Benítez:", desviacion_benitez))
print(t_test_d$statistic)
print(t_test_d$p.value)
print(c("Intervalo de confianza del 95% para la diferencia de medias:", ci_lower, ci_upper))

# e)
antes_tratamiento <- c(72, 92, 108, 97, 72, 69, 117, 87, 94, 109, 94, 96, 112, 80, 100, 81, 86, 113, 107, 77)
despues_tratamiento <- c(62, 90, 100, 95, 74, 70, 107, 87, 95, 109, 95, 90, 102, 81, 105, 80, 86, 103, 105, 70)
diferencias <- antes_tratamiento - despues_tratamiento
media_diferencias <- mean(diferencias)
desviacion_diferencias <- sd(diferencias)
n <- length(diferencias)
t_stat <- media_diferencias / (desviacion_diferencias / sqrt(n))
p_value <- t.test(antes_tratamiento, despues_tratamiento, paired = TRUE, alternative = "greater")$p.value
t_critical <- qt(1 - alpha / 2, df = n - 1)
margin_of_error <- t_critical * (desviacion_diferencias / sqrt(n))
ci_lower <- media_diferencias - margin_of_error
ci_upper <- media_diferencias + margin_of_error
print(c("Media de las diferencias:", media_diferencias))
print(c("Desviación estándar de las diferencias:", desviacion_diferencias))
print(c("Estadístico t:", t_stat))
print(c("Valor p:", p_value))
print(c("Intervalo de confianza del 95% para la media de las diferencias:", ci_lower, ci_upper))
