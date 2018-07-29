from django.contrib import admin
from entrypoint.models import MerchantCategoryChoices,ActiveMerchants,DealAccounts,MerchantCategory,BusinessAddress,RedemptionAddress,PlanSold,AdvertisementAccount,VideoAdvertsMeta,Driver,DisplayTabs,Cablet,AdRequest,PowerOn,PowerOff,CabletInactive,Document
# Register your models here.
admin.site.register(MerchantCategoryChoices)
admin.site.register(ActiveMerchants)
admin.site.register(DealAccounts)
#admin.site.register(MerchantInventory)
admin.site.register(MerchantCategory)
admin.site.register(BusinessAddress)
admin.site.register(RedemptionAddress)
admin.site.register(PlanSold)
admin.site.register(AdvertisementAccount)
admin.site.register(VideoAdvertsMeta)
admin.site.register(Driver)
admin.site.register(DisplayTabs)
admin.site.register(Cablet)
admin.site.register(AdRequest)
admin.site.register(PowerOn)
admin.site.register(PowerOff)
admin.site.register(CabletInactive)

# admin.site.register(DealsByMerchants)
admin.site.register(Document)
