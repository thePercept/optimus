from django.contrib import admin
from . models import AdVideo,DealRequestTable,FoodAndBeveragesInventory,TravelAndHotelsInventory,DealMeta,FoodAndBeveragesDealItem,TravelAndHotelsDealItem

# Register your models here.
admin.site.register(FoodAndBeveragesInventory)
admin.site.register(TravelAndHotelsInventory)
#admin.site.register(FoodAndBeveragesDeals)
admin.site.register(DealMeta)
admin.site.register(FoodAndBeveragesDealItem)
admin.site.register(TravelAndHotelsDealItem)
admin.site.register(DealRequestTable)
admin.site.register(AdVideo)
