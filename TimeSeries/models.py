from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=50, primary_key=True, default='error')
    currency = models.CharField(max_length=10, default='Unknown')
    longName = models.CharField(max_length=255, null=True)
    sector = models.CharField(max_length=50, null=True, blank=True)
    industry = models.CharField(max_length=50, null=True, blank=True)
    exchange = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    longBusinessSummary = models.TextField(null=True)

    def __str__(self):
        return self.symbol

