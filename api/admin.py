from django.contrib import admin
from api.models import Customer, Meter, MeterType, Account_Asset_Link, Consumption, Rate
# Register your models here.

admin.site.register(Customer)
admin.site.register(Meter)
admin.site.register(MeterType)
admin.site.register(Account_Asset_Link)
admin.site.register(Consumption)
admin.site.register(Rate)