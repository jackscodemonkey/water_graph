from django.db import models
from django.utils import timezone

# Create your models here.
class Customer(models.Model):

    first_name = models.TextField(null=False, blank=False,)
    last_name = models.TextField(null=False, blank=False,)

class MeterType(models.Model):
    class Meta:
        unique_together = (('meter_model','meter_vendor'),)

    meter_model = models.TextField(null=False, blank=False)
    meter_vendor = models.TextField(null=False, blank=False)

class Meter(models.Model):
    meter_type = models.ForeignKey(MeterType, null=False, on_delete=models.CASCADE)
    meter_serial = models.TextField(null=False, blank=False, unique=True)
    install_date = models.DateTimeField(null=False, blank=False, auto_now=True)
    retire_date = models.DateTimeField(null=True, blank=False)

class Account_Asset_Link(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, null=False)

class Consumption(models.Model):
    MEASURE = (
        ('L', 'Liter'),
        ('G', 'Gallon')
    )
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    read_time = models.DateTimeField(null=False, blank=False)
    reading = models.BigIntegerField(null=False, blank=False)
    unit_of_measure = models.CharField(max_length=1, choices=MEASURE)

class Rate(models.Model):
    MEASURE = (
        ('L', 'Liter'),
        ('G', 'Gallon')
    )
    rate = models.DecimalField(blank=False, max_digits=5, decimal_places=4)
    effective_start = models.DateField(null=False, blank=False)
    effective_end = models.DateField(null=True, blank=False,)
    unit_of_measure = models.CharField(max_length=1, choices=MEASURE)
