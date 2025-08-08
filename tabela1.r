pacman::p_load(sdcMicro, readxl, dplyr, readr) 

dados <- read_delim(file.choose(), delim = ";", locale = locale(encoding = "Latin1")
)

dados <- dados |> select(
  -txt_nome_empreendimento,
  -cod_ibge,
  -cod_empreendimento
)

# as.Date transforma strings em datas, e "format" as transforma em ano-mês
# p.19, p.31, p.32
dados$data_referencia <- format(as.Date(dados$data_referencia), "%Y-%m")

dados$dt_assinatura_contrato <- format(as.Date(dados$dt_assinatura_contrato), "%Y-%m")

# p. 19 (agrupamento de idade) e p. 35 (generalização para faixas)
dados$faixa_etaria <- cut(as.numeric(format(as.Date(dados$data_nascimento), "%Y")),
                          breaks = c(1900, 1980, 2000, 2010, 2025),
                          labels = c("até 29", "30-49", "50-64", "65+"),
                          right = FALSE)

dados <- dados |> select(-data_nascimento)

colnames(dados)[colnames(dados) == "Estado Civil"] <- "estado_civil"
colnames(dados)[colnames(dados) == "Tipo de Beneficiário"] <- "tipo_beneficiario"

quasi_identificadores <- c(
  "txt_municipio", "txt_uf", "txt_regiao",
  "txt_sexo", "estado_civil", "tipo_beneficiario", "faixa_etaria"
)

sdc <- createSdcObj(
  dat = dados,
  keyVars = quasi_identificadores
)

sdc <- localSuppression(sdc, k = 5)

sdc <- pram(sdc, variables = c("estado_civil", "txt_sexo"))


tryCatch({
  dados_anonimizados <- extractManipData(sdc)
  write.csv(dados_anonimizados, "tabela1_anonimizada.csv", row.names = FALSE)
  print("Dados salvos!")
}, error = function(e) {
  message("Erro ao extrair os dados anonimizados. Verifique se o objeto 'sdc' foi criado corretamente.")
})

