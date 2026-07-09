from django import forms

from django_cash_flow_manager.cashflows.models import Subcategory


class SubcategoryForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = Subcategory
        fields = ['category', 'name']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
