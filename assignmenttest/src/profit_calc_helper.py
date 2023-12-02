from assignmenttest.src.config import MF_BASE_URL
import requests
import random
from datetime import datetime

class ProfitCalcHelper(object):
    def __init__(self):
        self.mf_url = MF_BASE_URL

    def get_random_mf_scheme_code(self, qty=1):
        mf_scheme_rs = requests.get(self.mf_url)
        random_mf_scheme = random.sample(mf_scheme_rs.json(), int(qty))
        scheme_code = random_mf_scheme[0]['schemeCode']

        return scheme_code

    def get_single_mf_scheme_data(self, scheme_code):
        mf_scheme_data_rs = requests.get(f"{self.mf_url}/{scheme_code}")
        mf_scheme_data_rs_json = mf_scheme_data_rs.json()

        return mf_scheme_data_rs_json

    def get_start_and_end_date(self, scheme_code):
        single_scheme_details = self.get_single_mf_scheme_data(scheme_code)
        assert len(single_scheme_details['data']) > 2, f"This scheme has not enough data to calculate NAV "

        random_mf_scheme_data = random.sample(single_scheme_details['data'], 2)

        # Convert date strings to datetime objects
        date_objects = [datetime.strptime(entry['date'], "%d-%m-%Y") for entry in random_mf_scheme_data]

        # Find the greater date
        _start_date = min(date_objects)
        _end_date = max(date_objects)

        start_date = _start_date.strftime('%d-%m-%Y')
        end_date = _end_date.strftime('%d-%m-%Y')

        _data = {
            "start_date": start_date,
            "end_date": end_date,
            "related_mf_data": random_mf_scheme_data
        }
        return _data

class CreateProfitCalcQueryParams(object):
    def __init__(self):
        self.profit_calc_helper = ProfitCalcHelper()

    def create_profit_calc_query_params(self):

        scheme_code = self.profit_calc_helper.get_random_mf_scheme_code()
        _data = self.profit_calc_helper.get_start_and_end_date(scheme_code)
        start_date = _data['start_date']
        end_date = _data['end_date']
        capital = 1000000

        related_mf_data = _data['related_mf_data']

        query_params = {
            "scheme_code": scheme_code,
            "start_date": start_date,
            "end_date": end_date,
            "capital": capital,
            "related_mf_data": related_mf_data
        }

        return query_params

class CalculateNetProfit(object):

    def calculate_net_profit(self, start_date, end_date, capital, related_mf_scheme_data):

        nav_on_purchase_date = [float(data['nav']) for data in related_mf_scheme_data if data['date'] == start_date][0]
        nav_on_redemption_date = [float(data['nav']) for data in related_mf_scheme_data if data['date'] == end_date][0]

        _purchase_day_value = capital / nav_on_purchase_date
        purchase_day_value = round(_purchase_day_value, 2)

        _redemption_day_value = purchase_day_value * nav_on_redemption_date
        redemption_day_value = round(_redemption_day_value, 2)

        _net_profit = redemption_day_value - capital
        net_profit = round(_net_profit, 2)

        return net_profit


