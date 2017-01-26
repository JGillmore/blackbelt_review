from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^addbook$',addbook, name='addbook'),
    url(r'^add$',add, name='add'),
    url(r'^deletecomment/(?P<id>[0-9]*$)',deletecomment, name='deletecomment'),
    url(r'^addcomment/(?P<id>[0-9]*$)',addcomment, name='addcomment'),
    url(r'^user/(?P<id>[0-9]*$)',userpage, name='user'),
    url(r'^(?P<id>[0-9]*$)',book, name='book'),
]
