import logging
import warnings

from modules.xtb import get_data_xtb

# Ignore specific warnings
warnings.filterwarnings("ignore", category=UserWarning)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(filename)s %(lineno)d] %(message)s",
)

USD_CZK = 21.84
EUR_CZK = 24.66
CZK_CZK = 1


def run(request_json):

    # nacist zip soubor
    # rozbalit
    # ziskat seznam souboru xls
    # nacist kazdy ze zipu a ulozit kazdy radek pod klicek MENA-TICKER-CASTKA
    # projit vsechny klice a udelat 1 radek pro kazdy klic
    # zapsat do csv

    # Priklad pouziti
    directory_path = "files"  # zadejte cestu k adresari

    data_xtb = get_data_xtb(directory_path)

    logging.info("--------------------------------")
    data = convert_currency_to_czk(data_xtb)
    get_final_result(data)

    # logging.info(data)


def convert_currency_to_czk(data_xtb):
    result = {}
    for values in data_xtb:
        if values["base_currency"] == "EUR":
            value = values["value"] * EUR_CZK
        elif values["base_currency"] == "USD":
            value = values["value"] * USD_CZK
        elif values["base_currency"] == "CZK":
            value = values["value"] * CZK_CZK
        else:
            logging.info(f"unknown currency: {values['base_currency']}")
            exit(1)

        if values["country"] not in result:
            result[values["country"]] = {
                "dividend": 0,
                "tax": 0,
            }

        if values["type"] == "tax":
            result[values["country"]]["tax"] += value
        else:
            result[values["country"]]["dividend"] += value

        # print(result)

    return result


def get_final_result(result):

    dividend_total = 0
    to_pay_total = 0

    for country, value in result.items():
        to_pay = value["dividend"] / 100 * 15

        if to_pay > value["tax"]:
            to_pay = to_pay - value["tax"]

        else:
            to_pay = 0

        dividend = round(value["dividend"])
        tax = round(value["tax"])
        to_pay = round(to_pay)

        dividend_total += dividend - tax
        to_pay_total += to_pay

        logging.info(f"country={country}, dividend={dividend}, tax={tax}, to_pay={to_pay}")

    dividend_total = dividend_total - to_pay_total

    logging.info("--------------------------------")
    logging.info(f"dividend_total={dividend_total}, to_pay_total={to_pay_total}")


if __name__ == "__main__":
    request_json = {
        "is_local": True,
    }

    run(request_json)
