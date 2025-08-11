import pandas as pd

data = pd.read_csv("data ficticios.csv", sep=";", encoding="latin1")

#tirar colunas com drop (pandas)
data = data.drop(columns=["txt_nome_empreendimento", "cod_ibge", "cod_empreendimento"], errors="ignore")

#Converter datas para ano/mês
data["data_referencia"] = pd.to_datetime(data["data_referencia"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)
data["dt_assinatura_contrato"] = pd.to_datetime(data["dt_assinatura_contrato"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)

data["faixa_etaria"] = pd.to_datetime(data["data_nascimento"], dayfirst=True, errors="coerce").dt.year
data["faixa_etaria"] = pd.cut(data["faixa_etaria"], 
                               bins=[1900, 1980, 2000, 2010, 2025], 
                               labels=["até 29", "30-49", "50-64", "65+"], 
                               right=False)

data = data.drop(columns=["data_nascimento"], errors="ignore")

#Renomear colunas com rename (pandas)
data = data.rename(columns={
    "Estado Civil": "estado_civil",
    "Tipo de Beneficiário": "tipo_beneficiario"
})

#colunas monetárias para float
monet_colums = ["vr_garantia_inicial", "vr_subsidio_concessao", "vr_renda_familiar_comprovada"]
for col in monet_colums:
    if col in data.columns:
        data[col] = data[col].astype(str).replace({"R\$": "", "\.": "", ",": "."}, regex=True)
        data[col] = pd.to_numeric(data[col], errors="coerce")

#Amostragem estratificada
fac_per_group = 0.05  # 5% por modalidade
sample = data.groupby("txt_modalidade", group_keys=False).apply(
    lambda x: x.sample(frac=fac_per_group, random_state=123)
)

sample.to_csv("amostra_sdc.csv", index=False, encoding="utf-8-sig")
print("✅ Amostra estratificada salva como 'sample_sdc.csv'")

# EDA básica da sample
print("\nEstrutura da amostra:")
print(sample.info())

print("\nResumo estatístico numéricas:")
print(sample.describe(include="number"))

print("\nResumo estatístico categóricas:")
print(sample.describe(include="object"))

print("\nContagem por UF:")
print(sample["txt_uf"].value_counts())

print("\nContagem por modalidade:")
print(sample["txt_modalidade"].value_counts())
