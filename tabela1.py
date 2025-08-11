import pandas as pd

#Ler base
dados = pd.read_csv("dados ficticios.csv", sep=";", encoding="latin1")

#Remover colunas irrelevantes
dados = dados.drop(columns=["txt_nome_empreendimento", "cod_ibge", "cod_empreendimento"], errors="ignore")

#Converter datas para ano-mês
dados["data_referencia"] = pd.to_datetime(dados["data_referencia"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)
dados["dt_assinatura_contrato"] = pd.to_datetime(dados["dt_assinatura_contrato"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)

#Criar faixa etária
dados["faixa_etaria"] = pd.to_datetime(dados["data_nascimento"], dayfirst=True, errors="coerce").dt.year
dados["faixa_etaria"] = pd.cut(dados["faixa_etaria"], 
                               bins=[1900, 1980, 2000, 2010, 2025], 
                               labels=["até 29", "30-49", "50-64", "65+"], 
                               right=False)

#Remover coluna original de nascimento
dados = dados.drop(columns=["data_nascimento"], errors="ignore")

#Renomear colunas
dados = dados.rename(columns={
    "Estado Civil": "estado_civil",
    "Tipo de Beneficiário": "tipo_beneficiario"
})

#Converter colunas monetárias para float
colunas_monetarias = ["vr_garantia_inicial", "vr_subsidio_concessao", "vr_renda_familiar_comprovada"]
for col in colunas_monetarias:
    if col in dados.columns:
        dados[col] = dados[col].astype(str).replace({"R\$": "", "\.": "", ",": "."}, regex=True)
        dados[col] = pd.to_numeric(dados[col], errors="coerce")

#Amostragem estratificada por modalidade
frac_por_grupo = 0.05  # 5% de cada modalidade
amostra = dados.groupby("txt_modalidade", group_keys=False).apply(
    lambda x: x.sample(frac=frac_por_grupo, random_state=123)
)

#Salvar amostra para usar no sdcApp
amostra.to_csv("amostra_sdc.csv", index=False, encoding="utf-8-sig")
print("✅ Amostra estratificada salva como 'amostra_sdc.csv'")

# EDA básica da amostra
print("\nEstrutura da amostra:")
print(amostra.info())

print("\nResumo estatístico das variáveis numéricas:")
print(amostra.describe(include="number"))

print("\nResumo estatístico das variáveis categóricas:")
print(amostra.describe(include="object"))

print("\nContagem por UF:")
print(amostra["txt_uf"].value_counts())

print("\nContagem por modalidade:")
print(amostra["txt_modalidade"].value_counts())
