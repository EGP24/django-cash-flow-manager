from django.urls import path

from django_cash_flow_manager.cashflows.transactions import views


urlpatterns = [
    path('', views.transaction_list, name='transaction-list'),
    path('transactions/create/', views.transaction_create, name='transaction-create'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction-delete'),
]
