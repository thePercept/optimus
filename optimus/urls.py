"""optimus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
""" 
from django.conf.urls import url,include
from django.contrib import admin
from . routers import router
#from django.conf import settings
#from django.conf.urls.defaults import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^optimus/',include('entrypoint.urls') ),
    url(r'^merchants/',include('merchantportal.urls') ),
    url(r'^example/',include('example.urls') ),
    url(r'^api/',include('api.urls')),

    #url(r'^accounts/',include('django.contrib.auth.urls')),

]

# if settings.DEBUG :
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#     )
