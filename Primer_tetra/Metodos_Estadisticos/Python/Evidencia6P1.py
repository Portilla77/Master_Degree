import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import t
from Primer_tetra.helpers.helpers import save_plot
import scipy.stats as stats

def calculate_linear_model(x, y):
    """
    Calcula la ecuación del modelo de línea recta estimada (regresión lineal).

    Args:
        x (np.array): Valores de la variable independiente.
        y (np.array): Valores de la variable dependiente.

    Return:
        dict: Diccionario con la media de x, media de y, pendiente, intercepto y la ecuación del modelo.
    """
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    beta_1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)

    beta_0 = y_mean - beta_1 * x_mean

    model_equation = f"ŷ = {beta_0:.4f} + {beta_1:.4f}x"

    return {
        "x_mean": x_mean,
        "y_mean": y_mean,
        "B0": beta_0,
        "B1": beta_1,
        "Ecuación del modelo": model_equation
    }

def significance_test(x, y, alpha=0.05):
    """
    Realiza la prueba de significancia del modelo de regresión lineal.

    Args:
        x (np.array): Valores de la variable independiente.
        y (np.array): Valores de la variable dependiente.
        alpha (float): Nivel de significancia (por defecto 0.05).

    Return:
        dict: Resultados de la prueba incluyendo hipótesis, p-valor, comparación con alfa y conclusión.
    """
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    beta_1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    beta_0 = y_mean - beta_1 * x_mean
    y_pred = beta_0 + beta_1 * x
    residuals = y - y_pred
    s_squared = np.sum(residuals**2) / (n - 2)
    s = np.sqrt(s_squared)
    Sxx = np.sum((x - x_mean) ** 2)
    beta_1_std_error = s / np.sqrt(Sxx)
    t_stat = beta_1 / beta_1_std_error
    df = n - 2
    p_value = 2 * (1 - t.cdf(abs(t_stat), df))

    H0 = "El coeficiente B1 no es significativamente diferente de 0 (el modelo no es significativo)"
    H1 = "El coeficiente B1 es significativamente diferente de 0 (el modelo es significativo)"

    conclusion = "Rechazamos H0" if p_value < alpha else "No rechazamos H0"

    return {
        "H0": H0,
        "H1": H1,
        "Estadistico t": t_stat,
        "p_valor": p_value,
        "alpha": alpha,
        "conclusion": conclusion,
        "Ecuación del modelo": f"ŷ = {beta_0:.4f} + {beta_1:.4f}x"
    }

def calculate_r_squared(x, y):
    """
    Calcula el coeficiente de determinación R^2 para el modelo de regresión lineal.

    Args:
        x (np.array): Valores de la variable independiente.
        y (np.array): Valores de la variable dependiente.

    Return:
        dict: R^2 y comentarios sobre el desempeño del modelo.
    """
    model = calculate_linear_model(x, y)
    beta_1 = model['B1']
    beta_0 = model['B0']
    y_pred = beta_0 + beta_1 * x
    y_mean = np.mean(y)
    sst = np.sum((y - y_mean) ** 2)
    ssr = np.sum((y_pred - y_mean) ** 2)
    sse = np.sum((y - y_pred) ** 2)
    r_squared = ssr / sst
    if r_squared > 0.8:
        comment = "El modelo tiene un excelente ajuste, ya que R^2 es mayor al 80%."
    elif 0.5 < r_squared <= 0.8:
        comment = "El modelo tiene un ajuste moderado, ya que R^2 está entre 50% y 80%."
    else:
        comment = "El modelo tiene un ajuste bajo, ya que R^2 es menor al 50%."

    return {
        "R^2": r_squared,
        "SST": sst,
        "SSR": ssr,
        "SSE": sse,
        "Conclusión": comment
    }

def compute_regression_intervals(x, y, alpha=0.05):
    """
    Calcula los intervalos de confianza para los coeficientes
    beta_0 y beta_1 en una regresión lineal.

    Args:
        x (array-like): Variable independiente.
        y (array-like): Variable dependiente.
        alpha (float): Nivel de significancia (por defecto 0.05).

    Returns:
        tuple: Intervalos de confianza para beta_1 y beta_0, y una conclusión sobre la regresión al origen.
    """
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    beta_1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    beta_0 = y_mean - beta_1 * x_mean
    y_hat = beta_0 + beta_1 * x
    SSE = np.sum((y - y_hat) ** 2)
    SE_beta_1 = np.sqrt(SSE / ((n - 2) * np.sum((x - x_mean) ** 2)))
    SE_beta_0 = np.sqrt(SE_beta_1**2 * np.sum(x**2) / n + SSE / (n * (n - 2)))
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 2)
    IC_beta_1 = (beta_1 - t_crit * SE_beta_1, beta_1 + t_crit * SE_beta_1)
    IC_beta_0 = (beta_0 - t_crit * SE_beta_0, beta_0 + t_crit * SE_beta_0)

    conclusion = "Regresión al origen" if 0 in IC_beta_0 else "No hay evidencia de regresión al origen"
    return IC_beta_1, IC_beta_0, conclusion


