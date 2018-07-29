from django.db import models
from django.core.validators import RegexValidator
from api.models import MerchantDealStats


# Create your models here.

class DealVoucherGrabbed(models.Model):
	VOUCHER_STATUS = (
		('active','Active'),
		('redeemed','Redeemed'),
		)   	
	phone_regex = RegexValidator(regex=r'^\+?1?\d{10,12}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
	mobile_no = models.CharField(validators=[phone_regex], max_length=12, blank=True) # validators should be a list	
	deal_id =  models.ForeignKey (MerchantDealStats,null=False,on_delete=models.CASCADE)
	voucher_code = models.CharField (max_length=8, blank=False, null=False)
	voucher_status = models.CharField(choices=VOUCHER_STATUS,max_length=8,null = True)
	created_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return "(%s-%s)" % (self.mobile_no,self.deal_id)

class UserConverted(models.Model):
	user_mobile = models.ForeignKey(DealVoucherGrabbed,null=False,on_delete=models.CASCADE)
	requested_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return "(%s-%s)" % (self.user_mobile,self.user_mobile.deal_id)


