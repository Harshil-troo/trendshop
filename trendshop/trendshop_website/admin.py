from django.contrib import admin
from .models import Category,Product
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from trendshop_website.models import Cart, CartItem, Order, OrderPayment

admin.site.register(Category)
admin.site.register(Product)

@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    This class will register cart model in admin site.
    """
    date_hierarchy = 'created'
    search_fields = ['user__username', 'user__email', 'user__phone_number']
    list_display = ['user', 'status']
    list_filter = ['status']
    list_editable = ['status']
    list_per_page = 10


@admin.register(CartItem)
class CartItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    This class will register cart item model in admin site.
    """
    search_fields = ['cart__user__username', 'item__name']
    list_display = ['cart', 'item', 'quantity', 'food_image']
    list_per_page = 10

    def food_image(self, obj):
        return format_html("<img src='{}' width='55' height='55'/>".format(obj.item.image.url))

    food_image.short_description = 'Product Image'


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    This class will register order model in admin site.
    """
    date_hierarchy = 'created'
    search_fields = ['order', 'user__username', 'user__email', 'user__phone_number']
    list_display = ['order', 'user', 'total_amount', 'status']
    list_filter = ['status']
    list_editable = ['status']
    list_per_page = 10


@admin.register(OrderPayment)
class OrderPaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    This class will register order payment model in admin site.
    """
    date_hierarchy = 'created'
    search_fields = ['order', 'provider_order_id', 'payment_id', 'signature_id', 'user__username',
                     'user__email', 'user__phone_number']
    list_display = ['order', 'user', 'status']
    list_filter = ['status']
    list_editable = ['status']
    list_per_page = 10


