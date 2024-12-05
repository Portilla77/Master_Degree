import pandas as pd
import statsmodels.api as sm
import itertools
import matplotlib.pyplot as plt
from scipy.stats import shapiro, jarque_bera, normaltest
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
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


def fit_model(data, response_var, predictors):
    X = sm.add_constant(data[predictors])  # Agrega término constante
    y = data[response_var]
    model = sm.OLS(y, X).fit()
    return model

def evaluate_all_models(data, response_var, predictors):
    best_model = None
    best_aic = float('inf')
    best_combination = None
    
    for r in range(1, len(predictors) + 1):
        for combination in itertools.combinations(predictors, r):
            model = fit_model(data, response_var, list(combination))
            if model.aic < best_aic:
                best_model = model
                best_aic = model.aic
                best_combination = combination
    
    return best_model, best_combination

def calculate_confidence_intervals(model, alpha=0.05):
    return model.conf_int(alpha)

def regression_to_origin(data, response_var, predictors):
    X = data[predictors]
    y = data[response_var]
    model = sm.OLS(y, X).fit()
    return model

def check_model_assumptions(model):
    residuals = model.resid
    
    print("\nVerificación de supuestos del modelo:")
    print("Pruebas de normalidad de residuos:")
    print("Pruebas: ")
    print(f"Shapiro-Wilk: {shapiro(residuals)}")
    print(f"Jarque-Bera: {jarque_bera(residuals)}")
    print(f"D'Agostino: {normaltest(residuals)}")
    print("\nPrueba de homocedasticidad (Breusch-Pagan):")
    _, pval, __, f_pval = het_breuschpagan(residuals, model.model.exog)
    print(f"P-valor Breusch-Pagan: {pval}, F-P-valor: {f_pval}")
    print("\nPrueba de autocorrelación (Durbin-Watson):")
    print(f"Estadístico de Durbin-Watson: {durbin_watson(residuals)}")

def analyze_best_model(data, response_var, predictors):
    print("Revisando todas las combinaciones posibles de regresores...")
    best_model, best_combination = evaluate_all_models(data, response_var, predictors)
    
    print(f"\nMejor modelo encontrado con predictores: {best_combination}")
    print(f"AIC del mejor modelo: {best_model.aic}")
    print(best_model.summary())
    
    print("\nIntervalos de confianza del mejor modelo:")
    confidence_intervals = calculate_confidence_intervals(best_model)
    print(confidence_intervals)
    
    print("\nEvaluando regresión al origen...")
    origin_model = regression_to_origin(data, response_var, list(best_combination))
    print("\nResultados de la regresión al origen:")
    print(origin_model.summary())
    
    check_model_assumptions(best_model)
    
    return best_model, origin_model, best_combination


file_path = "Primer_tetra/Metodos_Estadisticos/Recursos/Dataset/Gold Price Prediction.csv"

columnas_originales = [
    "date", "price_2_days_ago", "price_1_day_ago", "current_price",
    "next_day_price", "next_day_change", "price_change_10_days",
    "std_dev_10_days", "ma_20_days", "ma_50_days", "ma_200_days",
    "monthly_inflation_rate", "effr_rate", "volume", "treasury_yield_month",
    "treasury_yield_2y", "treasury_yield_10y", "dxy", "sp_open", "vix", "crude_oil"
]

columnas_renombradas = [
    "fecha", "precio_2_dias_atras", "precio_1_dia_atras", "precio_hoy",
    "precio_mañana", "cambio_precio_mañana", "cambio_precio_10_dias",
    "desviacion_std_10", "promedio_movil_20_dias", "promedio_movil_50_dias",
    "promedio_movil_200_dias", "tasa_inflacion_mensual", "tasa_EFFR", "volumen",
    "rendimiento_par_tesoros_mes", "rendimiento_par_tesoros_2_años",
    "rendimiento_curva_tesoros_10_años", "dxy", "sp_abre", "vix", "crudo"
]


significant_variables = ["desviacion_std_10", "vix", "tasa_EFFR", 
                         "cambio_precio_10_dias", "cambio_precio_mañana"]
response_var = "precio_mañana"


# data_gold = pd.read_csv(file_path, encoding="utf-8-sig", names=columnas_originales, header=0)
# data_gold.columns = columnas_renombradas


# columns_to_use = significant_variables + [response_var]
# data_gold = data_gold[columns_to_use]

# data_gold = data_gold.dropna()  # Eliminar filas con valores faltantes
# data_gold = data_gold.replace([float('inf'), float('-inf')], float('nan')).dropna()  # Manejar valores infinitos


