pacman::p_load(sdcMicro, readxl, dplyr)

dados <- read_excel(file.choose(), sheet = 2)

dados <- dados |> select(-cpf, -nome_benefiniciário)

dados$data_referencia <- format(as.Date(dados$data_referencia), "%Y-%m")

dados <- dados |> select(-cod_ibge)

dados$txt_municipio <- dados$txt_uf

quasi_identificadores <- c("txt_uf", "txt_regiao")
variaveis_numericas <- c("vr_garantia_inicial", "vr_subsidio_concessao")

sdc <- createSdcObj(
  dat = dados,
  keyVars = quasi_identificadores,
  numVars = variaveis_numericas
)

sdc <- localSuppression(sdc, k = 5)

sdc <- microaggregation(sdc, method = "mdav", variables = variaveis_numericas)

dados_anonimizados <- extractManipData(sdc)
write.csv(dados_anonimizados, "tabela2_anonimizada.csv", row.names = FALSE)

if (!require("remotes")) install.packages("remotes")
remotes::install_github("sdcTools/sdcApp")
sdcApp::runApp()

