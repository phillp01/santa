from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from pprint import pprint
from orders.models import Order
from django.shortcuts import render, get_object_or_404
from shop.models import Product
from django.http import HttpResponse

def order_create(request):
	cart = Cart(request)
	for key, value in request.session.items():
   		print('{} => {} => {}'.format(key, value, type(value)))
	if request.method == 'POST': #if the view is being accessed from the compelted form
		if Order.objects.filter(ref=request.POST.get('ref')): # check to see if this ref exists in Orders table already.
			print("already exists") # Code here if the item already has posted data to the model
			a = Order.objects.get(ref=request.POST.get('ref'))

			print ("A =",a.pdf_download)

			if not a.pdf_download:
				print("we have a not")
				

			order = OrderCreateForm(request.POST, instance=a)
			updated_order = order.save()
			return render(request, # send the user to the preview sending the card and order data.
				'orders/santa/preview-order.html',
				{'order': updated_order, 'cart':cart},
			)
		else:
			print("does not exist")
			form = OrderCreateForm(request.POST) # create the form from the POST data
			if form.is_valid(): #check to see if the data is valid
				#import pdb; pdb.set_trace()
				order = form.save() # save the form to the model (database)
				if order.pdf_download == True: # if the user has selected PDF download add this to the cart
					product = get_object_or_404(Product, id=4)
					cart.add(product, ref=order.ref)
				else:
					print ("PDF NO")
				return render(request, # send the user to the preview sending the card and order data.
								'orders/santa/preview-order.html',
								{'order': order, 'cart':cart},
				)
			else:
				print ("Form Not Valid")    
	else:
		form = OrderCreateForm(initial={'ref':request.session['ref']}) #if not a post set the form and add the cart product ID
	#print ("PRINT THIS = %s" % cart.product_id)
	return render(request, # send user to complete the order details.
				  'orders/santa/order-detail.html',
				  {'cart': cart, 'form': form}
	)

def order_update(request, ref):

	cart = Cart(request)
	order = get_object_or_404(Order, ref=ref)

	form = OrderCreateForm(instance=order)
	return render(request, # send user to complete the order details.
				  'orders/santa/order-detail.html',
				  {'cart': cart, 'form': form}
	)


	#if Order.objects.filter(ref=request.POST.get('ref')):