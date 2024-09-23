import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Primer_tetra.helpers.helpers import save_plot

data_store_branch_A = np.array([
[30.5 ,28.4, 28 ,28.5 ,31.1 ,31.6 ,28.4 ,27.9],
[32.2 ,30.8 ,29.7 ,31.4, 31.9 ,29.1 ,9.4 ,29.6],
[31.2 ,29.3 ,26.9 ,29.5 ,27.7 ,27.7 ,26.8 ,32.7],
[27.6 ,32.3 ,27 ,28.8 ,31.2 ,26.8 ,26.2 ,32.5],
[30.8 ,30.6 ,27 ,31.4, 26 ,32 ,26.6 ,28.5],
[29   ,29.9 ,32.4 ,30.4 ,28.8 ,28.9 ,30.9 ,28.9],
[29.3 ,27.4 ,29.9 ,31.4 ,29.6 ,27.6 ,31.1 ,29.1] ,
[28.7 ,27.4 ,30 ,26.7 ,26.8, 28.8 ,28.2 ,28.4] ,
[32.3 ,26   ,31.5 ,26.4 ,26.5 ,32.6 ,28.2 ,32.2] ,
[28.1 ,32.4 ,31.1 ,31.6 ,28.3 ,28.3 ,28.9 ,32.7]
  ])

min_value = np.min(data_store_branch_A)
max_value = np.max(data_store_branch_A)
range_value = max_value - min_value
mean_value = np.mean(data_store_branch_A)
variance_value = np.var(data_store_branch_A, ddof=1)
std_dev = np.std(data_store_branch_A, ddof=1)
coef_variation = (std_dev / mean_value) * 100

result_values = pd.DataFrame({
    "Rango": [range_value],
    "Media": [mean_value],
    "Mínimo": [min_value],
    "Máximo": [max_value],
    "Varianza": [variance_value],
    "Coeficiente de variación": [coef_variation]
})


plt.figure()
plt.hist(data_store_branch_A.flatten(), bins=10, edgecolor='black')
plt.title('Histograma de ganancias de la sucursal A')
plt.xlabel('Ganancias')
plt.ylabel('Frecuencia')
fig = plt.gcf()
#save_plot(fig, "Histograma Ev1 problema2")
