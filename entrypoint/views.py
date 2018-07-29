import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from api.models import LiveDeals
from entrypoint.models import MerchantCategoryChoices,ActiveMerchants,RedemptionAddress,Document,DealAccounts,PlanSold,Dummy
from entrypoint.forms import DummyForm,PlanPurchasedForm,DocumentForm,CreateDealAccountForm,LoginForm,BasicDetails,BusinessAddress,RedemptionAddress,PlanPurchased
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from optimus import settings
from django.contrib.auth.decorators import login_required
from utils.utils_b import createAdAccount,getDealBannerDetails,makeDealLive,getMerchantListForTable,getQADoneCount,getTotalDealRequest,getMerchantInstance,getDealRequest,getAllMerchants,getRedemptionDetailsInstance,getDealAccountId,getPlanName,convertListToJson,getActiveMerchantCount,uploadCsv,getBusinessAddressInstance,getRedemptionAddressInstance,getPlanPurchased,getPlanInstance,createDealAccount
from django.core.mail import EmailMessage
from multiprocessing import Pool as ThreadPool



def ep_login(request):
    next = request.GET.get('next','/optimus/')
    login_form = LoginForm()
    merchant = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(next)
            else:
                HttpResponse("Inactive User")
        else :
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "entrypoint/nlogin.html", {'redirect_to':next,'login_form':login_form})


def update(i):
    i=i+1
    print(threading.get_ident(),i)
    


def ep_ads(request):
    # i=77
    # if request.is_ajax():
    #     a = threading.Thread(target =update(i) )
    #     b = threading.Thread(target =update(i) )
    #     c = threading.Thread(target =update(i) )
    #     d = threading.Thread(target =update(i) )
    #     a.start()
    #     b.start()
    #     c.start()
    #     d.start()
    #     return render(request,'entrypoint/nindex.html',{'i':i})   
    pass

def upload_data(request):
    upload_dummy_data = DummyForm()

    if request.method == 'POST':
        form = DummyForm(request.POST,request.FILES)
        if form.is_valid():
            f= open('media/dummydeals/dummy_deals_csv.csv','r')
            for line in f:
                line = line.split('|')
                obj_live_deals = LiveDeals(deal_id=line[0],lat=line[1],lon=line[2],city=line[3].rstrip('\n')) 
                print(obj_live_deals)
                obj_live_deals.save()       
    return render(request,'entrypoint/uploaddata.html',{'upload_form':upload_dummy_data})                              



@login_required
#@group_required('admins') Make it work ...
def ep_index(request):
    active_merchants = ActiveMerchants.objects.all()
    upload_merchants = DocumentForm()
    deal_request_dict = {}
    merchants = getAllMerchants()
    total_merchants=len(merchants)
    deal_requests = getTotalDealRequest()
    total_deals_requests = len(deal_requests)
    qadone = len(getQADoneCount())



    if request.method == 'POST':
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():

            form.save()
            f = open('media/mastercsv/master_file.csv','r')
            for line in f:
                line = line.split(',')
                obj_active_merchant = ActiveMerchants()
                unique_id = uuid.uuid4().hex[:6].upper()
                unique_id_final  = "".join(("M",unique_id))
                obj_active_merchant.m_id = unique_id_final
                obj_active_merchant.merchant_category = line[1]
                obj_active_merchant.merchant_name = line[2]
                obj_active_merchant.merchant_email = line[3]
                obj_active_merchant.save()
            f.close()
            return redirect('/optimus/')
    else:
        print("Inside ep_index:GETrequest")
        deal_request_dict=getDealRequest()

        print("OBTAINED deal_request_dict",deal_request_dict)

    return render(request,'entrypoint/nindex.html',{'upload_form':upload_merchants,'deal_request_dict':deal_request_dict,'total_merchants':total_merchants,'active_merchants':getActiveMerchantCount(),'total_deals_requests':total_deals_requests,'qadone':qadone})

@login_required
def ep_merchants(request):

    merchants = getAllMerchants()
    total_merchants=len(merchants)
    merchant_data_list = [] 
    merchant_data = []
    merchants_json_data=None

    upload_merchants = DocumentForm()
    if(request.method=='GET'):
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(getMerchantListForTable)
        merchant_data_list = async_result.get()

        print("LETS SEE THE LIST TO BE JSONIFIED NEXT",merchant_data_list)   

        merchants_json_data=convertListToJson(merchant_data_list)

        print("Inside Get Request ,printing JSON data",merchants_json_data,"Total : Merchants::total_merchants")
    
    if(request.method=='POST'):
        print("Inside POST request","Uploading CSV")   
        uploadCsv(request) 
    return render(request,'entrypoint/nmerchants.html',{'merchants_json_data':merchant_data_list,'total_merchants':total_merchants  ,'active_merchants':getActiveMerchantCount(),'upload_form':upload_merchants})

