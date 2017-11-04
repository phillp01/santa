from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$',
        views.order_create,
        name='order_create'),

    url(r'^update/(?P<ref>[\w{}.-]{1,32})/$',
        views.order_update,
        name='order_update'),
]