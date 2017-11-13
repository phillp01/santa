from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem
from .forms import OrderItemCreate,OrderOptionsCreate
from cart.cart import Cart
from pprint import pprint

from django.shortcuts import render, get_object_or_404
from shop.models import Product
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from orders.models import Order, OrderItem, ItemOption

from django.conf import settings
import random, string

# @never_cache
# def order_create(request):
# 	cart = Cart(request)

# 	if request.method == 'POST': #if the view is being accessed from the compelted form
# 		print("Request is POST")
# 		if Order.objects.filter(ref=request.POST.get('ref')): # check to see if this ref exists in Orders table already.
# 			print("Ref does already exists") # Code here if the item already has posted data to the model
# 			a = Order.objects.get(ref=request.POST.get('ref'))

# 			#import pdb; pdb.set_trace()
# 			print ("PDF Download =",request.POST.get('pdf_download'))
# 			if not request.POST.get('pdf_download'):
# 				print("No PDF (removed)")
# 				product = get_object_or_404(Product, id=4)
# 				cart.remove(product, ref=a.ref)
# 			else:
# 				product = get_object_or_404(Product, id=4)
# 				cart.add(product, ref=a.ref)

# 			order = OrderCreateForm(request.POST, instance=a)
# 			updated_order = order.save()

# 			for key, value in request.session.items():
#    				print('{} => {} => {}'.format(key, value, type(value)))

# 			return render(request, # send the user to the preview sending the card and order data.
# 				'orders/santa/preview-order.html',
# 				{'order': updated_order, 'cart':cart},
# 			)
# 		else:
# 			print("does not exist")
# 			form = OrderCreateForm(request.POST) # create the form from the POST data
# 			if form.is_valid(): #check to see if the data is valid
# 				#import pdb; pdb.set_trace()
# 				order = form.save() # save the form to the model (database)
# 				if order.pdf_download == True: # if the user has selected PDF download add this to the cart
# 					product = get_object_or_404(Product, id=4)
# 					cart.add(product, ref=order.ref)
# 				else:
# 					print ("PDF NO")
# 				return render(request, # send the user to the preview sending the card and order data.
# 								'orders/santa/preview-order.html',
# 								{'order': order, 'cart':cart},
# 				)
# 			else:
# 				print ("Form Not Valid")    
# 	else:
# 		form = OrderCreateForm(initial={'ref':request.session['ref']}) #if not a post set the form and add the cart product ID
# 	#print ("PRINT THIS = %s" % cart.product_id)
# 	return render(request, # send user to complete the order details.
# 				  'orders/santa/order-detail.html',
# 				  {'cart': cart, 'form': form}
# 	)

# def order_update(request, order):

# 	order = get_object_or_404(OrderItem, pk=order)

# 	form = OrderItemCreate(instance=order)
# 	return render(request, # send user to complete the order details.
# 				  'orders/santa/order-detail.html',
# 				  {'form': form}
# 	)


	#if Order.objects.filter(ref=request.POST.get('ref')):

def new_order(request, product_id):
	#import pdb; pdb.set_trace()
	additional = request.session['additional']
	print ("Is this an additional order :",additional)

	if request.method == 'POST':
		print ("New Order Request is POST")
	
	if 'order_id' in request.session:
		print ("Order ID already Exists in Session :",request.session['order_id'])

		setNewId = False 

		if not additional:
			
			print("Set New ID True")
			del request.session['order_id']
			print("Order_Id Deleted")
			start_order = Order()
			start_order.save()
			print ("New Order ID = ",start_order.id)
			print("Adding new Order_Id to session")
			request.session['order_id'] = str(start_order.id)
			print ("Session ID = ",request.session['order_id'])

	else:
		print ("Order ID Does NOT Exist in Session")
		print ("Set New ID False")
		start_order = Order()
		start_order.save()
		print ("New Order ID = ",start_order.id)
		request.session['order_id'] = start_order.id
		print ("Session ID = ",request.session['order_id'])
	
	product = get_object_or_404(Product, id=product_id)
	print ("Product = ",product.name)

	random_ref = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
	form = OrderItemCreate(initial={'order':request.session['order_id'],'product':product.id,'price':product.price,'quantity':1,'name':product.name,'ref':random_ref}) # create the form from the POST data

	return render(request, # send user to complete the order details.
				  'orders/santa/order-detail.html',
				  {'form': form}
	)

	# html = "<html><body><h1>ORDER ID IS " + request.session['order_id'] + "</h1></body></html>"

	# return HttpResponse(html)


def order_create(request):

	if request.method == 'POST': #if the view is being accessed from the compelted form
		print("Order Create Request is POST")
		
		if 'edited_order' in request.session:
			print ("Existing order found to Edit")

			edited_order = request.session['edited_order']
			del request.session['edited_order']

			print ("Order to Edit = ",edited_order)

			a = OrderItem.objects.get(pk=edited_order)

			order = OrderItemCreate(request.POST, instance=a)
			print ("order.price =",order['price'].value())
			order_data = order.save()

			if not request.POST.get('pdf_download'):
				print("No PDF download")
				if ItemOption.objects.filter(orderitem_id=edited_order).exists():
					print("PDF option found - needs removing")
					ItemOption.objects.filter(orderitem_id=edited_order).delete()
				else:
					print("No PDF Option found - nothing to do")
# 				product = get_object_or_404(Product, id=4)
# 				cart.remove(product, ref=a.ref)
			else:
				print("Yes PDF Download")
				if ItemOption.objects.filter(orderitem_id=edited_order).exists():
					print("PDF option found - nothing to do")
				else:
					print("no PDF option found - Needs adding")
					product = get_object_or_404(Product, id=4)
					pdf = ItemOption.objects.filter(orderitem_id=order_data.pk)
