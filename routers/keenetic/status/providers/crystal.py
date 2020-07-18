import requests
from requests.exceptions import ConnectionError, HTTPError
from ...tools.logger import Logger


class CrystalISPParser:
    def __init__(self, username, password, output):
        self.__logger = Logger("CrystalISPParser", output)
        self.__logger.log("Initialized")
        self.data = {"name": "crystal"}
        try:
            auth = requests.post("https://api.prosto.net/auth", json={
                "login": username,
                "password": password,
            }).json()

            resp = requests.get("https://api.prosto.net/objects", headers={
                'Authorization': 'Bearer '+auth["token"]
            }).json()
            self.data['account_id'] = resp[0]["id"]
            self.data['balance'] = float(resp[0]["balance"])
            self.data['bonus'] = float(resp[0]["bonus"])
            self.data['payment_fee'] = float(resp[0]["fee_to_pay"])
            self.data['next_payment_fee'] = float(resp[0]["fee_next_month"])
            self.data['subscription'] = resp[0]["tariff"]["name"]
        except ConnectionError as e:
            self.__logger.warnerr(e)
            self.data["error"] = "connection"
        except HTTPError as e:
            self.__logger.warnerr(e)
            self.data["error"] = "http"
