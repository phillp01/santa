orders.py
from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Customer(object):

	def __init__(self, request):
		"""
		Initialize the customer.
		"""
		self.session = request.session
		customer = self.session.get(settings.CUSTOMER_SESSION_ID)
		if not customer:
			# save an empty customer in the session
			customer = self.session[settings.CUSTOMER_SESSION_ID] = {}
		self.customer = customer

	def add(self):
		print ("test")