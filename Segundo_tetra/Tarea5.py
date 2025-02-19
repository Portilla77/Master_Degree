#############################################
#                Problema 1                 #
#############################################

import pandas as pd
import numpy as np
from scipy import stats

def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="PROB 1")
    df_cleaned = df.iloc[1:, [1, 2, 3, 4, 6, 7, 8, 9]].copy()
    df_cleaned.columns = ["x1_s1", "x2_s1", "x3_s1", "x4_s1", "x1_s2", "x2_s2", "x3_s2", "x4_s2"]
    df_cleaned = df_cleaned.apply(pd.to_numeric)
    df_cleaned = df_cleaned.dropna()
    return df_cleaned

def hypothesis_testing(df, alpha=0.05):
    results = {}
    for col in ["x1", "x2", "x3", "x4"]:
        stat, p_value = stats.ttest_ind(df[f"{col}_s1"], df[f"{col}_s2"], equal_var=False)
        results[col] = {"t_statistic": stat, "p_value": p_value, "reject_null": p_value < alpha}
    return results

def confidence_interval(data1, data2, confidence=0.95):
    mean_diff = np.mean(data1) - np.mean(data2)
    se_diff = np.sqrt(np.var(data1, ddof=1)/len(data1) + np.var(data2, ddof=1)/len(data2))
    margin_error = stats.t.ppf((1 + confidence) / 2, df=len(data1) + len(data2) - 2) * se_diff
    return mean_diff - margin_error, mean_diff + margin_error

def compute_confidence_intervals(df):
    return {
        col: confidence_interval(df[f"{col}_s1"], df[f"{col}_s2"])
        for col in ["x1", "x2", "x3", "x4"]
    }

def print_assumptions():
    print("\nInciso C: Supuestos utilizados")
    print("1. Independencia de las muestras: Se supone que las observaciones de ambas sierras son independientes.")
    print("2. Distribución normal de los datos: Se asume que los datos en cada grupo siguen una distribución normal.")
    print("3. Varianza no necesariamente igual: Se utilizó la prueba t de Welch, que relaja el supuesto de homocedasticidad.")

file_path = "Segundo_tetra/datos_tarea5.xlsx"
df_prob1_cleaned = load_data(file_path)

results_a = hypothesis_testing(df_prob1_cleaned)
print("\nInciso A: Prueba de hipótesis")
for var, res in results_a.items():
    print(f"Variable {var}: t-statistic = {res['t_statistic']:.4f}, p-value = {res['p_value']:.4f}, Rechazar H0: {res['reject_null']}")

results_b = compute_confidence_intervals(df_prob1_cleaned)
print("\nInciso B: Intervalos de confianza (95%)")
for var, interval in results_b.items():
    print(f"Variable {var}: [{interval[0]:.4f}, {interval[1]:.4f}]")
print_assumptions()

#############################################
#                Problema 2                 #
#############################################
import numpy as np
from scipy import stats

S1 = [
    [599.92092, 645.84289, 45.50137, 39.21181, 227.3114, 188.15965, 43.29901],
    [645.84289, 696.7868, 48.46133, 41.69736, 244.34511, 202.89604, 46.87387],
    [45.50137, 48.46133, 4.8676, 4.04492, 17.47205, 14.16381, 2.87871],
    [39.21181, 41.69736, 4.04492, 4.11783, 14.73732, 11.3687, 2.59717],
    [227.3114, 244.34511, 17.47205, 14.73732, 97.0569, 70.60495, 16.07998],
    [188.15965, 202.89604, 14.16381, 11.3687, 70.60495, 63.48021, 13.68793],
    [43.29901, 46.87387, 2.87871, 2.59717, 16.07998, 13.68793, 3.31663]
]

S2 = [
    [575.27043, 618.91886, 45.70737, 38.20195, 225.8663, 175.25235, 41.49424],
    [618.91886, 667.58465, 48.858, 40.40396, 243.20193, 189.21062, 44.853],
    [45.70737, 48.858, 4.71999, 3.95054, 18.03344, 13.29122, 3.01997],
    [38.20195, 40.40396, 3.95054, 4.17723, 14.44286, 10.82841, 2.56922],
    [225.8663, 243.20193, 18.03344, 14.44286, 95.49805, 67.83094, 16.08471],
    [175.25235, 189.21062, 13.29122, 10.82841, 67.83094, 58.56777, 12.80255],
    [41.49424, 44.853, 3.01997, 2.56922, 16.08471, 12.80255, 3.14181]
]

XBarra_M1 = [124.030, 133.900, 8.961, 7.988, 51.300, 39.730, 8.917]
XBarra_M2 = [125.730, 137.920, 8.206, 8.367, 50.930, 40.726, 9.179]

X1_M1 = [x[0] for x in S1]
X2_M1 = [x[1] for x in S1]
X1_M2 = [x[0] for x in S2]
X2_M2 = [x[1] for x in S2]

