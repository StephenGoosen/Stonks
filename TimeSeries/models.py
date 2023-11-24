from django.db import models

class TimeSeriesData(models.Model):
    timestamp = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f'{self.timestamp} - {self.value}'