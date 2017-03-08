# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('total_amount', models.DecimalField(default=0, verbose_name='Total Amount', max_digits=10, decimal_places=4, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update Date', null=True)),
            ],
            options={
                'db_table': 'billing_cart',
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'default_related_name': 'carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('term', models.PositiveSmallIntegerField(verbose_name='Term', choices=[(0, 'One-Time'), (1, 'Hourly'), (24, 'Daily')])),
                ('unit_price', models.DecimalField(verbose_name='Unit Price', max_digits=10, decimal_places=4)),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Quantity')),
                ('item_price', models.DecimalField(verbose_name='Item Price', max_digits=10, decimal_places=4)),
                ('cart', models.ForeignKey(related_name='items', to='billing.Cart')),
            ],
            options={
                'db_table': 'billing_cart_item',
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'default_related_name': 'items',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Is Active')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update Date', null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='billing.Category', null=True)),
            ],
            options={
                'db_table': 'billing_category',
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'default_related_name': 'categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryLang',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('url_key', models.CharField(max_length=255, verbose_name='URL Key', db_index=True)),
                ('meta_title', models.CharField(max_length=255, verbose_name='Meta Title', blank=True)),
                ('meta_description', models.CharField(max_length=255, verbose_name='Meta Description', blank=True)),
                ('category', models.ForeignKey(related_name='langs', to='billing.Category')),
            ],
            options={
                'db_table': 'billing_category_lang',
                'verbose_name': 'Category Language',
                'verbose_name_plural': 'Category Languages',
                'default_related_name': 'langs',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('iso_code', models.CharField(unique=True, max_length=2, verbose_name='ISO Code')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Is Active')),
            ],
            options={
                'db_table': 'billing_country',
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'default_related_name': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('iso_code', models.CharField(unique=True, max_length=3, verbose_name='ISO Code')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('prefix', models.CharField(max_length=255, verbose_name='Prefix', blank=True)),
                ('suffix', models.CharField(max_length=255, verbose_name='Suffix', blank=True)),
                ('rate', models.DecimalField(default=1, verbose_name='Conversion Rate', max_digits=10, decimal_places=4)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Is Active')),
            ],
            options={
                'db_table': 'billing_currency',
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'default_related_name': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('iso_code', models.CharField(unique=True, max_length=2, verbose_name='ISO Code')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Is Active')),
            ],
            options={
                'db_table': 'billing_language',
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'default_related_name': 'languages',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('enable_stock_control', models.BooleanField(default=False, verbose_name='Enable Stock Control')),
                ('payment_types', models.PositiveSmallIntegerField(default=2, verbose_name='Payment Type', choices=[(0, 'Free'), (1, 'One-Time'), (2, 'Recurring')])),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Is Active')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update Date', null=True)),
                ('category', models.ForeignKey(related_name='products', to='billing.Category')),
            ],
            options={
                'db_table': 'billing_product',
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'default_related_name': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductLang',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('url_key', models.CharField(max_length=255, verbose_name='URL Key', db_index=True)),
                ('meta_title', models.CharField(max_length=255, verbose_name='Meta Title', blank=True)),
                ('meta_description', models.CharField(max_length=255, verbose_name='Meta Description', blank=True)),
                ('language', models.ForeignKey(related_name='products', to='billing.Language')),
                ('product', models.ForeignKey(related_name='langs', to='billing.Product')),
            ],
            options={
                'db_table': 'billing_product_lang',
                'verbose_name': 'Product Language',
                'verbose_name_plural': 'Product Languages',
                'default_related_name': 'langs',
            },
        ),
        migrations.CreateModel(
            name='ProductPricing',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('onetime_setup_fee', models.DecimalField(default=-1, verbose_name='One Time (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('onetime', models.DecimalField(default=-1, verbose_name='One Time', max_digits=10, decimal_places=4, blank=True)),
                ('onetime_cost', models.DecimalField(default=0, verbose_name='One Time (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('hourly_setup_fee', models.DecimalField(default=-1, verbose_name='Hourly (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('hourly', models.DecimalField(default=-1, verbose_name='Hourly', max_digits=10, decimal_places=4, blank=True)),
                ('hourly_cost', models.DecimalField(default=0, verbose_name='Hourly (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('daily_setup_fee', models.DecimalField(default=-1, verbose_name='Daily (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('daily', models.DecimalField(default=-1, verbose_name='Daily', max_digits=10, decimal_places=4, blank=True)),
                ('daily_cost', models.DecimalField(default=0, verbose_name='Daily (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('weekly_setup_fee', models.DecimalField(default=-1, verbose_name='Weekly (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('weekly', models.DecimalField(default=-1, verbose_name='Weekly', max_digits=10, decimal_places=4, blank=True)),
                ('weekly_cost', models.DecimalField(default=0, verbose_name='Weekly (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('monthly_setup_fee', models.DecimalField(default=-1, verbose_name='Monthly (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('monthly', models.DecimalField(default=-1, verbose_name='Monthly', max_digits=10, decimal_places=4, blank=True)),
                ('monthly_cost', models.DecimalField(default=0, verbose_name='Monthly (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('quarterly_setup_fee', models.DecimalField(default=-1, verbose_name='Quarterly (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('quarterly', models.DecimalField(default=-1, verbose_name='Quarterly', max_digits=10, decimal_places=4, blank=True)),
                ('quarterly_cost', models.DecimalField(default=0, verbose_name='Quarterly (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('semi_annually_setup_fee', models.DecimalField(default=-1, verbose_name='Semi-Annually (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('semi_annually', models.DecimalField(default=-1, verbose_name='Semi-Annually', max_digits=10, decimal_places=4, blank=True)),
                ('semi_annually_cost', models.DecimalField(default=0, verbose_name='Semi-Annually (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('annually_setup_fee', models.DecimalField(default=-1, verbose_name='Annually (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('annually', models.DecimalField(default=-1, verbose_name='Annually', max_digits=10, decimal_places=4, blank=True)),
                ('annually_cost', models.DecimalField(default=0, verbose_name='Annually (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('biennially_setup_fee', models.DecimalField(default=-1, verbose_name='Biennially (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('biennially', models.DecimalField(default=-1, verbose_name='Biennially', max_digits=10, decimal_places=4, blank=True)),
                ('biennially_cost', models.DecimalField(default=0, verbose_name='Biennially (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('triennially_setup_fee', models.DecimalField(default=-1, verbose_name='Triennially (Setup Fee)', max_digits=10, decimal_places=4, blank=True)),
                ('triennially', models.DecimalField(default=-1, verbose_name='Triennially', max_digits=10, decimal_places=4, blank=True)),
                ('triennially_cost', models.DecimalField(default=0, verbose_name='Triennially (Cost)', max_digits=10, decimal_places=4, blank=True)),
                ('currency', models.ForeignKey(related_name='pricing', to='billing.Currency')),
                ('product', models.ForeignKey(related_name='pricing', to='billing.Product')),
            ],
            options={
                'db_table': 'billing_product_pricing',
                'verbose_name': 'Product Pricing',
                'verbose_name_plural': 'Product Pricing',
                'default_related_name': 'pricing',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
            ],
            options={
                'db_table': 'billing_setting',
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
                'default_related_name': 'settings',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('site_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='sites.Site')),
                ('url', models.URLField(max_length=255, verbose_name='Store Url')),
                ('is_default', models.BooleanField(default=False, db_index=True, verbose_name='Is Default')),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Is Active')),
                ('default_country', models.ForeignKey(related_name='stores', blank=True, to='billing.Country', null=True)),
                ('default_currency', models.ForeignKey(related_name='stores', blank=True, to='billing.Currency', null=True)),
                ('default_language', models.ForeignKey(related_name='stores', blank=True, to='billing.Language', null=True)),
            ],
            options={
                'db_table': 'billing_store',
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
                'default_related_name': 'stores',
            },
            bases=('sites.site',),
        ),
        migrations.AddField(
            model_name='setting',
            name='store',
            field=models.ForeignKey(related_name='settings', to='billing.Store'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(related_name='products', to='billing.Store'),
        ),
        migrations.AddField(
            model_name='country',
            name='default_currency',
            field=models.ForeignKey(related_name='countries', blank=True, to='billing.Currency', null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='default_language',
            field=models.ForeignKey(related_name='countries', blank=True, to='billing.Language', null=True),
        ),
        migrations.AddField(
            model_name='categorylang',
            name='language',
            field=models.ForeignKey(related_name='categories', to='billing.Language'),
        ),
        migrations.AddField(
            model_name='category',
            name='store',
            field=models.ForeignKey(related_name='categories', to='billing.Store'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(related_name='items', to='billing.Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='currency',
            field=models.ForeignKey(related_name='carts', to='billing.Currency'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(to='billing.Product', through='billing.CartItem'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(related_name='carts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='setting',
            unique_together=set([('store', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='productpricing',
            unique_together=set([('product', 'currency')]),
        ),
    ]
