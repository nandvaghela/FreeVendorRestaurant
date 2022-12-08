from django.contrib import admin
from .models import Order, OrderedFood, Payment


# Register your models here.


class OrderFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'is_ordered']
    inlines = [OrderFoodInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
admin.site.register(Payment)
