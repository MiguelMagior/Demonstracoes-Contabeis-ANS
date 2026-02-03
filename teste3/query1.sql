-- TOP 5 COMPANIES WITH THE HIGHEST PERCENTAGE GROWTH IN EXPENSES AMONG THE FIRST AND LAST QUARTER
USE Despesas;

SET @first_year = (SELECT MIN(ano) FROM DespesasConsolidadas);
SET @first_quarter = (SELECT MIN(trimestre) FROM DespesasConsolidadas WHERE ano = @first_year);
SET @last_year = (SELECT MAX(ano) FROM DespesasConsolidadas);
SET @last_quarter = (SELECT MAX(trimestre) FROM DespesasConsolidadas WHERE ano = @last_year);

SELECT
    o.razao_social as "Operadora",
    FORMAT(initial.total_value, 2, 'de_DE') as "Despesa Inicial(R$)",
    FORMAT(final.total_value, 2,'de_DE') as "Despesa Final(R$)",
    CONCAT(
        ROUND(((final.total_value - initial.total_value) / initial.total_value) * 100, 2), '%'
    ) as "Crescimento(%)"

    FROM Operadoras o
        INNER JOIN (
            SELECT cnpj, SUM(valor) as total_value
            FROM DespesasConsolidadas
            WHERE ano = @first_year AND trimestre = @first_quarter
            GROUP BY cnpj
        ) initial
        ON o.cnpj = initial.cnpj
        INNER JOIN (
            SELECT cnpj, SUM(valor) as total_value
            FROM DespesasConsolidadas
            WHERE ano = @last_year AND trimestre = @last_quarter
            GROUP BY cnpj
        ) final
        ON o.cnpj = final.cnpj

ORDER BY ((final.total_value - initial.total_value) / initial.total_value) * 100 DESC
LIMIT 5;