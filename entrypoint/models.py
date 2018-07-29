from django.db import models
#from merchantportal.models import DealMeta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.validators import RegexValidator



# Not required, maybe

# fnb|travelnhotels|spansaloon|activities|instore|others
class MerchantCategoryChoices(models.Model):
    CATEGORY_CHOICES = (
        ('fnb','Food and Beverages'),
        ('travelnhotels','Travel and Hotels'),
        ('spansaloon','Spa and Salon'),
        ('activities','Outdoor Activities'),
        ('instore','Instore'),
        ('others','Others')
    )
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20, null=True)
    def __str__(self):
        return self.category
    #merchant = models.OneToOneField(ActiveMerchants,null=False)

class ActiveMerchants(models.Model):
    CATEGORY_CHOICES = (
        ('fnb','Food and Beverages'),
        ('travelnhotels','Travel and Hotels'),
        ('spansaloon','Spa and Salon'),
        ('activities','Outdoor Activities'),
        ('instore','Instore'),
        ('others','Others')
    )
    m_id = models.CharField (max_length=8, blank=False, null=False)
    user = models.OneToOneField(User,null = True,on_delete=models.CASCADE)
    merchant_category = models.CharField(choices=CATEGORY_CHOICES,max_length=15,null = True)
    merchant_name = models.CharField (max_length=128, blank=False, null=False)
    merchant_email = models.EmailField(max_length=128, blank=False, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,11}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    personal_phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True) # validators should be a list
    deal_account_status = models.BooleanField(default=0,null=False)
    onboarded_date = models.DateTimeField(default=timezone.now)
    def is_active(self):
        return bool(self.deal_account_status)
    def __str__(self):
        return self.merchant_name


# Not required, maybe
class MerchantCategory(models.Model):
    CATEGORY_CHOICES = (
        ('fnb','Food and Beverages'),
        ('travelnhotels','Travel and Hotels'),
        ('spansaloon','Spa and Salon'),
        ('activities','Outdoor Activities'),
        ('instore','Instore'),
        ('others','Others')
    )
    merchant = models.OneToOneField(ActiveMerchants,null=False,on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20, null=True)
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant_name,self.category)


class BusinessAddress(models.Model):
    merchant = models.OneToOneField(ActiveMerchants,null=False,on_delete=models.CASCADE)
    address_line_one = models.CharField (max_length=128, blank=False, null=False)
    address_line_two = models.CharField (max_length=128, blank=False, null=False)
    city = models.CharField (max_length=128, blank=False, null=False)
    state = models.CharField (max_length=128, blank=False, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,11}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    business_phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True) # validators should be a list
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant_name,self.city)

class RedemptionAddress(models.Model):
    merchant = models.OneToOneField(ActiveMerchants,null=False,on_delete=models.CASCADE)
    address_line_one = models.CharField (max_length=128, blank=False, null=False)
    address_line_two = models.CharField (max_length=128, blank=False, null=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6,blank=False, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6,blank=False, null=True)
    sublocality = models.CharField (max_length=128, blank=False, null=True)
    city = models.CharField (max_length=128, blank=False, null=False)
    state = models.CharField (max_length=128, blank=False, null=False)
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant_name,self.city)

def get_deadline():
    return datetime.today() + timedelta(days=30)


class PlanSold(models.Model):
    PLAN_NAME = (
        ('P30','Package 30'),
        ('P60','Package 60'),
        ('P120','Package 120'),
    )
    PLAN_DURATION = (
        ('1','1 Month'),
        ('2','2 Months'),
        ('3','3 Months'),
        ('4','4 Months'),
        ('5','5 Months'),
        ('6','6 Months'),
        ('7','7 Months'),
        ('8','8 Months'),
        ('9','9 Months'),
        ('10','10 Months'),
        ('11','11 Months'),
        ('12','12 Months'),
    )
    PAYEMENT_METHOD = (
        ('online','Online'),
        ('cheque','Cheque'),
        ('pos','POS'),
    )
    merchant = models.OneToOneField(ActiveMerchants,null=False,on_delete=models.CASCADE)
    plan_name = models.CharField(choices=PLAN_NAME,max_length=20, null=True)
    plan_duration = models.CharField(choices=PLAN_DURATION,max_length=20, null=True)
    paid_amount = models.IntegerField(default=0,validators=[MinValueValidator(30000)],null=True)
    payement_method = models.CharField(choices=PAYEMENT_METHOD,max_length=20, null=True)
    payement_memo =  models.CharField (max_length=128, blank=False, null=False)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=get_deadline())
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant_name,self.plan_name)

# Have to change/refactor below tables as the Normalization is being done