def analyze_model_to_origin_v2(x, y, alpha=0.05):
    """
    Analiza el modelo de regresión al origen
    Args:
    x: array (variable independiente)
    y: array (variable dependiente)
    alpha: nivel de significancia (default 0.05)
    Return:
    - Ecuación del modelo
    - Prueba de significancia del modelo (t, p-valor, conclusión)
    - Coeficiente de determinación (R^2) y comentario
    """
    n = len(x)
    beta_1 = np.sum(x * y) / np.sum(x ** 2)
    equation = f"ŷ = {beta_1:.4f}x"

    y_hat = beta_1 * x
    SSE = np.sum((y - y_hat) ** 2)

    SE_beta_1 = np.sqrt(SSE / (n - 1) / np.sum(x ** 2))

    t_stat = beta_1 / SE_beta_1
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - 1))
    conclusion = "Rechazamos H0: El modelo es significativo" if p_value < alpha else "No rechazamos H0: El modelo no es significativo"

    SST = np.sum((y - np.mean(y)) ** 2)
    R2 = 1 - SSE / SST
    R2_comment = "El modelo tiene un buen ajuste" if R2 >= 0.8 else "El modelo tiene un ajuste bajo"

    return {
        "Ecuación del modelo": equation,
        "Prueba de significancia": {
            "t-stat": t_stat,
            "p-valor": p_value,
            "Conclusión": conclusion,
        },
        "Ajuste del modelo": {
            "R^2": R2,
            "Comentario": R2_comment,
        },
    }


def regression_test_origin(x, y, alpha=0.05):
    """
    Realiza la prueba de hipótesis para determinar
    si el modelo de regresión lineal pasa por el origen.
    Args:
    x : np.array
        Variables independientes (predictoras).
    y : np.array
        Variables dependientes (respuesta).
    alpha : float, opcional
        Nivel de significancia (por defecto 0.05).
    Return:
    dict : Resultados de la prueba de hipótesis.
    """
    n = len(x)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    beta_1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    beta_0 = y_mean - beta_1 * x_mean
    y_hat = beta_0 + beta_1 * x
    SSE = np.sum((y - y_hat) ** 2)
    SE_beta_0 = np.sqrt(SSE / n)
    t_beta_0 = beta_0 / SE_beta_0
    p_valor = 2 * (1 - stats.t.cdf(np.abs(t_beta_0), df=n - 2))
    decision = "Rechazamos H0" if p_valor <= alpha else "No rechazamos H0"
    return {
        "Ecuación del modelo": f"ŷ = {beta_1:.4f}x + {beta_0:.4f}",
        "t_beta_0": t_beta_0,
        "p_valor": p_valor,
        "decisión": decision
    }

def plot_and_save_regression(x, y, beta_0, beta_1, filename='Evidencia6_grafica_dispersion.png'):
    """
    Grafica la dispersión de los datos e incluye el ajuste del modelo, y guarda la gráfica.

    Args:
    - x: array de las variables independientes.
    - y: array de las variables dependientes.
    - beta_0: Intercepto del modelo.
    - beta_1: Pendiente del modelo.
    - filename: Nombre del archivo donde se guardará la gráfica.

    Returns:
    - Retorna un DataFrame con la información del modelo.
    """
    y_hat = beta_0 + beta_1 * x
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, color='blue', label='Datos observados', s=80, alpha=0.7)
    ax.plot(x, y_hat, color='red', label='Modelo ajustado', linewidth=2)
    ax.set_title("Dispersión de los Datos y Ajuste del Modelo")
    ax.set_xlabel("Horas")
    ax.set_ylabel("Cloro residual")
    ax.legend()
    ax.grid(alpha=0.5)
    save_plot(fig, filename=filename)
    return pd.DataFrame({
        'Intercepto (Beta 0)': [beta_0],
        'Pendiente (Beta 1)': [beta_1],
        'Nombre de archivo': [filename]
    })

beta_0 = 1.9000
beta_1 = -0.0857

