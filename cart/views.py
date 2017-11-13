from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from orders.models import Order, OrderItem, ItemOption

@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product,
				 #quantity=cd['quantity'],
				 quantity=1,
				 update_quantity=cd['update'])
	else:
		print ("Form is not Valid")
	#return redirect('cart:cart_detail') intercept order here to take straight to the Create Order page
	return redirect('orders:order_create')

def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')
	

def cart_detail(request):
	cart_total = 0
	order_id = request.session['order_id']
	print ("cart_detail order id =", order_id)
	if OrderItem.objects.filter(order_id=order_id).exists():
		print("Order Items Found")
		items = OrderItem.objects.filter(order_id=order_id)
		
		for item in items:
			cart_total += item.price
			if ItemOption.objects.filter(orderitem_id=item.id).exists():
				options = get_list_or_404(ItemOption, orderitem_id=item.id)
				print ("Item Options do exist")
			
				for option in options:
					cart_total += option.price
					print ("Product = ",option.price)
				print ("order.cart_detail item.price =",item.price)
			print ("Items in Cart =", items)
	else:
		print("No Order items found")
		items=''
	
	
	print ("Cart Total =", cart_total)

	# html = "<html><body><h1>Respose</h1></body></html>"
	# return HttpResponse(html)
	return render(request, 'santa/shopping-cart.html', {'cart': items,'cart_total':cart_total})