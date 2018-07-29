from django import forms
from entrypoint.models import DealAccounts
from django.contrib.auth.models import User
from .models import AdVideo,FoodAndBeveragesInventory,TravelAndHotelsInventory,DealMeta,FoodAndBeveragesDealItem,TravelAndHotelsDealItem

# class DealsBasicDetailForm(forms.ModelForm):
#
#     class Meta:
#         model = DealsByMerchants
#         fields = ['deal_id','created_date','end_date']

class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['username','password']

# class MerchantInventoryForm(forms.ModelForm):
#     class Meta:
#         model = MerchantInventory
#         fields = ['inventory_id']

class FoodAndBeveragesInventoryForm(forms.ModelForm):
    item_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Item Name'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Quantity'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Quantity'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Quantity'}))
    

    class Meta:
        model = FoodAndBeveragesInventory
        fields = ['item_name','quantity','price','description']

class TravelAndHotelsInventoryForm(forms.ModelForm):
    class Meta:
        model = TravelAndHotelsInventory
        fields = ['offer','no_of_people','price','description']

class DealMetaForm(forms.ModelForm):
    class Meta:
        model = DealMeta
        fields = ['deal_title']


class VideoForm(forms.ModelForm):
    class Meta:
        model = AdVideo 
        fields = ['video']     


# class FoodAndBeveragesDealItemForm(forms.ModelForm):
#     class Meta:
#         model = FoodAndBeveragesDealItem
#         fields = ['deal_items']

# class TravelAndHotelsDealItemForm(forms.ModelForm):
#     class Meta:
#         model = FoodAndBeveragesDealItem
#         fields = ['deal_items']
