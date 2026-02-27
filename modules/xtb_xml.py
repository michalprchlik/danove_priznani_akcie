import logging
import zipfile
import os


def get_xls_file_list(directory_path):

    zip_files = list_zip_files(directory_path)

    logging.info(f"Seznam zip souboru: {zip_files}")

    # Priklad pouziti
    zip_file = directory_path + "/" + zip_files[0]  # zadejte cestu k zip souboru
    extract_folder = "files"  # zadejte adresar pro rozbaleni
    os.makedirs(extract_folder, exist_ok=True)  # Vytvoreni adresare, pokud neexistuje

    xls_file_list = extract_xls_from_zip(zip_file, extract_folder)
    logging.info(f"Seznam XLS souboru: {xls_file_list}")

    logging.info("--------------------------------")

    return xls_file_list


def list_zip_files(directory):
    # Ziskani seznamu zip souboru v zadanem adresari
    zip_files = [file for file in os.listdir(directory) if file.endswith(".zip")]
    return zip_files


def extract_xls_from_zip(zip_file_path, extract_to_folder):
    # Nacteni zip souboru
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        # Rozbaleni obsahu
        zip_ref.extractall(extract_to_folder)

        # Ziskani seznamu XLS souboru, vcetne podadresaru
        xls_files = []
        for root, dirs, files in os.walk(extract_to_folder):
            for file in files:
                if file.endswith(".xlsx"):
                    xls_files.append(os.path.join(root, file))

    return xls_files
