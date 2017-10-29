from django.shortcuts import render, get_object_or_404
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from pprint import pprint
from orders.models import Order
from django.shortcuts import render, get_object_or_404
from shop.models import Product


def order_create(request):

	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()

			if order.pdf_download == True:
				product = get_object_or_404(Product, id=4)
				cart.add(product)
				
			else:
				print ("PDF NO")

			for item in cart:

				#print ("Running 'for item in cart'")

				#print ("Items here",item)
				product = get_object_or_404(Product, id=item['product'])
				#import pdb; pdb.set_trace()
				OrderItem.objects.create(order=order,
										product= product,
										price=item['price'],
										quantity=item['quantity'],
										name = product.name,
				)

				#print ("end 'item in cart'")
			# clear the cart
			#cart.clear()

			# session_keys = list(request.session.keys())
			# for key in session_keys:
			# 	del request.session[key]
	
			# request.session.modified = True



			return render(request,
							#Need to pass to order preview here.
							#'orders/order/created.html',
							'orders/santa/preview-order.html',
							{'order': order, 'cart':cart},
			)

		else:
			print ("Form Not Valid")    
	else:
		form = OrderCreateForm()

	#print ("PRINT THIS = %s" % cart.product_id)

	return render(request,
				  #'orders/order/create.html',
				  'orders/santa/order-detail.html',
				  {'cart': cart, 'form': form})