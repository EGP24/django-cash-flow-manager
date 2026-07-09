from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from django_cash_flow_manager.cashflows.catalogs.statuses.forms import CashFlowStatusForm
from django_cash_flow_manager.cashflows.models import CashFlowStatus


class StatusCreateView(SuccessMessageMixin, CreateView):  # type: ignore[type-arg]
    model = CashFlowStatus
    form_class = CashFlowStatusForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Статус создан'
    extra_context = {'title': 'Создать статус'}


class StatusUpdateView(SuccessMessageMixin, UpdateView):  # type: ignore[type-arg]
    model = CashFlowStatus
    form_class = CashFlowStatusForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Статус обновлен'
    extra_context = {'title': 'Редактировать статус'}


class StatusDeleteView(DeleteView):  # type: ignore[type-arg]
    model = CashFlowStatus
    template_name = 'cashflows/catalog_confirm_delete.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Статус удален'
    extra_context = {'title': 'Удалить справочник'}

    def form_valid(self, form: forms.Form) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


status_create = StatusCreateView.as_view()
status_update = StatusUpdateView.as_view()
status_delete = StatusDeleteView.as_view()
