from django import forms
from .models import Scanner

class ScannerForm(forms.ModelForm):
    class Meta:
        model = Scanner
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Tarama yapmak istediğiniz URL'}),
        }
