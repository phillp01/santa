from django.contrib import admin
from .models import Order, OrderItem, customer

class CustomerItemInline(admin.TabularInline):
	model = customer
	extra = 0

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


class OrderAdmin(admin.ModelAdmin):
	list_display = ['id','created']
	inlines = [CustomerItemInline,OrderItemInline]

admin.site.register(Order, OrderAdmin)