import pandas as pd

from Utils import cnpj_is_valid

try:
    consolidated_csv = pd.read_csv(
        "../data/consolidado_despesas.csv",
        sep=';',
        encoding='utf-8',
        decimal='.',
        dtype={"CNPJ": str, "ValorDespesas": float}
    )

    invalid_cnpjs = consolidated_csv[
        ~consolidated_csv["CNPJ"].apply(cnpj_is_valid)
    ]["CNPJ"]

    for cnpj in invalid_cnpjs:
        print(f"{cnpj} CNPJ invalido")

    print(f"Total de CNPJs inválidos: {len(invalid_cnpjs)}")

except FileNotFoundError:
    print(" Error - Base file dont exist")
except Exception as e:
    print(f" Error: {e}")

