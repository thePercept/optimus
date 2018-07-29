from django.conf.urls import url
from api import views

urlpatterns = [
	#url(r'^deals',views.DealList.as_view()),
	url(r'^deals',views.DealView.as_view()), 
	url(r'^visitor',views.visitor_grabbed), 
	url(r'^mercads',views.AdvertView.as_view()),
	]