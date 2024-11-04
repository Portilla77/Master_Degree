# antes = c(45,73,46,124,33,57,83,34,26,17,11)
# despues = c(36,60,44,119,35,51,77,29,24,11)
# #Hipotesis
#H0: d =antes-despues=0
# H1: d = antes-desp>0 esto implica que se
#tardaban más antes.
#t.test(antes,despues,paired = T,alternative)
#paired es pares)
#rechazo H0 si p-valor<alfa, 0.0029<0.05
#rechazo H0 si d= antes-desp!=0
#con IC de 2.283<antes-desp <8.1165


antes <- c(45, 73, 46, 124, 33, 57, 83, 34, 26, 17, 11)
despues <- c(36, 60, 44, 119, 35, 51, 77, 29, 24, 11)

# Hipótesis
# H0: d = antes - despues = 0
# H1: d > 0 implica que se tardaban más antes.

# Prueba t para datos emparejados
resultado = t.test(antes, despues, paired = TRUE, alternative = "greater")
#

# Mostrar el resultado de la prueba t
print(resultado)

# Rechazo H0 si p-valor < alfa, 0.0029 < 0.05
