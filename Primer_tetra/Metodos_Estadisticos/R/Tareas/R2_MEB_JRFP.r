data_gold_price  <- read.csv("Primer_tetra/Metodos_Estadisticos/Recursos/Dataset/Gold Price Prediction.csv")

data_gold_price <- read.csv("Primer_tetra/Metodos_Estadisticos/Recursos/Dataset/Gold Price Prediction.csv", fileEncoding = "UTF-8-BOM")
#colnames(data_gold_price)
datos_precio_oro <- c(
  "fecha", "precio_2_dias_atras", "precio_1_dia_atras", "precio_hoy",
  "precio_mañana", "cambio_precio_mañana", "cambio_precio_10_dias",
  "desviacion_std_10", "promedio_movil_20_dias", "promedio_movil_50_dias",
  "promedio_movil_200_dias","tasa_inflacion_mensual", "tasa_EFFR", "volumen",
  "rendimiento_par_tesoros_mes", "rendimiento_par_tesoros_2_años",
  "rendimiento_curva_tesoros_10_años", "dxy", "sp_abre", "vix", "crudo"
)
colnames(data_gold_price) <-datos_precio_oro
#colnames(data_gold_price)
#is.data.frame(data_gold_price)
data_gold_price$fecha <- as.Date(data_gold_price$fecha, format = "%m/%d/%y")
#str(data_gold_price)

#Resumen de las metricas descritivas básicas:
#summary(data_gold_price)

#Cálculo de la desviación estándar:
#sapply(data_gold_price,sd,na.rm=TRUE)

#Cálculo del rango:
numericas <- sapply(data_gold_price, is.numeric)
resultados_rango <- apply(data_gold_price[, numericas], 2, function(x) {
  if (all(is.na(x))) {
    return(NA)
  } else {
    return(max(x, na.rm = TRUE) - min(x, na.rm = TRUE))
  }
})

#print(resultados_rango)

get_mode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

# Cálculo de la moda
moda_resultados <- apply(data_gold_price[, numericas], 2, function(value) {
  if (all(is.na(value))) {
    return(NA)
  } else {
    return(get_mode(value))
  }
})
#print(moda_resultados)

get_mode <- function(v) {
  v <- na.omit(v)
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}
moda_price_change_ten <- get_mode(data_gold_price$cambio_precio_10_dias)
#print(moda_price_change_ten)

# Graficar frecuencias
variables <- c("precio_2_dias_atras", "precio_1_dia_atras", "precio_hoy", "precio_mañana",
               "cambio_precio_mañana", "cambio_precio_10_dias", "tasa_inflacion_mensual",
               "tasa_EFFR", "volumen", "rendimiento_par_tesoros_mes", "rendimiento_par_tesoros_2_años",
               "rendimiento_curva_tesoros_10_años", "dxy", "sp_abre", "vix", "crudo")

guardar_frecuencia_imagen <- function(data, variable, ruta_carpeta) {
  frecuencias <- table(cut(data[[variable]], breaks = 10))
  archivo <- file.path(ruta_carpeta, paste0(variable, "_frecuencia.png"))

  png(filename = archivo)
  barplot(frecuencias, main = paste("Frecuencia de", variable), xlab = variable, col = "lightblue")
  dev.off()
}
ruta_frecuencias <- "Primer_tetra/Metodos_Estadisticos/Frecuencias"

#for (var in variables) {
#  guardar_frecuencia_imagen(data_gold_price, var, ruta_frecuencias)
#}

# Graficar histogramas
guardar_histograma <- function(data, variable, ruta_carpeta) {
  if (!dir.exists(ruta_carpeta)) {
    dir.create(ruta_carpeta, recursive = TRUE)
  }
  archivo <- file.path(ruta_carpeta, paste0(variable, "_histograma.png"))
  png(filename = archivo)
  hist(data[[variable]], main = paste("Histograma de", variable), xlab = variable, col = "lightblue", breaks = 10)
  dev.off()
}

ruta_histogramas <- "Primer_tetra/Metodos_Estadisticos/Curvas_ajustadas"
# for (var in variables) {
#   guardar_histograma(data_gold_price, var, ruta_histogramas)
# }

# Generar boxplots
guardar_boxplot <- function(data, variable, ruta_carpeta) {
  if (!dir.exists(ruta_carpeta)) {
    dir.create(ruta_carpeta, recursive = TRUE)
  }
  archivo <- file.path(ruta_carpeta, paste0(variable, "_boxplot.png"))
  png(filename = archivo)
  boxplot(data[[variable]], main = paste("Boxplot de", variable), ylab = variable, col = "lightblue")
  dev.off()
}
ruta_boxplots <- "Primer_tetra/Metodos_Estadisticos/Boxplot"
# for (var in variables) {
#   guardar_boxplot(data_gold_price, var, ruta_boxplots)
# }


