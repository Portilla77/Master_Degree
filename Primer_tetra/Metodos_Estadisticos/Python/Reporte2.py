import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
from Primer_tetra.helpers.helpers import save_plot
from sklearn.metrics import mean_squared_error
import numpy as np

def load_data(file_path, columns, drop_columns=None):
    """
    Carga el dataset, asigna nombres de columnas y elimina columnas opcionales.
    Args:
        file_path (str): Ruta al archivo CSV.
        columns (list): Lista de nombres de columnas.
        drop_columns (list or str): Columnas a eliminar. Si es "None", no se eliminan columnas.
    Returns:
        pd.DataFrame: Dataset procesado.
    """
    gold_data = pd.read_csv(file_path)
    gold_data.columns = columns
    if drop_columns is not None:
        gold_data.drop(columns=drop_columns, inplace=True)
    gold_data.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
    gold_data.dropna(inplace=True)
    return gold_data

# Función para matriz de dispersión todas contra todas
def plot_pairwise_all(data, filename="Matriz_dispersión_Gold_Price_Prediction"):
    sns.pairplot(data, diag_kind='kde', plot_kws={'alpha': 0.6})
    plt.suptitle("Matriz de dispersión: Gold Price Prediction", y=1.02)
    fig = plt.gcf()
    save_plot(fig, filename)

def plot_vs_response(data, response_var="precio_mañana", filename="Matriz dispersión vs precio mañana"):
    independent_vars = data.columns.tolist()
    independent_vars.remove(response_var)
    fig, axes = plt.subplots(nrows=len(independent_vars), ncols=1, figsize=(10, len(independent_vars) * 3))
    for idx, var in enumerate(independent_vars):
        sns.scatterplot(data=data, x=var, y=response_var, ax=axes[idx], alpha=0.6)
        axes[idx].set_title(f'Dispersión: {var} vs {response_var}')
        axes[idx].set_xlabel(var)
        axes[idx].set_ylabel(response_var)
    plt.tight_layout()
    save_plot(fig, filename)

def calculate_and_plot_full_correlation(data, filename="Matriz_correlación"):
    """
    Calcula y grafica la matriz de correlación de todas las variables del dataset.
    Args:
        data (pd.DataFrame): Dataset con las variables.
        filename (str): Nombre del archivo para guardar la gráfica.
    Returns:
        pd.DataFrame: Matriz de correlación calculada.
    """
    correlation_matrix = data.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="Purples", cbar=True)
    plt.title("Matriz de Correlación")
    plt.tight_layout()
    fig = plt.gcf()
    save_plot(fig, filename)
    return correlation_matrix

def calculate_vif(data):
    """
    Calcula el VIF para un DataFrame de variables independientes.
    Args:
        data (pd.DataFrame): Variables independientes.
    Returns:
        pd.DataFrame: DataFrame con los valores de VIF.
    """
    vif_data = pd.DataFrame()
    vif_data["Variable"] = data.columns
    vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]
    return vif_data


def iterative_vif_reduction(data, threshold=10.0):
    """
    Reduce iterativamente las variables con multicolinealidad significativa usando el criterio VIF.
    Args:
        data (pd.DataFrame): Dataset con variables independientes.
        threshold (float): Valor límite para el VIF (por defecto, 10).
    Returns:
        pd.DataFrame: Dataset con las variables seleccionadas tras reducir el VIF.
        pd.DataFrame: Tabla de VIF final.
    """
    print("Inicio del proceso de reducción de VIF...")
    iteration = 1
    while True:
        vif_data = pd.DataFrame()
        vif_data["Variable"] = data.columns
        vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]
        print(f"\nIteración {iteration} - VIF actual:")
        print(vif_data.sort_values(by="VIF", ascending=False))
        max_vif = vif_data["VIF"].max()
        if max_vif <= threshold:
            print("\nTodas las variables tienen un VIF menor o igual al umbral definido.")
            break
        var_to_remove = vif_data.loc[vif_data["VIF"] == max_vif, "Variable"].values[0]
        print(f"Iteración {iteration}: Eliminando '{var_to_remove}' con VIF = {max_vif:.2f}")
        data = data.drop(columns=[var_to_remove])
        iteration += 1
    final_vif = pd.DataFrame()
    final_vif["Variable"] = data.columns
    final_vif["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]
    print("\nVIF final después de la reducción:")
    print(final_vif.sort_values(by="VIF", ascending=False))
    return data, final_vif

def regression_significance_test(data, dependent_var="precio_mañana"):
    """
    Realiza la prueba de significancia ajustando un modelo de regresión múltiple.
    Args:
        data (pd.DataFrame): Dataset con las variables independientes y dependiente.
        dependent_var (str): Nombre de la variable dependiente.
    Returns:
        sm.OLS: Objeto del modelo ajustado.
    """
    y = data[dependent_var]
    X = data.drop(columns=[dependent_var])
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())
    return model

