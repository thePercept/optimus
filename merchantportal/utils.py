
from django.shortcuts import render,redirect
from merchantportal.forms import FoodAndBeveragesInventoryForm,TravelAndHotelsInventoryForm
from entrypoint.models import ActiveMerchants
from . models import FoodAndBeveragesInventory,TravelAndHotelsInventory



def inventoryFormGenerator(merchant_id):


    merchant_instance = ActiveMerchants.objects.get(m_id=merchant_id)
    print (merchant_instance.merchant_name)

    if merchant_instance.merchant_category == 'fnb':
        print ("FNB")
        return FoodAndBeveragesInventoryForm()
    elif merchant_instance.merchant_category == 'travelnhotels':
        print ("Travel N Hotels")
        return TravelAndHotelsInventoryForm()
    elif merchant_instance.merchant_category == 'spansaloon':
         print ("Spa n SAlon")
    elif merchant_instance.merchant_category == 'activities':
         print ("Activities")
    elif merchant_instance.merchant_category == 'instore':
         print ("Instore")
    elif merchant_instance.merchant_category == 'others':
         print ("Others")
    else:
         print ("The category is not yet assigned :: Upload data ")
         return None

# def inventoryFormForPost(merchant_id,request):
#     merchant_instance = ActiveMerchants.objects.get(m_id=merchant_id)

#     if merchant_instance.merchant_category == 'fnb':
#         print ("FNB POST preparing to save ......")
#         inventory_form=FoodAndBeveragesInventoryForm(request.POST)

#         if inventory_form.is_valid():
#             print ("Okay ..inside if form is vvalid")
#             i_name = inventory_form.cleaned_data['item_name']
#             i_quantity = inventory_form.cleaned_data['quantity']
#             i_price = inventory_form.cleaned_data['price']
#             i_description = inventory_form.cleaned_data['description']
#             fnb_inventory_instance = FoodAndBeveragesInventory(merchant = MerchantInventory.objects.get(merchant = merchant_instance) ,item_name=i_name,quantity=i_quantity,price=i_price,description=i_description)
#             fnb_inventory_instance.save()
#             return redirect('/merchants/inventory/%s'%merchant_id)
#         return print("Error Occured while saving in FnB data")


#     elif merchant_instance.merchant_category == 'travelnhotels':
#         inventory_form=TravelAndHotelsInventoryForm(request.POST)

#         if inventory_form.is_valid():
#             print ("Okay ..inside if form is vvalid")
#             i_offer = inventory_form.cleaned_data['offer']
#             i_no_of_people = inventory_form.cleaned_data['no_of_people']
#             i_price = inventory_form.cleaned_data['price']
#             i_description = inventory_form.cleaned_data['description']
#             travelnhotels_inventory_instance = TravelAndHotelsInventory(merchant = MerchantInventory.objects.get(merchant = merchant_instance) ,offer=i_offer,no_of_people=i_no_of_people,price=i_price,description=i_description)
#             travelnhotels_inventory_instance.save()
#             return redirect('/merchants/inventory/%s'%merchant_id)

#     elif merchant_instance.merchant_category == 'spansaloon':
#          print ("Spa n SAlon POST")
#     elif merchant_instance.merchant_category == 'activities':
#          print ("Activities POST")
#     elif merchant_instance.merchant_category == 'instore':
#          print ("Instore POST")
#     elif merchant_instance.merchant_category == 'others':
#          print ("Others POST")
#     else:
#          print ("The category is not yet assigned for POST :: Upload data ")
#          return None

