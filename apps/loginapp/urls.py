from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login$',login, name='login'),
    url(r'^logout$',logout, name='logout'),
    url(r'^register$',register, name='register'),
]