# best_model, origin_model, best_combination = analyze_best_model(data_gold, response_var, significant_variables)
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, shapiro, levene
from statsmodels.stats.weightstats import DescrStatsW


def analyze_hypothesis_testing(data, variables, cutoff_method='median'):
    results = {}
    for variable in variables:
        print(f"\n--- Análisis para la variable: {variable} ---")
        
        if data[variable].isna().all():
            print(f"La variable {variable} tiene todos los valores nulos. Se omite.")
            continue
        
        if not np.issubdtype(data[variable].dtype, np.number):
            print(f"La variable {variable} no es numérica. Se omite.")
            continue

        if cutoff_method == 'median':
            cutoff = data[variable].median()
        else:
            cutoff = data[variable].mean()
        
        print(f"Dividiendo por el criterio de corte: {cutoff}")
        
        group_0 = data[data[variable] < cutoff][variable]
        group_1 = data[data[variable] >= cutoff][variable]
        
        print(f"Grupo 0: Menores a {cutoff} ({len(group_0)} elementos)")
        print(f"Grupo 1: Mayores o iguales a {cutoff} ({len(group_1)} elementos)")
        
        if len(group_0) < 2 or len(group_1) < 2:
            print(f"No hay suficientes datos en uno de los grupos para realizar pruebas. Se omite.")
            continue

        print("Verificando normalidad...")
        normal_0 = shapiro(group_0)
        normal_1 = shapiro(group_1)
        print(f"Grupo 0 Shapiro-Wilk p-valor: {normal_0.pvalue}")
        print(f"Grupo 1 Shapiro-Wilk p-valor: {normal_1.pvalue}")

        print("Verificando homocedasticidad...")
        var_test = levene(group_0, group_1)
        print(f"P-valor Levene: {var_test.pvalue}")

        if normal_0.pvalue > 0.05 and normal_1.pvalue > 0.05 and var_test.pvalue > 0.05:
            print("Se cumplen los requisitos para la prueba t de Student.")
            t_stat, t_pvalue = ttest_ind(group_0, group_1, equal_var=True)
            print(f"T-Statistic: {t_stat}, P-valor: {t_pvalue}")

            desc_0 = DescrStatsW(group_0)
            desc_1 = DescrStatsW(group_1)
            conf_interval = desc_0.get_compare(desc_1).summary_frame(alpha=0.05)['mean_ci']
            print(f"Intervalos de confianza: {conf_interval}")
            
            results[variable] = {
                'normalidad_grupo_0': normal_0.pvalue,
                'normalidad_grupo_1': normal_1.pvalue,
                'homocedasticidad': var_test.pvalue,
                't_stat': t_stat,
                't_pvalue': t_pvalue,
                'conf_interval': conf_interval
            }
        else:
            print("No se cumplen los requisitos para la prueba t de Student.")
            results[variable] = {
                'normalidad_grupo_0': normal_0.pvalue,
                'normalidad_grupo_1': normal_1.pvalue,
                'homocedasticidad': var_test.pvalue,
                't_stat': None,
                't_pvalue': None,
                'conf_interval': None
            }
    return results


from scipy.stats import shapiro


def evaluate_transformations_for_normality(data, variables, transformations=["original", "log", "sqrt", "z-score"]):
    """
    Evalúa transformaciones para normalidad en las variables indicadas.
    
    Args:
    - data: pd.DataFrame. Conjunto de datos.
    - variables: list. Variables a evaluar.
    - transformations: list. Tipos de transformaciones a aplicar.
    
    Return:
    - results: dict. Resultados de las pruebas de normalidad para cada variable y transformación.
    """
    results = {}
    for var in variables:
        if var not in data.columns:
            print(f"Variable {var} no encontrada en los datos.")
            continue
        
        print(f"Evaluando normalidad para la variable: {var}")
        valores = data[var].dropna()

        transformations_results = {}
        for trans in transformations:
            try:
                if trans == "original":
                    transformed = valores
                elif trans == "log":
                    transformed = np.log(valores[valores > 0])
                elif trans == "sqrt":
                    transformed = np.sqrt(valores[valores >= 0])
                elif trans == "z-score":
                    transformed = (valores - valores.mean()) / valores.std()
                else:
                    print(f"Transformación {trans} no reconocida.")
                    continue

                shapiro_stat, shapiro_p = shapiro(transformed)
                transformations_results[trans] = {
                    "shapiro_stat": shapiro_stat,
                    "shapiro_p": shapiro_p,
                    "normal": shapiro_p > 0.05
                }
            except Exception as e:
                print(f"Error aplicando transformación {trans} a la variable {var}: {e}")
                transformations_results[trans] = {
                    "shapiro_stat": None,
                    "shapiro_p": None,
                    "normal": False
                }
        
        results[var] = transformations_results

    return results


