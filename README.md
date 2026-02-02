# Demonstracoes-Contabeis-ANS
Tecnologias
- Python
- MySQL 

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

Teste 3
Scripts SQL para execução de tarefas
- Criação de tabelas:
  Semi-normalização das tabelas de modo a evitar a repetição de dados na base de dados porém sem perder eficiência ou aumentando a complexidade da arquitetura
  - Dados cadatrais das operadoras - contem todos os dados disponibilizados no CSV
  - Dados consolidados e agregados de Despesas - possuem dados referentes ao periodo e valores, com chave estrangeira para sua operadora
  Não são permitidos valores NULL em atributos utilizados nas demais queries
  Criação de indices para otimização de consultas
  Dados monetários foram tratados como DECIMAL para melhor precisão durante os cálculos.
  Datas inteiras foram armazenadas como DATE enquanto anos foram armazenados como YEAR, preservando seus valores específicos.
- Importação dos dados dos arquivos:
  Popular automaticamente a base de dados com os dados contidos nos CSVs
  Entradas com valores NULL em campos obrigatórios foram movidas previamente para a quarentena
  Strings foram convertidos para valores numéricos
- Queries Analíticas:
  - As 5 operadoras com maior crescimento percentual entre o primeiro e o último trimestre - é feita a verificação de quais operadoras possuem valores em ambos trimestre por meio de um join
  - As 5 UF com maiores valores de despesas totais junto a sua média gasta por operadora
  - Quantas operadoras tiveram despesas acima da média geral em pelo menos 2 trimestres - é calculado a média geral de cada trimestre e então adicionadas em uma tabela auxiliar as operadoras que tiveram despesas acima desse valor para cada trimestre. Ao final, as operadoras que tiveram duas ou mais entradas na tabela são adicionadas a contagem

Teste 4
    
