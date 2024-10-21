import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import os


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

print(data_gold_new.columns)


def plot_histogram_with_curve(data, variable_name, distribucion_sospechada, ruta_carpeta, bins=10):

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    plt.figure(figsize=(8, 6))

    count, bins, ignored = plt.hist(data, bins=bins, density=True, alpha=0.6, color='lightblue')

    if distribucion_sospechada == "normal":
        mu, std = np.mean(data), np.std(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = f'Histograma y Curva Normal Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "gamma":
        shape, loc, scale = stats.gamma.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.gamma.pdf(x, shape, loc, scale)
        plt.plot(x, p, 'r', linewidth=2)
        title = f'Histograma y Curva Gamma Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "exponencial":
        loc, scale = stats.expon.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.expon.pdf(x, loc, scale)
        plt.plot(x, p, 'g', linewidth=2)
        title = f'Histograma y Curva Exponencial Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "lognormal":
        shape, loc, scale = stats.lognorm.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.lognorm.pdf(x, shape, loc, scale)
        plt.plot(x, p, 'b', linewidth=2)
        title = f'Histograma y Curva Log-Normal Ajustada para {variable_name}'
        
    elif distribucion_sospechada == "uniforme":
        loc, scale = stats.uniform.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.uniform.pdf(x, loc, scale)
        plt.plot(x, p, 'm', linewidth=2)
        title = f'Histograma y Curva Uniforme Ajustada para {variable_name}'

    plt.title(title)
    plt.xlabel(variable_name)
    plt.ylabel('Frecuencia')

    archivo = os.path.join(ruta_carpeta, f"{variable_name}_histograma_{distribucion_sospechada}.png")
    plt.savefig(archivo)
    plt.show()

data_gold = pd.read_csv("Primer_tetra/Metodos_Estadisticos/Recursos/Dataset/Gold Price Prediction.csv")


ruta_curvas_ajustadas = "Primer_tetra/Metodos_Estadisticos/Curvas_ajustadas"

plot_histogram_with_curve(data_gold_new["cambio_precio_10_dias"], "cambio_precio_10_dias", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["cambio_precio_mañana"], "cambio_precio_mañana", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["crudo"], "crudo", "lognormal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["dxy"], "dxy", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["precio_1_dia_atras"], "precio_1_dia_atras", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["precio_2_dias_atras"], "precio_2_dias_atras", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["precio_hoy"], "precio_hoy", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["precio_mañana"], "precio_mañana", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["rendimiento_curva_tesoros_10_años"], "rendimiento_curva_tesoros_10_años", "gamma", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["rendimiento_par_tesoros_2_años"], "rendimiento_par_tesoros_2_años", "gamma", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["rendimiento_par_tesoros_mes"], "rendimiento_par_tesoros_mes", "gamma", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["sp_abre"], "sp_abre", "normal", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["tasa_EFFR"], "tasa_EFFR", "exponencial", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["tasa_inflacion_mensual"], "tasa_inflacion_mensual", "gamma", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["vix"], "vix", "gamma", ruta_curvas_ajustadas)
plot_histogram_with_curve(data_gold_new["volumen"], "volumen", "normal", ruta_curvas_ajustadas)