library(ggplot2)
library(MASS)

# Función para crear histogramas con curva ajustada
guardar_histograma_con_ajuste <- function(data, variable, distribucion, ruta_carpeta) {
  if (!dir.exists(ruta_carpeta)) {
    dir.create(ruta_carpeta, recursive = TRUE)
  }

  archivo <- file.path(ruta_carpeta, paste0(variable, "_histograma_con_curva.png"))
  png(filename = archivo)

  hist(data[[variable]], prob = TRUE, main = paste("Histograma con ajuste de", variable), 
       xlab = variable, col = "lightblue", breaks = 30)

  if (distribucion == "normal") {
    ajuste <- fitdistr(data[[variable]], "normal")
    curve(dnorm(x, mean = ajuste$estimate[1], sd = ajuste$estimate[2]), 
          col = "red", lwd = 2, add = TRUE)
  } else if (distribucion == "lognormal") {
    ajuste <- fitdistr(data[[variable]], "lognormal")
    curve(dlnorm(x, meanlog = ajuste$estimate[1], sdlog = ajuste$estimate[2]), 
          col = "red", lwd = 2, add = TRUE)
  } else if (distribucion == "gamma") {
    ajuste <- fitdistr(data[[variable]], "gamma")
    curve(dgamma(x, shape = ajuste$estimate[1], rate = ajuste$estimate[2]), 
          col = "red", lwd = 2, add = TRUE)
  } else if (distribucion == "exponential") {
    ajuste <- fitdistr(data[[variable]], "exponential")
    curve(dexp(x, rate = ajuste$estimate), 
          col = "red", lwd = 2, add = TRUE)
  }

  dev.off()
}

ruta_histogramas <- "Primer_tetra/Metodos_Estadisticos/Curvas_ajustadas"

variables_y_distribuciones <- list(
  list("Cambio_precio_10_dias", "normal"),
  list("Cambio_precio_mañana", "normal"),
  list("Crudo", "lognormal"),
  list("DXY", "normal"),
  list("Precio_1_dia_atras", "normal"),
  list("Precio_2_dias_atras", "normal"),
  list("Precio_hoy", "normal"),
  list("Precio_mañana", "normal"),
  list("Rendimiento_curva_tesoros_10_años", "gamma"),
  list("Rendimiento_par_tesoros_2_años", "gamma"),
  list("Rendimiento_par_tesoros_mes", "gamma"),
  list("SP_abre", "normal"),
  list("Tasa_EFFR", "exponential"),
  list("Tasa_inflacion_mensual", "gamma"),
  list("VIX", "gamma"),
  list("Volumen", "normal")
)

# for (variable in variables_y_distribuciones) {
#   guardar_histograma_con_ajuste(data_gold_price, variable[[1]], variable[[2]], ruta_histogramas)
# }

mu <- mean(data_gold_price$cambio_precio_10_dias, na.rm = TRUE)
sigma <- sd(data_gold_price$cambio_precio_10_dias, na.rm = TRUE)
prob <- pnorm(20, mean = mu, sd = sigma, lower.tail = FALSE)
#print(paste("Probabilidad de que el cambio sea superior a 20 unidades:", prob))

mu <- mean(data_gold_price$cambio_precio_mañana, na.rm = TRUE)
sigma <- sd(data_gold_price$cambio_precio_mañana, na.rm = TRUE)
prob <- pnorm(-15, mean = mu, sd = sigma)
#print(paste("Probabilidad de que el cambio sea menor que -15 unidades:", prob))

library(MASS)
fit <- fitdistr(data_gold_price$crudo, "lognormal")
mu <- fit$estimate["meanlog"]
sigma <- fit$estimate["sdlog"]
prob <- plnorm(75, meanlog = mu, sdlog = sigma)
#print(paste("Probabilidad de que el precio del crudo sea menor a 75 unidades:", prob))

min_dxy <- min(data_gold_price$dxy, na.rm = TRUE)
max_dxy <- max(data_gold_price$dxy, na.rm = TRUE)
prob <- punif(108, min = min_dxy, max = max_dxy) - punif(102, min = min_dxy, max = max_dxy)
#print(paste("Probabilidad de que el DXY esté entre 102 y 108:", prob))

#
media_precio_1_dia_atras <- mean(data_gold_price$precio_1_dia_atras, na.rm = TRUE)
desv_precio_1_dia_atras <- sd(data_gold_price$precio_1_dia_atras, na.rm = TRUE)

