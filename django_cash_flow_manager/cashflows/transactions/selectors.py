from datetime import date
from typing import Any, TypedDict

from django.db.models import QuerySet

from django_cash_flow_manager.cashflows.models import (
    CashFlowStatus,
    CashFlowTransaction,
    CashFlowType,
    Category,
    Subcategory,
)


class TransactionFilterOptions(TypedDict):
    statuses: QuerySet[CashFlowStatus]
    types: QuerySet[CashFlowType]
    categories: QuerySet[Category]
    subcategories: QuerySet[Subcategory]


def get_transaction_queryset(filters: dict[str, Any]) -> QuerySet[CashFlowTransaction]:
    transactions = CashFlowTransaction.objects.select_related('status', 'type', 'category', 'subcategory')
    date_from = filters.get('date_from')
    date_to = filters.get('date_to')

    if isinstance(date_from, date):
        transactions = transactions.filter(date__gte=date_from)
    if isinstance(date_to, date):
        transactions = transactions.filter(date__lte=date_to)
    if filters.get('status'):
        transactions = transactions.filter(status_id=filters['status'])
    if filters.get('type'):
        transactions = transactions.filter(type_id=filters['type'])
    if filters.get('category'):
        transactions = transactions.filter(category_id=filters['category'])
    if filters.get('subcategory'):
        transactions = transactions.filter(subcategory_id=filters['subcategory'])

    return transactions


def get_transaction_filter_options() -> TransactionFilterOptions:
    return {
        'statuses': CashFlowStatus.objects.all(),
        'types': CashFlowType.objects.all(),
        'categories': Category.objects.select_related('type'),
        'subcategories': Subcategory.objects.select_related('category'),
    }
