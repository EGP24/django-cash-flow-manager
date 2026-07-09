import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from django_cash_flow_manager.cashflows.models import (
    CashFlowStatus,
    CashFlowTransaction,
    CashFlowType,
    Category,
    Subcategory,
)


pytestmark = [pytest.mark.unit, pytest.mark.django_db]


def test_load_mock_data_creates_demo_admin_user() -> None:
    # arrange
    user_model = get_user_model()

    # act
    call_command('load_mock_data')

    # assert
    user = user_model.objects.get(username='admin')
    assert user.email == 'admin@example.com'
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.check_password('admin') is True


def test_load_mock_data_is_idempotent() -> None:
    # arrange
    user_model = get_user_model()

    # act
    call_command('load_mock_data')
    call_command('load_mock_data')

    # assert
    assert user_model.objects.filter(username='admin').count() == 1


def test_load_mock_data_repairs_existing_demo_user() -> None:
    # arrange
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username='admin',
        email='old@example.com',
        password='admin',
        is_staff=False,
        is_superuser=False,
    )

    # act
    call_command('load_mock_data')
    user.refresh_from_db()

    # assert
    assert user.email == 'admin@example.com'
    assert user.is_staff is True
    assert user.is_superuser is True


def test_load_mock_data_creates_cashflow_catalogs_and_transactions() -> None:
    # act
    call_command('load_mock_data')

    # assert
    assert CashFlowStatus.objects.filter(name='Бизнес').exists()
    assert CashFlowStatus.objects.filter(name='Личное').exists()
    assert CashFlowStatus.objects.filter(name='Налог').exists()
    assert CashFlowType.objects.filter(name='Пополнение').exists()
    assert CashFlowType.objects.filter(name='Списание').exists()
    assert Category.objects.filter(name='Маркетинг', type__name='Списание').exists()
    assert Subcategory.objects.filter(name='Avito', category__name='Маркетинг').exists()
    assert CashFlowTransaction.objects.filter(comment='Тестовая оплата Avito').exists()
    assert CashFlowTransaction.objects.count() == 6
