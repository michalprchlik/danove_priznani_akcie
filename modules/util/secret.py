import json
import logging

from google.cloud.secretmanager import SecretManagerServiceClient
import google_crc32c

if "unittest.util" in __import__("sys").modules:
    logging.disable(logging.CRITICAL)


# returns json
def get_secret(project_id, secret_id, version_id):
    """
    https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#access
    """

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    client = SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")
    json_response = json.loads(payload)

    return json_response


# returns plain value - for etherscan and bscscan
def access_secret_version(project_id, secret_id, version_id):
    """
    https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#access
    """

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    client = SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": name})

    is_testing = "unittest.util" in __import__("sys").modules
    if not is_testing:
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            logging.error("Data corruption detected.")
            return response

    payload = response.payload.data.decode("UTF-8")

    return payload
