import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from Primer_tetra.helpers.helpers import save_plot
from scipy.stats import norm, gamma, expon, lognorm, weibull_min, beta, kstest, chi2

data_gold = pd.read_csv("Primer_tetra/Metodos_Estadisticos/Recursos/Dataset/Gold Price Prediction.csv")

nuevos_nombres_columnas = [
    "fecha", "precio_2_dias_atras", "precio_1_dia_atras", "precio_hoy", 
    "precio_mañana", "cambio_precio_mañana", "cambio_precio_10_dias", 
    "desviacion_std_10", "promedio_movil_20_dias", "promedio_movil_50_dias", 
    "promedio_movil_200_dias", "tasa_inflacion_mensual", "tasa_EFFR", "volumen", 
    "rendimiento_par_tesoros_mes", "rendimiento_par_tesoros_2_años", 
    "rendimiento_curva_tesoros_10_años", "dxy", "sp_abre", "vix", "crudo"
]
data_gold.columns = nuevos_nombres_columnas

columnas_interes = [
    "cambio_precio_10_dias", "cambio_precio_mañana", "crudo", "dxy", 
    "precio_1_dia_atras", "precio_2_dias_atras", "precio_hoy", "precio_mañana", 
    "rendimiento_curva_tesoros_10_años", "rendimiento_par_tesoros_2_años", 
    "rendimiento_par_tesoros_mes", "sp_abre", "tasa_EFFR", "tasa_inflacion_mensual", 
    "vix", "volumen"
]
data_gold_new = data_gold[columnas_interes]

distribuciones_sospechadas = {
    "cambio_precio_10_dias": "normal",
    "cambio_precio_mañana": "normal",
    "crudo": "lognormal",
    "dxy": "normal",
    "precio_1_dia_atras": "normal",
    "precio_2_dias_atras": "normal",
    "precio_hoy": "normal",
    "precio_mañana": "normal",
    "rendimiento_curva_tesoros_10_años": "gamma",
    "rendimiento_par_tesoros_2_años": "gamma",
    "rendimiento_par_tesoros_mes": "gamma",
    "sp_abre": "normal",
    "tasa_EFFR": "exponencial",
    "tasa_inflacion_mensual": "gamma",
    "vix": "gamma",
    "volumen": "normal"
}

#########################
#       Histogramas     #
#########################