# 										
					if pdf.count() > 0:
						print ("PDF Option already exists")
					else:
						print ("no matching PDF order")
						#import pdb; pdb.set_trace()
						c = ItemOption(orderitem_id=order_data.pk,product_id=4,price=product.price,quantity=1)
						print ("c = ",c.price)
						c.save()
			
		else:
			print ("post get order =", request.POST.get('order'))
			order_item = OrderItemCreate(request.POST)
			item_id = request.POST.get('order')

			print ("Order Item PK = ",request.POST.get('id'))

			if order_item.is_valid():
				print("order item for order :",order_item.cleaned_data['order'])
				#order_data = order_item.cleaned_data
				print ("order.price =",order_item['price'].value())

				order_data = order_item.save()
				print ("Order Item ID =",order_data.pk)

				print("PDF Delivery =",order_item['pdf_download'].value())
				if order_item['pdf_download'].value():
					print("Yes PDF delivery")
					product = get_object_or_404(Product, id=4)
					print ("Product = ",product)

					pdf = ItemOption.objects.filter(orderitem_id=order_data.pk)

					print ("PDF Objects = ",pdf.count())	
					if pdf.count() > 0:
						print ("PDF Option already exists")
					else:
						print ("no matching PDF order")
						#import pdb; pdb.set_trace()
						c = ItemOption(orderitem_id=order_data.pk,product_id=4,price=product.price,quantity=1)
						print ("c = ",c.price)
						c.save()

	options = order_data.get_cost_options()
	total_cost = str(order_data.get_total_cost())

	return render(request, # send the user to the preview sending the card and order data.
					'orders/santa/preview-order.html',
					{'order': order_data, 'options':options, 'total_cost':total_cost},
	)



def order_update(request, order):
	
	order_id = request.session['order_id']
	if request.method == 'POST':
		print("Order Update Request is POST")
	else:
		print ("Order update Request is NOT Post")
		print ("Session ID = ",request.session['order_id'])
		
		order_item = get_object_or_404(OrderItem, pk=order)		

		print("Order ID = ",order_id)
		print("order Item ID = ",order_item.order_id)
		request.session['edited_order'] = order
		print ("Edited order Session Variable = ", request.session['edited_order'])

		if str(order_item.order_id) == str(order_id):
			print ("They are equal")
			form = OrderItemCreate(instance=order_item)
		str(order_item.get_total_cost())
		return render(request, # send the user to the preview sending the card and order data.
					'orders/santa/order-detail.html',
					{'form': form},
		)

def remove_item(request, item_id):

	order_id = request.session['order_id']
	if request.method == 'POST':
		print("Item Delete Request is POST")
	else:
		print("Item Delete Request is not a POST")

	print ("Item requested to delete = ",item_id)

	if OrderItem.objects.filter(pk=item_id).exists():
		print("Item to Remove Exists - needs removing")
		OrderItem.objects.filter(pk=item_id).delete()
	else:
		print("Item to Remove NOT found - nothing needs doing")

	return  redirect('cart:shopping_cart')

	# html = "<html><body><h1>RESPONSE!</h1></body></html>"
	# return HttpResponse(html)

 # @never_cache
 # def order_create(request):

 # 	if request.method == 'POST': #if the view is being accessed from the compelted form
 # 		print("Request is POST")
 # 		if Order.objects.filter(ref=request.POST.get('ref')): # check to see if this ref exists in Orders table already.
 # 			print("Ref does already exists") # Code here if the item already has posted data to the model
 # 			a = Order.objects.get(ref=request.POST.get('ref'))

# 			#import pdb; pdb.set_trace()
# 			print ("PDF Download =",request.POST.get('pdf_download'))
# 			if not request.POST.get('pdf_download'):
# 				print("No PDF (removed)")
# 				product = get_object_or_404(Product, id=4)
# 				cart.remove(product, ref=a.ref)
# 			else:
# 				product = get_object_or_404(Product, id=4)
# 				cart.add(product, ref=a.ref)

# 			order = OrderCreateForm(request.POST, instance=a)
# 			updated_order = order.save()

# 			for key, value in request.session.items():
#    				print('{} => {} => {}'.format(key, value, type(value)))

# 			return render(request, # send the user to the preview sending the card and order data.
# 				'orders/santa/preview-order.html',
# 				{'order': updated_order, 'cart':cart},
# 			)
# 		else:
# 			print("does not exist")
# 			form = OrderCreateForm(request.POST) # create the form from the POST data
# 			if form.is_valid(): #check to see if the data is valid
# 				#import pdb; pdb.set_trace()
# 				order = form.save() # save the form to the model (database)
# 				if order.pdf_download == True: # if the user has selected PDF download add this to the cart
# 					product = get_object_or_404(Product, id=4)
# 					cart.add(product, ref=order.ref)
# 				else:
# 					print ("PDF NO")
# 				return render(request, # send the user to the preview sending the card and order data.
# 								'orders/santa/preview-order.html',
# 								{'order': order, 'cart':cart},
# 				)
# 			else:
# 				print ("Form Not Valid")    
# 	else:
# 		form = OrderCreateForm(initial={'ref':request.session['ref']}) #if not a post set the form and add the cart product ID
# 	#print ("PRINT THIS = %s" % cart.product_id)
# 	return render(request, # send user to complete the order details.
# 				  'orders/santa/order-detail.html',
# 				  {'cart': cart, 'form': form}
# 	)