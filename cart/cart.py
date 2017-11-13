from decimal import Decimal
from django.conf import settings
from shop.models import Product
import random, string

class Cart(object):

	def __init__(self, request):
		"""
		Initialize the cart.
		"""
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			# save an empty cart in the session
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product, ref='a', quantity=1, update_quantity=False):
		"""
		Add a product to the cart or update its quantity.
		"""

		#print ("Add cart Order = ",order.child_first_name)
		
		for item in self:
			if item['product'] == 4 and item['ref'] == ref:
				item["quantity"] = 1
				self.save()


		product_id = str(product.id)
		
		if ref =='a':

			random_ref = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
			
			self.session['ref'] = str(random_ref)
				
				#print("Product ID is not in self.cart")
				
			self.cart[product_id] = {'quantity': 1,
									 'price': str(product.price),
									 'name': str(product.name),
									 'ref':str(random_ref),
			}
		else:
			self.cart[product_id] = {'quantity': 1,
									 'price': str(product.price),
									 'name': str(product.name),
									 'ref':str(ref),
			}

		str(self.cart[product_id]['quantity'])
		#print ("Quantity = %s" % self.cart[product_id]['quantity'])
		#print ("Price Var Type = %s" % type(self.cart[product_id]['price']))

		#for key, value in self.session.items():
			#print('{} => {} => {}'.format(key, value, type(value)))

		#print ("Prod Quantity in Cart = %s" % self.cart[product_id]['quantity'])
		self.save()

	def save(self):
		# update the session cart
		self.session[settings.CART_SESSION_ID] = self.cart
		# mark the session as "modified" to make sure it is saved
		self.session.modified = True

	def remove(self, product, ref='a'):
		"""
		Remove a product from the cart.
		"""
		product_id = str(product.id)

		for item in self:
			if item['product'] == 4 and item['ref'] == ref:
				item["quantity"] = 0
				self.save()

		#if product_id in self.cart:
			#del self.cart[product_id]
			

	def __iter__(self):
		"""
		Iterate over the items in the cart and get the products 
		from the database.
		"""
		
		#print("START  __ITER__  ")
				
		product_ids = self.cart.keys()
		# get the product objects and add them to the cart
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product.id

		for item in self.cart.values():
			item['price'] = str(Decimal(item['price']))
			#item['total_price'] = item['price'] * item['quantity']
			#item['total_price'] = str(item['total_price'])
			yield item

		#print ("End __iter__")

	def __len__(self):
		"""
		Count all items in the cart.
		"""
		return sum(item['quantity'] for item in self.cart.values())

	def clear(self):
		# remove cart from session
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())