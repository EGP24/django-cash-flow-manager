from django import forms

from django_cash_flow_manager.cashflows.models import CashFlowType


class CashFlowTypeForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = CashFlowType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
