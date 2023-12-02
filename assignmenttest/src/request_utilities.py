import pdb

from assignmenttest.src.config import API_HOST
import requests

class RequestUtility(object):
    def __init__(self):
        self.url = None
        self.res_status_code = None
        self.expected_status_code = None
        self.api_res_json = None
        self.api_base_url = API_HOST

    def assert_status_code(self):

        assert self.res_status_code == self.expected_status_code, \
            f"Bad status code, "\
            f"Expected status code: {self.expected_status_code}, "\
            f"Actual status code: {self.res_status_code}, "\
            f"URL:{self.url}, "\
            f"Response json: {self.api_res_json}"

    def get(self, endpoint, params=None, payload=None, headers=None, expected_status_code=200):

        self.url = f"{self.api_base_url}{endpoint}"
        if params:
            self.url = f"{self.api_base_url}{endpoint}?{params}"

        api_res = requests.get(url=self.url)
        self.res_status_code = api_res.status_code
        self.expected_status_code = expected_status_code
        self.api_res_json = api_res.json()

        self.assert_status_code()

        return self.api_res_json
