from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from django_cash_flow_manager.cashflows.catalogs.categories.forms import CategoryForm
from django_cash_flow_manager.cashflows.models import Category


class CategoryCreateView(SuccessMessageMixin, CreateView):  # type: ignore[type-arg]
    model = Category
    form_class = CategoryForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Категория создана'
    extra_context = {'title': 'Создать категорию'}


class CategoryUpdateView(SuccessMessageMixin, UpdateView):  # type: ignore[type-arg]
    model = Category
    form_class = CategoryForm
    template_name = 'cashflows/catalog_form.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Категория обновлена'
    extra_context = {'title': 'Редактировать категорию'}


class CategoryDeleteView(DeleteView):  # type: ignore[type-arg]
    model = Category
    template_name = 'cashflows/catalog_confirm_delete.html'
    success_url = reverse_lazy('cashflows:catalogs')
    success_message = 'Категория удалена'
    extra_context = {'title': 'Удалить справочник'}

    def form_valid(self, form: forms.Form) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


category_create = CategoryCreateView.as_view()
category_update = CategoryUpdateView.as_view()
category_delete = CategoryDeleteView.as_view()
