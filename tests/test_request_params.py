from datetime import date

import pytest
from django.http import QueryDict

from django_cash_flow_manager.cashflows.transactions.forms import (
    DEFAULT_PAGE_SIZE,
    TransactionFilterForm,
)


pytestmark = pytest.mark.unit


def test_transaction_filter_form_parses_filters_and_pagination() -> None:
    # arrange
    params = QueryDict(
        'date_from=2025-01-01&date_to=2025-01-31&status=2&type=3&category=4&subcategory=5&page=2&page_size=50'
    )

    # act
    form = TransactionFilterForm(data=params)

    # assert
    assert form.is_valid()
    assert form.cleaned_data == {
        'date_from': date(2025, 1, 1),
        'date_to': date(2025, 1, 31),
        'status': 2,
        'type': 3,
        'category': 4,
        'subcategory': 5,
        'page': '2',
        'page_size': 50,
    }


def test_transaction_filter_form_ignores_invalid_ids_and_page_size() -> None:
    # arrange
    params = QueryDict('page_size=999&status=bad')

    # act
    form = TransactionFilterForm(data=params)

    # assert
    assert form.is_valid()
    assert form.cleaned_data['status'] is None
    assert form.cleaned_data['page_size'] == DEFAULT_PAGE_SIZE
