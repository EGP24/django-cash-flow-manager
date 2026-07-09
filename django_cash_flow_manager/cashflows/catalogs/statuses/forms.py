from django import forms

from django_cash_flow_manager.cashflows.models import CashFlowStatus


class CashFlowStatusForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = CashFlowStatus
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
