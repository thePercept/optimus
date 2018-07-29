import os

import json
import uuid
import datetime

from django.contrib.auth.models import User

from django.shortcuts import redirect
from entrypoint.models import ActiveMerchants,DealAccounts,BusinessAddress,RedemptionAddress,PlanSold,AdvertisementAccount,VideoAdvertsMeta
from merchantportal.models import DealRequestTable,DealMeta,FoodAndBeveragesInventory,TravelAndHotelsInventory
from api.models import MerchantDealStats,LiveDeals,RequestedDetails
from visitor.models import DealVoucherGrabbed

from entrypoint.forms import DocumentForm
from merchantportal.forms import FoodAndBeveragesInventoryForm



import cloudinary
import cloudinary.uploader
import cloudinary.api

from optimus.settings import BASE_DIR,UPLOAD_ROOT



cloudinary.config( 
  cloud_name = "devbizz", 
  api_key = "251571844322985", 
  api_secret = "qxuYrAADniT-rXiLuKToH9vNai4" 
)




"""
	Basic methods to get info* by Merchant ID

"""

def getMerchantInstance(merchant_id):
    merchant_obj = ActiveMerchants.objects.get(m_id=merchant_id)
    return merchant_obj

def getDealAccountInstance(merchant_id):
	deal_account_instance = None
	try:
		deal_account_instance = DealAccounts.objects.get(m_id=merchant_id) 
		deal_account_id=deal_account_instance.deal_acc_id
	except :
		print("Deal Account doesn't exist")
	return deal_account_instance




def getDealAccountId(merchant_id):
	deal_account_id = "None"
	try:
		deal_account_instance = DealAccounts.objects.get(merchant=getMerchantInstance(merchant_id)) 
		deal_account_id=deal_account_instance.deal_acc_id
	except :
		print("Deal Account doesn't exist")
	return deal_account_id

def getRedemptionDetailsInstance(merchant_id):
	redemption_address_complete = "None"
	try:

		redemption_address_instance = RedemptionAddress.objects.get(merchant=getMerchantInstance(merchant_id)) 
		redemption_address_complete=redemption_address_instance.address_line_one + "  ,"+redemption_address_instance.sublocality+"  ,"+redemption_address_instance.city + " " +redemption_address_instance.state
	except :
		print("Deal Account doesn't exist")
	return redemption_address_complete	

def getBusinessAddressInstance(merchant_id):
	business_address_instance = None
	try:
		print(">>>>>>>>Inside Business Add Instance ::",business_address_instance)
		merchant_instance = getMerchantInstance(merchant_id)
		business_address_instance = BusinessAddress.objects.get(merchant=merchant_instance)
	except :
		print("getBusinessAddress :: No address exist,exception")
	return business_address_instance	

def getRedemptionAddressInstance(merchant_id):
	redemption_address_instance = None
	try:
		merchant_instance = getMerchantInstance(merchant_id)
		redemption_address_instance = RedemptionAddress.objects.get(merchant=merchant_instance)
		print(">>>>>>>>Inside Rdemption Add Instance ::",redemption_address_instance)
	except :
		print("Inside Rdemption :: No address exist,...................................")
	return redemption_address_instance

def getPlanPurchased(merchant_id):
	plan_purchased_instance = None
	try:
		plan_purchased_instance =getPlanInstance(merchant_id)
	except :
		print("No pLan Exists , exception")
	return plan_purchased_instance	




"""
	Get all Merchants on the system

"""

def getAllMerchants():
	merchants = ActiveMerchants.objects.all()
	print("::utils_b:: Getting all Merchants &","the no of merchants are ",len(merchants))
	return merchants



"""
	Get All published Deal related stuff below

# """
# def getTotalDealRequest(merchant_id):
# 	deal_owner=getDealAccountInstance(merchant_id)
# 	published_deal = DealMeta.objects.get(deal_owner=deal_owner)
# 	return published_deal


# get all deals which are published by merchants and waiting for QA to be done
def getTotalDealRequest():
	all_deals_requests = DealRequestTable.objects.all()
	return all_deals_requests

