import pandas as pd

# === 1. Ler dados ===
data = pd.read_csv("dados/dados ficticios.csv", sep=";", encoding="latin1")

# === 2. Limpar colunas ===
data = data.drop(columns=["txt_nome_empreendimento", "cod_ibge", "cod_empreendimento"], errors="ignore")

# === 3. Converter datas para ano/mês ===
data["data_referencia"] = pd.to_datetime(data["data_referencia"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)
data["dt_assinatura_contrato"] = pd.to_datetime(data["dt_assinatura_contrato"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)

# === 4. Criar faixa etária ===
data["faixa_etaria"] = pd.to_datetime(data["data_nascimento"], dayfirst=True, errors="coerce").dt.year
data["faixa_etaria"] = pd.cut(data["faixa_etaria"], 
                              bins=[1900, 1980, 2000, 2010, 2025], 
                              labels=["até 29", "30-49", "50-64", "65+"], 
                              right=False)

data = data.drop(columns=["data_nascimento"], errors="ignore")

# === 5. Renomear colunas ===
data = data.rename(columns={
    "Estado Civil": "estado_civil",
    "Tipo de Beneficiário": "tipo_beneficiario"
})

# === 6. Converter colunas monetárias para float ===
monet_colums = ["vr_garantia_inicial", "vr_subsidio_concessao", "vr_renda_familiar_comprovada"]
for col in monet_colums:
    if col in data.columns:
        data[col] = data[col].astype(str).replace({"R\$": "", "\.": "", ",": "."}, regex=True)
        data[col] = pd.to_numeric(data[col], errors="coerce")

# === 7. Amostragem estratificada ===
fac_per_group = 0.05  # 5% por modalidade
sample = data.groupby("txt_modalidade", group_keys=False).apply(
    lambda x: x.sample(frac=fac_per_group, random_state=123)
)

# Salvar amostra para sdcApp
sample.to_csv("amostra_sdc.csv", index=False, encoding="utf-8-sig")
print("✅ Amostra estratificada salva como 'amostra_sdc.csv'")

# === 8. Criar DataFrame para EDA ===
eda_parts = []

# Estrutura (salva só o número de linhas/colunas e tipos)
eda_parts.append(pd.DataFrame({
    "Info": [f"{sample.shape[0]} linhas, {sample.shape[1]} colunas", 
             f"Tipos de dados: {dict(sample.dtypes)}"]
}))

# Resumo numéricas
desc_num = sample.describe(include="number").reset_index()
desc_num.insert(0, "Seção", "Resumo numéricas")
eda_parts.append(desc_num)

# Resumo categóricas
desc_cat = sample.describe(include="object").reset_index()
desc_cat.insert(0, "Seção", "Resumo categóricas")
eda_parts.append(desc_cat)

# Contagem por UF
uf_counts = sample["txt_uf"].value_counts().reset_index()
uf_counts.columns = ["UF", "Contagem"]
uf_counts.insert(0, "Seção", "Contagem por UF")
eda_parts.append(uf_counts)

# Contagem por modalidade
mod_counts = sample["txt_modalidade"].value_counts().reset_index()
mod_counts.columns = ["Modalidade", "Contagem"]
mod_counts.insert(0, "Seção", "Contagem por modalidade")
eda_parts.append(mod_counts)

# Concatenar tudo e salvar
eda_final = pd.concat(eda_parts, ignore_index=True)
eda_final.to_csv("eda_amostra.csv", index=False, encoding="utf-8-sig")

