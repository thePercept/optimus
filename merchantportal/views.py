import json
from django.shortcuts import render,redirect
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from optimus import settings
from django.contrib.auth.models import User
from entrypoint.models import ActiveMerchants,DealAccounts
from merchantportal.forms import FoodAndBeveragesInventoryForm,TravelAndHotelsInventoryForm,LoginForm,DealMetaForm,VideoForm
from django.contrib.auth.decorators import login_required
from . utils import inventoryFormGenerator,inventoryInstanceGenerator,dealCategoryFormGenerator,dealCategoryFormForPost
from django.forms.models import modelformset_factory
from . models import FoodAndBeveragesDealItem,DealMeta,AdVideo
from utils.utils_b import saveToCloudinary,getVideoAds,getVouchersGrabbed,getGrabbedCount,getLiveDealsCountOfMerchants,getMerchantAdCount,getMerchantInstance,publishAndGenerateRequest,getDealMeta,dealMetaInstanceSave,getMerchantInventoryForm,getMerchantCategory,getSavedInventory
from django.core.files.storage import FileSystemStorage






def mp_login(request):
    next = request.GET.get('next','/merchants/')
    login_form = LoginForm()
    merchant = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                user_instance = User.objects.get(username=username)
                merchant_obj = ActiveMerchants.objects.get(user = user_instance)
                print(merchant_obj.merchant_name)
                login(request,user)
                request.session['logged_in_m_id'] = merchant_obj.m_id
                return HttpResponseRedirect(next)
            else:
                HttpResponse("Inactive User")
        else :
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "merchantportal/nlogin.html", {'redirect_to':next,'login_form':login_form})

def mp_logout(request):
    logout(request)
    return HttpResponseRedirect('/merchants')


@login_required
def mp_index(request):
    ads_displayed=0
    voucher_grabbed_dict ={}

    if 'logged_in_m_id' in request.session:
        merchant_id = request.session['logged_in_m_id']
        # merchant_category = getMerchantCategory(merchant_id)
        print("Got the merchant Id from session!! in mp_invetory view")
        ads_displayed = getMerchantAdCount(merchant_id)
        live_deals_count = getLiveDealsCountOfMerchants(merchant_id)
        grabbed = getGrabbedCount(merchant_id)
        voucher_grabbed_dict = getVouchersGrabbed(merchant_id)
        print("Voucher LISTS ::>>",voucher_grabbed_dict)
        

        
    else:
        print("Error::: Merchant is not logged in . Logout from Admin")      

    return render(request,"merchantportal/nindex.html",{'ads_displayed':ads_displayed,'live_deals_count':live_deals_count,'grabbed_count':grabbed,'voucher_grabbed_dict':voucher_grabbed_dict})



@login_required                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
def mp_inventory(request):
    merchant_inv_form=None
    saved_inventory = None
    # merchant_category=None
    # How can i get the form basd on category for post ??  

    if 'logged_in_m_id' in request.session:
        merchant_id = request.session['logged_in_m_id']
        # merchant_category = getMerchantCategory(merchant_id)
        print("Got the merchant Id from session!! in mp_invetory view")
        saved_inventory = getSavedInventory(merchant_id)
        merchant_inv_form = getMerchantInventoryForm(merchant_id,request)


    else:
        print("Error::: Merchant is not logged in . Logout from Admin")  

    return render(request,"merchantportal/ninventory.html",{'merchant_inv_form':merchant_inv_form,'saved_inventory':saved_inventory,'total_items':len(json.loads(saved_inventory))})


   
@login_required
def mp_deals(request):
    merchant_inv_form=None
    saved_inventory = None
    # merchant_category=None
    # How can i get the form basd on category for post ??  

    if 'logged_in_m_id' in request.session:
        merchant_id = request.session['logged_in_m_id']
        # merchant_category = getMerchantCategory(merchant_id)
        print("Got the merchant Id from session!! in mp_invetory view")
        saved_inventory = getSavedInventory(merchant_id)
        merchant_inv_form = getMerchantInventoryForm(merchant_id,request)


    else:
        print("Error::: Merchant is not logged in . Logout from Admin")      

    return render(request,"merchantportal/ndeals.html",{'saved_inventory':saved_inventory})




@login_required
def mp_deals_add_info_new(request):

    saved_inventory = None



    print("INSIDE NEW METHOD")
    if 'logged_in_m_id' in request.session:
        merchant_id = request.session['logged_in_m_id']
        print("USER IS LOGGED IN")   

        saved_inventory = getSavedInventory(merchant_id)
        merchant_inv_form = getMerchantInventoryForm(merchant_id,request)

        if request.is_ajax():
            print("AJAX Request")

            body_unicode = request.body.decode('utf-8')
            parsed=json.loads(body_unicode)
            print(parsed['old_price'])


            d_items = parsed['items']
            d_title = parsed['title']
            d_old_price = parsed['old_price']
            d_new_price = parsed['new_price']
            print("META INFO:",d_title," ||||||",d_old_price,d_new_price)
            meta ={}
            # here adding merchant id
            meta["merchant_id"] = merchant_id
            meta["deal_title"] = d_title
            meta["old_price"] = d_old_price
            meta["new_price"] = d_new_price     
            meta["item_image_1"] = "http://lorempixel.com/200/200/food/"

            # Save Deal Meta  and get the UUID
            deal_uuid=dealMetaInstanceSave(meta)
           
            deal_meta_instance =getDealMeta(deal_uuid)


            print("WHATS IN HERE??",d_items)

            val = {}
            pack_deal_list= []


            for items in d_items:
                print("INDI",items)
                val["deal_meta"] = deal_meta_instance
                val["di_item"]=items[0]
                val["di_quantity"]=int(items[1])
                val["dil_price"]=int(items[2])
                #val["description"]=items[3]
                pack_deal_list.append(val)
                print(val)                
                val = {}       

            print(pack_deal_list)

            # Pass all the deal items / save it in Models
            for deal_list_items in pack_deal_list:

                inst = FoodAndBeveragesDealItem(**deal_list_items)
                inst.save()
                print("DEAL ITEMS SAVED::",inst)
            # Now,  create publish and create a New Deal Request 
            publishAndGenerateRequest(deal_uuid,merchant_id)
            print("PUBLISHING DEAL IN THE TABLE NOW and Rendering back to DEALS PAGE")

            

            response = {'status':1,'message':"OK, Deals Published",'url':'/merchants/'}

            return HttpResponse(json.dumps(response),content_type= 'application/json')        
            #return render(request,"merchantportal/ndeals.html",{'saved_inventory':saved_inventory})          


    else:
        print("NOT A LOGGED IN USER")
    return render(request,"merchantportal/ndeals_add_info.html")
















