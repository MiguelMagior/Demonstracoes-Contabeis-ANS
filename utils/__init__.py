import io
import os
import shutil
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
import requests


def list_files_http(base_url):
    files = []
    response = requests.get(base_url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                files.append(base_url + href)
        except Exception as e:
            print(f" Exceção: {e}")
    return files


def create_zip(file_path, zip_name, output_dir=".."):
    if not os.path.exists(file_path):
        print(f" Error - File not found: {file_path}")
        return False
    try:
        shutil.make_archive(base_name=str(Path(output_dir) / zip_name),
                            format='zip',
                            base_dir=file_path,
                            )
    except Exception as e:
        print(f" Exceção - Criando arquivo zip: {e}")


def download_file(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        downloaded_file_data = io.BytesIO(response.content)

        print(f" Download: {os.path.basename(url)}")
        return downloaded_file_data
    except Exception as e:
        print(f" Exceção - Baixando {url}: {e}")
    return None

def cnpj_is_valid(cnpj):
    if pd.isna(cnpj):
        return False

    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False

    base_digits1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    base_digits2 = [6] + base_digits1

    total_sum = sum(int(cnpj[i]) * base_digits1[i] for i in range(12))
    final_digit1 = 11 - (total_sum % 11)
    if final_digit1 > 9:
        final_digit1 = 0
    if final_digit1 != int(cnpj[12]):
        return False

    total_sum = sum(int(cnpj[i]) * (base_digits2[i]) for i in range(13))
    final_digit2 = 11 - (total_sum % 11)
    if final_digit2 > 9:
        final_digit2 = 0
    if final_digit2 != int(cnpj[13]):
        return False

    return True