from django.db import models
from django.utils import timezone

class Cities(models.Model):
    city = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.city

class WeatherData(models.Model):
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=5)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.city.city} - {self.timestamp}'
