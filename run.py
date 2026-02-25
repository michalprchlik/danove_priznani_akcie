import logging
import zipfile
import os
import pandas as pd
import re



from datetime import datetime, timedelta
from os import getenv

from ote import get_data_ote
from price import get_current_price
from solar_plant import handle_solar_plant
from modules.util.secret import access_secret_version
import warnings

# Ignore specific warnings
warnings.filterwarnings("ignore", category=UserWarning)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format="[%(levelname)s %(filename)s, %(lineno)d] %(message)s",
)


USD_CZK=100
EUR_CZK=100
GBP_CZK=100
CZK_CZK=100


def run(request_json):

    # nacist zip soubor
    # rozbalit
    # ziskat seznam souboru xls
    # nacist kazdy ze zipu a ulozit kazdy radek pod klicek MENA-TICKER-CASTKA
    # projit vsechny klice a udelat 1 radek pro kazdy klic
    # zapsat do csv

    # Priklad pouziti
    directory_path = 'files'  # zadejte cestu k adresari
    zip_files = list_zip_files(directory_path)

    print("Seznam zip souboru:", zip_files)

    # Priklad pouziti
    zip_file = directory_path + '/'+zip_files[0]  # zadejte cestu k zip souboru
    extract_folder = 'files'  # zadejte adresar pro rozbaleni
    os.makedirs(extract_folder, exist_ok=True)  # Vytvoreni adresare, pokud neexistuje

    xls_files = extract_xls_from_zip(zip_file, extract_folder)
    print("Seznam XLS souboru:", xls_files)

    value_list = ['Withholding tax', 'Dividend',] 

    data = {}

    for file in xls_files:
        # files/50878198/USD_50878198_2024-12-31_2025-12-31.xlsx
        # -> USD
        pattern = r'files/\d+/([A-Z\d]+)'

        match = re.search(pattern, file)
        # print(text)

        if match:
            base_currency = match.group(1)
            print(base_currency)

            print(f'-----------------------------{file}')        
            cash_data = read_cash_operations_sheet(file)

            if cash_data is not None:
                data = parse_xml_file(cash_data,value_list, data)


    # print(data)

def list_zip_files(directory):
    # Ziskani seznamu zip souboru v zadanem adresari
    zip_files = [file for file in os.listdir(directory) if file.endswith('.zip')]
    return zip_files



def extract_xls_from_zip(zip_file_path, extract_to_folder):
    # Nacteni zip souboru
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Rozbaleni obsahu
        zip_ref.extractall(extract_to_folder)
        
        # Ziskani seznamu XLS souboru, vcetne podadresaru
        xls_files = []
        for root, dirs, files in os.walk(extract_to_folder):
            for file in files:
                if file.endswith('.xlsx'):
                    xls_files.append(os.path.join(root, file))
    
    return xls_files


def read_cash_operations_sheet(xls_file_path):
    # Otevrit xls soubor
    try:
        xls = pd.ExcelFile(xls_file_path)

        # print(xls.sheet_names)

        sheet_name = 'Cash Operations'
        
        # Ziskat data ze zalozky "Cash operation"
        if sheet_name in xls.sheet_names:
            cash_operation_data = pd.read_excel(xls, sheet_name=sheet_name)
            return cash_operation_data
        else:
            print(f"Zalozka '{sheet_name}' nenalezena v souboru.")
            return None
    except Exception as e:
        print(f"Nastala chyba pri cteni souboru: {e}")
        return None


def filter_rows_by_values(dataframe, column_index, values):
    # Projit datovy ramec a filtracni hodnoty
    filtered_rows = dataframe[dataframe.iloc[:, column_index].isin(values)]
    return filtered_rows


def parse_xml_file(cash_data, value_list, data):
    # print(cash_data)

    result = filter_rows_by_values(cash_data, 0, value_list)
    list_of_rows = result.values.tolist()
    # print(list_of_rows)

    for row in list_of_rows:
        key = get_key(row)

        if key == 'DE-GBP':
            print(row)

        if key not in data:
            data[key] = {
                'tax_rate': 0,
                'dividend': 0,
                'tax': 0,
            }

        data = update_data(row, data, key)

    print(data)
    

    return data



def get_key(row):

    text = row[5]
    # Regulární výraz pro extrakci klíče
    pattern = r'[A-Z\d]+\.([A-Z]+)\s+([A-Z]{3})'

    match = re.search(pattern, text)
    # print(text)

    if match:
        # Vytvoření klíče ve tvaru MONET.CZ-CZK
        key = f"{match.group(1)}-{match.group(2)}"
        # print("Extrahovaný klíč:", key)
    else:
        key = ''
        # print(f"Žádný klíč nebyl nalezen: {text}")

    return key


def update_data(row, data, key):

    if row[0] == 'Dividend':
        # Přičtení částky k dividendě
        data[key]['dividend'] += float(row[3])
    elif row[0] == 'Withholding tax':
        # Nastavení sazby a přičtení daně
        data[key]['tax_rate'] = get_tax_rate(row)
        data[key]['tax'] += float(row[3])

    return data


def get_tax_rate(row):

    pattern = r'(\d+)%$'
    tax_rate = 0

    # Hledání vzoru v textu
    match = re.search(pattern, row[5])

    if match:
        tax_rate = int(match.group(1))  # Výběr první skupiny jako celé číslo
        # print("Extrahovaná sazba daně:", tax_rate)
    else:
        print(f"Sazba daně nebyla nalezena: {row[5]}")    
        pass

    return tax_rate


if __name__ == "__main__":
    request_json = {
        'is_local': True,
    }

    run(request_json)
