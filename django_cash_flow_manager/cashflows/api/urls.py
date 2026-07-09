from django.urls import path

from django_cash_flow_manager.cashflows.api import views


urlpatterns = [
    path('categories/', views.CategoryOptionsViewSet.as_view({'get': 'list'}), name='category-options'),
    path('subcategories/', views.SubcategoryOptionsViewSet.as_view({'get': 'list'}), name='subcategory-options'),
]
