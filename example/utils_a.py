from entrypoint.models import ActiveMerchants,DealAccounts
from merchantportal.utils import inventoryInstanceGenerator
from merchantportal.models import FoodAndBeveragesDealItem
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def getMerchantInstance(merchant_id):
    merchant_obj = ActiveMerchants.objects.get(m_id=merchant_id)
    return merchant_obj

def getLoggedInMerchantId(request):
    merchant_id = request.session['logged_in_m_id']
    #merchant_obj = getMerchantInstance(merchant_id)
    print("Returning :",merchant_id)
    return merchant_id

def getInventoryPaginated(merchant_id,request):
    inventory_obj = inventoryInstanceGenerator(merchant_id)
    inv_json = serializers.serialize("json", inventory_obj)
    if inventory_obj is not None:
        page = request.GET.get('page',1)
        paginator = Paginator(inventory_obj,10)
        try:
            inv_objs = paginator.page(page)
        except PageNotAnInteger:
            inv_objs = paginator.page(1)
        except EmptyPage:
            inv_objs = paginator.page(paginator.num_pages)
    inv_tools = [inv_objs,inv_json]

    return inv_tools

def saveInventoryItem(deal_item):
    for items in deal_item:
        inv_instance = FoodAndBeveragesDealItem(**items)
        inv_instance.save()
        print("SAVED......SAVED......SAVED......")
