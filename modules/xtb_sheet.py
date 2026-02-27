import logging
import pandas as pd


def get_sheet_data_list(xml_file):

    value_list = [
        "Withholding tax",
        "Dividend",
    ]

    # files/50878198/USD_50878198_2024-12-31_2025-12-31.xlsx
    # -> USD
    cash_data_list = read_cash_operations_sheet(xml_file)

    if cash_data_list is not None:
        result = convert_panda_data_frame_to_list(cash_data_list, 0, value_list)
        list_of_rows = result.values.tolist()

    else:
        logging.error("No cash sheet found")

    return list_of_rows


def read_cash_operations_sheet(xls_file_path):
    # Otevrit xls soubor
    try:
        xls = pd.ExcelFile(xls_file_path)

        # logging.info(xls.sheet_names)

        sheet_name = "Cash Operations"

        # Ziskat data ze zalozky "Cash operation"
        if sheet_name in xls.sheet_names:
            cash_operation_data = pd.read_excel(xls, sheet_name=sheet_name)
            return cash_operation_data
        else:
            logging.info(f"Zalozka '{sheet_name}' nenalezena v souboru.")
            return None
    except Exception as e:
        logging.info(f"Nastala chyba pri cteni souboru: {e}")
        return None


def convert_panda_data_frame_to_list(cash_data_list, column_index, value_list):
    # Projit datovy ramec a filtracni hodnoty
    filtered_rows = cash_data_list[cash_data_list.iloc[:, column_index].isin(value_list)]
    return filtered_rows
