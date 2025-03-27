import csv
import datetime

from django.http import HttpResponse
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
    actions = ['export_to_csv']


    def order_stripe_payment(self, obj):
        url = obj.get_stripe_url()
        if obj.stripe_id:
            return mark_safe(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{obj.stripe_id}</a>')
        return None
    
    order_stripe_payment.short_description = 'id платежа (ссылка в Stripe)'


    @admin.action(description='Экспорт в CSV')
    def export_to_csv(self, request, queryset):
        opts = self.model._meta
        response = HttpResponse(
            content_type='text/csv',
            headers={
                "Content-Disposition": 'attachment; filename=orders.csv'
                },
            )
        writer = csv.writer(response)
        fields = [field for field in opts.get_fields() \
                if not field.many_to_many and not field.one_to_many]
        writer.writerow([field.verbose_name for field in fields])

        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                data_row.append(value)
            writer.writerow(data_row)
            
        return response