# get all deals which are published by merchants and waiting for QA to be done
def getQANotDoneCount():
	all_deals_requests = DealRequestTable.objects.filter(status="notdone")
	return all_deals_requests


def getQADoneCount():
	all_deals_requests = DealRequestTable.objects.filter(status="done")
	return all_deals_requests

def getAllPublishedDealsMerchantsId():	
	published_merchant_ids = []
	all_published_deals = DealMeta.objects.all()
	for deal_metas in all_published_deals:
		published_merchant_ids.append(deal_metas.deal_owner.merchant.m_id)
	if len(published_merchant_ids)>0:
		return 	published_merchant_ids
	else :
		return None
	
def getAllPublishedDealsDealsId():	
	published_deals_ids = []
	all_published_deals = DealMeta.objects.all()
	for deal_metas in all_published_deals:
		published_deals_ids.append(deal_metas.deal_id)
	if len(published_merchant_ids)>0:
		return 	published_deals_ids
	else :
		return None

def getPlanInstance(merchant_id):
	plan_instance = None
	merchant_instance=getMerchantInstance(merchant_id)
	try:
		print("TRYING TO GET PLAN SOLD")
		plan_instance = PlanSold.objects.get(merchant=merchant_instance) 
	except :
		print("Plan is not purchased by this merchant")
	return plan_instance

def getPlanName(merchant_id):
	plan_inst = getPlanInstance(merchant_id)
	if plan_inst is None:
		plan_inst = "N/A"
		return plan_inst
	else :
		return plan_inst.plan_name	

def getActiveMerchantCount():
	total_plans_sold=len(PlanSold.objects.all())
	return total_plans_sold



def convertListToJson(array_list):
	json_string = json.dumps(array_list)
	return json_string





def uploadCsv(request):
	form = DocumentForm(request.POST,request.FILES)
	if form.is_valid():
		form.save()
		f = open('media/mastercsv/master_data_merchants.csv','r')
		for line in f:
			line = line.split('|')
			
			unique_id = uuid.uuid4().hex[:6].upper()
			unique_id_final  = "".join(("M",unique_id))

			for x in range(1,5):
				print ("LINE DETAILS-A",line[x])
			obj_active_merchant = ActiveMerchants(m_id=unique_id_final,merchant_category=line[0],merchant_name=line[1],merchant_email=line[2],personal_phone_number=line[3])
			obj_active_merchant.save()	
			print("Merchant Personal Details ......saving")

			for x in range(5,10):
				print ("LINE DETAILS-B",line[x])
			obj_business_address =BusinessAddress(merchant=getMerchantInstance(unique_id_final),address_line_one=line[4],address_line_two=line[5],city=line[6],state=line[7],business_phone_number=line[8]) 
			obj_business_address.save()
			print("Merchant Business Details ......saving")


			for x in range(10,16):
				print ("LINE DETAILS-B",line[x])
			obj_redemption_address =RedemptionAddress(merchant=getMerchantInstance(unique_id_final),address_line_one=line[9],address_line_two=line[10],sublocality=line[11],city=line[12],state=line[13],lat=line[14],lon=line[15]) 
			obj_redemption_address.save()
			print("Merchant Redemptin Details ......saving")
			

			
		f.close()  
	return redirect('/optimus/')	
	  
	  	
	  	
