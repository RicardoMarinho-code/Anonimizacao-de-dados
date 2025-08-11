import pandas as pd
import numpy as np

dados = pd.read_csv('dados ficticios.csv', sep=';', encoding='latin1')

dados = dados.drop(columns=['txt_nome_empreendimento', 'cod_ibge', 'cod_empreendimento'])

# Converter datas para ano-mês (corrigido para dayfirst=True)
dados['data_referencia'] = pd.to_datetime(dados['data_referencia'], dayfirst=True).dt.strftime('%Y-%m')
dados['dt_assinatura_contrato'] = pd.to_datetime(dados['dt_assinatura_contrato'], dayfirst=True).dt.strftime('%Y-%m')

# Criar faixa_etaria baseado no ano de nascimento
anos = pd.to_datetime(dados['data_nascimento'], dayfirst=True).dt.year
bins = [1900, 1980, 2000, 2010, 2025]
labels = ['até 29', '30-49', '50-64', '65+']
dados['faixa_etaria'] = pd.cut(anos, bins=bins, labels=labels, right=False)

# Remover data_nascimento
dados = dados.drop(columns=['data_nascimento'])

# Renomear colunas para evitar espaços
dados = dados.rename(columns={
    'Estado Civil': 'estado_civil',
    'Tipo de Beneficiário': 'tipo_beneficiario'
})

# 3. Criar amostra fixa (seed)
np.random.seed(123)
amostra = dados.sample(n=500, random_state=123)

# Salvar amostra
amostra.to_csv('amostra_sdc.csv', index=False)

# 4. EDA básica
print(amostra.info())
print(amostra.describe(include='all'))
print(amostra['txt_uf'].value_counts())
