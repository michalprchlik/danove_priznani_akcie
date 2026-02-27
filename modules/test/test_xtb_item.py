import unittest
import datetime


from modules.xtb_item import get_item


class GetItem1(unittest.TestCase):
    def test(self):
        sheet_data = [
            "Dividend",
            "Kraft Heinz",
            datetime.datetime(2025, 6, 27, 9, 42, 2, 99000),
            2,
            "854996111",
            "KHC.US USD 0.4000/ SHR",
            "My Trades",
        ]
        base_currency = "CZK"

        result = get_item(sheet_data, base_currency)
        expected_result = {
            "type": "dividend",
            "value": 2.0,
            "base_currency": "CZK",
            "country": "US",
        }

        self.assertEqual(result, expected_result)


class GetItem2(unittest.TestCase):
    def test(self):
        sheet_data = [
            "Withholding tax",
            "Alphabet",
            datetime.datetime(2025, 6, 16, 9, 45, 3, 743000),
            -0.09,
            "843256836",
            "GOOGC.US USD WHT 15%",
            "My Trades",
        ]
        base_currency = "CZK"

        result = get_item(sheet_data, base_currency)
        expected_result = {
            "type": "tax",
            "tax_rate": 15,
            "value": 0.09,
            "country": "US",
            "base_currency": "CZK",
        }

        self.assertEqual(result, expected_result)


class GetItem3(unittest.TestCase):
    def test(self):
        sheet_data = [
            "Dividend",
            "TSMC",
            datetime.datetime(2025, 6, 13, 9, 16, 54, 614000),
            -2.26,
            "840826531",
            "corr TSM.US USD 0.7520/ SHR",
            "My Trades",
        ]
        base_currency = "CZK"

        result = get_item(sheet_data, base_currency)
        expected_result = {
            "type": "dividend",
            "value": -2.26,
            "base_currency": "CZK",
            "country": "US",
        }

        self.assertEqual(result, expected_result)


class GetItem4(unittest.TestCase):
    def test(self):
        sheet_data = [
            "Withholding tax",
            "TSMC",
            datetime.datetime(2025, 6, 12, 15, 5, 33, 906000),
            0.47,
            "839644109",
            "corr TSM.US USD WHT 21%",
            "My Trades",
        ]
        base_currency = "CZK"

        result = get_item(sheet_data, base_currency)
        expected_result = {
            "type": "tax",
            "tax_rate": 21,
            "value": 0.47,
            "base_currency": "CZK",
            "country": "US",
        }

        self.assertEqual(result, expected_result)
