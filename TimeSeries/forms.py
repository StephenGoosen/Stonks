from django import forms
from .models import Stock

class StockSelectionForm(forms.Form):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())

class StockForm(forms.Form):
    stock_symbol = forms.CharField(label='Stock Symbol', max_length=10)
    num_years = forms.IntegerField(label='Number of Years', min_value=1)
