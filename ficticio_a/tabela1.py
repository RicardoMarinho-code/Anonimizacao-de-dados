import pandas as pd
import sweetviz as sv
import os

data = pd.read_csv("dados/dados ficticios.csv", sep=";", encoding="latin1")

data = data.drop(columns=["txt_nome_empreendimento", "cod_ibge", "cod_empreendimento"], errors="ignore")

data["data_referencia"] = pd.to_datetime(data["data_referencia"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)
data["dt_assinatura_contrato"] = pd.to_datetime(data["dt_assinatura_contrato"], dayfirst=True, errors="coerce").dt.to_period("M").astype(str)

data["faixa_etaria"] = pd.to_datetime(data["data_nascimento"], dayfirst=True, errors="coerce").dt.year
data["faixa_etaria"] = pd.cut(data["faixa_etaria"], 
                              bins=[1900, 1980, 2000, 2010, 2025], 
                              labels=["até 29", "30-49", "50-64", "65+"], 
                              right=False)

data = data.drop(columns=["data_nascimento"], errors="ignore")

data = data.rename(columns={
    "Estado Civil": "estado_civil",
    "Tipo de Beneficiário": "tipo_beneficiario"
})

monet_colums = ["vr_garantia_inicial", "vr_subsidio_concessao", "vr_renda_familiar_comprovada"]
for col in monet_colums:
    if col in data.columns:
        data[col] = data[col].astype(str).replace({r"R\$": "", r"\.": "", ",": "."}, regex=True)
        data[col] = pd.to_numeric(data[col], errors="coerce")

fac_per_group = 0.05  # 5% por modalidade
sample = data.groupby("txt_modalidade", group_keys=False).apply(
    lambda x: x.sample(frac=fac_per_group, random_state=123)
)

sample.to_csv("amostra_sdc.csv", index=False, encoding="utf-8-sig")
print("✅ Amostra estratificada salva como 'amostra_sdc.csv'")

dataset_name = "dados_ficticios"
output_dir = "relatorios_sweetviz"
os.makedirs(output_dir, exist_ok=True)

profiling_html_path = os.path.join(output_dir, f"{dataset_name}.html")

profile_report = sv.analyze(sample, pairwise_analysis='on')
profile_report.show_html(profiling_html_path)