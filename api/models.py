from django.db import models
from django.utils import timezone
from merchantportal.models import DealMeta,ActiveMerchants
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class LiveDeals(models.Model):
    deal= models.ForeignKey (DealMeta,null=False,on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6,blank=False, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6,blank=False, null=True)
    city = models.CharField (max_length=128, blank=True, null=False)
    def __str__(self):
    	return "(%s-%s) : %s" % (self.deal.deal_id,self.deal.deal_title,self.city)


#Deal created for a merchant
class MerchantDealStats(models.Model):
    DEAL_STATUS = (
        ('live','Live'),
        ('notlive','Not Live'),
    )    
    merchant = models.ForeignKey(ActiveMerchants,null=False,on_delete=models.CASCADE)  
    deal_id =  models.CharField (max_length=128, blank=False, null=False)
    deal_status = models.CharField(choices=DEAL_STATUS,max_length=7, null=False)
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant,self.deal_id,self.deal_status)


class RequestedDetails(models.Model):
    deal = models.ForeignKey(MerchantDealStats,null=False,on_delete=models.CASCADE)
    requested_date = models.DateTimeField(auto_now_add=True)
    requested_by_cablet_id = models.CharField (max_length=128, blank=False, null=False)
    no_of_times = models.IntegerField(default=0,validators=[MaxValueValidator(4), MinValueValidator(0)],null=True)
    def __str__(self):
        return "Requested by: %s on : %s" % (self.requested_by_cablet_id,self.requested_date)
