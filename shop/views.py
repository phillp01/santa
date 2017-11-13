from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart


def product_list(request, additional=False, category_slug=None):
	
	request.session['additional'] = additional
	print ("Is this an additional Letter :",request.session['additional'])
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	cart = Cart(request)
	cart.clear()

	return render(request,
				  #'shop/product/list.html',
				  'shop/santa/index.html',
				  {'category': category,
				   'categories': categories,
				   'products': products})  

def product_detail(request, id, slug):
	product = get_object_or_404(Product,
								id=id,
								slug=slug,
								available=True)
	cart_product_form = CartAddProductForm()
	return render(request,
				  'shop/product/detail.html',
				  {'product': product,
				  'cart_product_form': cart_product_form}) 