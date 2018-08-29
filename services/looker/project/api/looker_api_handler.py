import requests
import json
import os
import pprint
from project.api.util import clean_invoice_json
from project.api.models import InvoicingByLibrary
# from project import create_app


class LookerApiHandler(object):
    def __init__(self, client_id: str, client_secret: str, endpoint: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token = None

        self.endpt = endpoint
        self.session = requests.session()

    def login(self):
        """Updates session with Looker token from given client credentials"""
        params = {"client_id": self._client_id,
                  "client_secret": self._client_secret}
        response = self.session.post("{}/login".format(self.endpt),
                                     params=params)
        self._token = response.json().get("access_token")
        self.session.headers.update(
            {"Authorization": "token {}".format(self._token)}
        )

    def run_look(self, look_id: str, result_format="json"):
        """Returns response from GET of specified look_id"""
        return self.session.get("{}/api/3.0/looks/{}/run/{}".format(
            self.endpt, look_id, result_format)
        )

    def logout(self):
        """Logout to revoke access token"""
        return self.session.delete("{}/api/3.0/logout".format(self.endpt))


def main():
    # app = create_app()
    # app.config.from_object("project.config.BaseConfig")

    # language = app.config["LANGUAGE"]

    sg_client_id = os.environ.get("LOOKER_CLIENT_ID")
    sg_client_secret = os.environ.get("LOOKER_CLIENT_SECRET")
    sg_endpoint = os.environ.get("SENDGRID_LOOKER")

    looker_api = LookerApiHandler(sg_client_id, sg_client_secret, sg_endpoint)
    looker_api.login()
    json_object = looker_api.run_look("4405").json()
    print(json_object)
    clean_json = []
    for j in json_object:
        c = clean_invoice_json(j, "email_send_month", "total_ei_revenue")
        clean_json.append(c)

    print(clean_json)
    looker_api.logout()
    return clean_json
