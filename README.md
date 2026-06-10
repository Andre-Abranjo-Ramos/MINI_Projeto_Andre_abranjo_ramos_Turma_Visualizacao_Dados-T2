# Mini-Projeto Avaliativo - Análise Exploratória de Dados (Varejo)

## Contextualização do Projeto
Este projeto realiza uma Análise Exploratória de Dados em uma base de dados real do setor de varejo. O principal objetivo é executar o pipeline de ETL (Extração, Transformação e Carga), garantindo a qualidade dos dados antes de qualquer etapa de tomada de decisão ou alimentação de dashboards de Business Intelligence.

----

## Reflexão Teórica: ETL e Qualidade de Dados
O processo de **ETL (Extract, Transform, Load)** é a espinha dorsal da engenharia de dados e do BI. 
* **Extração:** Realizada de forma nativa e controlada utilizando `csv.DictReader`, mitigando falhas de parsing inicial.
* **Transformação:** A fase crítica onde regras de negócio limpam inconsistências. Dados brutos frequentemente apresentam problemas que distorcem análises estatísticas (ex: valores nulos interpretados como zero de forma errônea ou formatos de data inconsistentes). O tratamento sistemático previne o fenômeno *Garbage In, Garbage Out* (Entrada de Lixo gera Saída de Lixo).
* **Carga:** Armazenamento dos dados tratados em um DataFrame estruturado e exportação para um arquivo `.csv` limpo, pronto para consumo analítico confiável.

----

## Principais Insights Obtidos
1. **Tratamento de Categorias Ocultas:** A aplicação da lógica de condicional revelou compras sem classificação adequada, as quais foram mapeadas sob a marcação `"Sem Categoria"`, impedindo a perda de registros financeiros históricos.
2. **Impacto das Linhas Duplicadas:** Foram identificados e expurgados registros duplicados idênticos, garantindo que o faturamento total da empresa não fosse inflado artificialmente na análise operacional.
3. **Perfil Familiar do Consumidor:** A análise descritiva da coluna de filhos revelou a distribuição central dos clientes, métrica fundamental para direcionar campanhas de marketing direcionadas a famílias ou solteiros.
4. **Concentração de Vendas por Categoria:** O agrupamento por categorias permitiu identificar quais setores geram a maior fatia da receita do varejo, permitindo otimizar a gestão e alocação de estoque.

----

## Instruções de Execução
1. Faça o upload do arquivo `Varejo.csv` no diretório raiz do seu ambiente (VsCode ou Google Colab).
2. Execute todas as células do script Python fornecido.
3. O script exibirá os relatórios diretamente no terminal e exportará a base tratada como `base_varejo_limpa_final.csv`.