file_path = "Primer_tetra/Metodos_Estadisticos/Recursos/Dataset/Gold Price Prediction.csv"

data = pd.read_csv(file_path)
columnas_originales = data.columns.tolist()
columnas_renombradas = [
    "fecha", "precio_2_dias_atras", "precio_1_dia_atras", "precio_hoy",
    "precio_mañana", "cambio_precio_mañana", "cambio_precio_10_dias",
    "desviacion_std_10", "promedio_movil_20_dias", "promedio_movil_50_dias",
    "promedio_movil_200_dias", "tasa_inflacion_mensual", "tasa_EFFR", "volumen",
    "rendimiento_par_tesoros_mes", "rendimiento_par_tesoros_2_años",
    "rendimiento_curva_tesoros_10_años", "dxy", "sp_abre", "vix", "crudo"
]
data.columns = columnas_renombradas

# results = analyze_hypothesis_testing(data, significant_variables, cutoff_method='median')


# print("\nResultados finales:")
# for var, res in results.items():
#     print(f"\nVariable: {var}")
#     for key, value in res.items():
#         print(f"  {key}: {value}")

from scipy.stats import shapiro, ttest_ind
from sklearn.preprocessing import StandardScaler


significant_variables = ["desviacion_std_10", "vix", "tasa_EFFR", 
                         "cambio_precio_10_dias", "cambio_precio_mañana"]

data = pd.read_csv(file_path, usecols=columnas_originales)
data.columns = columnas_renombradas

data = data[significant_variables]


def evaluar_transformaciones(data, variables):
    resultados = {}
    for variable in variables:
        print(f"\nEvaluando normalidad para la variable: {variable}")
        original_data = data[variable].dropna()

        transformaciones = {
            'original': original_data,
            'log': np.log(original_data[original_data > 0]),
            'sqrt': np.sqrt(original_data[original_data >= 0]),
            'z-score': StandardScaler().fit_transform(original_data.values.reshape(-1, 1)).flatten()
        }
        
        resultados[variable] = {}
        for nombre, datos_trans in transformaciones.items():
            if len(datos_trans) > 0:
                shapiro_p = shapiro(datos_trans).pvalue
                resultados[variable][nombre] = shapiro_p
                print(f"Transformación: {nombre}, Shapiro-Wilk p-valor: {shapiro_p}, ¿Normal?: {shapiro_p > 0.05}")
    
    return resultados

def pruebas_hipotesis(data, variables, transformacion):
    resultados = {}
    for variable in variables:
        print(f"\n--- Pruebas de hipótesis para la variable: {variable} ---")
        datos = data[variable].dropna()
        
        if transformacion == 'log':
            datos = np.log(datos[datos > 0])
        elif transformacion == 'sqrt':
            datos = np.sqrt(datos[datos >= 0])
        elif transformacion == 'z-score':
            datos = StandardScaler().fit_transform(datos.values.reshape(-1, 1)).flatten()
        

        mediana = datos.median()
        grupo_0 = datos[datos < mediana]
        grupo_1 = datos[datos >= mediana]
        

        t_stat, p_value = ttest_ind(grupo_0, grupo_1, equal_var=False)
        resultados[variable] = {'t_stat': t_stat, 'p_value': p_value}
        print(f"Prueba t: t_stat={t_stat}, p_value={p_value}")
    
    return resultados


# resultados_transformaciones = evaluar_transformaciones(data, significant_variables)


# transformacion_seleccionada = 'sqrt'  # Cambiar según los resultados obtenidos
# resultados_pruebas = pruebas_hipotesis(data, significant_variables, transformacion_seleccionada)

# resultados_transformaciones, resultados_pruebas

from scipy.stats import boxcox, yeojohnson, shapiro

