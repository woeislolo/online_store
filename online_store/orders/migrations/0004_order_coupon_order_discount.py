# Generated by Django 5.0 on 2025-04-07 05:55

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0003_alter_coupon_active_alter_coupon_code_and_more'),
        ('orders', '0003_order_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='coupons.coupon', verbose_name='Промокод'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка, %'),
        ),
    ]