@login_required
def ep_merchant_page(request,merchant_id):
    print("Inside EP_MERCHANT_PAGE and now printing all merchant by category FNB :::")
    temp=ActiveMerchants.objects.all().filter(merchant_category="fnb")
    for obj in temp:
        print(obj.m_id)
    print(temp)
    
    basic_form_data = {}
    business_form_data = {}
    redemption_form_data = {}
    plan_form_data = {}

    basic_details_instance = getMerchantInstance(merchant_id)
    business_address_instance = getBusinessAddressInstance(merchant_id)
    redemption_address_instance = getRedemptionAddressInstance(merchant_id)
    plan_purchased_instance = getPlanInstance(merchant_id)

    m_name = basic_details_instance.merchant_name
    m_id = basic_details_instance.m_id
    m_category = basic_details_instance.merchant_category
    m_email = basic_details_instance.merchant_email
    m_onboarding_date = basic_details_instance.onboarded_date
    m_deal_acc_status = basic_details_instance.deal_account_status

    if business_address_instance is None:
        print("Business Address is None")
        m_buss_add_l_one = ""
        m_buss_add_l_two = ""
        m_buss_city = ""
        m_buss_state = ""
    else :    
        m_buss_add_l_one = business_address_instance.address_line_one
        m_buss_add_l_two = business_address_instance.address_line_two
        m_buss_city = business_address_instance.city
        m_buss_state = business_address_instance.state

    if redemption_address_instance is None : 
        m_red_add_l_one = ""
        m_red_add_l_two = ""
        m_red_add_lat = ""
        m_red_add_lon = ""
        m_red_add_sublocality = ""
        m_red_add_city = ""
        m_red_add_state = ""
    else:
        print(redemption_address_instance)
        m_red_add_l_one = redemption_address_instance.address_line_one
        m_red_add_l_two = redemption_address_instance.address_line_two
        m_red_add_lat = redemption_address_instance.lat
        m_red_add_lon = redemption_address_instance.lon
        m_red_add_sublocality = redemption_address_instance.sublocality
        m_red_add_city = redemption_address_instance.city
        m_red_add_state = redemption_address_instance.state


    if  plan_purchased_instance is None : 

        m_plan_name = ""
        m_plan_duration = ""
        m_plan_paid_amount  = ""
        m_plan_payement_method = ""
        m_plan_payement_memo  = ""
        m_plan_start_date = ""
        m_plan_end_date = ""          

    else:

        m_plan_name = plan_purchased_instance.plan_name
        m_plan_duration = plan_purchased_instance.plan_duration
        m_plan_paid_amount  = plan_purchased_instance.paid_amount 
        m_plan_payement_method = plan_purchased_instance.payement_method
        m_plan_payement_memo  = plan_purchased_instance.payement_memo 
        m_plan_start_date = plan_purchased_instance.start_date
        m_plan_end_date = plan_purchased_instance.end_date        

        print("Checking Plan Purchased data here >>>>",plan_purchased_instance)

