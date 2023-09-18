from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'total_price', 'grand_total_price', 'status', 'created']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]