def hypothesis_testing(data1, data2, alpha=0.05):
    stat, p_value = stats.ttest_ind(data1, data2, equal_var=False)
    return {"t_statistic": stat, "p_value": p_value, "reject_null": p_value < alpha}

def confidence_interval(data1, data2, confidence=0.95):
    mean_diff = np.mean(data1) - np.mean(data2)
    se_diff = np.sqrt(np.var(data1, ddof=1)/len(data1) + np.var(data2, ddof=1)/len(data2))
    margin_error = stats.t.ppf((1 + confidence) / 2, df=len(data1) + len(data2) - 2) * se_diff
    return mean_diff - margin_error, mean_diff + margin_error

def print_assumptions():
    print("\nInciso C: Supuestos utilizados")
    print("1. Independencia de las muestras: Se supone que las observaciones de ambas maquinarias son independientes.")
    print("2. Distribución normal de los datos: La prueba t de Student supone que los datos en cada grupo siguen una distribución normal.")
    print("3. Varianza no necesariamente igual: Se utilizó la prueba t de Welch, que relaja el supuesto de homocedasticidad.")

results_a = {
    "X1": hypothesis_testing(X1_M1, X1_M2),
    "X2": hypothesis_testing(X2_M1, X2_M2)
}

print("\nInciso A: Prueba de hipótesis")
for var, res in results_a.items():
    print(f"Variable {var}: t-statistic = {res['t_statistic']:.4f}, p-value = {res['p_value']:.4f}, Rechazar H0: {res['reject_null']}")

results_b = {
    "X1": confidence_interval(X1_M1, X1_M2),
    "X2": confidence_interval(X2_M1, X2_M2)
}

print("\nInciso B: Intervalos de confianza (95%)")
for var, interval in results_b.items():
    print(f"Variable {var}: [{interval[0]:.4f}, {interval[1]:.4f}]")

print_assumptions()

#############################################
#                Problema 3                 #
#############################################
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.correlation_tools import cov_nearest

file_path = "Segundo_tetra/datos_tarea5.xlsx"
xls = pd.ExcelFile(file_path)
df_prob3 = pd.read_excel(xls, sheet_name="PROB 3")

df_prob3_cleaned = pd.DataFrame({
    "X1_T1": df_prob3.iloc[1:, 0].astype(float),
    "X2_T1": df_prob3.iloc[1:, 1].astype(float),
    "X3_T1": df_prob3.iloc[1:, 2].astype(float),
    "X4_T1": df_prob3.iloc[1:, 3].astype(float),
    "X5_T1": df_prob3.iloc[1:, 4].astype(float),
    "X6_T1": df_prob3.iloc[1:, 5].astype(float),
    
    "X1_T2": df_prob3.iloc[1:, 7].astype(float),
    "X2_T2": df_prob3.iloc[1:, 8].astype(float),
    "X3_T2": df_prob3.iloc[1:, 9].astype(float),
    "X4_T2": df_prob3.iloc[1:, 10].astype(float),
    "X5_T2": df_prob3.iloc[1:, 11].astype(float),
    "X6_T2": df_prob3.iloc[1:, 12].astype(float),

    "X1_T3": df_prob3.iloc[1:, 14].astype(float),
    "X2_T3": df_prob3.iloc[1:, 15].astype(float),
    "X3_T3": df_prob3.iloc[1:, 16].astype(float),
    "X4_T3": df_prob3.iloc[1:, 17].astype(float),
    "X5_T3": df_prob3.iloc[1:, 18].astype(float),
    "X6_T3": df_prob3.iloc[1:, 19].astype(float),
}).dropna()

def anova_bartlett(df, variable):
    group1 = df[f"{variable}_T1"].values
    group2 = df[f"{variable}_T2"].values
    group3 = df[f"{variable}_T3"].values
    
    f_stat, p_value = stats.f_oneway(group1, group2, group3)

    bartlett_stat, bartlett_p = stats.bartlett(group1, group2, group3)
    
    return {"ANOVA": (f_stat, p_value), "Bartlett": (bartlett_stat, bartlett_p)}

print("\nInciso A: Prueba ANOVA y Bartlett")
for var in ["X1", "X2", "X3", "X4", "X5", "X6"]:
    results = anova_bartlett(df_prob3_cleaned, var)
    print(f"Variable {var} - ANOVA: F={results['ANOVA'][0]:.4f}, p={results['ANOVA'][1]:.4f}")
    print(f"Variable {var} - Bartlett: Chi2={results['Bartlett'][0]:.4f}, p={results['Bartlett'][1]:.4f}")

def tukey_test(df, variable):
    data = []
    groups = []
    for turno in ["T1", "T2", "T3"]:
        data.extend(df[f"{variable}_{turno}"].values)
        groups.extend([turno] * len(df))
    
    tukey = pairwise_tukeyhsd(data, groups, alpha=0.05)
    return tukey

