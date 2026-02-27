import logging
import re

from modules.xtb_xml import get_xls_file_list
from modules.xtb_sheet import get_sheet_data_list
from modules.xtb_item import get_item


def get_data_xtb(directory_path):

    result = []
    xml_file_list = get_xls_file_list(directory_path)

    for xml_file in xml_file_list:
        logging.info(f"filename={xml_file}")
        sheet_data_list = get_sheet_data_list(xml_file)
        base_currency = get_base_currency(xml_file)

        for sheet_data in sheet_data_list:
            item = get_item(sheet_data, base_currency)
            result.append(item)

    return result


def get_base_currency(xml_file):
    pattern = r"files/\d+/([A-Z\d]+)"

    match = re.search(pattern, xml_file)
    # logging.info(text)

    if match:
        base_currency = match.group(1)

    return base_currency
