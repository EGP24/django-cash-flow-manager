import pytest
from django.test import RequestFactory
from django.urls import resolve, reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from django_cash_flow_manager.cashflows.catalogs import views as catalog_views
from django_cash_flow_manager.cashflows.catalogs.categories import views as category_views
from django_cash_flow_manager.cashflows.catalogs.statuses import views as status_views
from django_cash_flow_manager.cashflows.catalogs.subcategories import views as subcategory_views
from django_cash_flow_manager.cashflows.catalogs.types import views as type_views
from django_cash_flow_manager.cashflows.transactions import views as transaction_views


pytestmark = pytest.mark.unit


def test_transaction_routes_are_implemented_with_plain_django_view_functions() -> None:
    # arrange
    expected_routes = {
        'cashflows:transaction-list': transaction_views.transaction_list,
        'cashflows:transaction-create': transaction_views.transaction_create,
        'cashflows:transaction-update': transaction_views.transaction_update,
        'cashflows:transaction-delete': transaction_views.transaction_delete,
    }

    for route_name, expected_view in expected_routes.items():
        kwargs = {'pk': 1} if route_name in {'cashflows:transaction-update', 'cashflows:transaction-delete'} else None

        # act
        resolved_view = resolve(reverse(route_name, kwargs=kwargs)).func

        # assert
        assert resolved_view is expected_view
        assert not hasattr(resolved_view, 'actions')
        assert not hasattr(resolved_view, 'cls')


def test_catalog_list_route_is_implemented_with_plain_django_view_function() -> None:
    # arrange
    resolved_view = resolve(reverse('cashflows:catalogs')).func

    # assert
    assert resolved_view is catalog_views.catalog_list
    assert not hasattr(resolved_view, 'actions')
    assert not hasattr(resolved_view, 'cls')


def test_catalog_crud_routes_use_django_generic_views() -> None:
    # arrange
    expected_routes = {
        'cashflows:status-create': (status_views.StatusCreateView, CreateView),
        'cashflows:status-update': (status_views.StatusUpdateView, UpdateView),
        'cashflows:status-delete': (status_views.StatusDeleteView, DeleteView),
        'cashflows:type-create': (type_views.TypeCreateView, CreateView),
        'cashflows:type-update': (type_views.TypeUpdateView, UpdateView),
        'cashflows:type-delete': (type_views.TypeDeleteView, DeleteView),
        'cashflows:category-create': (category_views.CategoryCreateView, CreateView),
        'cashflows:category-update': (category_views.CategoryUpdateView, UpdateView),
        'cashflows:category-delete': (category_views.CategoryDeleteView, DeleteView),
        'cashflows:subcategory-create': (subcategory_views.SubcategoryCreateView, CreateView),
        'cashflows:subcategory-update': (subcategory_views.SubcategoryUpdateView, UpdateView),
        'cashflows:subcategory-delete': (subcategory_views.SubcategoryDeleteView, DeleteView),
    }

    for route_name, (expected_view_class, generic_base) in expected_routes.items():
        kwargs = {'pk': 1} if route_name.split(':', maxsplit=1)[1].endswith(('-update', '-delete')) else None

        # act
        resolved_view = resolve(reverse(route_name, kwargs=kwargs)).func

        # assert
        assert resolved_view.view_class is expected_view_class
        assert issubclass(expected_view_class, generic_base)
        assert not hasattr(resolved_view, 'actions')


def test_transaction_list_rejects_unsafe_methods() -> None:
    # arrange
    request = RequestFactory().post('/')

    # act
    response = transaction_views.transaction_list(request)

    # assert
    assert response.status_code == 405