def inventoryInstanceGenerator(merchant_id):
        merchant_instance = ActiveMerchants.objects.get(m_id=merchant_id)
        inventory_instance = None
        try:
            inventory_instance = MerchantInventory.objects.get(merchant = merchant_instance)
        except :
            print("Inventory doesn't exist")
        
        if merchant_instance.merchant_category == 'fnb':
            inv = FoodAndBeveragesInventory.objects.filter(merchant=inventory_instance)
            print ("Getting FnB inventory of this merchant")
            if inv is not None:
                print("FNB Inventory exists")
            else:
                print("doesn't exist")
                inv = None
            return inv

        elif merchant_instance.merchant_category == 'travelnhotels':
            inv = TravelAndHotelsInventory.objects.filter(merchant=inventory_instance)
            print ("Travel N Hotels POST")
            print (inventory_instance)
            if inv is not None:
                print("Travel inv exists !!!")
                #print(inv.offer)
            else:
                print("Travel inv doesn't exist")
                inv = None
            return inv


        elif merchant_instance.merchant_category == 'spansaloon':
             print ("Spa n SAlon POST")
        elif merchant_instance.merchant_category == 'activities':
             print ("Activities POST")
        elif merchant_instance.merchant_category == 'instore':
             print ("Instore POST")
        elif merchant_instance.merchant_category == 'others':
             print ("Others POST")
        else:
             print ("The category is not yet assigned for POST :: Upload data ")
             return None

def dealCategoryFormGenerator(merchant_id):
    merchant_instance = ActiveMerchants.objects.get(m_id=merchant_id)
    print ("Inside dealCategoryFormGenerator")

    if merchant_instance.merchant_category == 'fnb':
        print ("FNB Deal Form requested")
        return FoodAndBeveragesDealItemForm()
    elif merchant_instance.merchant_category == 'travelnhotels':
        print ("Travel N Hotels Deal Form requested")
        return TravelAndHotelsDealsForm()
    elif merchant_instance.merchant_category == 'spansaloon':
         print ("Spa n SAlon Deal Form Requested")
    elif merchant_instance.merchant_category == 'activities':
         print ("Activities Deal Form Requested")
    elif merchant_instance.merchant_category == 'instore':
         print ("Instore Deal Form Requested")
    elif merchant_instance.merchant_category == 'others':
         print ("Others Deal Form Requested")
    else:
         print ("No Deal Form is present ... Error occured")
         return None
def dealCategoryFormForPost(merchant_id,request):
    merchant_instance = ActiveMerchants.objects.get(m_id=merchant_id)

    if merchant_instance.merchant_category == 'fnb':
        print ("FNB DEAl POST preparing to save ......")
        fnb_deal_form=FoodAndBeveragesDealsForm(request.POST)

        if inventory_form.is_valid():
            print ("Okay ..inside if form is vvalid")
            i_old_price = inventory_form.cleaned_data['old_price']
            i_new_price = inventory_form.cleaned_data['new_price']
            i_description = inventory_form.cleaned_data['description']
            fnb_deal_instance = FoodAndBeveragesDeals(merchant = MerchantInventory.objects.get(merchant = merchant_instance) ,item_name=i_name,quantity=i_quantity,price=i_price,description=i_description)
            fnb_deal_instance.save()
            return redirect('/merchants/inventory/%s'%merchant_id)
        return print("Error Occured while saving in FnB data")


    elif merchant_instance.merchant_category == 'travelnhotels':
        inventory_form=TravelAndHotelsInventoryForm(request.POST)

        if inventory_form.is_valid():
            print ("Okay ..inside if form is vvalid")
            i_offer = inventory_form.cleaned_data['offer']
            i_no_of_people = inventory_form.cleaned_data['no_of_people']
            i_price = inventory_form.cleaned_data['price']
            i_description = inventory_form.cleaned_data['description']
            travelnhotels_inventory_instance = TravelAndHotelsInventory(merchant = MerchantInventory.objects.get(merchant = merchant_instance) ,offer=i_offer,no_of_people=i_no_of_people,price=i_price,description=i_description)
            travelnhotels_inventory_instance.save()
            return redirect('/merchants/inventory/%s'%merchant_id)

    elif merchant_instance.merchant_category == 'spansaloon':
         print ("Spa n SAlon POST")
    elif merchant_instance.merchant_category == 'activities':
         print ("Activities POST")
    elif merchant_instance.merchant_category == 'instore':
         print ("Instore POST")
    elif merchant_instance.merchant_category == 'others':
         print ("Others POST")
    else:
         print ("The category is not yet assigned for POST :: Upload data ")
         return None
