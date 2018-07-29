from django.conf.urls import url
from entrypoint import views

urlpatterns = [
	url(r'^login/',views.ep_login,name='ep_login'),
    url(r'^$',views.ep_index,name='ep_index'),
	url(r'^merchants/$',views.ep_merchants,name='merchants'),
	url(r'^merchants/(?P<merchant_id>\w+)/$',views.ep_merchant_page,name='merchant_detail_page'),
	url(r'^update/$',views.ep_ads,name='ep_ads'),
	url(r'^uploaddata/$',views.upload_data,name='upload_data'),
	url(r'^verifydeals/$',views.ep_verify_deal_step_one,name='ep_verify_deal_step_one'),
	url(r'^verifydealsfinal/$',views.ep_verify_deal_step_two,name='ep_verify_deal_step_two')


    ]

