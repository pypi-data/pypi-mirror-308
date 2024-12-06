import pytest
import pandas as pd
import yaml
from neurostats_API.utils import StatsProcessor


def test_value():
    from neurostats_API.fetchers import ValueFetcher
    fetcher = ValueFetcher(ticker='2330')

    fetched_data = fetcher.query_data()

    assert ('daily_data' in fetched_data)
    assert ('yearly_data' in fetched_data)

    assert isinstance(fetched_data['daily_data'], dict)
    assert isinstance(fetched_data['yearly_data'], pd.DataFrame)

def test_profit_lose():
    from neurostats_API.utils import StatsFetcher

    fetcher = StatsFetcher()

    data = fetcher.get_profit_lose("2330")

    table_settings = StatsProcessor.load_yaml("profit_lose.yaml")
    
    for key in table_settings.keys():
        assert key in data.keys()

def test_cash_flow():
    from neurostats_API.utils import StatsFetcher

    fetcher = StatsFetcher()
    data = fetcher.get_cash_flow("2330")

    assert("cash_flow" in data.keys())

def test_month_revenue():
    from neurostats_API.utils import StatsFetcher

    fetcher = StatsFetcher()
    data = fetcher.get_month_revenue_sheet("2330")

    assert("month_revenue" in data.keys())

def test_balance_sheet():
    from neurostats_API.utils import StatsFetcher

    fetcher = StatsFetcher()

    data = fetcher.get_balance_sheet("2330")

    table_settings = StatsProcessor.load_yaml("profit_lose.yaml")
    
    "balance_sheet" in data.keys()

def test_finance_overview():
    from neurostats_API.fetchers import FinanceOverviewFetcher
    fetcher = FinanceOverviewFetcher(ticker='2330')
    fetched_data = fetcher.query_data()

    expected_keys = [
    # Queried items
        'revenue',
        'gross_profit',
        'operating_income',
        'net_income',
        'operating_cash_flow',
        'invest_cash_flow',
        'financing_cash_flow',
        'capital',
        'eps',
        'total_asset',
        'equity',
        'net_income_before_tax',
        'interest',
        'operating_expenses',
        'net_income_rate',
        'revenue_YoY',
        'gross_prof_YoY',
        'operating_income_YoY',
        'net_income_YoY',
        'account_receive',
        'account_pay',
        'inventories',
        'operating_cost',
        'application',
        'current_assets',
        'current_liabilities',
        'total_liabilities',
        'cash_and_cash_equivalents',
        'interest_expense',

        # calculated_items
        'fcf',
        'EBIT',
        'share_outstanding',
        'revenue_per_share',
        'gross_per_share',
        'operating_income_per_share',
        'operating_cash_flow_per_share',
        'fcf_per_share',
        'roa',
        'roe',
        'gross_over_asset',
        'roce',
        'gross_profit_margin',
        'operation_profit_rate',
        'operating_cash_flow_profit_rate',
        'dso',
        'account_receive_over_revenue',
        'dpo',
        'inventories_cycle_ratio',
        'dio',
        'inventories_revenue_ratio',
        'cash_of_conversion_cycle',
        'asset_turnover',
        'applcation_turnover',
        'current_ratio',
        'quick_ratio',
        'debt_to_equity_ratio',
        'net_debt_to_equity_ratio',
        'interest_coverage_ratio',
        'debt_to_operating_cash_flow',
        'debt_to_free_cash_flow',
        'cash_flow_ratio',
    ]

    for key in expected_keys:
        assert key in fetched_data['seasonal_data'], f"{key} not found in fetched_data"
        # assert fetched_data['seasonal_data'][0][key] is not None, f"{key} is None"