def createDealAccount(merchant_id):
	print("Creating DEAL ACC NOW")
	merchant_instance = getMerchantInstance(merchant_id)

    #Deal Acc Id generation
	dac_id = "-".join(("DAC",merchant_id))
	deal_account = DealAccounts(merchant=merchant_instance,deal_acc_id=dac_id,total_deals_created=0,total_active_deals=0)
	deal_account.save()
	print("Deal account created")

    # Generate and save Inventory Id
	#obj_inv =MerchantInventory()
	#inv_id = "-".join(("INV",merchant_id))
	#obj_inv.merchant = merchant_instance
	#obj_inv.inventory_id = inv_id
	#print("INV Generated")
	#obj_inv.save()



    #Generate UserId and Password
	user_id = uuid.uuid4().hex[:6].lower()
	u_name = merchant_instance.merchant_name
	u_name = u_name[:3].lower()
	user_id_final =  "".join((u_name,user_id))
	print("User Id and Pass generated")

	#Update Active Merchant for Deal Acc Status
	merchant_instance.deal_account_status = 1
	user = User.objects.create_user(username=user_id_final,email=merchant_instance.merchant_email,password=user_id_final,first_name=u_name)
	user.save()
	print("User Saved..")
	
	merchant_instance.user = User.objects.get(username=user_id_final)
	merchant_instance.save()		  
	return {'user_id':user_id_final,'password':user_id_final}

def getMerchantCategory(merchant_id):
	merchant_category = getMerchantInstance(merchant_id).merchant_category
	return merchant_category





def getMerchantInventoryForm(merchant_id,request):
	merchant_inv_form = None
	merchant_category = getMerchantInstance(merchant_id).merchant_category
	print("The category is ",merchant_category)

	if merchant_category == 'fnb':
		if request.method=='POST':
			merchant_inv_form=FoodAndBeveragesInventoryForm(request.POST)
			if merchant_inv_form.is_valid():
				data = merchant_inv_form.cleaned_data
				fnb_obj = FoodAndBeveragesInventory(merchant=getMerchantInstance(merchant_id),item_name=data['item_name'],price=data['price'],quantity=data['quantity'],description=data['description'])
				fnb_obj.save()
				print("Saving Inventory")
		else:
			merchant_inv_form=FoodAndBeveragesInventoryForm()
			print("Sending FNB Inventory Form",merchant_inv_form)

	elif merchant_category == 'travelnhotels':
		print("Sending TRAVELnHOTELS Inventory Form",merchant_inv_form)
		merchant_inv_form = TravelAndHotelsInventoryForm(request.POST)
	else :
		print("Inventory form for this category is not created yet !!")
		return merchant_inv_form
	return	merchant_inv_form	

def getSavedInventory(merchant_id):
	saved_inventories=None
	saved_inventories_list = []
	inventory = []
	saved_inventories_json=None

	print("Inside getSavedInventory")
	saved_inventories = FoodAndBeveragesInventory.objects.filter(merchant=getMerchantInstance(merchant_id))
	for inv in saved_inventories:
		#inventory["item_name"]=inv.item_name
		inventory.append(inv.item_name)
		inventory.append(inv.quantity)
		inventory.append(inv.price)
		inventory.append(inv.description)
		inventory.append("")

		saved_inventories_list.append(inventory)
		inventory = []
		print (inv,"Inside >>",inv.item_name,"Price :",inv.price,inv.quantity,)
	
	saved_inventories_json = convertListToJson(saved_inventories_list)	
	print(saved_inventories_json,len(json.loads(saved_inventories_json)))
	return saved_inventories_json
	

def dealMetaInstanceSave(meta):
	deal_id = uuid.uuid4()
	meta["deal_id"] = deal_id
	meta_inst = DealMeta(**meta)
	meta_inst.save()
	return deal_id

def getDealMeta(deal_uuid):
	deal_meta_instance = None
	try:
		deal_meta_instance = DealMeta.objects.get(deal_id=deal_uuid) 
	except :
		print("Deal META doesn't exist")
	return deal_meta_instance	

def publishAndGenerateRequest(deal_uuid,merchant_id):
	table_instance = DealRequestTable(meta=getDealMeta(deal_uuid),merchant=getMerchantInstance(merchant_id),status="notdone" )
	table_instance.save()