media_precio_2_dias_atras <- mean(data_gold_price$precio_2_dias_atras, na.rm = TRUE)
desv_precio_2_dias_atras <- sd(data_gold_price$precio_2_dias_atras, na.rm = TRUE)

media_precio_hoy <- mean(data_gold_price$precio_hoy, na.rm = TRUE)
desv_precio_hoy <- sd(data_gold_price$precio_hoy, na.rm = TRUE)

media_precio_mañana <- mean(data_gold_price$precio_mañana, na.rm = TRUE)
desv_precio_mañana <- sd(data_gold_price$precio_mañana, na.rm = TRUE)

#Problema 5
valor_limite <- 2000
probabilidad_precio_1_dia_atras <- 1 - pnorm(valor_limite, mean = media_precio_1_dia_atras, sd = desv_precio_1_dia_atras)
probabilidad_precio_2_dias_atras <- 1 - pnorm(valor_limite, mean = media_precio_2_dias_atras, sd = desv_precio_2_dias_atras)
probabilidad_precio_hoy <- 1 - pnorm(valor_limite, mean = media_precio_hoy, sd = desv_precio_hoy)
probabilidad_precio_mañana <- 1 - pnorm(valor_limite, mean = media_precio_mañana, sd = desv_precio_mañana)

prob_precio_1_dia_atras_porcentaje <- probabilidad_precio_1_dia_atras * 100
prob_precio_2_dias_atras_porcentaje <- probabilidad_precio_2_dias_atras * 100
prob_precio_hoy_porcentaje <- probabilidad_precio_hoy * 100
prob_precio_mañana_porcentaje <- probabilidad_precio_mañana * 100

#paste("Probabilidad (1 día atrás) en porcentaje:", prob_precio_1_dia_atras_porcentaje, "%")
#paste("Probabilidad (2 días atrás) en porcentaje:", prob_precio_2_dias_atras_porcentaje, "%")
#paste("Probabilidad (hoy) en porcentaje:", prob_precio_hoy_porcentaje, "%")
#paste("Probabilidad (mañana) en porcentaje:", prob_precio_mañana_porcentaje, "%")

#problema 6

fit <- fitdistr(data_gold_price$rendimiento_curva_tesoros_10_años, "gamma")
shape <- fit$estimate["shape"]
rate <- fit$estimate["rate"]
prob <- pgamma(4.5, shape = shape, rate = rate, lower.tail = FALSE)
#print(paste("Probabilidad de que el rendimiento de bonos a 10 años sea mayor al 4.5%:", prob))

#problema 7
fit <- fitdistr(data_gold_price$rendimiento_par_tesoros_2_años, "gamma")
shape <- fit$estimate["shape"]
rate <- fit$estimate["rate"]
prob <- pgamma(3.5, shape = shape, rate = rate)
#print(paste("Probabilidad de que el rendimiento de bonos a 2 años sea inferior al 3.5%:", prob))

#problema8
mu <- mean(data_gold_price$sp_abre, na.rm = TRUE)
sigma <- sd(data_gold_price$sp_abre, na.rm = TRUE)
prob <- pnorm(4500, mean = mu, sd = sigma, lower.tail = FALSE)
#print(paste("Probabilidad de que el S&P abra con más de 4500 puntos:", prob))

#problema9
fit <- fitdistr(data_gold_price$tasa_EFFR, "exponential")
rate <- fit$estimate["rate"]
prob <- pexp(5, rate = rate, lower.tail = FALSE)
#print(paste("Probabilidad de que la EFFR supere el 5%:", prob))

#problema10
fit <- fitdistr(data_gold_price$tasa_inflacion_mensual, "gamma")
shape <- fit$estimate["shape"]
rate <- fit$estimate["rate"]
prob <- pgamma(4, shape = shape, rate = rate)
#print(paste("Probabilidad de que la inflación mensual sea menor al 4%:", prob))

#problema11
fit <- fitdistr(data_gold_price$vix, "gamma")
shape <- fit$estimate["shape"]
rate <- fit$estimate["rate"]
prob <- pgamma(30, shape = shape, rate = rate, lower.tail = FALSE)
#print(paste("Probabilidad de que el VIX sea mayor a 30:", prob))

#problema12
mu_volumen <- mean(data_gold_price$volumen, na.rm = TRUE)
sigma_volumen <- sd(data_gold_price$volumen, na.rm = TRUE)
valor_limite_volumen <- 120
probabilidad_volumen_mayor_120 <- 1 - pnorm(valor_limite_volumen, mean = mu_volumen, sd = sigma_volumen)
probabilidad_volumen_mayor_120_porcentaje <- probabilidad_volumen_mayor_120 * 100
paste("Probabilidad en porcentaje:", probabilidad_volumen_mayor_120_porcentaje, "%")



