from django.apps import AppConfig


class CashflowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_cash_flow_manager.cashflows'
    verbose_name = 'Движение денежных средств'
