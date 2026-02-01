-- TOP 5 STATES WITH HIGHEST EXPENSES
SELECT
    o.uf as "UF",
    FORMAT(SUM(d.valor), 2, 'de_DE') as "Total Despesas($)",
    FORMAT(AVG(d.valor), 2, 'de_DE') as "Média Despesas Operadora($)"
FROM DespesasConsolidadas d
    INNER JOIN Operadoras o
    ON d.cnpj = o.cnpj
GROUP BY o.uf
ORDER BY SUM(d.valor) DESC
LIMIT 5;