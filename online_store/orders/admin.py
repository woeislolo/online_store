from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'post_code', 'city', 'paid', 
                    'order_stripe_payment', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    def order_stripe_payment(self, obj):
        url = obj.get_stripe_url()
        if obj.stripe_id:
            return mark_safe(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{obj.stripe_id}</a>')
        return None

    order_stripe_payment.short_description = 'id платежа (ссылка в Stripe)'
   