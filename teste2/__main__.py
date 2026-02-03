import os
import pandas as pd
from utils import cnpj_is_valid, download_file, create_zip


def validate_data(csv_path):
    try:
        consolidated_csv = pd.read_csv(
            csv_path,
            sep=';',
            encoding='utf-8',
            decimal='.',
            dtype={"CNPJ": str, "ValorDespesas": float}
        )

        mask_cnpj = consolidated_csv['CNPJ'].apply(cnpj_is_valid)
        mask_value = (
                consolidated_csv['ValorDespesas'].notna() &
                (consolidated_csv['ValorDespesas'] > 0)
        )
        mask_razao = consolidated_csv['RazaoSocial'].notna()

        mask_valid = mask_cnpj & mask_value & mask_razao

        valid_data = consolidated_csv[mask_valid]
        invalid_data = consolidated_csv[~mask_valid]

        invalid_data.to_csv("data/quarentena_invalidos.csv", sep=';', encoding='utf-8', index=False)

        print(f" Quarentena: {len(invalid_data)} entradas movidas")
        return valid_data
    except FileNotFoundError:
        print(" Erro - Arquivo base não existe")
    except Exception as e:
        print(f" Exceção - Validando dados: {e}")


def merge_csv(data_frame):
    try:
        if 'operadoras.csv' not in os.listdir("data"):
            companies_csv = download_file(
                "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv")
            with open('data/operadoras.csv', 'wb') as f:
                f.write(companies_csv.read())
        companies_data = pd.read_csv('data/operadoras.csv',
                                     sep=';',
                                     encoding='utf-8',
                                     usecols=["CNPJ", "REGISTRO_OPERADORA", "Modalidade", "UF"],
                                     dtype={"CNPJ": str, "Registro_ANS": str})

        data_frame = data_frame.merge(companies_data, on="CNPJ", how="left")
        data_frame.rename(columns={"REGISTRO_OPERADORA": "RegistroANS"}, inplace=True)
    except Exception as e:
        print(f" Exceção - Join CSVs: {e}")
    return data_frame


def group_csv(data_frame):
    try:
        data_frame["MediaValorTrimestral"] = data_frame.groupby(["UF", "RazaoSocial", "Trimestre"])[
            "ValorDespesas"].transform("mean").round(2)
        data_frame["DesvioPadraoTrimestral"] = data_frame.groupby(["UF", "RazaoSocial", "Trimestre"])[
            "ValorDespesas"].transform("std").round(2)
        grouped_data_frame = data_frame.groupby(
            ["UF", "RazaoSocial", "Trimestre"],
            as_index=False).agg({
            "Ano": "first",
            "CNPJ": "first",
            "RegistroANS": "first",
            "Modalidade": "first",
            "ValorDespesas": "sum",
            "MediaValorTrimestral": "first",
            "DesvioPadraoTrimestral": "first"
        })
        grouped_data_frame.sort_values('ValorDespesas', ascending=False, inplace=True)
        return grouped_data_frame
    except Exception as e:
        print(f" Exceção - Agrupando CSVs: {e}")


def main():
    try:
        valid_data = validate_data("data/consolidado_despesas.csv")
        merged_data = merge_csv(valid_data)
        grouped_data = group_csv(merged_data)
        grouped_data.to_csv("data/despesas_agregadas.csv", sep=';', encoding='utf-8', index=False)
        create_zip(file_path="data/despesas_agregadas.csv", zip_name="Teste_Miguel_Magior")
        print(f" Criado ZIP: Teste_Miguel_Magior.zip")
    except Exception as e:
        print(f" Exceção - Criando Arquivo: {e}")


if __name__ == "__main__":
    main()
