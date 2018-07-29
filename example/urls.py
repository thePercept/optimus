from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    url(r'^$',views.ex_index,name='ex_index'),
    url(r'^ajax/', csrf_exempt(views.ex_ajax),name='ajax'),

    ]