def test_regression_origin(X, y, alpha=0.05):
    """
    Prueba si la regresión pasa por el origen (𝛽0 = 0).
    Args:
        X (pd.DataFrame): Variables independientes.
        y (pd.Series): Variable dependiente.
        alpha (float): Nivel de significancia para la prueba (por defecto 0.05).
    Returns:
        dict: Resultados de la prueba del origen con el p-valor y conclusión.
    """
    X_with_intercept = sm.add_constant(X)
    model = sm.OLS(y, X_with_intercept).fit()
    intercept = model.params['const']
    intercept_pvalue = model.pvalues['const']
    if intercept_pvalue <= alpha:
        conclusion = (
            f"Rechazamos H0: el intercepto (β0) es significativamente diferente de 0 "
            f"con un nivel de significancia de {alpha:.2f}."
        )
    else:
        conclusion = (
            f"No podemos rechazar H0: no hay evidencia suficiente para concluir que el intercepto (β0) "
            f"es diferente de 0 con un nivel de significancia de {alpha:.2f}."
        )
    return {
        "Intercepto (β0)": intercept,
        "p-valor del intercepto": intercept_pvalue,
        "Conclusión": conclusion,
        "Resumen del modelo": model.summary()
    }

def analyze_coefficients(model):
    """
    Calcula los intervalos de confianza y analiza todos los coeficientes del modelo.
    Args:
        model: Modelo ajustado de statsmodels (OLS).
    Returns:
        pd.DataFrame: DataFrame con los coeficientes, intervalos de confianza, y conclusiones.
    """
    coefficients = model.params
    conf_intervals = model.conf_int(alpha=0.05)
    results = pd.DataFrame({
        "Coeficiente (β)": coefficients,
        "Inferior (95%)": conf_intervals[0],
        "Superior (95%)": conf_intervals[1],
        "p-valor": model.pvalues
    })
    results["Conclusión"] = results["p-valor"].apply(
        lambda p: "Significativo (rechazamos H0)" if p <= 0.05 else "No significativo (no rechazamos H0)"
    )
    return results

def calculate_mse_rmse(model, y):
    """
    Calcula el Error Cuadrático Medio (MSE) y su raíz (RMSE) del modelo ajustado.
    Args:
        model: Modelo ajustado de statsmodels (OLS).
        y: Valores reales de la variable dependiente.
    Returns:
        dict: Diccionario con el MSE y RMSE.
    """
    predictions = model.fittedvalues
    mse = mean_squared_error(y, predictions)
    rmse = np.sqrt(mse)
    return {"MSE": mse, "RMSE": rmse}

file_path = "Primer_tetra/Metodos_Estadisticos/Recursos/Dataset/Gold Price Prediction.csv"
columnas = [
    "fecha", "precio_2_dias_atras", "precio_1_dia_atras", "precio_hoy",
    "precio_mañana", "cambio_precio_mañana", "cambio_precio_10_dias",
    "desviacion_std_10", "promedio_movil_20_dias", "promedio_movil_50_dias",
    "promedio_movil_200_dias","tasa_inflacion_mensual", "tasa_EFFR", "volumen",
    "rendimiento_par_tesoros_mes", "rendimiento_par_tesoros_2_años",
    "rendimiento_curva_tesoros_10_años", "dxy", "sp_abre", "vix", "crudo"
]
va_discard = ["fecha","desviacion_std_10", "promedio_movil_20_dias", "promedio_movil_50_dias",
    "promedio_movil_200_dias"]
fecha = ["fecha"]
va_VIF = ["fecha", "precio_mañana"]
va_after_VIF = ["desviacion_std_10","vix","tasa_EFFR","cambio_precio_10_dias","cambio_precio_mañana"
                 ,"precio_mañana"]
if __name__=="__main__":
    gold_data = load_data(file_path, columns= columnas)
    gold_data_after = gold_data[va_after_VIF]
    #print(gold_data_after.columns)
    #print(gold_data.columns)
    plot_pairwise_all(gold_data)
    plot_vs_response(gold_data)
    calculate_and_plot_full_correlation(gold_data_after)
    print(calculate_vif(gold_data))
    final_data, final_vif = iterative_vif_reduction(gold_data)
    regression_model = regression_significance_test(gold_data_after)
    y = gold_data_after["precio_mañana"]
    X = gold_data_after.drop(columns=["precio_mañana"])
    results = test_regression_origin(X, y, alpha=0.05)
    X = sm.add_constant(X)
    results = sm.OLS(y, X).fit()
    intercept_analysis = analyze_coefficients(results)
    #print(intercept_analysis)
    mse_rmse = calculate_mse_rmse(results, y)
    #print(f"Error Cuadrático Medio (MSE): {mse_rmse['MSE']}")
    #print(f"Raíz del Error Cuadrático Medio (RMSE): {mse_rmse['RMSE']}")