def exponential_model_analysis(x, y, alpha=0.05):
    """
    Realiza el análisis del modelo exponencial linealizable.
    Args:
        x (array-like): Valores independientes.
        y (array-like): Valores dependientes.
        alpha (float): Nivel de significancia para las pruebas.
    Returns:
        dict: Resultados del análisis del modelo.
    """
    ln_y = np.log(y)
    x_mean = np.mean(x)
    ln_y_mean = np.mean(ln_y)
    beta_1 = np.sum((x - x_mean) * (ln_y - ln_y_mean)) / np.sum((x - x_mean) ** 2)
    beta_0 = ln_y_mean - beta_1 * x_mean
    A = np.exp(beta_0)
    B = beta_1
    y_hat = A * np.exp(B * x)
    SSE = np.sum((y - y_hat) ** 2)
    SST = np.sum((y - np.mean(y)) ** 2)
    n = len(x)
    SE_beta_1 = np.sqrt(SSE / ((n - 2) * np.sum((x - x_mean) ** 2)))
    SE_beta_0 = np.sqrt(SE_beta_1**2 * np.sum(x**2) / n + SSE / (n * (n - 2)))
    t_beta_1 = beta_1 / SE_beta_1
    p_valor = 2 * (1 - t.cdf(np.abs(t_beta_1), df=n - 2))
    decision = "Rechazamos H0" if p_valor < alpha else "No rechazamos H0"
    R_squared = 1 - SSE / SST
    ajuste_comentario = "El modelo tiene un buen ajuste" if R_squared > 0.8 else "El modelo tiene un ajuste bajo"
    t_crit = t.ppf(1 - alpha / 2, df=n - 2)
    IC_beta_1 = (beta_1 - t_crit * SE_beta_1, beta_1 + t_crit * SE_beta_1)
    IC_beta_0 = (beta_0 - t_crit * SE_beta_0, beta_0 + t_crit * SE_beta_0)
    regresion_origen = "Sí" if 0 in IC_beta_0 else "No"
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, color='blue', label='Datos observados', s=80, alpha=0.7)
    ax.plot(x, y_hat, color='red', label='Modelo ajustado', linewidth=2)
    ax.set_title("Dispersión de los Datos y Ajuste del Modelo Exponencial")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    save_plot(fig, filename='modelo_exponencial.png')
    results = {
        "Modelo Exponencial": f"ŷ = {A:.4f} * e^({B:.4f}x)",
        "Prueba de significancia": {
            "t_beta_1": t_beta_1,
            "p_valor": p_valor,
            "Decisión": decision
        },
        "Ajuste del modelo": {
            "R^2": R_squared,
            "Comentario": ajuste_comentario
        },
        "Intervalos de confianza": {
            "IC_beta_1": IC_beta_1,
            "IC_beta_0": IC_beta_0
        },
        "Regresión al origen": regresion_origen,
        "Gráfica guardada en": "plots/exponential_model_plot.png"
    }
    
    return results

def prueba_hipotesis_origen_exponencial(x, y, alpha=0.05):
    """
    Realiza la prueba de hipótesis para determinar si el modelo exponencial pasa por el origen.

    Args:
        x (array): Valores independientes.
        y (array): Valores dependientes.
        alpha (float): Nivel de significancia para la prueba. Default es 0.05.

    Returns:
        dict: Resultados de la prueba de hipótesis.
    """
    y_log = np.log(y)
    x_mean = np.mean(x)
    y_log_mean = np.mean(y_log)
    beta_1 = np.sum((x - x_mean) * (y_log - y_log_mean)) / np.sum((x - x_mean)**2)
    ln_beta_0 = y_log_mean - beta_1 * x_mean
    n = len(x)
    y_log_hat = ln_beta_0 + beta_1 * x
    SSE = np.sum((y_log - y_log_hat)**2)
    SE_ln_beta_0 = np.sqrt(SSE / (n - 2) * (1 / n + x_mean**2 / np.sum((x - x_mean)**2)))
    t_ln_beta_0 = ln_beta_0 / SE_ln_beta_0
    p_valor = 2 * (1 - stats.t.cdf(abs(t_ln_beta_0), df=n - 2))
    decision = "Rechazamos H0" if p_valor < alpha else "No rechazamos H0"
    resultados = {
        "ln(beta_0)": ln_beta_0,
        "t_ln_beta_0": t_ln_beta_0,
        "p_valor": p_valor,
        "decisión": decision
    }

    return resultados


x = np.array([2, 4, 6, 8, 10, 12])
y = np.array([1.8, 1.5, 1.4, 1.1, 1.1, 0.9])
if __name__ =='__main__':
    #result = calculate_linear_model(x, y)
    #print(result["B0"])
    #print(result["B1"])
    #print(result["Ecuación del modelo"])
    # test_results = significance_test(x, y)
    # print(test_results["H0"])
    # print(test_results["H1"])
    # print(test_results["Estadistico t"])
    # print(test_results["p_valor"])
    # print(test_results["alpha"])
    # print(test_results["conclusion"])
    # print(test_results["Ecuación del modelo"])
    #r_squared_results = calculate_r_squared(x, y)
    #print(r_squared_results['R^2'])
    #print(r_squared_results['SST'])
    #print(r_squared_results['SSR'])
    #print(r_squared_results['SSE'])
    #print(r_squared_results['Conclusión'])
    #intervals_beta_1, intervals_beta_0, regression_conclusion = compute_regression_intervals(x, y)
    #print(intervals_beta_1, intervals_beta_0, regression_conclusion)
    #results_v2 = analyze_model_to_origin_v2(x, y)
    #print(results_v2)
    #resultados = regression_test_origin(x, y, alpha=0.05)
    #print(resultados)
    #info_df = plot_and_save_regression(x, y, beta_0, beta_1)
    #print(info_df)
    #resultados = exponential_model_analysis(x, y)
    #print(resultados)
    #resultados = exponential_model_analysis(x, y)
    #print(resultados)
    resultados = prueba_hipotesis_origen_exponencial(x, y)
    for clave, valor in resultados.items():
        print(f"{clave}: {valor}")