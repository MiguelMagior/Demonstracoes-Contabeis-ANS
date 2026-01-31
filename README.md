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

