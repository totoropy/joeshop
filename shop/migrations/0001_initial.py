# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from decimal import Decimal
import shop.util.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('address2', models.CharField(max_length=255, verbose_name='Address2', blank=True)),
                ('zip_code', models.CharField(max_length=20, verbose_name='Zip Code')),
                ('city', models.CharField(max_length=20, verbose_name='City')),
                ('state', models.CharField(max_length=255, verbose_name='State')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('cart', models.ForeignKey(related_name='items', to='shop.Cart')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtraOrderItemPriceField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('value', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Amount', max_digits=30, decimal_places=2)),
                ('data', jsonfield.fields.JSONField(null=True, verbose_name='Serialized extra data', blank=True)),
            ],
            options={
                'verbose_name': 'Extra order item price field',
                'verbose_name_plural': 'Extra order item price fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtraOrderPriceField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('value', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Amount', max_digits=30, decimal_places=2)),
                ('data', jsonfield.fields.JSONField(null=True, verbose_name='Serialized extra data', blank=True)),
                ('is_shipping', models.BooleanField(default=False, verbose_name='Is shipping', editable=False)),
            ],
            options={
                'verbose_name': 'Extra order price field',
                'verbose_name_plural': 'Extra order price fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=10, verbose_name='Status', choices=[(10, 'Processing'), (20, 'Confirming'), (30, 'Confirmed'), (40, 'Completed'), (50, 'Shipped'), (60, 'Canceled')])),
                ('order_subtotal', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Order subtotal', max_digits=30, decimal_places=2)),
                ('order_total', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Order Total', max_digits=30, decimal_places=2)),
                ('shipping_address_text', models.TextField(null=True, verbose_name='Shipping address', blank=True)),
                ('billing_address_text', models.TextField(null=True, verbose_name='Billing address', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('cart_pk', models.PositiveIntegerField(null=True, verbose_name='Cart primary key', blank=True)),
                ('country', models.ForeignKey(verbose_name='Country', blank=True, to='shop.Country', null=True)),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderExtraInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='Extra info', blank=True)),
                ('order', models.ForeignKey(related_name='extra_info', verbose_name='Order', to='shop.Order')),
            ],
            options={
                'verbose_name': 'Order extra info',
                'verbose_name_plural': 'Order extra info',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_reference', models.CharField(max_length=255, verbose_name='Product reference')),
                ('product_name', models.CharField(max_length=255, null=True, verbose_name='Product name', blank=True)),
                ('unit_price', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Unit price', max_digits=30, decimal_places=2)),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('line_subtotal', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Line subtotal', max_digits=30, decimal_places=2)),
                ('line_total', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Line total', max_digits=30, decimal_places=2)),
                ('order', models.ForeignKey(related_name='items', verbose_name='Order', to='shop.Order')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Order item',
                'verbose_name_plural': 'Order items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='Email', blank=True)),
                ('amount', shop.util.fields.CurrencyField(default=0, verbose_name='Amount', max_digits=10, decimal_places=2)),
                ('currency', models.CharField(max_length=3, verbose_name='Currency')),
                ('result', models.CharField(max_length=20, verbose_name='Result')),
                ('wallet_address', models.CharField(max_length=34, unique=True, null=True, verbose_name='Wallet address')),
                ('status', models.IntegerField(default=10, verbose_name='Payment status', choices=[(10, 'Created'), (20, 'Unconfirmed'), (30, 'Confirmed'), (40, 'Canceled')])),
                ('transaction_id', models.CharField(max_length=255, null=True, verbose_name='Transaction ID', blank=True)),
                ('payment_method', models.CharField(max_length=255, verbose_name='Payment method')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('order', models.ForeignKey(verbose_name='Order', to='shop.Order')),
            ],
            options={
                'verbose_name': 'Order payment',
                'verbose_name_plural': 'Order payments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('unit_price', shop.util.fields.CurrencyField(default=Decimal('0.0'), verbose_name='Unit price', max_digits=30, decimal_places=2)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_shop.product_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Product', blank=True, to='shop.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extraorderpricefield',
            name='order',
            field=models.ForeignKey(verbose_name='Order', to='shop.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extraorderitempricefield',
            name='order_item',
            field=models.ForeignKey(verbose_name='Order item', to='shop.OrderItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(to='shop.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='shop.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='user_billing',
            field=models.OneToOneField(related_name='billing_address', null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='user_shipping',
            field=models.OneToOneField(related_name='shipping_address', null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
