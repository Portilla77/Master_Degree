from scipy.stats import norm
from scipy.stats import ttest_ind
from scipy.stats import t
from scipy.stats import ttest_1samp
from scipy.stats import ttest_rel
import numpy as np

#a)
pacientes_alvarez = [72,92,108,97,72,69,117,87,94,109,94,96,112,80,100,81,86,113,107,
77,84,99,73,69,103,103,117,100,66,66,84]

media_alvarez = np.mean(pacientes_alvarez)
print(media_alvarez)
desviacion_alvarez = np.std(pacientes_alvarez, ddof = 1)
print(desviacion_alvarez)


mu_0 = 130
t_stat, p_value = ttest_1samp(pacientes_alvarez, mu_0)
print("Estadístico t:", t_stat)
print(f"Valor p: {p_value/2}")

alpha_confianza = 0.05
n = len(pacientes_alvarez)
gl = n - 1
t_critico_confianza = t.ppf(1 - alpha_confianza / 2, gl)

margen_error = t_critico_confianza * (desviacion_alvarez / np.sqrt(n))
limite_inferior = media_alvarez - margen_error
limite_superior = media_alvarez + margen_error
print(f"Intervalo de confianza: {(limite_inferior, limite_superior)}")

#b)
pacientes_casas = [73, 70, 117, 114, 111, 109, 92, 89, 80, 111, 122, 69, 72, 90, 69, 87, 111, 85, 82, 70]
pacientes_dominguez = [119, 76, 94, 74, 107, 115, 66, 94, 122, 68, 95, 88, 82, 114, 109, 105, 97, 95, 88, 101,
                     114, 110, 116, 124, 72, 120, 106]

desviacion_casas = np.std(pacientes_casas, ddof = 1)
desviacion_dominguez = np.std(pacientes_dominguez, ddof = 1)
print(f"Pacientes Casas: {desviacion_casas}, Pacientes Dominguez: {desviacion_dominguez}")

t_stat, p_value = ttest_ind(pacientes_casas, pacientes_dominguez, alternative='less', equal_var=False)
media_casas = np.mean(pacientes_casas)
media_dominguez = np.mean(pacientes_dominguez)

n_casas = len(pacientes_casas)
n_dominguez = len(pacientes_dominguez)

mean_diff = media_casas - media_dominguez

numerador_df = (desviacion_casas**2 / n_casas + desviacion_dominguez**2 / n_dominguez)**2
denominador_df = ((desviacion_casas**2 / n_casas)**2 / (n_casas - 1)) + ((desviacion_dominguez**2 / n_dominguez)**2 / (n_dominguez - 1))
df = numerador_df / denominador_df
alpha = 0.05
t_critical = t.ppf(1 - alpha/2, df)

margin_of_error = t_critical * np.sqrt(desviacion_casas**2 / n_casas + desviacion_dominguez**2 / n_dominguez)

ci_lower = mean_diff - margin_of_error
ci_upper = mean_diff + margin_of_error

print("Media de Pacientes Casas:", media_casas)
print("Media de Pacientes Dominguez:", media_dominguez)
print("Desviación Estándar de Pacientes Casas:", desviacion_casas)
print("Desviación Estándar de Pacientes Dominguez:", desviacion_dominguez)
print("Estadístico t:", t_stat)
print("Valor p:", p_value)
print(f"Intervalo de confianza: {(ci_lower, ci_upper)}")

#c)
p_0 = 0.15
n = len(pacientes_dominguez)
no_controlados = sum(1 for glucosa in pacientes_dominguez if glucosa < 80 or glucosa > 130)
p_muestral = no_controlados / n
z = (p_muestral - p_0) / np.sqrt((p_0 * (1 - p_0)) / n)
p_value = 1 - norm.cdf(z)
z_critical = norm.ppf(1 - alpha / 2)

margin_of_error = z_critical * np.sqrt((p_muestral * (1 - p_muestral)) / n)

ci_lower = p_muestral - margin_of_error
ci_upper = p_muestral + margin_of_error

print(f"Número de pacientes 'no controlados': {no_controlados}")
print(f"Proporción muestral de pacientes no controlados: {p_muestral:.3f}")
print(f"Estadístico z: {z:.3f}")
print(f"Valor p: {p_value:.3f}")
print(f"Intervalo de confianza del 95% para la proporción muestral: ({ci_lower:.3f}, {ci_upper:.3f})")

#d)
pacientes_benitez = [112,123,122,122,112,85,98,105,110,112,69,86,78,117,114,84,74,103,109,100]

media_casas = np.mean(pacientes_casas)
media_benitez = np.mean(pacientes_benitez)
desviacion_casas = np.std(pacientes_casas, ddof=1)
desviacion_benitez = np.std(pacientes_benitez, ddof=1)

n_casas = len(pacientes_casas)
n_benitez = len(pacientes_benitez)

media_diff = media_casas - media_benitez

numerador_df = (desviacion_casas**2 / n_casas + desviacion_benitez**2 / n_benitez)**2
denominador_df = ((desviacion_casas**2 / n_casas)**2 / (n_casas - 1)) + ((desviacion_benitez**2 / n_benitez)**2 / (n_benitez - 1))
df = numerador_df / denominador_df

t_critical = t.ppf(1 - alpha/2, df)

margin_of_error = t_critical * np.sqrt((desviacion_casas**2 / n_casas) + (desviacion_benitez**2 / n_benitez))

ci_lower = media_diff - margin_of_error
ci_upper = media_diff + margin_of_error

t_stat, p_value = ttest_ind(pacientes_casas, pacientes_benitez, alternative='greater', equal_var=False)

print(f"Media Dr. Casas: {media_casas:.2f}, Desviación estándar Dr. Casas: {desviacion_casas:.2f}")
print(f"Media Dr. Benítez: {media_benitez:.2f}, Desviación estándar Dr. Benítez: {desviacion_benitez:.2f}")
print(f"Estadístico t: {t_stat:.2f}")
print(f"Valor p: {p_value:.4f}")
print(f"Intervalo de confianza del 95% para la diferencia de medias: ({ci_lower:.2f}, {ci_upper:.2f})")

#e)
antes_tratamiento = [72, 92, 108, 97, 72, 69, 117, 87, 94, 109, 94, 96, 112, 80, 100, 81, 86, 113, 107, 77]
despues_tratamiento = [62, 90, 100, 95, 74, 70, 107, 87, 95, 109, 95, 90, 102, 81, 105, 80, 86, 103, 105, 70]
diferencias = np.array(antes_tratamiento) - np.array(despues_tratamiento)
media_diferencias = np.mean(diferencias)
desviacion_diferencias = np.std(diferencias, ddof=1)
n = len(diferencias)
t_stat = media_diferencias / (desviacion_diferencias / np.sqrt(n))
p_value = ttest_rel(antes_tratamiento, despues_tratamiento, alternative='greater').pvalue
t_critical = t.ppf(1 - alpha / 2, df=n - 1)
margin_of_error = t_critical * (desviacion_diferencias / np.sqrt(n))
ci_lower = media_diferencias - margin_of_error
ci_upper = media_diferencias + margin_of_error
print(f"Media de las diferencias: {media_diferencias:.2f}")
print(f"Desviación estándar de las diferencias: {desviacion_diferencias:.2f}")
print(f"Estadístico t: {t_stat:.2f}")
print(f"Valor p: {p_value:.4f}")
print(f"Intervalo de confianza del 95% para la media de las diferencias: ({ci_lower:.2f}, {ci_upper:.2f})")

