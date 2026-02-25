from unittest.mock import patch


import unittest

from modules.util.secret import get_secret


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999  # pylint: disable=protected-access


class GetSecret(unittest.TestCase):
    @patch("modules.util.secret.SecretManagerServiceClient")
    def test(self, mock_secret_manager):
        mock_secret_manager.return_value.access_secret_version.return_value.payload.data = b'{"super_secret_token": "1"}'

        project_id = "project_id"  # nosec 259
        secret_id = "secret_id"  # nosec 259
        version_id = "latest"  # nosec 259

        result = get_secret(project_id, secret_id, version_id)
        expected_result = {"super_secret_token": "1"}

        self.assertTrue(result, expected_result)
        self.assertTrue(mock_secret_manager.called)
