import io
import os
import shutil
from pathlib import Path
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
            print(f" Exception - {e}")
    return files


def create_zip(file_path, zip_name, output_dir=".."):
    if not os.path.exists(file_path):
        print(f" Error - File not found: {file_path}")
        return False
    try:
        shutil.make_archive(base_name=str(Path(output_dir) / zip_name),
                            format='zip',
                            base_dir=file_path)
    except Exception as e:
        print(f" Exception - Creating zip: {e}")


def download_files(url_list):
    files = []
    for url in url_list:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            downloaded_file_data = io.BytesIO(response.content)  # Tudo de uma vez

            downloaded_file_data.seek(0)
            files.append(downloaded_file_data)
            print(f" Downloaded {os.path.basename(url)}")

        except Exception as e:
            print(f" Exception - Downloading {url}: {e}")
    return files
