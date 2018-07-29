import uuid
from django.db import models
from entrypoint.models import ActiveMerchants,DealAccounts
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from django.utils import timezone

class FoodAndBeveragesInventory(models.Model):
    merchant =  models.ForeignKey(ActiveMerchants,null=False,on_delete=models.CASCADE)
    item_name = models.CharField (max_length=128, blank=False, null=False)
    quantity = models.CharField (max_length=128, blank=False, null=False)
    price = models.CharField (max_length=128, blank=False, null=False)
    description =models.CharField (max_length=128, blank=True, null=True,)
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant_name,self.item_name)


class TravelAndHotelsInventory (models.Model):
    merchant =  models.ForeignKey(ActiveMerchants,null=False,on_delete=models.CASCADE)
    offer = models.CharField (max_length=128, blank=False, null=False)
    no_of_people = models.IntegerField(default=0,validators=[MaxValueValidator(10), MinValueValidator(0)],null=True)
    price = models.CharField (max_length=128, blank=False, null=False)
    description =models.CharField (max_length=128, blank=True, null=True,)
    def __str__(self):
        return "(%s-%s) : %s" % (self.merchant.m_id,self.merchant.merchant.merchant_name,self.item_name)

def get_deadline():
    return datetime.today() + timedelta(days=30)






class DealMeta(models.Model):
    merchant_id=  models.CharField (max_length=128, blank=False, null=False)

    deal_id = models.CharField (max_length=128, blank=False, null=False)
    deal_title = models.CharField (max_length=128, blank=False, null=False)
    item_image_1 = models.CharField (max_length=128, blank=True, null=True)
    item_image_2 = models.CharField (max_length=128, blank=True, null=True)
    old_price = models.IntegerField(default=0,validators=[MinValueValidator(0)],null=True)
    new_price = models.IntegerField(default=0,validators=[MinValueValidator(0)],null=True)
    end_date = models.DateTimeField(default=get_deadline())
    created_date = models.DateTimeField(default=timezone.now)
    description = models.CharField (max_length=128, blank=True, null=True)
    merchant_website = models.URLField( blank=True, null=True)

    # deal_detail = models.ForeignKey(ContentType)#FnbDeals,TravelDeals,InstoreDeals...etc
    # object_id = models.PositiveIntegerField()
    # item_type= GenericForeignKey('deal_detail','object_id')
    def __str__(self):
        return "(%s-%s)" % (self.deal_title,self.deal_id)







class FoodAndBeveragesDealItem(models.Model):
    deal_meta = models.ForeignKey(DealMeta,blank=False,null=True,on_delete=models.CASCADE)
    di_item = models.CharField (max_length=128, blank=False, null=True)
    di_quantity = models.CharField (max_length=128, blank=False, null=True)
    dil_price = models.CharField (max_length=128, blank=False, null=True)

    def get_deal_item_details(self):
        return self.di_item + ' cost is '+self.dil_price +' Rupees.'

    def __str__(self):
        return "%s" % (self.di_item)


class TravelAndHotelsDealItem(models.Model):
    deal_meta = models.ForeignKey(DealMeta,blank=False,null=True,on_delete=models.CASCADE)
    deal_items = models.CharField (max_length=128, blank=False, null=False)




class DealRequestTable(models.Model):
    CATEGORY_CHOICES = (
        ('notdone','NOT CHECKED'),
        ('done','CHECKED'),
    )
    
    meta = models.ForeignKey(DealMeta,blank=False,null=True,on_delete=models.CASCADE)
    merchant = models.ForeignKey(ActiveMerchants,null=False,on_delete=models.CASCADE)
    status = models.CharField(choices=CATEGORY_CHOICES,max_length=20, null=True)
    
class AdVideo(models.Model):
    video = models.FileField(upload_to='merchant_ads/')