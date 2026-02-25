import logging
import requests

from backoff import on_exception, constant


def get_data_ote(now):
    data = {}

    date_now = get_date_now(now)
    url = get_url(date_now)

    data = get_data_from_url(url)

    return data


@on_exception(constant, requests.exceptions.HTTPError, max_tries=10, interval=0.5)
def get_data_from_url(url):

    try:
        response = requests.get(url, timeout=10)

        json_data = response.json()
        logging.info(json_data)

    except requests.exceptions.Timeout as excetion:
        logging.info(f"requests.exceptions.Timeout, {excetion}")
        raise requests.exceptions.HTTPError

    except requests.exceptions.JSONDecodeError as excetion:
        logging.info(f"requests.exceptions.JSONDecodeError, {excetion}")
        raise requests.exceptions.HTTPError

    return json_data


def get_date_now(now):

    date_now = "2025-09-26"

    return date_now


def get_url(date_now):
    # https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date=2025-09-11

    url = f"https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date={date_now}"

    return url