def plot_histogram(data, variable_name, distribucion_sospechada, filename, bins=10):
    """
    Genera un histograma con la curva ajustada para la distribución sospechada.

    Args:
        data (pd.Series): Datos para el histograma.
        variable_name (str): Nombre de la variable analizada.
        distribucion_sospechada (str): Distribución sospechada ('normal', 'gamma', etc.).
        filename (str): Nombre del archivo para guardar la gráfica.
        bins (int, optional): Número de bins para el histograma. Por defecto es 10.
    """
    plt.figure(figsize=(8, 6))
    count, bins, ignored = plt.hist(data.dropna(), bins=bins, density=True, alpha=0.6, color='lightblue', edgecolor='black')

    if distribucion_sospechada == "normal":
        mu, std = np.mean(data), np.std(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = f'Distribución Normal Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "gamma":
        shape, loc, scale = stats.gamma.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.gamma.pdf(x, shape, loc, scale)
        plt.plot(x, p, 'r', linewidth=2)
        title = f'Distribución Gamma Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "exponencial":
        loc, scale = stats.expon.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.expon.pdf(x, loc, scale)
        plt.plot(x, p, 'g', linewidth=2)
        title = f'Distribución Exponencial Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "lognormal":
        shape, loc, scale = stats.lognorm.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.lognorm.pdf(x, shape, loc, scale)
        plt.plot(x, p, 'b', linewidth=2)
        title = f'Distribución Log-Normal Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "uniforme":
        loc, scale = stats.uniform.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.uniform.pdf(x, loc, scale)
        plt.plot(x, p, 'm', linewidth=2)
        title = f'Distribución Uniforme Ajustada para {variable_name}'

    plt.xlim(data.min() - 0.1 * abs(data.min()), data.max() + 0.1 * abs(data.max()))
    plt.ylim(0, max(count) * 1.2)
    plt.title(title, fontsize=14)
    plt.xlabel(f'Valores de {variable_name}', fontsize=12)
    plt.ylabel('Densidad de Frecuencia', fontsize=12)
    save_plot(plt.gcf(), filename=filename, dpi=300, show=False)

#############################
#       Prueba Kolmogorv    #
#############################

def prueba_kolmogorov_smirnov(valores, distribucion):
    """
    Realiza la prueba de bondad de ajuste Kolmogorov-Smirnov.
    """
    if distribucion == "normal":
        mu, sigma = norm.fit(valores)
        estadistico, p_value = kstest(valores, 'norm', args=(mu, sigma))
    elif distribucion == "gamma":
        shape, loc, scale = gamma.fit(valores)
        estadistico, p_value = kstest(valores, 'gamma', args=(shape, loc, scale))
    elif distribucion == "exponencial":
        loc, scale = expon.fit(valores)
        estadistico, p_value = kstest(valores, 'expon', args=(loc, scale))
    
    print(f"\nPrueba Kolmogorov-Smirnov para {distribucion.capitalize()}:")
    print(f"Estadístico KS: {estadistico:.4f}")
    print(f"p-valor: {p_value:.4f}")
    
    if p_value < 0.05:
        print("Resultado: Se rechaza la hipótesis nula. Los datos no se ajustan bien a esta distribución.")
    else:
        print("Resultado: No se rechaza la hipótesis nula. Los datos se ajustan bien a esta distribución.")

################################
#      Prueba Chi cuadrada     #
################################

def prueba_chi_cuadrado(valores, distribucion, bins=10):
    """
    Realiza la prueba de bondad de ajuste Chi-cuadrado para una distribución.
    """
    observados, limites = np.histogram(valores, bins=bins)

    if distribucion == "normal":
        mu, sigma = norm.fit(valores)
        esperados = np.diff(norm.cdf(limites, mu, sigma)) * len(valores)
    elif distribucion == "gamma":
        shape, loc, scale = gamma.fit(valores)
        esperados = np.diff(gamma.cdf(limites, shape, loc, scale)) * len(valores)
    elif distribucion == "exponencial":
        loc, scale = expon.fit(valores)
        esperados = np.diff(expon.cdf(limites, loc, scale)) * len(valores)

    chi2_stat = np.sum((observados - esperados) ** 2 / esperados)
    grados_libertad = bins - 1 - (2 if distribucion == "gamma" else 1)
    p_value = 1 - chi2.cdf(chi2_stat, grados_libertad)
    
    print(f"\nPrueba Chi-cuadrado para {distribucion.capitalize()}:")
    print(f"Estadístico Chi-cuadrado: {chi2_stat:.4f}")
    print(f"Grados de libertad: {grados_libertad}")
    print(f"p-valor: {p_value:.4f}")
    
    if p_value < 0.05:
        print("Resultado: Se rechaza la hipótesis nula. Los datos no se ajustan bien a esta distribución.")
    else:
        print("Resultado: No se rechaza la hipótesis nula. Los datos se ajustan bien a esta distribución.")

#########################################
#       Transformaciones aplicadas      #
#########################################
def ajustar_transformar_datos(data, variable, distribucion):
    """
    Ajusta una distribución con transformaciones y genera QQ-plots.
    """
    valores = data[variable].dropna()

    transformaciones = {
        'original': valores,
        'log': np.log(valores[valores > 0]),  # Log-transform solo para valores > 0
        'sqrt': np.sqrt(valores[valores >= 0]),  # Raíz cuadrada para valores >= 0
        'z-score': (valores - valores.mean()) / valores.std()
    }

    resultados = {}
    for nombre, datos_trans in transformaciones.items():
        if len(datos_trans) == 0:
            continue

        params = distribucion.fit(datos_trans)

        # Prueba Kolmogorov-Smirnov
        ks_stat, ks_p = stats.kstest(datos_trans, distribucion.name, args=params)

        # Prueba Chi-cuadrado
        bins = np.histogram_bin_edges(datos_trans, bins='auto')
        hist, bin_edges = np.histogram(datos_trans, bins=bins, density=False)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        expected_prob = distribucion.pdf(bin_centers, *params)
        expected_freq = expected_prob * np.sum(hist) * (bin_edges[1] - bin_edges[0])
        expected_freq *= np.sum(hist) / np.sum(expected_freq)

        if not np.isclose(np.sum(hist), np.sum(expected_freq), rtol=1e-8):
            print(f"Warning: Discrepancia entre las frecuencias observadas y esperadas para {variable} ({nombre})")

        chi_stat, chi_p = stats.chisquare(f_obs=hist, f_exp=expected_freq)

        resultados[nombre] = {
            'params': params,
            'ks_stat': ks_stat, 'ks_p': ks_p,
            'chi_stat': chi_stat, 'chi_p': chi_p
        }

        fig = plt.figure(figsize=(6, 6))
        stats.probplot(datos_trans, dist=distribucion, sparams=params, plot=plt)
        plt.title(f'QQ-plot para {variable} ({nombre}) ajustado a {distribucion.name}')
        save_plot(fig, f'qqplot_{variable}_{nombre}.png')

    return resultados

########################################
#       Prueba de bondad de ajuste     #
########################################

# Lista de distribuciones a probar
distribuciones = {
    "normal": norm,
    "gamma": gamma,
    "exponencial": expon,
    "log-normal": lognorm,
    "weibull": weibull_min,
    "beta": beta
}

def probar_distribuciones(data, variable):
    """
    Prueba múltiples distribuciones para una variable y selecciona la mejor.
    """
    valores = data[variable].dropna()
    if valores.empty:
        print(f"La variable {variable} no tiene datos válidos.")
        return None

    resultados = {}
    for nombre, distribucion in distribuciones.items():
        try:
            params = distribucion.fit(valores)
            
            # Prueba Kolmogorov-Smirnov
            ks_stat, ks_p = stats.kstest(valores, distribucion.name, args=params)
            resultados[nombre] = {
                "params": params,
                "ks_stat": ks_stat,
                "ks_p": ks_p
            }
        except Exception as e:
            print(f"Error al ajustar {nombre} a la variable {variable}: {e}")

    if not resultados:
        print(f"Ninguna distribución se ajustó a la variable {variable}.")
        return None

    mejor_ajuste = max(resultados.items(), key=lambda x: x[1]["ks_p"])
    print(f"Mejor ajuste para {variable}: {mejor_ajuste[0]} con p-valor={mejor_ajuste[1]['ks_p']:.4f}")
    return mejor_ajuste

#####################
#       QQPLOTS     #
#####################

def generar_qqplots(data, resultados_ajustes):
    """
    Genera QQ-plots basados en los mejores ajustes encontrados para cada variable.

    Args:
    - data: DataFrame que contiene las variables.
    - resultados_ajustes: Diccionario donde las claves son los nombres de las variables
      y los valores son tuplas (nombre_distribucion, resultado), donde resultado contiene "params".
    """
    for variable, (nombre_distribucion, resultado) in resultados_ajustes.items():
        try:
            distribucion = {
                "normal": stats.norm,
                "gamma": stats.gamma,
                "exponencial": stats.expon,
                "log-normal": stats.lognorm,
                "weibull": stats.weibull_min,
                "beta": stats.beta
            }.get(nombre_distribucion)

            if not distribucion:
                print(f"Distribución {nombre_distribucion} no reconocida para la variable {variable}.")
                continue
            valores = data[variable].dropna()
            if nombre_distribucion == "sqrt":
                valores = np.sqrt(valores)
                distribucion = stats.norm

            params = resultado["params"]
            fig = plt.figure(figsize=(6, 6))
            stats.probplot(valores, dist=distribucion, sparams=params, plot=plt)
            plt.title(f'QQ-plot para {variable} ajustado a {nombre_distribucion}')
            save_plot(fig, f'qqplot_{variable}_{nombre_distribucion}.png')
            print(f"QQ-plot generado para {variable} con distribución {nombre_distribucion}.")
        except Exception as e:
            print(f"Error al generar QQ-plot para {variable} con distribución {nombre_distribucion}: {e}")
if __name__ == '__main__':
    #Histogramas
    for variable, distribucion in distribuciones_sospechadas.items():
        if variable in data_gold_new.columns:
            filename = f"{variable}_{distribucion}.png"
            plot_histogram(data_gold_new[variable], variable, distribucion, filename)
    variables_distribuciones = {
        "desviacion_std_10": "normal",
        "vix": "gamma",
        "tasa_EFFR": "exponencial",
        "cambio_precio_10_dias": "normal",
        "cambio_precio_mañana": "normal",
        "precio_mañana": "normal"
    }
    supuestos_variables_distribuciones = {
    "desviacion_std_10": norm,
    "vix": gamma,
    "tasa_EFFR": expon,
    "cambio_precio_10_dias": norm,
    "cambio_precio_mañana": norm,
    "precio_mañana": norm,
    }
    # Pruebas KS y Chi cuadrada
    for variable, distribucion in variables_distribuciones.items():
        valores = data_gold[variable].dropna()
        print(f"\nVariable: {variable}")
        # Prueba Kolmogorov-Smirnov
        prueba_kolmogorov_smirnov(valores, distribucion)
        # Prueba Chi-cuadrado
        print("---------")
        prueba_chi_cuadrado(valores, distribucion, bins=10)

    resultados = {}
    for variable, distribucion in supuestos_variables_distribuciones.items():
        resultados[variable] = ajustar_transformar_datos(data_gold, variable, distribucion)
    for variable, res in resultados.items():
        print(f"Resultados para {variable}:")
        for transformacion, datos in res.items():
            print(f" Transformación: {transformacion}")
            print(f"  Parámetros: {datos['params']}")
            print(f"  KS: Estadístico={datos['ks_stat']:.4f}, p-valor={datos['ks_p']:.4f}")
            print(f"  Chi-cuadrado: Estadístico={datos['chi_stat']:.4f}, p-valor={datos['chi_p']:.4f}")
        print("-" * 40)

    variables_especificas = [
        "desviacion_std_10", "vix", "tasa_EFFR",
        "cambio_precio_10_dias", "cambio_precio_mañana", "precio_mañana"
    ]

    mejores_ajustes = {}
    for variable in variables_especificas:
        if variable in data_gold.columns:
            ajuste = probar_distribuciones(data_gold, variable)
            if ajuste:
                mejores_ajustes[variable] = ajuste
            else:
                mejores_ajustes[variable] = "No se pudo ajustar"
        else:
            print(f"La variable {variable} no está en el DataFrame.")
            mejores_ajustes[variable] = "No existe en el DataFrame"
    
    for variable, ajuste in mejores_ajustes.items():
        if ajuste == "No se pudo ajustar" or ajuste == "No existe en el DataFrame":
            print(f"{variable} -> {ajuste}")
        else:
            nombre, resultado = ajuste
            print(f"{variable} -> Mejor distribución: {nombre}, p-valor={resultado['ks_p']:.4f}")
    mejores_ajustes = {
    "desviacion_std_10": ("log-normal", {"params": (2.9346, 0.4622)}),
    "vix": ("gamma", {"params": (1.598, 11.505, 5.242)}),
    "tasa_EFFR": ("exponencial", {"params": (0.08, 3.601)}),
    "cambio_precio_10_dias": ("log-normal", {"params": (3.4166, 1.2423)}),
    "cambio_precio_mañana": ("gamma", {"params": (3.3069, 1.5736)}),
    "precio_mañana": ("log-normal", {"params": (7.575, 0.096)})
    }
    generar_qqplots(data_gold, mejores_ajustes)