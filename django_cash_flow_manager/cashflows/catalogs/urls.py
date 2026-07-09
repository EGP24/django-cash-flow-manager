from django.urls import path

from django_cash_flow_manager.cashflows.catalogs import views
from django_cash_flow_manager.cashflows.catalogs.categories import views as category_views
from django_cash_flow_manager.cashflows.catalogs.statuses import views as status_views
from django_cash_flow_manager.cashflows.catalogs.subcategories import views as subcategory_views
from django_cash_flow_manager.cashflows.catalogs.types import views as type_views


urlpatterns = [
    path('catalogs/', views.catalog_list, name='catalogs'),
    path('catalogs/statuses/create/', status_views.status_create, name='status-create'),
    path('catalogs/statuses/<int:pk>/edit/', status_views.status_update, name='status-update'),
    path('catalogs/statuses/<int:pk>/delete/', status_views.status_delete, name='status-delete'),
    path('catalogs/types/create/', type_views.type_create, name='type-create'),
    path('catalogs/types/<int:pk>/edit/', type_views.type_update, name='type-update'),
    path('catalogs/types/<int:pk>/delete/', type_views.type_delete, name='type-delete'),
    path('catalogs/categories/create/', category_views.category_create, name='category-create'),
    path('catalogs/categories/<int:pk>/edit/', category_views.category_update, name='category-update'),
    path('catalogs/categories/<int:pk>/delete/', category_views.category_delete, name='category-delete'),
    path('catalogs/subcategories/create/', subcategory_views.subcategory_create, name='subcategory-create'),
    path('catalogs/subcategories/<int:pk>/edit/', subcategory_views.subcategory_update, name='subcategory-update'),
    path('catalogs/subcategories/<int:pk>/delete/', subcategory_views.subcategory_delete, name='subcategory-delete'),
]
