from django import forms
from .models import Equipment


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'name', 'serial_number', 'location', 'condition',
            'status', 'critical', 'last_service_date', 'next_due_date', 'notes'
        ]
        widgets = {
            'name':              forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Centrifugal Pump P-101'}),
            'serial_number':     forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. SLB-2024-00123'}),
            'location':          forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Lagos Depot - Loading Bay 2'}),
            'condition':         forms.Select(attrs={'class': 'form-select'}),
            'status':            forms.Select(attrs={'class': 'form-select'}),
            'critical':          forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'last_service_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'next_due_date':     forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes':             forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Additional remarks, fault history...'}),
        }
        labels = {
            'critical': 'Mark as Safety / Production Critical',
        }