def getMerchantListForTable():
	merchants = getAllMerchants()
	merchant_data_list = []
	merchant_data = []	
	for merchant in merchants:
	    m_name = merchant.merchant_name
	    print("::views.py:: Merchant Name is :",m_name)
	    m_id = merchant.m_id
	    print("::views.py:: Merchant ID is :",m_id)
	    m_category = merchant.merchant_category
	    m_location = getRedemptionDetailsInstance(m_id)
	    m_deal_acc_id = getDealAccountId(m_id)
	    plan_purchased = getPlanName(m_id)
	            
	    merchant_data.append(m_id)
	    merchant_data.append(m_category)
	    merchant_data.append(m_name)
	    merchant_data.append(m_location)
	    merchant_data.append(m_deal_acc_id)
	    merchant_data.append(plan_purchased)
	    print("Lets see The data :::::::::",merchant_data)
	    merchant_data_list.append(merchant_data)
	    merchant_data=[]
	return merchant_data_list

def getLat(merchant_id):
	redemption_address = getRedemptionAddressInstance(merchant_id)
	lat = redemption_address.lat
	return lat

def getLon(merchant_id):
	redemption_address = getRedemptionAddressInstance(merchant_id)
	lon = redemption_address.lon
	return lon	

def getCity(merchant_id):
	redemption_address = getRedemptionAddressInstance(merchant_id)
	city = redemption_address.city
	return city		

def makeDealLive(deal_uuid,merchant_id):
	print("Following steps to make a deal go live :")
	print(" 1: Make the reqiest in Request table inactive ")
	table_instance = DealRequestTable.objects.filter(meta=getDealMeta(deal_uuid)).update(status="done")
	#table_instance = DealRequestTable(meta=getDealMeta(deal_uuid),merchant=getMerchantInstance(merchant_id),status="inactive" )
	#table_instance.save()	
	print("2: Save it in the LiveDeals Table...now doing that")
	# Get deal meta instabnce by uuid
	deal_meta_inst = getDealMeta(deal_uuid)
	lat = getLat(merchant_id)
	lon = getLon(merchant_id)
	city =getCity(merchant_id)

	# Create instance of the LiveDeal and save it
	live_deal_instance = LiveDeals(deal =deal_meta_inst,lat =lat,lon=lon,city=city)
	live_deal_instance.save()

	print("2: Save it in the MerchantDeal Table...doing this")	

	merchant_deal_stats_instance = MerchantDealStats(merchant=getMerchantInstance(merchant_id),deal_id=deal_uuid,deal_status="live")
	merchant_deal_stats_instance.save()

	print("SUCCESFULLY MADE A DEAL LIVE")


def getDealTitle(deal_uuid):
	meta_inst = getDealMeta(deal_uuid)
	return meta_inst.deal_title

def getDealOldPrice(deal_uuid):
	meta_inst = getDealMeta(deal_uuid)
	return meta_inst.old_price

def getDealNewPrice(deal_uuid):
	meta_inst = getDealMeta(deal_uuid)
	return meta_inst.new_price	

def getDealEndDate(deal_uuid):
	meta_inst = getDealMeta(deal_uuid)
	return meta_inst.end_date	

def getDealBannerDetails(deal_uuid,merchant_id):
	banner_contents = {}
	banner_contents["status"] = 1	
	banner_contents["deal_title"]=getDealTitle(deal_uuid)
	banner_contents["deal_image_1"] = "http://www.auntminnie.com/user/images/content_images/nws_rad/2015_01_28_12_24_19_220_hamburger_200.jpg"
	banner_contents["deal_image_2"] = "http://www.manrepeller.com/wp-content/uploads/2017/05/Moda-Operandi-Online-Sale-Fashion-Clothing-Style-Tag-Man-Repeller-01-01-200x200.jpg"
	banner_contents["merchant_name"] = getMerchantInstance(merchant_id).merchant_name
	banner_contents["old_price"] = getDealOldPrice(deal_uuid)
	banner_contents["new_price"] = getDealNewPrice(deal_uuid)
	#banner_contents["end_date"] = getDealEndDate(deal_uuid)

	return banner_contents



def getMerchantDealStatsInstance(deal_uuid):
	
	instance = MerchantDealStats.objects.get(deal_id=deal_uuid,deal_status="live")
	print("Getting a MerchantDealStatsInstances by UUID and returning back----->",instance)
	return instance

