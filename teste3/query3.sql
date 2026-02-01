-- QUANTITY OF COMPANIES WITH AT LEAST 2 QUARTERLY EXPENSES ABOVE THE AVERAGE
WITH QuarterAverage AS (
    SELECT
        trimestre,
        ano,
        AVG(valor) AS general_average
    FROM DespesasConsolidadas
    GROUP BY trimestre, ano
),
AboveAvarage AS (
    SELECT
        d.cnpj,
        d.trimestre,
        d.ano
    FROM DespesasConsolidadas d
    JOIN QuarterAverage m
        ON d.trimestre = m.trimestre
       AND d.ano = m.ano
    WHERE d.valor > m.general_average
)
SELECT COUNT(*) AS "Quantidade Operadoras"
FROM (
    SELECT cnpj
    FROM AboveAvarage
    GROUP BY cnpj
    HAVING COUNT(*) >= 2
) t;
