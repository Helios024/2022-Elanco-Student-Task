from django.db import models

# Create your models here.
class ElancoData(models.Model):
    ConsumedQuantity = models.FloatField()
    Cost = models.FloatField()
    Date = models.DateField()
    InstanceId = models.CharField(max_length=200)
    MeterCategory = models.CharField(max_length=200)
    ResourceGroup = models.CharField(max_length=200)
    ResourceLocation = models.CharField(max_length=200)
    Tags = models.JSONField()
    UnitOfMeasure = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    ServiceName = models.CharField(max_length=200)

class Resources(models.Model):
    name = models.CharField(max_length=200)
    apiurl = models.CharField(max_length=200)