def getRequestedDetailsInstancesCount(deal_uuid):
	print("INSIDE getRequestedDetailsInstane")
	instances = 0
	merchant_deal_stat_instance_obj=getMerchantDealStatsInstance(deal_uuid)
	try:
		instances = RequestedDetails.objects.filter(deal=merchant_deal_stat_instance_obj)
		print("Let's see how many no of times this deal has been requested--->) ",print(instances))	
	except:
		print("ERR")	
	return len(instances)	


def checkCabletStats(cablet_id):
	return True



def getCabletTodaysEntry(deal_id):
	todays_object_entry_times = 0
	todays_date_inst = datetime.date.today()
	req_detail_count=getRequestedDetailsInstancesCount(deal_id)

	if req_detail_count > 0:
		todays_object_entry_times = req_detail_count
		print("This deal has beeen requested > 0 times")
	else:
		print("this deal has not been requested yet")




	return todays_object_entry_times


def executeRequest(deal_id,cablet_id):
	executed_status = False
	todays_date_inst = datetime.date.today()
	todays_entry = getCabletTodaysEntry(deal_id)
	request_new_obj = RequestedDetails(deal=getMerchantDealStatsInstance(deal_id),requested_by_cablet_id=cablet_id,no_of_times=1)
	request_new_obj.save()
	executed_status =True
	# Currently we are not calculating frequency , just adding any cablet who has called
	
	return executed_status

			
def getRequestedDealsCount(deal_uuid):
	count = 0
	m_d_stats_inst = RequestedDetails.objects.filter(deal=getMerchantDealStatsInstance(deal_uuid))
	count = len(m_d_stats_inst)
	print("DEAL IS REQUESTED FOR >>",count)
	return count 

#HERE !!--delete this comment later

			
def getDealRequest():
	print("Inside  getDealRequest()")
	deal_req_obj = DealRequestTable.objects.all()
	print(deal_req_obj)

	if len(deal_req_obj) >0:
		deal_data = []
		deal_request_list = []
		for req in deal_req_obj:
	  		deal_data.append(req.merchant.m_id)
	  		deal_data.append(req.merchant.merchant_name)
	  		deal_data.append(req.merchant.merchant_category)

	  		deal_data.append(req.status)
	  		print("STATUS IS :::: ",req.status)

	  		deal_data.append(req.meta.deal_id)
	  		if req.status == "notdone":
	  			deal_data.append("n/a")
	  			deal_data.append("PUBLISH")
	  		else:
	  			print(getRequestedDealsCount(req.meta.deal_id))
	  			deal_data.append(getRequestedDealsCount(req.meta.deal_id))
	  			deal_data.append("VIEW")	

	  		deal_request_list.append(deal_data)
	  		print("APPENDING :: ",deal_data)
	  		deal_data = []

		deal_request_dict = convertListToJson(deal_request_list)
		print (deal_request_dict)
		return deal_request_dict	
	else:
		print("No metas")	


def getLiveDealsCountOfMerchants(merchant_id):
	count = 0
	try:
		merchant_deal_stat_objs = MerchantDealStats.objects.filter(merchant=getMerchantInstance(merchant_id))
		count = len(merchant_deal_stat_objs)
	except:
		print("NO LIVE DEALS")
	return count	

def getGrabbedCount(merchant_id):
	deals_grabbed_count = 0

	try :
		merchant_deal_stat_objs = MerchantDealStats.objects.filter(merchant=getMerchantInstance(merchant_id))

		for objs in merchant_deal_stat_objs:
			print("PRINTING OBJS OF DSTS ",objs)
			deal_grabbed_objects = DealVoucherGrabbed.objects.filter(deal_id=objs)
			for grabbed in deal_grabbed_objects :
				print("This is being grabbed: ",grabbed)
				deals_grabbed_count = deals_grabbed_count + 1
	except:
		print("EXCEPTION ???")
	return deals_grabbed_count

