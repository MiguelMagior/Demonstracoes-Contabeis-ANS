import os
import re
import zipfile
import pandas as pd
from Utils import create_zip, list_files_http, download_file


def extract_csv_from_zip(zip_list):
    extracted_data = []
    for file in zip_list:
        try:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                for csv_file in zip_ref.namelist():
                    with zip_ref.open(csv_file) as f:
                        data_frame = pd.read_csv(f,
                                                 sep=';',
                                                 encoding='utf-8',
                                                 usecols=["REG_ANS", "DESCRICAO", "VL_SALDO_FINAL"],
                                                 decimal=",")
                        extracted_data.append((csv_file, data_frame))

            print(f" Extracted {csv_file}")
        except Exception as e:
            print(f" Exception - Extracting ZIP file: {e}")

    return extracted_data


def extract_date_from_name(file_name):
    pattern = re.compile(r'(\d)T(\d{4})', re.IGNORECASE)
    match = pattern.search(file_name)
    if match:
        quarter = match.group(1)
        year = match.group(2)
        return [quarter, year]
    return None, None


def process_csv(file):
    try:
        quarter, year = extract_date_from_name(file[0])
        data_frame = file[1]
        # filter EVENTOS/SINISTROS
        data_frame = data_frame[data_frame["DESCRICAO"].str.contains(r"eventos|sinistros", na=False, regex=True, case=False)]
        data_frame.drop(columns=["DESCRICAO"], inplace=True)

        # correct negative values
        data_frame["VL_SALDO_FINAL"] = data_frame["VL_SALDO_FINAL"].abs()

        data_frame["Trimestre"] = quarter
        data_frame["Ano"] = year

        data_frame.rename(columns={"VL_SALDO_FINAL": "ValorDespesas"}, inplace=True)
        data_frame.drop_duplicates(inplace=True)
        print(f" Processed {file[0]}")
        return data_frame
    except Exception as e:
        print(f" Exception - Processing CSV: {e}")
    return None

def merge_csv(csv_base):
    #add CNPJ/RAZAO SOCIAL
    try:
        operators_csv = download_file("https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv")
        operators_data = pd.read_csv(operators_csv,
                    sep=';',
                    encoding='utf-8',
                    usecols=["REGISTRO_OPERADORA", "CNPJ", "Razao_Social"],
                                     dtype={"CNPJ": str})
        csv_base.rename(columns={"REG_ANS": "REGISTRO_OPERADORA"}, inplace=True)
        csv_base = csv_base.merge(operators_data, on="REGISTRO_OPERADORA", how="left")
        csv_base.drop(columns=["REGISTRO_OPERADORA"], inplace=True)
        csv_base.rename(columns={"Razao_Social": "RazaoSocial"}, inplace=True)
        csv_base = csv_base[["CNPJ", "RazaoSocial", "Trimestre", "Ano", "ValorDespesas"]]
    except Exception as e:
        print(f" Exception - Joining CSV: {e}")
    return csv_base


def concat_csv(data_list):
    data_frames = []
    try:
        for data_frame in data_list:
            data_frames.append(data_frame)
        return pd.concat(data_frames, ignore_index=True)
    except Exception as e:
        print(f" Exception - Concatenating CSV: {e}")
    return data_frames


def main():
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    os.makedirs(os.path.dirname("../data"), exist_ok=True)

    url_list = list_files_http(base_url)
    url_list.pop()  # remove dictionary
    last_files_url = url_list[-1]
    last_three_files = list_files_http(last_files_url)[-3:]

    files = [download_file(file) for file in last_three_files]
    csv_files = extract_csv_from_zip(files)
    processed_csvs = [process_csv(file) for file in csv_files]
    concatened_csv = concat_csv(processed_csvs)
    merged_csv = merge_csv(concatened_csv)
    merged_csv.to_csv("../data/consolidado_despesas.csv", sep=';', encoding='utf-8', index=False)
    create_zip(file_path="../data/consolidado_despesas.csv", zip_name="consolidado_despesas")


if __name__ == "__main__":
    main()