##
    basic_form_data["merchant_name"] = m_name
    basic_form_data["merchant_ID"] =m_id
    basic_form_data["merchant_category"] =m_category
    basic_form_data["email"] = m_email
    basic_form_data["onboarding_date"] = m_onboarding_date
    basic_form_data["deal_account_status"] = m_deal_acc_status

    business_form_data["business_address_line_1"] = m_buss_add_l_one
    business_form_data["business_address_line_2"] = m_buss_add_l_two
    business_form_data["city"] = m_buss_city
    business_form_data["state"] = m_buss_state

    redemption_form_data["redemption_address_line_1"] = m_red_add_l_one
    redemption_form_data["redemption_address_line_2"] = m_red_add_l_two
    redemption_form_data["city"] = m_red_add_city
    redemption_form_data["state"] = m_red_add_state
    redemption_form_data["lat"] = m_red_add_lat
    redemption_form_data["lon"] = m_red_add_lon
    redemption_form_data["sublocality"] = m_red_add_sublocality

    plan_form_data["plan_name"] = m_plan_name
    plan_form_data["plan_duration"] = m_plan_duration
    plan_form_data["payement_method"] = m_plan_payement_method
    plan_form_data["paid_amount"] = m_plan_paid_amount
    plan_form_data["plan_started"] = m_plan_start_date
    plan_form_data["plan_ends"] = m_plan_end_date
    plan_form_data["payement_memo"] = m_plan_payement_memo

    
    basic_detail_form = BasicDetails(basic_form_data)
    buss_detail_form = BusinessAddress(business_form_data)
    redempt_detail_form = RedemptionAddress(redemption_form_data)
    plan_detail_form = PlanPurchased(plan_form_data)

    update_verification_form = PlanPurchasedForm(plan_form_data)


    if request.method=='GET':
        merchant_instance = getMerchantInstance(merchant_id)
        print("Merchant clicked is :",merchant_instance.merchant_name)
        return render(request,'entrypoint/nmerchantpage.html',{'update_verification_form':update_verification_form,'basic_detail_form':basic_detail_form,'buss_detail_form':buss_detail_form,'redempt_detail_form':redempt_detail_form,'plan_detail_form':plan_detail_form})
    else :
        if 'SAVE' in request.POST:
            plan_purchased_form = PlanPurchasedForm(request.POST)
            idx = request.POST['idx']

            print("---------------+++++++++++Inside desired method",idx)
            # So finally getting the merchant ID from the template to view
            # see LOG
            if plan_purchased_form.is_valid():
                m_id = plan_purchased_form.cleaned_data['idx']
                plan_name = plan_purchased_form.cleaned_data['plan_name']
                plan_duration = plan_purchased_form.cleaned_data['plan_duration']
                paid_amount = plan_purchased_form.cleaned_data['paid_amount']
                payement_method = plan_purchased_form.cleaned_data['payement_method']
                payement_memo = plan_purchased_form.cleaned_data['payement_memo']
                print("Valid Form",m_id,plan_name,plan_duration,paid_amount,payement_method,m_plan_payement_memo)

                plan_obj = PlanSold(merchant=getMerchantInstance(m_id),plan_name = plan_name,plan_duration = plan_duration,paid_amount = paid_amount,payement_method = payement_method,payement_memo = payement_memo)
                plan_obj.save()
                user_details=createDealAccount(merchant_id)
                createAdAccount(merchant_id)
                body = "Your User Name : %s and Password %s. \nLogin using this link : http://139.59.38.184/merchants/  " %(user_details['user_id'],user_details['password'])
                email = EmailMessage('BizzInno merchant account generated', body, to=['dev.bizzinnostrategist@gmail.com'])
                print("EMAIL & PASS generated :" ,user_details['user_id']," : ",user_details['password'])
                email.send()
                return redirect('/optimus/')


                # plan_obj, created = PlanSold.objects.update_or_create(
                #      merchant=getMerchantInstance(m_id), defaults={"plan_name": plan_name,"plan_duration":plan_duration,"paid_amount":paid_amount,"payement_method":payement_method,"payement_memo":payement_memo}
                #     )
                # if created:
                #     print("Adding a new plan for this merchant ",plan_obj)
                # else:

                #     print("Plan exists for this merchant ....Now Updating",plan_obj)   
                #    # plan_obj.save() 



            else:
                print("INVALID >>>>>>>>>>>>>>>>>",plan_purchased_form.errors)   
                return redirect('/optimus/')



@login_required
def ep_verify_deal_step_one(request):
    m_id = None
    deal_id = None

    if request.is_ajax():
        if request.method == 'POST':
            print("ITS A POST REQUEST inside AJAX no grabbing DEAL ID & MERCHANT ID")

            body_unicode = request.body.decode('utf-8')
            #data = request.GET
            parsed_data=json.loads(body_unicode)      
            m_id=parsed_data['merchant_id']
            deal_id = parsed_data['deal_id']
            print("DATA is PArsed now",parsed_data)    
            print("DEAL & MERCHANT ID",m_id,":",deal_id)   

            deal_content_dict=getDealBannerDetails(deal_id,m_id)


            response = deal_content_dict
            return HttpResponse(json.dumps(response),content_type= 'application/json')                     
        else:
            print("ITS A GET REQUEST")
          
    else:
        if 'VERIFY_DEAL' in request.POST:
            print("DEAL GOING LIVE  IDS ARE !!",m_id,"::",deal_id)


@login_required
def ep_verify_deal_step_two(request):
    m_id = None
    deal_id = None

    if request.is_ajax():
        if request.method == 'POST':
            print("1.)  ")

            body_unicode = request.body.decode('utf-8')
            #data = request.GET
            parsed_data=json.loads(body_unicode)      
            m_id=parsed_data['merchant_id']
            deal_id = parsed_data['deal_id']
            print("Calling makeDealLive now !!")
            makeDealLive(deal_id,m_id)


        else:
            print("ITS A GET REQUEST")
    else:
        pass


