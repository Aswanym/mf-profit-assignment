from .exceptions import DateFormatException, InvalidMutualFundDateException, InvalidSchemeCodeException
from .config import MF_DATA_BASE_URL
from .utils import validate_date_format
from datetime import datetime, timedelta
import requests


class CalculateNetProfit:

    def calculate_profit(self, scheme_code, start_date, end_date, capital):

        given_dates = [start_date, end_date]

        # Validate date formats
        if not all(validate_date_format(date_str) for date_str in given_dates):
            raise DateFormatException

        url = f"{MF_DATA_BASE_URL}{scheme_code}"

        # call mutual fund data url
        rs_api = requests.get(url)
        rs_api_data = rs_api.json()['data']

        # if response api data is empty, something wrong with the scheme code, raise exception
        if not rs_api_data:
            raise InvalidSchemeCodeException

        # get list of all dates in a given MF scheme code.
        list_of_mf_dates = [data['date'] for data in rs_api_data]

        # check if start date is available in the list, else find next available date from the list
        if start_date not in list_of_mf_dates:
            start_date = self.find_next_available_date(start_date, list_of_mf_dates)

        # check if end date is available in the list, else find next available date from the list
        if end_date not in list_of_mf_dates:
            end_date = self.find_next_available_date(end_date, list_of_mf_dates)

        # loop through rs_api_data to get the nav associated with a given date
        nav_on_purchase_date = [float(data['nav']) for data in rs_api_data if data['date'] == start_date][0]
        nav_on_redemption_date = [float(data['nav']) for data in rs_api_data if data['date'] == end_date][0]

        # Calculate the number of units allotted on the purchase date: Initial investment / NAV on purchase date
        _purchase_day_value = capital / nav_on_purchase_date
        purchase_day_value = round(_purchase_day_value, 2)

        # Calculate the number of units allotted on the redemption date: Number of units allotted on purchase date * NAV on redemption date
        _redemption_day_value = purchase_day_value * nav_on_redemption_date
        redemption_day_value = round(_redemption_day_value, 2)

        # Calculate the net profit: Value on redemption date - Initial investment
        _net_profit = redemption_day_value - capital
        net_profit = round(_net_profit, 2)

        return {"message": "success", "net_profit": net_profit}

    @staticmethod
    def find_next_available_date(given_date, date_list):
        converted_date_list = [datetime.strptime(date, "%d-%m-%Y") for date in date_list]
        converted_given_date = datetime.strptime(given_date, "%d-%m-%Y")

        next_date = converted_given_date + timedelta(days=1)
        while next_date not in converted_date_list:
            next_date += timedelta(days=1)
            if next_date > max(converted_date_list):
                raise InvalidMutualFundDateException

        result = next_date.strftime('%d-%m-%Y')
        return result
