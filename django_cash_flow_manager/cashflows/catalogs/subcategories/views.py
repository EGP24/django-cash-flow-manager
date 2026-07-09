from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from django_cash_flow_manager.cashflows.catalogs.subcategories.forms import SubcategoryForm
from django_cash_flow_manager.cashflows.models import Subcategory


class SubcategoryCreateView(SuccessMessageMixin, CreateView):  # type: ignore[type-arg]
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Подкатегория создана'
    extra_context = {'title': 'Создать подкатегорию'}


class SubcategoryUpdateView(SuccessMessageMixin, UpdateView):  # type: ignore[type-arg]
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Подкатегория обновлена'
    extra_context = {'title': 'Редактировать подкатегорию'}


class SubcategoryDeleteView(DeleteView):  # type: ignore[type-arg]
    model = Subcategory
    template_name = 'cashflows/catalog_confirm_delete.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Подкатегория удалена'
    extra_context = {'title': 'Удалить справочник'}

    def form_valid(self, form: forms.Form) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


subcategory_create = SubcategoryCreateView.as_view()
subcategory_update = SubcategoryUpdateView.as_view()
subcategory_delete = SubcategoryDeleteView.as_view()
