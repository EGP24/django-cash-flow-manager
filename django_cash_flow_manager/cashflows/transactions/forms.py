from typing import Any, cast

from django import forms

from django_cash_flow_manager.cashflows.models import CashFlowTransaction, Category, Subcategory
from django_cash_flow_manager.cashflows.rules import validate_transaction_dependencies


PAGE_SIZE_OPTIONS = (10, 25, 50)
DEFAULT_PAGE_SIZE = 25


class OptionalIntegerField(forms.IntegerField):
    def to_python(self, value: Any) -> int | None:
        if value in self.empty_values:
            return None
        try:
            return int(value)
        except TypeError, ValueError:
            return None


class PageSizeField(OptionalIntegerField):
    def to_python(self, value: Any) -> int:
        parsed_value = super().to_python(value)
        return parsed_value if parsed_value in PAGE_SIZE_OPTIONS else DEFAULT_PAGE_SIZE


class TransactionFilterForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    status = OptionalIntegerField(required=False)
    type = OptionalIntegerField(required=False)
    category = OptionalIntegerField(required=False)
    subcategory = OptionalIntegerField(required=False)
    page = forms.CharField(required=False)
    page_size = PageSizeField(required=False)


class CashFlowTransactionForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = CashFlowTransaction
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        category_field = cast('forms.ModelChoiceField[Any]', self.fields['category'])
        subcategory_field = cast('forms.ModelChoiceField[Any]', self.fields['subcategory'])
        category_field.queryset = Category.objects.none()
        subcategory_field.queryset = Subcategory.objects.none()

        if self.data:
            category_field.queryset = Category.objects.all()
            subcategory_field.queryset = Subcategory.objects.all()
            return

        type_id = self.data.get('type') or getattr(self.instance, 'type_id', None)
        category_id = self.data.get('category') or getattr(self.instance, 'category_id', None)

        if type_id:
            category_field.queryset = Category.objects.filter(type_id=type_id).order_by('name')

        if category_id:
            subcategory_field.queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean() or {}
        transaction_type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        validate_transaction_dependencies(
            type_id=transaction_type.id if transaction_type else None,
            category_id=category.id if category else None,
            category_type_id=category.type_id if category else None,
            subcategory_category_id=subcategory.category_id if subcategory else None,
        )

        return cleaned_data
