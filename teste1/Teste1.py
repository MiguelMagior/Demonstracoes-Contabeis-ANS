import os
import re
import zipfile
import pandas as pd
from Utils import create_zip, list_files_http, download_files


def extract_csv_from_zip(zip_list):
    extracted_data = []
    for file in zip_list:
        try:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                for csv_file in zip_ref.namelist():
                    with zip_ref.open(csv_file) as f:
                        # Lê e guarda o DataFrame (não o arquivo)
                        data_frame = pd.read_csv(f,
                                                 sep=';',
                                                 encoding='utf-8',
                                                 usecols=["REG_ANS", "DESCRICAO", "VL_SALDO_FINAL"],
                                                 decimal=",")
                        extracted_data.append((csv_file, data_frame))

            print(f" Extracted {csv_file}")
            file.close()
            del file
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


def process_csv(csv_file):
    try:
        quarter, year = extract_date_from_name(csv_file[0])
        data_frame = csv_file[1]
        # filter EVENTOS/SINISTROS
        data_frame = data_frame[data_frame["DESCRICAO"].str.contains("EVENTOS|SINITROS", na=False, regex=True)]
        data_frame.drop(columns=["DESCRICAO"], inplace=True)

        # correct negative values
        data_frame["VL_SALDO_FINAL"] = data_frame["VL_SALDO_FINAL"].abs()

        data_frame["Trimestre"] = quarter
        data_frame["Ano"] = year

        data_frame.rename(columns={"VL_SALDO_FINAL": "ValorDespesas"}, inplace=True)

        print(f" Processed {csv_file[0]}")
        return data_frame
    except Exception as e:
        print(f" Exception - Processing CSV: {e}")
    return None


def concat_csv(data_list):
    data_frames = []
    try:
        for data in data_list:
            data_frame = process_csv(data)
            if not data_frame.empty:
                data_frames.append(data_frame)
        if data_frames:
            return pd.concat(data_frames, ignore_index=True)
    except Exception as e:
        print(f" Exception - Concatenating CSV: {e}")
    return None


def main():
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    os.makedirs(os.path.dirname("data"), exist_ok=True)
    try:
        directories = list_files_http(base_url)
        directories.pop()  # remove dictionary
        last_files_path = directories[-1]
        last_three_files = list_files_http(last_files_path)[-3:]
        files = download_files(last_three_files)
        csv_files = extract_csv_from_zip(files)
        concat_csv(csv_files).to_csv("../data/consolidado_despesas.csv", sep=';', encoding='utf-8', index=False)
        create_zip(file_path="../data/consolidado_despesas.csv", zip_name="consolidado_despesas")
    except Exception as e:
        print(f" Exception - Main execution: {e}")


if __name__ == "__main__":
    main()