def getVouchersGrabbed(merchant_id):
	single_voucher_info = []
	voucher_list = []


	print("Inside getVouchersGrabbed")

	try :
		merchant_deal_stat_objs = MerchantDealStats.objects.filter(merchant=getMerchantInstance(merchant_id))

		for objs in merchant_deal_stat_objs:
			print("PRINTING this LIVE DEAL ",objs)
			deal_grabbed_objects = DealVoucherGrabbed.objects.filter(deal_id=objs)
			print("Now printing grabbed info of this deal")


			for grabbed in deal_grabbed_objects :
				print("HERE >>",grabbed.mobile_no," ",grabbed.voucher_code," ",grabbed.voucher_status)
				
				single_voucher_info.append(grabbed.mobile_no)
				single_voucher_info.append(grabbed.voucher_code)
				single_voucher_info.append(grabbed.voucher_status)
				if(grabbed.voucher_status == 'active'):
					single_voucher_info.append("REDEEM")
					print("CHECK 2: HERE")
				else:
					single_voucher_info.append("SOLD")
					
					
				voucher_list.append(single_voucher_info)
				single_voucher_info = []
				print("The above deal has been grabbed and voucherr generated: ",grabbed)

			
			

		voucher_list = convertListToJson(voucher_list)
		print("Voucher list converted to JSON sending to viuew ",grabbed)
	except:
		print("EXCEPTION IN getVouchersGrabbed")
	return voucher_list	






def getMerchantAdCount(merchant_id):
	merchant_deal_stat_objs = None
	count = 0
	try:
		merchant_deal_stat_objs = MerchantDealStats.objects.filter(merchant=getMerchantInstance(merchant_id))
	except:
		print("NO DEAL STAT OBJECTS FOR THIS MERCHANT")
	if merchant_deal_stat_objs is not None:
		for obj in merchant_deal_stat_objs:
			deal_id = obj.deal_id
			count = count+ getRequestedDetailsInstancesCount(deal_id)
			print("Total ADS DISPLAYED FOR THIS MERCHANTS ALL DEALS",count)
	else:
		print("NO DEAL STAT OBJECTS FOR THIS MERCHANTXXXX")
	return count	


def getVideoAds(merchant_id):
	ad_account_inst = None	
	merchant_ads_list = None


	try:
		ad_account_inst = AdvertisementAccount.objects.get(merchant=getMerchantInstance(merchant_id))
		merchant_ads_list = VideoAdvertsMeta.objects.filter(ad_acc_id=ad_account_inst)
	except:
		print("NO ADS PRESENT")

	return merchant_ads_list		


def getAdAccount(merchant_id):
	ad_account_inst=None
	try:
		ad_account_inst = AdvertisementAccount.objects.get(merchant=getMerchantInstance(merchant_id))
	except:
		print("No Ad-Account")	
	return 	ad_account_inst

def getVideoAdvertsMeta(merchant_id):
	video_adverts_meta = VideoAdvertsMeta.objects.get(ad_acc_id=getAdAccount(merchant_id))	
	return video_adverts_meta



def createAdAccount(merchant_id):
	merchant_instance = getMerchantInstance(merchant_id)
	adac_id = "-".join(("AD",merchant_id))
	ad_account = AdvertisementAccount(merchant=merchant_instance,ad_acc_id=adac_id,total_ads_created=0,total_active_ads=0)
	ad_account.save()	
	print("AdvertisementAccount created !!!")




def saveToCloudinary(filename,merchant_id):
	print("FILE PRINTING VID :::::::::::::::::::")

	file = os.path.join(UPLOAD_ROOT, filename)

	folder_path = "%s/ADV/" % merchant_id
	response_cloudinary=cloudinary.uploader.upload(file,folder=folder_path,resource_type = "video",async="true")
	#x=convertListToJson(x)




	video_adverts_meta_instance = VideoAdvertsMeta(ad_acc_id=getAdAccount(merchant_id))


	video_adverts_meta_instance.ad_video_path = response_cloudinary['secure_url']
	video_adverts_meta_instance.save()


	print("UPLOADED TO CLOUDINARY",response_cloudinary)
	print(response_cloudinary['secure_url'])


