import numpy as np
from scipy.special import gamma
from scipy.stats import norm

#Problema 2
#a)
duration_component = [184.2, 116.3, 154.1, 98.5, 106.2, 126.5, 130.7,
155.1, 142, 100.9, 135, 102.1, 104.5, 76.8, 130.9, 121.2, 102.2, 165.1,
190.6, 99.5, 89.2 ]

alpha = np.mean(duration_component)

gamma_value = gamma(1.4)
#print(gamma_value)
betha_value = alpha/gamma_value
print(betha_value)

#b)
Esp_X= betha_value*gamma_value
print(Esp_X)

#c)
alpha = 2.5
beta = betha_value
x = 100

probability_greater_100 = np.exp(-(x / beta) ** alpha)
print(probability_greater_100)

#problema3
#a)
temperature_values = [39.4, 39.3, 36.1,	38.7, 37.4,	37.9, 38, 37.7,
39.8, 37.4, 37.1, 37.1, 38, 39.1, 37, 37.7, 38.9, 38.1, 36.6, 39.9,
38, 39.3, 37.2, 38.2, 39.5, 36.8, 38.4, 36.5]

temperature_mean = np.mean(temperature_values)
print(temperature_mean)
temperature_var = np.var(temperature_values, ddof=1)
print(temperature_var)
#b)
temperature_desv = np.sqrt(temperature_var)

z_value = (40 - temperature_mean) / temperature_desv

probability_greater_40 = 1 - norm.cdf(z_value)
print(probability_greater_40)