# Deal Account is to be made once the payement is done. i.e PLAN SOLD entry for a model for a merchant is done.

class DealAccounts(models.Model):
    merchant = models.OneToOneField(ActiveMerchants,null=False,on_delete=models.CASCADE)
    deal_acc_id = models.CharField (max_length=11, blank=False, null=True)
    total_deals_created = models.IntegerField(default=0,validators=[MaxValueValidator(30), MinValueValidator(0)],null=True)
    total_active_deals = models.IntegerField(default=0,validators=[MaxValueValidator(30), MinValueValidator(0)],null=True)
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant_name,self.deal_acc_id)




# AdvertisementAccount  is to be made once the payement is done. i.e PLAN SOLD entry for a model for a merchant is done.
class AdvertisementAccount(models.Model):
    merchant = models.OneToOneField(ActiveMerchants,null=False,on_delete=models.CASCADE)
    ad_acc_id = models.CharField (max_length=11, blank=False, null=True)
    total_ads_created = models.IntegerField(default=0,validators=[MaxValueValidator(30), MinValueValidator(0)],null=True)
    total_active_ads = models.IntegerField(default=0,validators=[MaxValueValidator(30), MinValueValidator(0)],null=True)
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant_name,self.ad_acc_id)

# Video Recieved by email is uploaded here and a path to the file is saved in this model.
#Every ad uploaded will increment serial count
class VideoAdvertsMeta(models.Model):
    ad_acc_id = models.ForeignKey(AdvertisementAccount,null=False,on_delete=models.CASCADE)
    ad_serial_count = models.IntegerField(default=0,validators=[MaxValueValidator(30), MinValueValidator(0)],null=True)
    ad_status = models.BooleanField(default=0,null=False)
    ad_video_path =  models.CharField (max_length=128, blank=False, null=False)
    def __str__(self):
        return "(%s-%s) : %s" % (self.ad_acc_id.merchant.m_id,self.ad_acc_id.merchant.merchant_name,self.ad_serial_count)




# To add dl-snapshot,vehicle
#Driver onboarding excelfile/form will populate this model
class Driver(models.Model):
    driver_name = models.CharField (max_length=128, blank=False, null=False)
    driver_email = models.EmailField(max_length=128, blank=False, null=False)    
    phone_number = models.IntegerField(default=0,validators=[MaxValueValidator(10), MinValueValidator(10)],null=True)
    address_proof_details = models.CharField (max_length=128, blank=False, null=False)

#Tablet onboarding form will populate this model
class DisplayTabs(models.Model):
    device_imei = models.IntegerField(default=0,validators=[MaxValueValidator(17), MinValueValidator(15)],null=True)
    device_phone_number = models.IntegerField(default=0,validators=[MaxValueValidator(10), MinValueValidator(10)],null=True)

#Drivers who will start using the service will be activated by this model    

class Cablet(models.Model):
    display_tab = models.OneToOneField(DisplayTabs,null=False,on_delete=models.CASCADE)
    driver = models.OneToOneField(Driver,null=False,on_delete=models.CASCADE)
    cablet_id = models.CharField (max_length=16, blank=False, null=True) 
    activation_date = models.DateTimeField(default=timezone.now)



    

# The no. of times the ads are requested and by whom and at what date 
class AdRequest(models.Model):
    ad_acc_id = models.OneToOneField(AdvertisementAccount,null=False,on_delete=models.CASCADE) 
    request_time = models.DateTimeField(default=timezone.now)
    requested_by_cablet = models.OneToOneField(Cablet,null=False,on_delete=models.CASCADE)
    

# Cablets stats monitoring below 3 models:

class PowerOn(models.Model):
    cablet_id = models.OneToOneField(Cablet,null=False,on_delete=models.CASCADE)
    power_on_time = models.DateTimeField(default=timezone.now)

class PowerOff(models.Model):
    cablet_id = models.OneToOneField(Cablet,null=False,on_delete=models.CASCADE)
    power_off_time = models.DateTimeField(default=timezone.now)  

class CabletInactive(models.Model):
    cablet_id = models.OneToOneField(Cablet,null=False,on_delete=models.CASCADE)
    power_off_time = models.DateTimeField(default=timezone.now)        



# class DealStats(models.Model):
#     deal_id= models.OneToOneField(DealsByMerchants,null=False)
#     no_of_times_played = models.IntegerField(default=0,validators=[MinValueValidator(0)])
#     tablet_id = models.CharField (max_length=10, blank=False, null=False)
#     def __str__(self):
#         return self.no_of_times_played

class Document(models.Model):
    csv = models.FileField(upload_to = 'mastercsv/')

class Dummy(models.Model):
    csv = models.FileField(upload_to = 'dummydeals/')    

