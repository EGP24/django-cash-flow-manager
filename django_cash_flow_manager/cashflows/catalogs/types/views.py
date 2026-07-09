from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from django_cash_flow_manager.cashflows.catalogs.types.forms import CashFlowTypeForm
from django_cash_flow_manager.cashflows.models import CashFlowType


class TypeCreateView(SuccessMessageMixin, CreateView):  # type: ignore[type-arg]
    model = CashFlowType
    form_class = CashFlowTypeForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Тип создан'
    extra_context = {'title': 'Создать тип'}


class TypeUpdateView(SuccessMessageMixin, UpdateView):  # type: ignore[type-arg]
    model = CashFlowType
    form_class = CashFlowTypeForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Тип обновлен'
    extra_context = {'title': 'Редактировать тип'}


class TypeDeleteView(DeleteView):  # type: ignore[type-arg]
    model = CashFlowType
    template_name = 'cashflows/catalog_confirm_delete.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Тип удален'
    extra_context = {'title': 'Удалить справочник'}

    def form_valid(self, form: forms.Form) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


type_create = TypeCreateView.as_view()
type_update = TypeUpdateView.as_view()
type_delete = TypeDeleteView.as_view()
