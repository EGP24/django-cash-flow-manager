from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.urls import reverse

from django_cash_flow_manager.cashflows.models import (
    CashFlowStatus,
    CashFlowTransaction,
    CashFlowType,
    Category,
    Subcategory,
)


pytestmark = [pytest.mark.functional, pytest.mark.django_db]


@pytest.fixture
def cashflow_catalogs():
    status_business = CashFlowStatus.objects.create(name='Бизнес')
    status_personal = CashFlowStatus.objects.create(name='Личное')
    income_type = CashFlowType.objects.create(name='Пополнение')
    outcome_type = CashFlowType.objects.create(name='Списание')
    marketing = Category.objects.create(name='Маркетинг', type=outcome_type)
    infrastructure = Category.objects.create(name='Инфраструктура', type=outcome_type)
    sales = Category.objects.create(name='Продажи', type=income_type)
    avito = Subcategory.objects.create(name='Avito', category=marketing)
    vps = Subcategory.objects.create(name='VPS', category=infrastructure)
    direct_sales = Subcategory.objects.create(name='Прямые продажи', category=sales)
    return {
        'status_business': status_business,
        'status_personal': status_personal,
        'income_type': income_type,
        'outcome_type': outcome_type,
        'marketing': marketing,
        'infrastructure': infrastructure,
        'sales': sales,
        'avito': avito,
        'vps': vps,
        'direct_sales': direct_sales,
    }


def create_cashflow_transactions(cashflow_catalogs, count: int, *, status: CashFlowStatus | None = None) -> None:
    transaction_status = status or cashflow_catalogs['status_business']
    for index in range(count):
        CashFlowTransaction.objects.create(
            date=date(2025, 1, 1) + timedelta(days=index),
            status=transaction_status,
            type=cashflow_catalogs['outcome_type'],
            category=cashflow_catalogs['marketing'],
            subcategory=cashflow_catalogs['avito'],
            amount=Decimal('1000.00'),
            comment=f'Операция {index + 1}',
        )


