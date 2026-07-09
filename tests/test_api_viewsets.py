import pytest
from django.urls import resolve, reverse
from rest_framework.viewsets import ViewSet

from django_cash_flow_manager.cashflows.api.views import CategoryOptionsViewSet, SubcategoryOptionsViewSet


pytestmark = pytest.mark.unit


def test_dependent_select_api_is_implemented_with_drf_viewsets() -> None:
    # act
    category_view = resolve(reverse('cashflows:category-options')).func
    subcategory_view = resolve(reverse('cashflows:subcategory-options')).func

    # assert
    assert issubclass(CategoryOptionsViewSet, ViewSet)
    assert issubclass(SubcategoryOptionsViewSet, ViewSet)
    assert category_view.cls is CategoryOptionsViewSet
    assert category_view.actions['get'] == 'list'
    assert subcategory_view.cls is SubcategoryOptionsViewSet
    assert subcategory_view.actions['get'] == 'list'
