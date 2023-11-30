from django import forms
from .models import Stock

class StockSelectionForm(forms.Form):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())
