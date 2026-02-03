# Demonstrações Contábeis - Agência Nacional de Saúde Suplementar
Versão 1.0

## Tecnologias
- Python 
- MySQL
- Vue.js

## Requisitos
Instalar biblotecas do Python:  
```
cd Demonstracoes-Contabeis-ANS/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Teste 1 - Integração com API Pública 
<p align="justify"> Script em Python que baixa os arquivos de Demonstrações Contábeis dos últimos 3 semetres disponibilizados pela ANS por meio de solicitações HTTP.  </p>
  
<p align="justify"> Os arquivos são armazenados, extraidos e processados em memória a fim de evitar operações de I/O. Esses processos no momento são realizados de maneira incremental, com a possibilidade de ser implementado processos assíncronos no futuro para melhor desempenho e velocidade.  </p>
  
Gera um arquivo CSV final de Despesas Consolidadas contendo as colunas:
  - CNPJ e Razão Social: obtidas pelo join com a tabela de Operadoras de Plano de Saúde Ativas da ANS;
  - Trimeste e Ano: obtidos pelo nome do arquivo de entrada;
  - ValorDespesas: valores tratados como decimais positivos.
  
Executar teste:  
```
python -m teste1
```

## Teste 2 - Transformação e Validação de Dados
Script para validação e processamento dos dados gerados no Teste 1:
  - CNPJ não vazio e válido;
  - Valores numéricos positivos e não nulos;
  - Razão Social não vazio.
  
<p align="justify">Registros com dados inválidos são direcionados a um arquivo CSV de quarentena. Isso proporciona a melhor qualidade e confiabilidade do conjunto de dados sem a exclusão permanente das entradas invalidadas, permitindo seu tratamento futuro. Essa solução gera o custo de armazenamento desses dados em disco, que necessitarão de um novo fluxo de processamento no sistema. </p> 
  
<p align="justify">Após a validação ocorre a adição das colunas de Número de Registro da ANS, Modalidade da Operadora e sua UF por meio de um novo join com a tabela de Operadoras. As linhas então são agrupadas por Razão Social, UF e Trimestre de modo a permitir o cálculo de novas colunas de:</p>

  - Total de despesas da operado por trimestre (odenadas de maneira decrescente);
  - Média de custo por trimestre;
  - Desvio padrão dessas despesas.  
  
Gera um arquivo CSV final de Despesas Agregadas com todos os dados obtidos em ambos os testes.  
   
Executar teste:  
```
python -m teste2
```

## Teste 3 - Banco de dados
Scripts SQL compatível com MySQL para a criação de tabelas, importação e consulta dos dados obtidos nos testes anteriores.
### Criação de tabelas:
<p align="justify">Queries DDL seguindo uma abordagem de semi-normalização dos dados, de modo a evitar sua repetição desnecessária sem comprometer a eficiência das consultas ou aumentando a complexidade da arquitetura.</p>
  
  - Dados cadatrais das operadoras - contêm todos os dados disponibilizados no CSV de Operadoras;
  - Dados consolidados e agregados de Despesas - possuem dados referentes ao seu período e valores, com chave estrangeira para a operadora correspondente
  
Não são permitidos valores NULL em atributos utilizados em operações de consulta.  
Criação de índices para otimização de consultas.  
Dados monetários foram tratados como DECIMAL para melhor precisão durante os cálculos.  
Datas completa foram armazenadas como DATE enquanto anos foram armazenados como YEAR, preservando sua semântica.  
Criar tabelas:  
```
mysql -u root -o < teste3/setup.sql
```

### Importação dos dados dos arquivos:
Queries para popular a base de dados com os dados importados dos arquivos CSVs.  
Esses dados foram previamente tratados nos outros processos, evitando valores null em campos obrigatórios.  
Strings em campos numéricos e datas são convertidos pela linguagem.  
Popular base de dados:  
```
mysql -u root -o < teste3/load_data.sql
```

### Queries Analíticas:
Foram desenvolvidas as seguintes consultas:
  - <p align="justify">As 5 operadoras com maior crescimento percentual entre o primeiro e o último trimestre - é obtido utilizando os valores apenas das operadoras que possuem valores no primeiro e último semestre da análise:  </p>
  
    ```
    mysql -u root -o < teste3/query1.sql
    ```
    
  - As 5 UF com maiores valores de despesas totais junto a sua média gasta por operadora:  
    ```
    mysql -u root -o < teste3/query2.sql
    ```
    
  - <p align="justify">Quantas operadoras tiveram despesas acima da média geral em pelo menos 2 trimestres - é calculado a média geral de cada trimestre e então adicionadas em uma tabela auxiliar as operadoras que tiveram despesas acima desse valor para cada trimestre. Ao final, as operadoras que tiveram duas ou mais entradas na tabela são adicionadas a contagem:  </p>
  
     ```
    mysql -u root -o < teste3/query3.sql
     ```

## Teste 4 - API e Interface Web
Criação de API com back-end em Python/FastAPI e interface front-end web com Vue.js.
### Back-end
A API possui as seguintes rotas:
- `GET /api/operadoras` - listar todas as operadoras com paginação;
- `GET /api/operadoras/{cnpj}` - retornar detalhes de uma operadora específica;
- `GET /api/operadoras/{cnpj}/despesas` - retornar histórico de despesas de um operadora específica;
- `GET /api/estatisticas` - retornar estatísticas agregadas(total de despesas, média, top 5 operadoras).

Importar coleção de rotas para o Postman utilizando o arquivo:
`postman.json` 

<p align="justify">Foi escolhido o FastAPI por ser um framework moderno focado no desenvolvimento de APIs REST, que oferece uma boa performance e documentação automática. Por conta do pequeno escopo deste projeto, sua implementação foi simples e garante uma fácil leitura e manutenibilidade do código.  </p>
  
A estratégia de paginação adotada foi a de Offset-based, por ser atender adequadamente o volume de dados do projeto de maneira satisfátoria sem adicionar complexidade desnecessária ao projeto.  
  
<p align="justify">A rota de estatísticas, no momento atual, é calculada a cada requisição, de modo a simplificar sua implementação inicial, atendendo aos requisitos do sistema considerando o baixo fluxo de acesso e o volume de dados. Espera-se que, por se tratarem de dados com praticamente nenhuma atualização, esses valores sejam futuramente pré-calculados e armazenados no servidor.  </p>
  
As respostas da API são compostas pelos seu dados e metadados, de modo a facilitar sua legibilidade e seu uso dentro do front-end.  
  
Iniciar servidor back-end e acessar documentação:  
 ```
 uvicorn teste4.backend.main:app --reload
 http://localhost:8000/docs
 ```

### Front-end
<p align="justify">Como estratégia de Busca e Filtro foi escolhida a opção de Busca no Servidor, uma vez que o front-end trabalha com dados paginados e não possui acesso à base completa. Dentro do escopo do projeto, essa decisão não trouxe impactos negativos à experiência do usuário.</p>
  
Para o gerenciamento de estado foi adotada a utilização de props e eventos simples por se tratar de uma aplicação de pequeno porte e complexidade, mantendo o código simples e de fácil leitura.  
  
Erros são tratados por meio de captura de exceções, mostrando mensagens genéricas ao usuário enquanto registra os detalhes técnicos no console. Assim é evitado mostrar detalhes internos do sistema ao cliente.  
  
Estados de loading oferecem um indicar visual ao usuário de modo a evitar a sensação de travamento da página e melhorar sua experiência.  
  
Dados vazios retornam uma mensagem informativa ao usuário indicando que a requisição foi bem-sucedida mas não retornou resultados.  
  
Iniciar e acessar interface front-end:  
  ```
 python -m http.server 5500
 http://localhost:5500/teste4/frontend/
  ```



