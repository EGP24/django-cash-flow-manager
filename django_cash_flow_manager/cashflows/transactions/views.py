from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from django_cash_flow_manager.cashflows.models import CashFlowTransaction
from django_cash_flow_manager.cashflows.transactions.forms import (
    DEFAULT_PAGE_SIZE,
    PAGE_SIZE_OPTIONS,
    CashFlowTransactionForm,
    TransactionFilterForm,
)
from django_cash_flow_manager.cashflows.transactions.selectors import (
    get_transaction_filter_options,
    get_transaction_queryset,
)


@require_safe
def transaction_list(request: HttpRequest) -> HttpResponse:
    filter_form = TransactionFilterForm(data=request.GET)
    filters = filter_form.cleaned_data if filter_form.is_valid() else {}
    page_size = filters.get('page_size', DEFAULT_PAGE_SIZE)
    paginator = Paginator(get_transaction_queryset(filters), page_size)
    page_obj = paginator.get_page(filters.get('page'))
    context = {
        'transactions': page_obj.object_list,
        'page_obj': page_obj,
        'page_size': page_size,
        'page_size_options': PAGE_SIZE_OPTIONS,
        'filters': request.GET,
        **get_transaction_filter_options(),
    }
    return render(request, 'cashflows/transaction_list.html', context)


@require_http_methods(['GET', 'POST'])
def transaction_create(request: HttpRequest) -> HttpResponse:
    form = CashFlowTransactionForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Запись ДДС создана')
        return redirect('cashflows:transaction-list')
    return render(request, 'cashflows/transaction_form.html', {'form': form, 'title': 'Создать запись ДДС'})


@require_http_methods(['GET', 'POST'])
def transaction_update(request: HttpRequest, pk: int) -> HttpResponse:
    transaction = get_object_or_404(CashFlowTransaction, pk=pk)
    form = CashFlowTransactionForm(request.POST if request.method == 'POST' else None, instance=transaction)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Запись ДДС обновлена')
        return redirect('cashflows:transaction-list')
    return render(request, 'cashflows/transaction_form.html', {'form': form, 'title': 'Редактировать запись ДДС'})


@require_http_methods(['GET', 'POST'])
def transaction_delete(request: HttpRequest, pk: int) -> HttpResponse:
    transaction = get_object_or_404(CashFlowTransaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Запись ДДС удалена')
        return redirect('cashflows:transaction-list')
    return render(request, 'cashflows/confirm_delete.html', {'object': transaction, 'title': 'Удалить запись ДДС'})
