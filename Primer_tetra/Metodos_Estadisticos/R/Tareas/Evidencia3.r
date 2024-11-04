# Problema 1
lambda <- 1 / 4

# a) Probabilidad de que el tiempo de servicio sea mayor a 4 minutos
prob_a <- pexp(4, rate = lambda, lower.tail = FALSE)

# b) Probabilidad de que el tiempo de servicio sea menor a 6 minutos
prob_b <- pexp(6, rate = lambda, lower.tail = TRUE)

# c) Tiempo que garantiza que el 80% de los clientes se atiendan antes
time_c <- qexp(0.80, rate = lambda)

list(prob_a = prob_a, prob_b = prob_b, time_c = time_c)

# Problema 2
mu <- 4000
sigma <- 120

# a) Probabilidad de que la resistencia sea menor que 3900
prob_a <- pnorm(3900, mean = mu, sd = sigma)

# b) Probabilidad de que la resistencia sea menor que 3850
prob_b <- pnorm(3850, mean = mu, sd = sigma)

# c) Probabilidad de que la resistencia sea mayor que 3880
prob_c <- pnorm(3880, mean = mu, sd = sigma, lower.tail = FALSE)

# d) Resistencia que asegura el 95% de los ítems
resistencia_95 <- qnorm(0.95, mean = mu, sd = sigma)

list(prob_a = prob_a, prob_b = prob_b, prob_c = prob_c, resistencia_95 = resistencia_95)

# Problema 3
n <- 35
p <- 0.25

# a) Probabilidad de acertar como máximo 10 preguntas correctas
prob_a <- pbinom(10, size = n, prob = p)

# b) Probabilidad de aprobar (al menos 25 correctas)
prob_b <- 1 - pbinom(24, size = n, prob = p)

# c) Probabilidad de que la 5ta pregunta sea la 4ta incorrecta
# Probabilidad de que las primeras 4 contengan 3 fallos y 1 acierto
prob_primero <- dbinom(3, size = 4, prob = 0.75)
# Probabilidad de que la quinta sea incorrecta
prob_quinta <- 0.75
# Probabilidad total
prob_c <- prob_primero * prob_quinta

list(prob_a = prob_a, prob_b = prob_b, prob_c = prob_c)

# Problema 4
n <- 1000
p <- 0.01

# Probabilidad de que nadie compre el seguro
prob_nadie <- dbinom(0, size = n, prob = p)

prob_nadie

# Problema 5
lambda <- 2
k <- 1.5

# a) Gráfica de la función de probabilidad
t <- seq(0, 10, length.out = 100)
f_t <- (lambda / k) * (t / k)^(lambda - 1) * exp(-(t / k)^lambda)
plot(t, f_t, type = "l", col = "blue", lwd = 2, 
     main = "Distribución Weibull (λ = 2, k = 1.5)", 
     xlab = "Tiempo (t)", ylab = "f(t)")

# b) Probabilidad de que la devolución tarde más de 5 semanas
prob_b <- pweibull(5, shape = lambda, scale = k, lower.tail = FALSE)

prob_b