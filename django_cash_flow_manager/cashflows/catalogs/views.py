from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe

from django_cash_flow_manager.cashflows.models import CashFlowStatus, CashFlowType, Category, Subcategory


@require_safe
def catalog_list(request: HttpRequest) -> HttpResponse:
    context = {
        'statuses': CashFlowStatus.objects.all(),
        'types': CashFlowType.objects.all(),
        'categories': Category.objects.select_related('type'),
        'subcategories': Subcategory.objects.select_related('category', 'category__type'),
    }
    return render(request, 'cashflows/catalogs.html', context)
