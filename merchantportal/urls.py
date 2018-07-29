from django.conf.urls import url
from merchantportal import views

urlpatterns = [

    url(r'^$',views.mp_index,name='mp_index'),
    #url(r'^merchants/(?P<merchant_id>\w+)/',views.mp_index,name='mp_index'),
    url(r'^login/',views.mp_login,name='mp_login'),
    url(r'^logout/',views.mp_logout,name='mp_logout'),
    url(r'^inventory/$',views.mp_inventory,name='mp_inventory'),
    url(r'^deals/$',views.mp_deals,name='mp_deals'),
    url(r'^deals/add$',views.mp_deals_add_info_new,name='mp_deals_add_info_new'),   
    #url(r'^deals/add$',views.mp_deals_add_info,name='mp_deals_add_info'),
     
    
    #url(r'^inventory/addinventory$',views.mp_add_inventory,name='mp_add_inventory'),
    url(r'^inventory/(?P<merchant_id>\w+)/add_category',views.add_category,name='add_category'),
    #url(r'^delete/(?P<merchant_id>\w+)/(?P<id>\d+)',views.delete_item,name='delete'),
    url(r'^dealcreation/',views.mp_deal_creation_steps,name='dealcreation'),
    url(r'^adddealitem/',views.add_deal_item_form,name='adddealitem'),
    url(r'^adverts/',views.mp_adverts,name='adverts')


]