print("\nInciso B: Intervalos de confianza simultáneos (Tukey HSD)")
for var in ["X1", "X2", "X3", "X4", "X5", "X6"]:
    tukey_result = tukey_test(df_prob3_cleaned, var)
    print(f"\nVariable {var}:")
    print(tukey_result)

def box_m_test(df):
    matrices = [df[[f"X{i}_T1", f"X{i}_T2", f"X{i}_T3"]].values for i in range(1, 7)]
    cov_matrices = [np.cov(matrix, rowvar=False) for matrix in matrices]
    pooled_cov = np.mean(cov_matrices, axis=0)
    pooled_cov = cov_nearest(pooled_cov)
    box_m_stat = np.linalg.det(pooled_cov)
    p_value = stats.chi2.sf(box_m_stat, df=len(pooled_cov) - 1)
    return {"M-Statistic": box_m_stat, "p-value": p_value}

print("\nInciso C: Prueba M de Box")
box_m_results = box_m_test(df_prob3_cleaned)
print(f"M-Statistic: {box_m_results['M-Statistic']:.4f}, p-value: {box_m_results['p-value']:.4f}")
#############################################
#                Problema 4                 #
#############################################
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.correlation_tools import cov_nearest

file_path = "Segundo_tetra/datos_tarea5.xlsx"
df_prob4 = pd.read_excel(file_path, sheet_name="PROB5")

num_columns = len(df_prob4.columns)
if num_columns == 7:
    df_prob4.columns = ["Universidad", "X1", "X2", "X3", "X4", "X5", "X6"]
else:
    df_prob4.columns = ["Universidad"] + [f"X{i}" for i in range(1, num_columns)]
    print(f"Advertencia: El archivo tiene {num_columns} columnas. Se asignaron nombres genéricos.")

df_prob4 = df_prob4.dropna()

df_prob4 = df_prob4[df_prob4["Universidad"].isin(["A", "B", "C"])]

def anova_bartlett(df, variable):
    groups = [df[df["Universidad"] == uni][variable].values for uni in df["Universidad"].unique() if len(df[df["Universidad"] == uni]) > 1]
    if len(groups) < 2:
        return None
    f_stat, p_value = stats.f_oneway(*groups)
    bartlett_stat, bartlett_p = stats.bartlett(*groups)
    return {"ANOVA": (f_stat, p_value), "Bartlett": (bartlett_stat, bartlett_p)}

print("\nInciso A: Prueba ANOVA y Bartlett")
for var in df_prob4.columns[1:]:
    results = anova_bartlett(df_prob4, var)
    if results:
        print(f"Variable {var} - ANOVA: F={results['ANOVA'][0]:.4f}, p={results['ANOVA'][1]:.4f}")
        print(f"Variable {var} - Bartlett: Chi2={results['Bartlett'][0]:.4f}, p={results['Bartlett'][1]:.4f}")
    else:
        print(f"No hay suficientes datos para ANOVA en {var}")

def tukey_test(df, variable):
    data = []
    groups = []
    for uni in df["Universidad"].unique():
        subset = df[df["Universidad"] == uni][variable].values
        if len(subset) > 1:
            data.extend(subset)
            groups.extend([uni] * len(subset))
    if len(set(groups)) < 2:
        print(f"No hay suficientes grupos para realizar la prueba de Tukey en {variable}")
        return None
    tukey = pairwise_tukeyhsd(data, groups, alpha=0.05)
    return tukey

print("\nInciso B: Intervalos de confianza simultáneos (Tukey HSD)")
for var in df_prob4.columns[1:]:
    tukey_result = tukey_test(df_prob4, var)
    if tukey_result:
        print(f"\nVariable {var}:")
        print(tukey_result)

def box_m_test(df):
    universities = df["Universidad"].unique()
    matrices = [df[df["Universidad"] == uni].iloc[:, 1:].values for uni in universities if len(df[df["Universidad"] == uni]) > 1]
    if len(matrices) < 2:
        print("No hay suficientes grupos para realizar la prueba M de Box")
        return None
    cov_matrices = [np.cov(matrix, rowvar=False) for matrix in matrices]
    pooled_cov = np.mean(cov_matrices, axis=0)
    pooled_cov = cov_nearest(pooled_cov)
    box_m_stat = np.linalg.det(pooled_cov)
    p_value = stats.chi2.sf(box_m_stat, df=len(pooled_cov) - 1)
    return {"M-Statistic": box_m_stat, "p-value": p_value}

print("\nInciso C: Prueba M de Box")
box_m_results = box_m_test(df_prob4)
if box_m_results:
    print(f"M-Statistic: {box_m_results['M-Statistic']:.4f}, p-value: {box_m_results['p-value']:.4f}")