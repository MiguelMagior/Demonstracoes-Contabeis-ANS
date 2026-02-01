# Demonstracoes-Contabeis-ANS
Tecnologias
- Python 3.14.2

Teste 1
Baixa os arquivos de Demonstrações Contábeis dos últimos 3 semetres disponibilizados pela ANS por meio de solicitações HTTP.
Os arquivos são armazenados, extraidos e processados em memória a fim de evitar operações de I/O. Esses processos no momento são realizados de maneira incremental, com a possibilidade de ser implementado processos assíncronos no futuro para melhor desempenho e velocidade.
Gera um arquivo CSV final contendo as colunas:
  - CNPJ e Razão Social: obtidas pelo join com a tabela de Operadoras de Plano de Saúde Ativas da ANS
  - Trimeste e Ano
  - ValorDespesas: valores tratados como decimais positivos

Teste 2
Validação dos dados gerados no Teste 1:
  - CNPJ não nulo e válido
  - Valores numéricos positivos e não nulos
  - Razão Social não nulo
Registros com valores inválidos são direcionados a um arquivo CSV de quarentena. Isso proporciona a melhor qualidade e confiabilidade do conjunto de dados sem a exclusão permanente dessas entradas, permitindo seu tratamento futuro. O custo dessa solução é o armazenamento desses dados em disco, que necessitarão de um novo fluxo de processamento no sistema.
Após a validação ocorre a adição das colunas de Número de Registro da ANS, Modalidade da Operadora e sua UF. As linhas então são agrupadas por Razão Social, UF e Trimestre de modo a permitir o cálculo de novas colunas de:
  - Total de despesas da operado por trimestre (odenadas de maneira decrescente)
  - Média de custo por trimestre
  - Desvio padrão das despesas