@login_required
def mp_deal_creation_steps(request):
    merchant_obj = None
    deal_meta_form = None
    #deal_category_form = None
    formset = None
    deal_item_instance = None

    if 'logged_in_m_id' in request.session :
        merchant_id = request.session['logged_in_m_id']
        print("Lets check if deal creation steps function is getting merchant id or not ;/")
        print(merchant_id)
        merchant_obj = ActiveMerchants.objects.get(m_id=merchant_id)
        deal_meta_form = DealMetaForm()
        print("Got the deal meta form..")
        print(deal_meta_form)
        json_data=json.loads(request.body)
        print(json_data)

        if merchant_obj.merchant_category == 'fnb':
            print("Got the FNB")
            DealItemFormSet = modelformset_factory(model = FoodAndBeveragesDealItem,form=FoodAndBeveragesDealItemForm,extra=0)
            formset = DealItemFormSet()
            print(formset)
            print("POST should check ")

        #deal_category_form = dealCategoryFormGenerator(merchant_id)
        if request.method == 'POST':
            formset = DealItemFormSet(request.POST)
            deal_meta_form = DealMetaForm(request.POST)
            #print(deal_meta_form)
            if deal_meta_form.is_valid():
                print("Deal Meta form is valid ......Stting values")
                d_id = "random-1234"
                d_title = deal_meta_form.cleaned_data['deal_title']
                print(d_title)
                d_item_image_1 = "random/image/address/dummy1.jpg"
                d_item_image_2 = "random/image/address/dummy2.jpg"
                d_old_price = "1000"
                d_new_price = "400"
                deal_owner_inst=DealAccounts.objects.get(merchant=merchant_obj)
                meta_instance = DealMeta(deal_owner=deal_owner_inst,deal_id=d_id,deal_title=d_title,item_image_1=d_item_image_1,item_image_2=d_item_image_2,old_price=d_old_price,new_price=d_new_price)
                print("Trying to save values")
                meta_instance.save()
                print("Saving MEta.........")
            else:
                print("Error Happened !!!")
                print(deal_meta_form.errors)
            #print("saving meta ?? Let's see")

            for form in formset.forms:
                if form.is_valid():
                    print(form)
                    print("INSIDE for loop and now lets save the item FnB here......")
                    f = form.cleaned_data
                    print(f)
                    fnb_item = f.get('deal_items')
                    print(fnb_item)
                    deal_owner_inst=DealAccounts.objects.get(merchant=merchant_obj)
                    print(deal_owner_inst)

                    deal_meta_inst = DealMeta.objects.get(deal_owner=deal_owner_inst)
                    deal_item_instance = FoodAndBeveragesDealItem(deal_meta =deal_meta_inst,deal_item=fnb_item)
                    deal_item_instance.save()
                    print("Saving deal ITEM---FNB")

                    #print ("You've picked {0}".format(form.cleaned_data['deal_items']))

        return render(request,'merchantportal/deal_creation_steps.html',{'deal_meta_form':deal_meta_form,'merchant_obj':merchant_obj,'formset':formset})



def add_deal_item_form(request):
    print("add_deal_item_form funtion called....")
    if 'logged_in_m_id' in request.session :
        merchant_id = request.session['logged_in_m_id']
        print("Lets get a DealItem Form based on id and category")
        print(merchant_id)
        merchant_obj = ActiveMerchants.objects.get(m_id=merchant_id)
        deal_category_form = dealCategoryFormGenerator(merchant_id)
        print(deal_category_form)
    return render(request,'merchantportal/dummy_page.html',{deal_category_form:'deal_category_form'})


def add_category(request,merchant_id):
    pass

@login_required
def mp_adverts(request):
    video_form = VideoForm()
    ad_video_list = None

    if 'logged_in_m_id' in request.session:
        merchant_id=request.session['logged_in_m_id']

        if request.method == 'GET':
            ad_video_list = getVideoAds(merchant_id)
            print(merchant_id)
        else:
            video_form = VideoForm(request.POST,request.FILES)
            if video_form.is_valid():


                
                video_form.save()
                

                new_vid_up = request.FILES['video']
                print(new_vid_up.name,"PRINTING ADS ?")
                
                saveToCloudinary(new_vid_up.name,merchant_id)

                return redirect('adverts')
                
    return render(request,'merchantportal/nadvertisement.html',{'ad_upload_form':video_form,'ads_list':ad_video_list})
           
                  





