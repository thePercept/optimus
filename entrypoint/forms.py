from entrypoint.models import Dummy,Document,DealAccounts,PlanSold
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['username','password']

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['csv',]

class DummyForm(forms.ModelForm):

    class Meta:
        model = Dummy
        fields = ['csv',]       



class CreateDealAccountForm(forms.ModelForm):
    class Meta:
        model = DealAccounts
        #fields = ['merchant_id']
        fields = ['total_deals_created','total_active_deals']

class PlanPurchasedForm(forms.ModelForm):
    idx = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))

    class Meta:
        model =  PlanSold

        fields = ['plan_name','plan_duration','paid_amount','payement_method','payement_memo']    
        # widgets = {
        #     'plan_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
        #     'plan_duration' : forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
        #     'paid_amount' : forms.Select(attrs={'class':'form-control','placeholder':'Name'}),
        #     'payement_method' : forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
        #     'payement_memo' : forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),

        # }   

class BasicDetails(forms.Form):
    merchant_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    merchant_ID = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    merchant_category =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    email =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    onboarding_date =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    deal_account_status =forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))

class BusinessAddress(forms.Form):
    business_address_line_1=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    business_address_line_2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    city=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    state=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))

class RedemptionAddress(forms.Form):
    redemption_address_line_1=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    redemption_address_line_2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    city=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    state=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))      
    lat = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))    
    lon = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))    
    sublocality = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))        

class PlanPurchased(forms.Form):
    plan_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    plan_duration = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    payement_method = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    paid_amount = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    plan_started = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    plan_ends = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))
    payement_memo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name','readonly':'True'}))

# class VerifyDealForm(forms.Form):
#     confirm_verification = forms.CheckboxInput(widget=forms.CheckboxInput(attrs={'class':'form-control'))