from importlib.util import find_spec

import pytest


pytestmark = pytest.mark.unit


def module_exists(module_name: str) -> bool:
    try:
        return find_spec(module_name) is not None
    except ModuleNotFoundError:
        return False


def test_custom_architecture_wrapper_modules_are_removed() -> None:
    # arrange
    removed_modules = [
        'django_cash_flow_manager.cashflows.api.requests',
        'django_cash_flow_manager.cashflows.forms',
        'django_cash_flow_manager.cashflows.query',
        'django_cash_flow_manager.cashflows.transactions.filters',
        'django_cash_flow_manager.cashflows.transactions.pagination',
        'django_cash_flow_manager.cashflows.transactions.requests',
        'django_cash_flow_manager.cashflows.transactions.services',
        'django_cash_flow_manager.cashflows.catalogs.common.services',
        'django_cash_flow_manager.cashflows.catalogs.common.specs',
        'django_cash_flow_manager.cashflows.catalogs.common.views',
        'django_cash_flow_manager.cashflows.catalogs.categories.selectors',
        'django_cash_flow_manager.cashflows.catalogs.categories.services',
        'django_cash_flow_manager.cashflows.catalogs.statuses.selectors',
        'django_cash_flow_manager.cashflows.catalogs.statuses.services',
        'django_cash_flow_manager.cashflows.catalogs.subcategories.selectors',
        'django_cash_flow_manager.cashflows.catalogs.subcategories.services',
        'django_cash_flow_manager.cashflows.catalogs.types.selectors',
        'django_cash_flow_manager.cashflows.catalogs.types.services',
    ]

    # assert
    assert [module for module in removed_modules if module_exists(module)] == []
