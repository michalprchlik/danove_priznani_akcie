import logging


def get_current_price(data_ote, now):

    data_price_transformed = transform_data_ote(data_ote)
    current_hour = get_current_hour(now)

    current_price = get_current_price_from_data_price(data_price_transformed, current_hour)

    return current_price


def transform_data_ote(data_ote):
    data_price = get_data_price(data_ote)
    data_price_transformed = transform_data_price(data_price)

    return data_price_transformed


def get_current_hour(now):

    current_hour = now.hour

    logging.info(f"current_hour={current_hour}")

    return current_hour


def get_current_price_from_data_price(data_price_transformed, current_hour):

    current_price = data_price_transformed[current_hour]
    logging.info(f"current_price={current_price}")

    return current_price


def get_data_price(data_ote):
    data_price = {}
    for item in data_ote["data"]["dataLine"]:
        if item["title"] == "Cena (EUR/MWh)" or item["tooltip"] == "Cena":
            logging.info(item["point"])
            data_price = item["point"]

    return data_price


def transform_data_price(data_price):
    data_price_transformed = {}

    for item in data_price:
        key = int(item["x"])
        value = item["y"]
        data_price_transformed[key] = value

    logging.info(f"data_price_transformed={data_price_transformed}")

    return data_price_transformed
