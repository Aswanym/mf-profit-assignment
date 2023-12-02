from assignmenttest.src.profit_calc_helper import CreateProfitCalcQueryParams, CalculateNetProfit
from assignmenttest.src.request_utilities import RequestUtility
import pytest
from datetime import datetime
import pdb

@pytest.mark.net_profit
@pytest.mark.tcid12
def test_calculate_net_profit_success():

    # create query params
    query_param_helper = CreateProfitCalcQueryParams()
    query_params = query_param_helper.create_profit_calc_query_params()

    related_mf_scheme_data = query_params['related_mf_data']
    scheme_code = query_params['scheme_code']
    start_date = query_params['start_date']
    end_date = query_params['end_date']
    capital = query_params['capital']

    # calculate the nav for this given mutual fund scheme using the created query params
    net_profit = CalculateNetProfit.calculate_net_profit(scheme_code, start_date, end_date, capital, related_mf_scheme_data)

    # call api
    params = f"scheme_code={scheme_code}&start_date={start_date}&end_date={end_date}&capital={capital}"

    req_helper = RequestUtility()
    rs_api = req_helper.get('profit', params=params)
    net_profit_api_rs = rs_api['net_profit']

    # varify response
    assert net_profit == net_profit_api_rs, f"calculated net profit and api response net profit doesn't match. " \
                                            f"calculated net_profit: {net_profit}," \
                                            f"api response net_profit: {net_profit_api_rs}"


@pytest.mark.net_profit
@pytest.mark.tcid13
def test_calculate_net_profit_failed_invalid_scheme_code():
    # create query params
    query_param_helper = CreateProfitCalcQueryParams()
    query_params = query_param_helper.create_profit_calc_query_params()

    scheme_code = query_params['scheme_code']
    start_date = query_params['start_date']
    end_date = query_params['end_date']
    capital = query_params['capital']
    wrong_scheme_code = '9098'

    # create params with wrong scheme code
    params = f"scheme_code={wrong_scheme_code}&start_date={start_date}&end_date={end_date}&capital={capital}"

    # call api
    req_helper = RequestUtility()
    rs_api = req_helper.get('profit', params=params, expected_status_code=400)
    assert rs_api['detail'] == 'Invalid scheme code', f"Calculating mutual fund net profit using wrong scheme code, giving " \
                                                      f"unexpected message. Expected: 'Invalid scheme code'" \
                                                      f"Actual: {rs_api['detail']}"

@pytest.mark.net_profit
@pytest.mark.tcid14
def test_calculate_net_profit_failed_invalid_date_format():
    # create query params
    query_param_helper = CreateProfitCalcQueryParams()
    query_params = query_param_helper.create_profit_calc_query_params()

    scheme_code = query_params['scheme_code']
    _start_date = query_params['start_date']
    end_date = query_params['end_date']
    capital = query_params['capital']

    # Convert _start_date to datetime object
    datetime_obj = datetime.strptime(_start_date, "%d-%m-%Y")

    # Format the datetime object to "dd-mm-y"
    invalid_start_date = datetime_obj.strftime("%d-%m-%y")

    # create params with wrong scheme code
    params = f"scheme_code={scheme_code}&start_date={invalid_start_date}&end_date={end_date}&capital={capital}"

    # call api
    req_helper = RequestUtility()
    rs_api = req_helper.get('profit', params=params, expected_status_code=400)
    assert rs_api[
               'detail'] == 'Invalid date format. Please use dd-mm-yyyy format.', f"Calculating mutual fund net profit with " \
                                                                                  f"invalid date format giving unexpected message." \
                                                                                  f" Expected: 'Invalid scheme code'" \
                                                                                  f"Actual: {rs_api['detail']}"
