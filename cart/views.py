from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

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
	cart = Cart(request)
	#return render(request, 'cart/detail.html', {'cart': cart})
	return render(request, 'santa/shopping-cart.html', {'cart': cart})