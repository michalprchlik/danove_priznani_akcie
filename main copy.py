#!/usr/bin/env python3

import logging

from functions_framework import http

from run import run

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format="[%(levelname)s %(filename)s, %(lineno)d] %(message)s",
)


@http
def main(request):
    try:
        request_json = request.get_json(silent=True)

        run(request_json)
        return "OK", 200

    except Exception as exception:  # pylint: disable=broad-except
        logging.exception("Got an exception")
        return "Exception", 500
