from django import forms

from django_cash_flow_manager.cashflows.models import Category


class CategoryForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = Category
        fields = ['type', 'name']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
