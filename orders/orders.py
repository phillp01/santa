from decimal import Decimal
from django.conf import settings
from shop.models import Product

class SessionOrder(object):

	def __init__(self, request):
		"""
		Initialize the customer.
		"""
		self.session = request.session
		order = self.session.get(settings.ORDER_SESSION_ID)
		if not order:
			# save an empty customer in the session
			order = self.session[settings.ORDER_SESSION_ID] = {}
		self.order = order

	def add(self, order_id):
		print ("running add order test")
		self.order['order_id'] = str(order_id)
		self.save()

	def save(self):
		# update the session cart
		self.session[settings.ORDER_SESSION_ID] = self.order
		# mark the session as "modified" to make sure it is saved
		self.session.modified = True

	def clear(self):
		# remove cart from session
		del self.session[settings.ORDER_SESSION_ID]
		self.session.modified = True