def aplicar_transformaciones_avanzadas(data, variables):
    resultados = {}
    for variable in variables:
        valores = data[variable].dropna()
        transformaciones = {}

        if np.all(valores > 0):
            transformaciones['boxcox'], lambda_bc = boxcox(valores)
            transformaciones['boxcox_lambda'] = lambda_bc

        transformaciones['yeojohnson'], lambda_yj = yeojohnson(valores)
        transformaciones['yeojohnson_lambda'] = lambda_yj


        resultados[variable] = {
            nombre: {
                'datos': datos_trans,
                'shapiro_p': shapiro(datos_trans)[1],
                'es_normal': shapiro(datos_trans)[1] > 0.05
            }
            for nombre, datos_trans in transformaciones.items() if nombre != 'boxcox_lambda' and nombre != 'yeojohnson_lambda'
        }
    return resultados

variables_analizar = [
    "desviacion_std_10",
    "vix",
    "tasa_EFFR",
    "cambio_precio_10_dias",
    "cambio_precio_mañana"
]

resultados_transformaciones = aplicar_transformaciones_avanzadas(data, variables_analizar)

def resumen_transformaciones(resultados_transformaciones):
    resumen = []
    for variable, transformaciones in resultados_transformaciones.items():
        for nombre_transformacion, resultados in transformaciones.items():
            resumen.append({
                "Variable": variable,
                "Transformación": nombre_transformacion,
                "P-valor Shapiro": resultados['shapiro_p'],
                "Cumple Normalidad": resultados['es_normal']
            })
    return pd.DataFrame(resumen)


# resumen_resultados = resumen_transformaciones(resultados_transformaciones)
# print(resumen_resultados)

#import ace_tools as tools; tools.display_dataframe_to_user(name="Resumen Transformaciones Normalidad", dataframe=resumen_resultados)

from scipy.stats import boxcox, yeojohnson, shapiro, ttest_ind

def aplicar_transformaciones_avanzadas(data, variables):
    """
    Aplica transformaciones avanzadas (Box-Cox, Yeo-Johnson) y evalúa la normalidad.
    """
    resultados = {}
    for variable in variables:
        valores = data[variable].dropna()
        transformaciones = {}

        if np.all(valores > 0):
            datos_bc, lambda_bc = boxcox(valores)
            transformaciones['boxcox'] = datos_bc
            transformaciones['boxcox_lambda'] = lambda_bc

        datos_yj, lambda_yj = yeojohnson(valores)
        transformaciones['yeojohnson'] = datos_yj
        transformaciones['yeojohnson_lambda'] = lambda_yj

        resultados[variable] = {
            nombre: {
                'datos': datos_trans,
                'shapiro_p': shapiro(datos_trans)[1],
                'es_normal': shapiro(datos_trans)[1] > 0.05
            }
            for nombre, datos_trans in transformaciones.items() if nombre != 'boxcox_lambda' and nombre != 'yeojohnson_lambda'
        }

        if 'boxcox_lambda' in transformaciones:
            resultados[variable]['boxcox_lambda'] = transformaciones['boxcox_lambda']
        if 'yeojohnson_lambda' in transformaciones:
            resultados[variable]['yeojohnson_lambda'] = transformaciones['yeojohnson_lambda']
    
    return resultados

variables_analizar = [
    "desviacion_std_10",
    "vix",
    "tasa_EFFR",
    "cambio_precio_10_dias",
    "cambio_precio_mañana"
]

resultados_transformaciones = aplicar_transformaciones_avanzadas(data, variables_analizar)

variable_seleccionada = 'cambio_precio_10_dias'
valores_originales = data[variable_seleccionada].dropna()
datos_transformados = pd.Series(
    resultados_transformaciones[variable_seleccionada]['yeojohnson']['datos'], 
    index=valores_originales.index
)
lambda_yj = resultados_transformaciones[variable_seleccionada]['yeojohnson_lambda']

criterio_corte = valores_originales.median()
grupo_0 = datos_transformados[valores_originales < criterio_corte]
grupo_1 = datos_transformados[valores_originales >= criterio_corte]


t_stat, p_value = ttest_ind(grupo_0, grupo_1, equal_var=True)


print(f"Prueba t para {variable_seleccionada} transformado (Yeo-Johnson):")
print(f"T-statistic: {t_stat}, P-value: {p_value}")

def yeojohnson_inverse(y, lambda_yj):
    if lambda_yj == 0:
        return np.exp(y) - 1
    else:
        return np.sign(y) * (np.abs(y) * lambda_yj + 1)**(1 / lambda_yj) - 1

grupo_0_original = yeojohnson_inverse(grupo_0, lambda_yj)
grupo_1_original = yeojohnson_inverse(grupo_1, lambda_yj)

print("\nGrupo 0 (restaurado a escala original):", grupo_0_original[:5])
print("Grupo 1 (restaurado a escala original):", grupo_1_original[:5])