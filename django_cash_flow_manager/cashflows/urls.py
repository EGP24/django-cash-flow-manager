from django.urls import include, path

from django_cash_flow_manager.cashflows.api.urls import urlpatterns as api_urlpatterns
from django_cash_flow_manager.cashflows.catalogs.urls import urlpatterns as catalog_urlpatterns
from django_cash_flow_manager.cashflows.transactions.urls import urlpatterns as transaction_urlpatterns


app_name = 'cashflows'

urlpatterns = [
    *transaction_urlpatterns,
    *catalog_urlpatterns,
    path('api/', include(api_urlpatterns)),
]
