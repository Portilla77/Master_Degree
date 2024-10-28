# Problema 2
#a)
duration_component <- c(184.2, 116.3, 154.1, 98.5, 106.2, 126.5, 130.7,
                        155.1, 142, 100.9, 135, 102.1, 104.5, 76.8, 130.9,
                        121.2, 102.2, 165.1, 190.6, 99.5, 89.2)

alpha <- mean(duration_component)

gamma_value <- gamma(1.4)

beta_value <- alpha / gamma_value
print(beta_value)

#b)
expected_X <- beta_value * gamma_value
print(expected_X)

#c)
alpha <- 2.5
beta <- beta_value
x <- 100

# Probabilidad P(X > 100)
probability_greater_100 <- exp(-(x / beta) ^ alpha)
print(probability_greater_100)

# Problema 3
#a)
temperature_values <- c(39.4, 39.3, 36.1, 38.7, 37.4, 37.9, 38, 37.7,
                        39.8, 37.4, 37.1, 37.1, 38, 39.1, 37, 37.7,
                        38.9, 38.1, 36.6, 39.9, 38, 39.3, 37.2, 38.2,
                        39.5, 36.8, 38.4, 36.5)

temperature_mean <- mean(temperature_values)
print(temperature_mean)
temperature_var <- var(temperature_values)
print(temperature_var)

#b)
temperature_desv <- sqrt(temperature_var)

z_value <- (40 - temperature_mean) / temperature_desv

# Probabilidad P(X > 40)
probability_greater_40 <- 1 - pnorm(z_value)
print(probability_greater_40)
