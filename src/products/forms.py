from django import forms
from .models import Info

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['ativo', 'email', 'inferior', 'superior', 'status', 'time_interval']

class InfoFormEditar(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['ativo', 'email', 'inferior', 'superior', 'status', 'editar_time_interval']