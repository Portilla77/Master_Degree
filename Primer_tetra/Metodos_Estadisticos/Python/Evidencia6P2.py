import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import scipy.stats as stats
from itertools import combinations
import matplotlib.pyplot as plt
from Primer_tetra.Metodos_Estadisticos.Python.Reporte2 import iterative_vif_reduction
from Primer_tetra.Metodos_Estadisticos.Python.Reporte2 import calculate_and_plot_full_correlation
from Primer_tetra.helpers.helpers import save_plot


def calculate_vif(data, response_variable):
    """
    Calculate Variance Inflation Factor (VIF) for a given dataset and response variable.
    
    Args:
    - data (pd.DataFrame): A dataframe containing predictors and the response variable.
    - response_variable (str): The name of the response variable in the dataset.

    Returns:
    - pd.DataFrame: A dataframe containing the VIF values for each predictor.
    """
    X = data.drop(columns=[response_variable])
    X = sm.add_constant(X)
    vif_data = pd.DataFrame({
        "Variable": X.columns,
        "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    })
    return vif_data


def regression_analysis(data):
    """
    Realiza análisis de regresión múltiple.
    Args:
        data (pd.DataFrame): DataFrame con las columnas x1 (IQ), x2 (horas de estudio) y y (puntuación).
    Return:
        dict: Resultados de los incisos a, b y c.
    """
    X = sm.add_constant(data[['x1', 'x2']])
    y = data['y']
    model = sm.OLS(y, X).fit()
    beta_0 = model.params['const']
    beta_1 = model.params['x1']
    beta_2 = model.params['x2']
    equation = f"ŷ = {beta_0:.4f} + {beta_1:.4f}x1 + {beta_2:.4f}x2"
    variable_comments = {
        'x1 (IQ)': "Positiva" if beta_1 > 0 else "Negativa",
        'x2 (Horas de estudio)': "Positiva" if beta_2 > 0 else "Negativa"
    }
    hypotheses = {
        "H0": "Los coeficientes del modelo no son significativos.",
        "H1": "Al menos uno de los coeficientes del modelo es significativo."
    }
    p_values = model.pvalues
    alpha = 0.05
    significance = {
        'const': "Rechazamos H0" if p_values['const'] < alpha else "No rechazamos H0",
        'x1': "Rechazamos H0" if p_values['x1'] < alpha else "No rechazamos H0",
        'x2': "Rechazamos H0" if p_values['x2'] < alpha else "No rechazamos H0",
    }
    r_squared = model.rsquared
    r2_comment = "El modelo tiene un buen ajuste" if r_squared > 0.8 else "El modelo tiene un ajuste bajo"
    results = {
        'a) Ecuación del modelo': equation,
        'Relación entre las variables': variable_comments,
        'b) Prueba de significancia': {
            'Hipótesis': hypotheses,
            'p-valores': p_values.to_dict(),
            'Significancia': significance
        },
        'c) Ajuste del modelo': {
            'R2': r_squared,
            'Comentario': r2_comment
        }
    }

    return results

def adjusted_r2_from_model(model, n, k):
    """
    Calcula el R² ajustado utilizando un modelo de regresión de statsmodels.

    Args:
    - model: Objeto ajustado del modelo de statsmodels.
    - n (int): Número total de observaciones.
    - k (int): Número de variables independientes en el modelo.

    Returns:
    - float: El R² ajustado.
    """
    r_squared = model.rsquared
    return 1 - (1 - r_squared) * ((n - 1) / (n - k - 1))

def select_best_model(data, response_variable, alpha=0.05):
    """
    Selecciona el mejor modelo basado en R² ajustado y significancia estadística.
    Args:
    - data (pd.DataFrame): DataFrame con las variables predictoras y la variable de respuesta.
    - response_variable (str): Nombre de la variable de respuesta en el DataFrame.
    - alpha (float): Nivel de significancia para evaluar los p-valores.
    Return:
    - dict: Información del mejor modelo seleccionado.
    """
    predictors = [col for col in data.columns if col != response_variable]
    best_model = None
    best_adjusted_r2 = -float('inf')
    all_models = []
    for k in range(1, len(predictors) + 1):
        for combo in combinations(predictors, k):
            X = sm.add_constant(data[list(combo)])
            y = data[response_variable]
            model = sm.OLS(y, X).fit()
            significant = all(p < alpha for p in model.pvalues[1:])
            adjusted_r2 = model.rsquared_adj
            model_info = {
                'Predictores': combo,
                'Ecuación': "ŷ = " + " + ".join([f"{model.params[0]:.4f}"] + [f"{coef:.4f}{col}" for col, coef in zip(combo, model.params[1:])]),
                'R2': model.rsquared,
                'R2 ajustado': adjusted_r2,
                'P-valores': model.pvalues.to_dict(),
                'Significancia': significant
            }
            all_models.append(model_info)
            if significant and adjusted_r2 > best_adjusted_r2:
                best_model = model_info
                best_adjusted_r2 = adjusted_r2
    return best_model, all_models


def confidence_intervals_and_origin(model, alpha=0.05):
    """
    Calcula los intervalos de confianza para los coeficientes del modelo
    y evalúa si existe evidencia de regresión al origen.

    Args:
        model: Modelo ajustado de statsmodels.
        alpha (float): Nivel de significancia (por defecto 0.05 para 95% de confianza).

    Returns:
        dict: Intervalos de confianza y decisión sobre regresión al origen.
    """
    params = model.params
    conf_int = model.conf_int(alpha=alpha)
    t_value = stats.t.ppf(1 - alpha / 2, df=model.df_resid)
    p_value_beta0 = model.pvalues['const']
    results = {
        'Intervalos de confianza': {
            'Intercepto (β0)': (conf_int.loc['const', 0], conf_int.loc['const', 1]),
            'Coeficiente de x1 (β1)': (conf_int.loc['x1', 0], conf_int.loc['x1', 1])
        },
        'Evidencia de regresión al origen': {
            'Hipótesis': {
                'H0': 'β0 = 0 (La regresión pasa por el origen)',
                'H1': 'β0 ≠ 0 (La regresión no pasa por el origen)'
            },
            'p-valor': p_value_beta0,
            'Decisión': 'Rechazamos H0' if p_value_beta0 < alpha else 'No rechazamos H0'
        }
    }

    return results

def analyze_model_at_origin(data, response_variable, predictor_variable, alpha=0.01):
    """
    Analiza el modelo ajustado al origen (sin intercepto)

    Args:
    - data (pd.DataFrame): Dataset con las variables independientes y dependientes.
    - response_variable (str): Nombre de la variable dependiente.
    - predictor_variable (str): Nombre de la variable independiente.
    - alpha (float): Nivel de significancia para las pruebas de hipótesis.

    Return:
    - dict: Resultados del análisis con los incisos a, b y c.
    """
    y = data[response_variable]
    X = data[[predictor_variable]]
    model = sm.OLS(y, X).fit()
    beta_1 = model.params[predictor_variable]
    equation = f"ŷ = {beta_1:.4f}{predictor_variable}"
    hypotheses = {
        "H0": f"β1 = 0 (No hay relación entre {response_variable} y {predictor_variable})",
        "H1": f"β1 ≠ 0 (Hay relación entre {response_variable} y {predictor_variable})"
    }
    p_value = model.pvalues[predictor_variable]
    decision = "Rechazamos H0" if p_value < alpha else "No rechazamos H0"
    r_squared = model.rsquared
    r2_comment = "El modelo tiene un buen desempeño" if r_squared > 0.8 else "El modelo tiene un desempeño moderado o bajo"
    results = {
        "a) Ecuación del modelo": equation,
        "b) Prueba de significancia": {
            "Hipótesis": hypotheses,
            "p-valor": p_value,
            "Decisión": decision
        },
        "c) Ajuste del modelo": {
            "R2": r_squared,
            "Comentario": r2_comment
        }
    }
    return results

def analyze_residuals(model, X, y, save_filename='Residuos.png'):
    """
    Analiza los residuos del modelo y verifica los supuestos mediante gráficos.
    Args:
    - model: Objeto de modelo ajustado (statsmodels).
    - X: Variables independientes usadas en el modelo.
    - y: Variable dependiente usada en el modelo.
    - save_filename: Nombre del archivo donde se guardará el gráfico.
    Return:
    - dict: Indicadores clave de los supuestos analizados.
    """
    y_pred = model.predict(X)
    residuals = y - y_pred
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    axes[0].scatter(y_pred, residuals, alpha=0.7)
    axes[0].axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    axes[0].set_title('Residuos vs. Predicciones')
    axes[0].set_xlabel('Predicciones')
    axes[0].set_ylabel('Residuos')
    sm.qqplot(residuals, line='45', fit=True, ax=axes[1])
    axes[1].set_title('QQ Plot de Residuos')
    save_plot(fig, filename=save_filename)
    residual_analysis = {
        "Varianza constante": "Cumple" if not np.any(np.abs(residuals) > 15) else "No cumple",
        "Normalidad de residuos (Visual)": "Cumple parcialmente" if np.all(np.abs(residuals) < 15) else "No cumple"
    }

    return residual_analysis
# Datos
data = pd.DataFrame({
    'x1': [112, 126, 100, 114, 112, 121, 110, 103, 111, 124],
    'x2': [5, 13, 3, 7, 11, 9, 8, 4, 6, 2],
    'y': [79, 97, 51, 65, 82, 93, 81, 38, 60, 86]
})
data_independent = data.drop(columns='y')

if __name__ =='__main__':
    results = regression_analysis(data)
    #for key, value in results.items():
    #    print(f"{key}:\n{value}\n")
    #vif_results = calculate_vif(data, response_variable="y")
    #print(vif_results)
    #calculate_and_plot_full_correlation(data, filename="Matriz_correlación_R6P2")
    # X = sm.add_constant(data[['x1', 'x2']])
    # y = data['y']
    # model = sm.OLS(y, X).fit()
    # results = regression_analysis(data)
    # n = len(data)
    # k = 2
    # adjusted_r2_result = adjusted_r2_from_model(model, n, k)
    # print(f"R² ajustado: {adjusted_r2_result}")
    ######################################################
    ##      Selección del mejor modelo de regresión     ##
    ######################################################
    # best_model, all_models = select_best_model(data, response_variable='y')
    # print("\nTodos los modelos probados:")
    # for model in all_models:
    #     print(model)
    # print("--------------------------------------")
    # print("Mejor modelo seleccionado:")
    # print(best_model)

    ######################################################
    ##             Intervalos de confianza              ##
    ######################################################
    X = sm.add_constant(data[['x1']])
    y = data['y']
    model = sm.OLS(y, X).fit()
    #results = confidence_intervals_and_origin(model)
    #print(results)
    # origin_analysis_results = analyze_model_at_origin(data, response_variable='y', predictor_variable='x1')
    # print(origin_analysis_results)
    analyze_residuals(model, X, y, save_filename='ResidualesE6P2.png')
