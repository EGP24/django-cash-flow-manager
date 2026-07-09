from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from django_cash_flow_manager.cashflows.catalogs.categories.forms import CategoryForm
from django_cash_flow_manager.cashflows.catalogs.subcategories.forms import SubcategoryForm
from django_cash_flow_manager.cashflows.catalogs.types.forms import CashFlowTypeForm
from django_cash_flow_manager.cashflows.models import (
    CashFlowStatus,
    CashFlowTransaction,
    CashFlowType,
    Category,
    Subcategory,
)
from django_cash_flow_manager.cashflows.transactions.forms import CashFlowTransactionForm


pytestmark = [pytest.mark.unit, pytest.mark.django_db]


@pytest.fixture
def cashflow_catalogs():
    status = CashFlowStatus.objects.create(name='Бизнес')
    income_type = CashFlowType.objects.create(name='Пополнение')
    outcome_type = CashFlowType.objects.create(name='Списание')
    marketing = Category.objects.create(name='Маркетинг', type=outcome_type)
    sales = Category.objects.create(name='Продажи', type=income_type)
    avito = Subcategory.objects.create(name='Avito', category=marketing)
    direct_sales = Subcategory.objects.create(name='Прямые продажи', category=sales)
    return {
        'status': status,
        'income_type': income_type,
        'outcome_type': outcome_type,
        'marketing': marketing,
        'sales': sales,
        'avito': avito,
        'direct_sales': direct_sales,
    }


def test_transaction_form_filters_categories_and_subcategories_for_existing_transaction(cashflow_catalogs):
    # arrange
    transaction = CashFlowTransaction.objects.create(
        date=date(2025, 1, 1),
        status=cashflow_catalogs['status'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['marketing'],
        subcategory=cashflow_catalogs['avito'],
        amount=Decimal('1000.00'),
    )

    # act
    form = CashFlowTransactionForm(instance=transaction)

    # assert
    assert list(form.fields['category'].queryset) == [cashflow_catalogs['marketing']]
    assert list(form.fields['subcategory'].queryset) == [cashflow_catalogs['avito']]


def test_transaction_form_rejects_subcategory_from_another_category(cashflow_catalogs):
    # arrange
    form = CashFlowTransactionForm(
        data={
            'date': '2025-01-01',
            'status': cashflow_catalogs['status'].pk,
            'type': cashflow_catalogs['outcome_type'].pk,
            'category': cashflow_catalogs['marketing'].pk,
            'subcategory': cashflow_catalogs['direct_sales'].pk,
            'amount': '1000.00',
        }
    )

    # act
    is_valid = form.is_valid()

    # assert
    assert is_valid is False
    assert 'Подкатегория не относится к выбранной категории' in form.errors['subcategory']


def test_catalog_forms_apply_bootstrap_classes(cashflow_catalogs):
    # act
    type_form = CashFlowTypeForm()
    category_form = CategoryForm()
    subcategory_form = SubcategoryForm()

    # assert
    assert type_form.fields['name'].widget.attrs['class'] == 'form-control'
    assert category_form.fields['type'].widget.attrs['class'] == 'form-select'
    assert subcategory_form.fields['category'].widget.attrs['class'] == 'form-select'


def test_transaction_model_clean_rejects_invalid_dependencies(cashflow_catalogs):
    # arrange
    transaction = CashFlowTransaction(
        date=date(2025, 1, 1),
        status=cashflow_catalogs['status'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['sales'],
        subcategory=cashflow_catalogs['direct_sales'],
        amount=Decimal('1000.00'),
    )

    # act
    with pytest.raises(ValidationError) as exc_info:
        transaction.clean()

    # assert
    assert 'Категория не относится к выбранному типу' in str(exc_info.value)


def test_transaction_model_clean_rejects_subcategory_from_another_category(cashflow_catalogs):
    # arrange
    transaction = CashFlowTransaction(
        date=date(2025, 1, 1),
        status=cashflow_catalogs['status'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['marketing'],
        subcategory=cashflow_catalogs['direct_sales'],
        amount=Decimal('1000.00'),
    )

    # act
    with pytest.raises(ValidationError) as exc_info:
        transaction.clean()

    # assert
    assert 'Подкатегория не относится к выбранной категории' in str(exc_info.value)