def test_home_page_lists_cashflow_transactions_and_filters_by_status(client, cashflow_catalogs):
    # arrange
    CashFlowTransaction.objects.create(
        date=date(2025, 1, 1),
        status=cashflow_catalogs['status_business'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['marketing'],
        subcategory=cashflow_catalogs['avito'],
        amount=Decimal('1000.00'),
        comment='Реклама на Avito',
    )
    CashFlowTransaction.objects.create(
        date=date(2025, 1, 2),
        status=cashflow_catalogs['status_personal'],
        type=cashflow_catalogs['income_type'],
        category=cashflow_catalogs['sales'],
        subcategory=cashflow_catalogs['direct_sales'],
        amount=Decimal('2500.00'),
        comment='Личный перевод',
    )

    # act
    response = client.get(reverse('cashflows:transaction-list'), {'status': cashflow_catalogs['status_business'].pk})

    # assert
    assert response.status_code == 200
    assert 'Реклама на Avito' in response.text
    assert 'Личный перевод' not in response.text
    assert 'table-responsive' in response.text
    assert 'Создать запись' in response.text


def test_home_page_paginates_transactions_with_default_page_size(client, cashflow_catalogs):
    # arrange
    create_cashflow_transactions(cashflow_catalogs, 32)

    # act
    response = client.get(reverse('cashflows:transaction-list'))

    # assert
    assert response.status_code == 200
    assert 'Показано 1–25 из 32' in response.text
    assert 'Операция 32' in response.text
    assert 'Операция 8' in response.text
    assert 'Операция 7' not in response.text
    assert 'href="?page=2&amp;page_size=25"' in response.text
    assert 'transaction-pagination-summary' in response.text
    assert 'transaction-page-size page-size-list' in response.text
    assert response.text.count('page-link page-size-link') == 3


def test_home_page_uses_requested_page_and_page_size(client, cashflow_catalogs):
    # arrange
    create_cashflow_transactions(cashflow_catalogs, 32)

    # act
    response = client.get(reverse('cashflows:transaction-list'), {'page': '2', 'page_size': '10'})

    # assert
    assert response.status_code == 200
    assert 'Показано 11–20 из 32' in response.text
    assert 'Операция 22' in response.text
    assert 'Операция 13' in response.text
    assert 'Операция 23' not in response.text
    assert 'Операция 12' not in response.text


def test_home_page_preserves_filters_in_pagination_and_page_size_links(client, cashflow_catalogs):
    # arrange
    create_cashflow_transactions(cashflow_catalogs, 12, status=cashflow_catalogs['status_business'])
    create_cashflow_transactions(cashflow_catalogs, 5, status=cashflow_catalogs['status_personal'])

    # act
    response = client.get(
        reverse('cashflows:transaction-list'),
        {
            'status': cashflow_catalogs['status_business'].pk,
            'page': '2',
            'page_size': '10',
        },
    )

    # assert
    assert response.status_code == 200
    assert 'Показано 11–12 из 12' in response.text
    assert f'href="?status={cashflow_catalogs["status_business"].pk}&amp;page_size=25"' in response.text
    assert f'href="?status={cashflow_catalogs["status_business"].pk}&amp;page=1&amp;page_size=10"' in response.text


def test_home_page_filters_by_period_type_category_and_subcategory(client, cashflow_catalogs):
    # arrange
    CashFlowTransaction.objects.create(
        date=date(2025, 1, 10),
        status=cashflow_catalogs['status_business'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['marketing'],
        subcategory=cashflow_catalogs['avito'],
        amount=Decimal('1000.00'),
        comment='Нужная операция',
    )
    CashFlowTransaction.objects.create(
        date=date(2025, 2, 10),
        status=cashflow_catalogs['status_business'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['infrastructure'],
        subcategory=cashflow_catalogs['vps'],
        amount=Decimal('2000.00'),
        comment='Лишняя операция',
    )

    # act
    response = client.get(
        reverse('cashflows:transaction-list'),
        {
            'date_from': '2025-01-01',
            'date_to': '2025-01-31',
            'type': cashflow_catalogs['outcome_type'].pk,
            'category': cashflow_catalogs['marketing'].pk,
            'subcategory': cashflow_catalogs['avito'].pk,
        },
    )

    # assert
    assert response.status_code == 200
    assert 'Нужная операция' in response.text
    assert 'Лишняя операция' not in response.text


def test_cashflow_transaction_can_be_created_from_bootstrap_form(client, cashflow_catalogs):
    # arrange
    payload = {
        'date': '2025-01-03',
        'status': cashflow_catalogs['status_business'].pk,
        'type': cashflow_catalogs['outcome_type'].pk,
        'category': cashflow_catalogs['marketing'].pk,
        'subcategory': cashflow_catalogs['avito'].pk,
        'amount': '1500.50',
        'comment': 'Тестовая рекламная операция',
    }

    # act
    response = client.post(reverse('cashflows:transaction-create'), data=payload, follow=True)

    # assert
    assert response.status_code == 200
    assert CashFlowTransaction.objects.filter(comment='Тестовая рекламная операция').exists()
    assert 'Запись ДДС создана' in response.text


def test_cashflow_transaction_can_be_updated_and_deleted_from_ui(client, cashflow_catalogs):
    # arrange
    transaction = CashFlowTransaction.objects.create(
        date=date(2025, 1, 1),
        status=cashflow_catalogs['status_business'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['marketing'],
        subcategory=cashflow_catalogs['avito'],
        amount=Decimal('1000.00'),
        comment='Старая операция',
    )
    payload = {
        'date': '2025-01-04',
        'status': cashflow_catalogs['status_business'].pk,
        'type': cashflow_catalogs['outcome_type'].pk,
        'category': cashflow_catalogs['infrastructure'].pk,
        'subcategory': cashflow_catalogs['vps'].pk,
        'amount': '990.00',
        'comment': 'VPS для проекта',
    }

    # act
    update_response = client.post(
        reverse('cashflows:transaction-update', kwargs={'pk': transaction.pk}), data=payload, follow=True
    )
    transaction.refresh_from_db()
    delete_response = client.post(reverse('cashflows:transaction-delete', kwargs={'pk': transaction.pk}), follow=True)

    # assert
    assert update_response.status_code == 200
    assert transaction.comment == 'VPS для проекта'
    assert transaction.subcategory == cashflow_catalogs['vps']
    assert 'Запись ДДС обновлена' in update_response.text
    assert delete_response.status_code == 200
    assert not CashFlowTransaction.objects.filter(pk=transaction.pk).exists()
    assert 'Запись ДДС удалена' in delete_response.text


def test_cashflow_transaction_edit_and_delete_pages_are_available(client, cashflow_catalogs):
    # arrange
    transaction = CashFlowTransaction.objects.create(
        date=date(2025, 1, 1),
        status=cashflow_catalogs['status_business'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['marketing'],
        subcategory=cashflow_catalogs['avito'],
        amount=Decimal('1000.00'),
    )

    # act
    edit_response = client.get(reverse('cashflows:transaction-update', kwargs={'pk': transaction.pk}))
    delete_response = client.get(reverse('cashflows:transaction-delete', kwargs={'pk': transaction.pk}))

    # assert
    assert edit_response.status_code == 200
    assert 'Редактировать запись ДДС' in edit_response.text
    assert delete_response.status_code == 200
    assert 'Удалить запись ДДС' in delete_response.text


def test_cashflow_form_rejects_category_from_another_type(client, cashflow_catalogs):
    # arrange
    payload = {
        'date': '2025-01-03',
        'status': cashflow_catalogs['status_business'].pk,
        'type': cashflow_catalogs['income_type'].pk,
        'category': cashflow_catalogs['marketing'].pk,
        'subcategory': cashflow_catalogs['avito'].pk,
        'amount': '1500.50',
        'comment': 'Неверная связка',
    }

    # act
    response = client.post(reverse('cashflows:transaction-create'), data=payload)

    # assert
    assert response.status_code == 200
    assert not CashFlowTransaction.objects.filter(comment='Неверная связка').exists()
    assert 'Категория не относится к выбранному типу' in response.text


def test_dependent_select_endpoints_return_filtered_options(client, cashflow_catalogs):
    # arrange
    categories_url = reverse('cashflows:category-options')
    subcategories_url = reverse('cashflows:subcategory-options')

    # act
    categories_response = client.get(categories_url, {'type': cashflow_catalogs['outcome_type'].pk})
    subcategories_response = client.get(subcategories_url, {'category': cashflow_catalogs['marketing'].pk})

    # assert
    assert categories_response.status_code == 200
    assert categories_response.json() == {
        'results': [
            {'id': cashflow_catalogs['marketing'].pk, 'name': 'Маркетинг'},
            {'id': cashflow_catalogs['infrastructure'].pk, 'name': 'Инфраструктура'},
        ]
    }
    assert subcategories_response.status_code == 200
    assert subcategories_response.json() == {'results': [{'id': cashflow_catalogs['avito'].pk, 'name': 'Avito'}]}


def test_dependent_select_endpoints_return_empty_results_for_missing_or_invalid_filters(client):
    # arrange
    categories_url = reverse('cashflows:category-options')
    subcategories_url = reverse('cashflows:subcategory-options')

    # act
    categories_response = client.get(categories_url, {'type': 'invalid'})
    subcategories_response = client.get(subcategories_url)

    # assert
    assert categories_response.status_code == 200
    assert categories_response.json() == {'results': []}
    assert subcategories_response.status_code == 200
    assert subcategories_response.json() == {'results': []}


def test_catalog_status_can_be_created_from_ui(client):
    # arrange
    payload = {'name': 'Налог'}

    # act
    response = client.post(reverse('cashflows:status-create'), data=payload, follow=True)

    # assert
    assert response.status_code == 200
    assert CashFlowStatus.objects.filter(name='Налог').exists()
    assert 'Статус создан' in response.text


def test_catalog_page_uses_tables_with_local_add_buttons_and_icon_actions(client, cashflow_catalogs):
    # act
    response = client.get(reverse('cashflows:catalogs'))

    # assert
    assert response.status_code == 200
    assert response.text.count('class="catalog-table table') == 4
    assert 'aria-label="Добавить статус"' in response.text
    assert 'aria-label="Добавить тип"' in response.text
    assert 'aria-label="Добавить категорию"' in response.text
    assert 'aria-label="Добавить подкатегорию"' in response.text
    assert '<i class="bi bi-plus-lg"' in response.text
    assert '<i class="bi bi-pencil"' in response.text
    assert '<i class="bi bi-trash"' in response.text
    assert 'catalog-header-actions' not in response.text


def test_transaction_list_uses_icon_action_buttons(client, cashflow_catalogs):
    # arrange
    CashFlowTransaction.objects.create(
        date=date(2025, 1, 1),
        status=cashflow_catalogs['status_business'],
        type=cashflow_catalogs['outcome_type'],
        category=cashflow_catalogs['marketing'],
        subcategory=cashflow_catalogs['avito'],
        amount=Decimal('1000.00'),
    )

    # act
    response = client.get(reverse('cashflows:transaction-list'))

    # assert
    assert response.status_code == 200
    assert 'aria-label="Редактировать запись"' in response.text
    assert 'aria-label="Удалить запись"' in response.text
    assert '<i class="bi bi-pencil"' in response.text
    assert '<i class="bi bi-trash"' in response.text


def test_catalog_status_can_be_updated_and_deleted_from_ui(client):
    # arrange
    status = CashFlowStatus.objects.create(name='Черновик')

    # act
    update_response = client.post(
        reverse('cashflows:status-update', kwargs={'pk': status.pk}),
        data={'name': 'Налог'},
        follow=True,
    )
    status.refresh_from_db()
    delete_response = client.post(reverse('cashflows:status-delete', kwargs={'pk': status.pk}), follow=True)

    # assert
    assert update_response.status_code == 200
    assert status.name == 'Налог'
    assert 'Статус обновлен' in update_response.text
    assert delete_response.status_code == 200
    assert not CashFlowStatus.objects.filter(pk=status.pk).exists()
    assert 'Статус удален' in delete_response.text


def test_catalog_type_can_be_updated_and_deleted_from_ui(client):
    # arrange
    cashflow_type = CashFlowType.objects.create(name='Черновой тип')

    # act
    update_response = client.post(
        reverse('cashflows:type-update', kwargs={'pk': cashflow_type.pk}),
        data={'name': 'Возврат'},
        follow=True,
    )
    cashflow_type.refresh_from_db()
    delete_response = client.post(reverse('cashflows:type-delete', kwargs={'pk': cashflow_type.pk}), follow=True)

    # assert
    assert update_response.status_code == 200
    assert cashflow_type.name == 'Возврат'
    assert 'Тип обновлен' in update_response.text
    assert delete_response.status_code == 200
    assert not CashFlowType.objects.filter(pk=cashflow_type.pk).exists()
    assert 'Тип удален' in delete_response.text


def test_catalog_category_can_be_updated_and_deleted_from_ui(client):
    # arrange
    cashflow_type = CashFlowType.objects.create(name='Списание')
    category = Category.objects.create(name='Черновая категория', type=cashflow_type)

    # act
    update_response = client.post(
        reverse('cashflows:category-update', kwargs={'pk': category.pk}),
        data={'type': cashflow_type.pk, 'name': 'Комиссии'},
        follow=True,
    )
    category.refresh_from_db()
    delete_response = client.post(reverse('cashflows:category-delete', kwargs={'pk': category.pk}), follow=True)

    # assert
    assert update_response.status_code == 200
    assert category.name == 'Комиссии'
    assert 'Категория обновлена' in update_response.text
    assert delete_response.status_code == 200
    assert not Category.objects.filter(pk=category.pk).exists()
    assert 'Категория удалена' in delete_response.text


def test_catalog_subcategory_can_be_updated_and_deleted_from_ui(client):
    # arrange
    cashflow_type = CashFlowType.objects.create(name='Списание')
    category = Category.objects.create(name='Маркетинг', type=cashflow_type)
    subcategory = Subcategory.objects.create(name='Черновая подкатегория', category=category)

    # act
    update_response = client.post(
        reverse('cashflows:subcategory-update', kwargs={'pk': subcategory.pk}),
        data={'category': category.pk, 'name': 'Банк'},
        follow=True,
    )
    subcategory.refresh_from_db()
    delete_response = client.post(
        reverse('cashflows:subcategory-delete', kwargs={'pk': subcategory.pk}),
        follow=True,
    )

    # assert
    assert update_response.status_code == 200
    assert subcategory.name == 'Банк'
    assert 'Подкатегория обновлена' in update_response.text
    assert delete_response.status_code == 200
    assert not Subcategory.objects.filter(pk=subcategory.pk).exists()
    assert 'Подкатегория удалена' in delete_response.text


def test_catalog_form_and_delete_confirmation_pages_are_available(client):
    # arrange
    status = CashFlowStatus.objects.create(name='Черновик')

    # act
    form_response = client.get(reverse('cashflows:status-create'))
    delete_response = client.get(reverse('cashflows:status-delete', kwargs={'pk': status.pk}))

    # assert
    assert form_response.status_code == 200
    assert 'Создать статус' in form_response.text
    assert delete_response.status_code == 200
    assert 'Удалить справочник' in delete_response.text


def test_catalog_type_category_and_subcategory_create_pages_work(client, cashflow_catalogs):
    # arrange
    category_payload = {'type': cashflow_catalogs['outcome_type'].pk, 'name': 'Комиссии'}

    # act
    type_response = client.post(reverse('cashflows:type-create'), data={'name': 'Возврат'}, follow=True)
    category_response = client.post(reverse('cashflows:category-create'), data=category_payload, follow=True)
    category = Category.objects.get(name='Комиссии')
    subcategory_response = client.post(
        reverse('cashflows:subcategory-create'),
        data={'category': category.pk, 'name': 'Банк'},
        follow=True,
    )

    # assert
    assert type_response.status_code == 200
    assert category_response.status_code == 200
    assert subcategory_response.status_code == 200
    assert CashFlowType.objects.filter(name='Возврат').exists()
    assert Subcategory.objects.filter(name='Банк', category=category).exists()
