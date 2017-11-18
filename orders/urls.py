from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$',
        views.order_create,
        name='order_create'),

    url(r'^update/(?P<order>[\w{}.-]{1,32})/$',
        views.order_update,
        name='order_update'),

	url(r'^newOrder/(?P<product_id>\d+)/$',
		views.new_order,
		name='new_order'),

	url(r'^removeItem/(?P<item_id>\d+)/$',
		views.remove_item,
		name='remove_item'),

	url(r'^checkout/$',
		views.checkout,
		name='checkout'),
]