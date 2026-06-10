# MINI-PROJETO: ANÁLISE EXPLORATÓRIA DE DADOS (VAREJO)
# Estudante: André Abranjo Ramos

# Importando as bibliotecas necessárias para o projeto
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import os

# SPRINT 1: Importação dos Dados
# Aqui como a base é da platafoma Kaggle, eu não consegui validar e baixar diretomente, então deixei o caminho local para o arquivo CSV.
ARQUIVO_CSV = 'Base varejo.csv'

# SPRINT 2 e 3: Transformação e Limpeza dos Dados
dados_limpos = []
total_registros = 0
linhas_duplicadas = 0
vistos = set()

# Abrindo o arquivo e lendo linha por linha para aplicar os critérios de limpeza
with open(ARQUIVO_CSV, mode='r', encoding='utf-8') as f:
    # Essa base do varejo utiliza delimitador ';'
    leitor = csv.DictReader(f, delimiter=';')
    # Contando quantidade total de registros para o relatório final
    for linha in leitor:
        total_registros += 1

        # Identificador de linha única e remoção de linhas duplicadas ---
        identificador_registro = tuple(linha.items())
        if identificador_registro in vistos:
            linhas_duplicadas += 1
            continue
        vistos.add(identificador_registro)

        # Tratamento e limpeza dos delimitadores de texto e nulos
        cat_original = linha.get('PR_CAT', '')
        genero_original = linha.get('CL_GENERO', '')

        # Tratamento de nulos/vazios em colunas de texto que tem nulos/Nall
        if not cat_original or cat_original.strip().upper() in ['', 'NAN', '#N/D', 'ND']:
            continue
        if not genero_original or genero_original.strip().upper() in ['', 'NAN', '#N/D', 'ND']:
            continue

        # Salvando os valores tratados
        linha['PR_CAT'] = cat_original.strip()
        linha['CL_GENERO'] = genero_original.strip()

        # Tratamento de nulos das colunas númericas de dimensões (peso, altura, largura, comprimento)
        for dimensao in ['peso', 'altura', 'largura', 'comprimento']:
            if dimensao in linha:
                val_dim = linha[dimensao]
                if not val_dim or val_dim.strip().upper() in ['', 'NAN', '#N/D', 'ND']:
                    linha[dimensao] = 0.0
                else:
                    try:
                        # troca a vírgula por ponto para conversão correta
                        linha[dimensao] = float(val_dim.replace(',', '.'))
                    except ValueError:
                        linha[dimensao] = 0.0

        # Conversão de datas usando o datetime
        data_original = linha.get('DATA', '')
        if data_original and data_original.strip().upper() not in ['NAN', '#N/D', '']:
            try:
                # Aplica o formato padrão ISO
                linha['DATA_FORMATADA'] = datetime.strptime(
                    data_original.strip(), '%Y-%m-%d')
            except ValueError:
                try:
                    # Aplica o formato padrão brasileiro
                    linha['DATA_FORMATADA'] = datetime.strptime(
                        data_original.strip(), '%d/%m/%Y')
                except ValueError:
                    linha['DATA_FORMATADA'] = None
        else:
            linha['DATA_FORMATADA'] = None

        # Tratamento da coluna de valor de venda (VR_VND)
        col_venda_real = 'VR_VND' if 'VR_VND' in linha else [
            c for c in linha.keys() if 'VND' in str(c).upper() or 'VALOR' in str(c).upper()]
        col_venda = col_venda_real if isinstance(col_venda_real, str) else (
            col_venda_real[0] if col_venda_real else None)
        # Tratamento da coluna de valor de venda (VR_VND_TRATADO)
        if col_venda and linha.get(col_venda):
            try:
                linha['VR_VND_TRATADO'] = float(
                    linha[col_venda].strip().replace(',', '.'))
            except ValueError:
                linha['VR_VND_TRATADO'] = 0.0
        else:
            linha['VR_VND_TRATADO'] = 0.0

        dados_limpos.append(linha)

# Criação do Dataframe final a partir dos dados limpos coletados e tratados
df = pd.DataFrame(dados_limpos)

# Tratamento de dados vazios ou faltantes na coluna de filhos (CL_FHL) apliquei o valor que está mediana da coluna.
if 'CL_FHL' in df.columns:
    # Converte a coluna para numérico
    df['CL_FHL'] = pd.to_numeric(df['CL_FHL'].astype(
        str).str.replace(',', '.'), errors='coerce')
    mediana_filhos = df['CL_FHL'].median()
    # Se a mediana não existir  adota 0
    if np.isnan(mediana_filhos):
        mediana_filhos = 0.0
    df['CL_FHL'] = df['CL_FHL'].fillna(mediana_filhos).astype(int)

print("\nRelatório Final de Limpesa ")
print(f"Total de registros lidos: {total_registros}")
print(
    f"Total de linhas duplicadas que foram deletadas: {linhas_duplicadas}")
print(f"Total de linhas na base limpa: {len(df)} linhas.")

# SPRINT 4: estatística descritiva

print("\nEstatística Descritiva da Coluna CL_FHL (Número de Filhos):")
if 'CL_FHL' in df.columns:
    col_filhos = df['CL_FHL']
    estatisticas_filhos = pd.DataFrame({
        'Métrica': ['Contagem', 'Média', 'Mediana', 'Moda', 'Desvio Padrão', 'Mínimo', 'Máximo'],
        'Valor': [
            col_filhos.count(),
            col_filhos.mean(),
            col_filhos.median(),
            col_filhos.mode().iloc[0] if not col_filhos.mode(
            ).empty else np.nan,
            col_filhos.std(),
            col_filhos.min(),
            col_filhos.max()
        ]
    })
    print(estatisticas_filhos.to_string(index=False))
else:
    print("A coluna 'CL_FHL' não disponível para cálculos estatísticos.")
