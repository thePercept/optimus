from django.contrib import admin
from . models import LiveDeals,RequestedDetails,MerchantDealStats

# Register your models here.

admin.site.register(LiveDeals)
admin.site.register(RequestedDetails)
admin.site.register(MerchantDealStats)
