# ---
# title: "Script para Propuesta Comparativo Correo Informe"
# author: "BRS101490"
# date: "2024-11-20"
# output: html_document
# ---

# ```{r}
# suppressWarnings(library(lubridate))
# suppressWarnings(library(dplyr))
# suppressWarnings(library(tidyr))
# suppressWarnings(library(writexl))
# suppressWarnings(library(openxlsx))
# suppressWarnings(library(stringr))
# suppressWarnings(library(tools))
# ```

# ```{r}
# fecha <- Sys.Date() - months(2)
# year_month <- format(fecha, "%Y%m")
# ```

# ```{r}
# df <- read.csv(paste("G:/Unidades compartidas/Solvencia/Información de la CNBV/", 
# str_to_title(format(fecha,"%Y/%m. %B")),"/1. ICAP/040_TO.csv", sep=""))
# # ```

# ```{r}
library(openxlsx)
conceptos <- c("4021750",  # ICAP
               "900000",   # RA
               "4030211",  # Capital Neto
               "4030249",  # Activos Sujetos a Riesgo 
               "4030212",  # Capital Básico
               "40100002", # Capital Contable
               "40100001") # Activo


inst <- read.xlsx("External/instituciones.xlsx")
#print(inst)
#stop("Script finalizado")
# ```

# ```{r}
df1 <- subset(df, concepto %in% conceptos) %>% filter(fecha==year_month & institucion %in% inst$institucion & tipo_saldo=="Consolidado con SOFOMER") 

print(df1)
stop("Script finalizado")
df1 <- df1 %>% select(-tipo_saldo, -fecha)

df2 <- df1 %>% pivot_wider(names_from = concepto, values_from = saldo_se) 

df3 <- left_join(inst, df2) #%>% group_by(grupo)

df4 <- df3 %>% group_by(grupo) %>% arrange(desc(4021750), .by_group = TRUE)

df5 <- df3 %>% arrange(desc("4021750"),.by_group=TRUE)

df6 <- df3 %>% 
  group_by(grupo) %>% 
  mutate(orden = rank(-4021750)) %>%  # Agrega una columna con el ranking descendente
  arrange(grupo, orden)
```

```{r}
wb <- loadWorkbook(paste("G:/Unidades compartidas/Solvencia/00. Presentaciones ICAP/Correo Informe ICAP/",str_to_title(format(fecha, "%Y/%m. %B")), "/Insumos/3. ICAP e Indicadores/Tabla Correo Informe ICAP.xlsx",sep=""))

writeData(wb, sheet = "Base", df3$"4021750", startRow = 5, startCol = 5)
writeData(wb, sheet = "Propuesta 1", df3$"900000", startRow = 5, startCol = 7)
writeData(wb, sheet = "Propuesta 1", df3$"4030211"/1000000 ,startRow = 5, startCol = 9)
writeData(wb, sheet = "Propuesta 1", df3$"4030249"/1000000, startRow = 5, startCol = 11)
writeData(wb, sheet = "Propuesta 1", df3$"4030212"/1000000, startRow = 5, startCol = 13)
writeData(wb, sheet = "Propuesta 1", df3$"40100002"/1000000, startRow = 5, startCol = 17)
writeData(wb, sheet = "Propuesta 1", df3$"40100001"/1000000, startRow = 5, startCol = 19)

saveWorkbook(wb, file = "C:/Users/BRS101490/Documents/Propuestas comparativo bancos - Informe ICAP.xlsx", overwrite=TRUE)
```
Tengo dos columnas en un dataframe y las quiero organizar con df4, que me traiga registros
en base al cirterio que puse, pero no me trae todos los registros que deberia, no se que este mal en mi filtro