import logging
import re


def get_item(sheet_data, base_currency):
    item = {}

    if sheet_data[0] == "Dividend":
        item["type"] = "dividend"
        item["value"] = float(sheet_data[3])
        item["base_currency"] = base_currency

        text = sheet_data[5]
        # Regulární výraz pro extrakci klíče
        # GOOGC.US USD 0.2000/ SHR
        pattern = r"^[a-z\s]*[A-Z\d]+\.([A-Z]+)"

        match = re.search(pattern, text)
        # logging.info(text)

        item["country"] = match.group(1)

    elif sheet_data[0] == "Withholding tax":
        # GOOGC.US USD WHT 15%
        # Nastavení sazby a přičtení daně
        item["type"] = "tax"
        item["tax_rate"] = get_tax_rate(sheet_data)
        item["value"] = abs(float(sheet_data[3]))
        item["base_currency"] = base_currency

        text = sheet_data[5]
        pattern = r"^[a-z\s]*[A-Z\d]+\.([A-Z]+)"

        match = re.search(pattern, text)
        # logging.info(text)

        item["country"] = match.group(1)

    else:
        raise Exception

    return item


def get_tax_rate(row):

    pattern = r"(\d+)%$"
    tax_rate = 0

    # Hledání vzoru v textu
    match = re.search(pattern, row[5])

    if match:
        tax_rate = int(match.group(1))  # Výběr první skupiny jako celé číslo
        # logging.info("Extrahovaná sazba daně:", tax_rate)
    else:
        logging.info(f"Sazba daně nebyla nalezena: {row[5]}")

    return tax_rate
