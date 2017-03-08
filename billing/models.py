from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _

from account.models import User


class Language(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    iso_code = fields.CharField(
        verbose_name=_('ISO Code'),
        max_length=2,
        null=False,
        blank=False,
        unique=True,
    )
    title = fields.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    is_active = fields.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_language'
        default_related_name = 'languages'
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __unicode__(self):
        return '%(id)d: %(title)s (%(iso_code)s)' % {
            'id': self.id,
            'iso_code': self.iso_code,
            'title': self.title,
        }


class Currency(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    iso_code = fields.CharField(
        verbose_name=_('ISO Code'),
        max_length=3,
        null=False,
        blank=False,
        unique=True,
    )
    title = fields.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    prefix = fields.CharField(
        verbose_name=_('Prefix'),
        max_length=255,
        null=False,
        blank=True,
    )
    suffix = fields.CharField(
        verbose_name=_('Suffix'),
        max_length=255,
        null=False,
        blank=True,
    )
    rate = fields.DecimalField(
        verbose_name=_('Conversion Rate'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=False,
        default=1,
    )
    is_active = fields.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_currency'
        default_related_name = 'currencies'
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __unicode__(self):
        return '%(id)d: %(title)s (%(iso_code)s)' % {
            'id': self.id,
            'iso_code': self.iso_code,
            'title': self.title,
        }


class Country(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    iso_code = fields.CharField(
        verbose_name=_('ISO Code'),
        max_length=2,
        null=False,
        blank=False,
        unique=True,
    )
    title = fields.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    default_language = models.ForeignKey(
        Language,
        related_name='countries',
        null=True,
        blank=True,
    )
    default_currency = models.ForeignKey(
        Currency,
        related_name='countries',
        null=True,
        blank=True,
    )
    is_active = fields.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_country'
        default_related_name = 'countries'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __unicode__(self):
        return '%(id)d: %(title)s (%(iso_code)s)' % {
            'id': self.id,
            'iso_code': self.iso_code,
            'title': self.title,
        }


class Store(Site):
    url = fields.URLField(
        verbose_name=_('Store Url'),
        max_length=255,
        null=False,
        blank=False,
    )
    default_language = models.ForeignKey(
        Language,
        related_name='stores',
        null=True,
        blank=True,
    )
    default_currency = models.ForeignKey(
        Currency,
        related_name='stores',
        null=True,
        blank=True,
    )
    default_country = models.ForeignKey(
        Country,
        related_name='stores',
        null=True,
        blank=True,
    )
    is_default = fields.BooleanField(
        verbose_name=_('Is Default'),
        null=False,
        blank=False,
        default=False,
        db_index=True,
    )
    is_active = fields.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_store'
        default_related_name = 'stores'
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __unicode__(self):
        return '%(id)d: %(name)s (%(domain)s)' % {
            'id': self.id,
            'domain': self.domain,
            'name': self.name,
        }


class SettingQuerySet(models.QuerySet):

    def site(self):
        return self.filter(site=settings.SITE_ID)


class SettingManager(models.Manager):

    def get_queryset(self):
        return SettingQuerySet(self.model, using=self._db)

    def site(self):
        return self.get_queryset().site()


class Setting(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    store = models.ForeignKey(
        Store,
        related_name='settings',
        null=False,
        blank=False,
    )
    name = fields.CharField(
        verbose_name=_('Name'),
        max_length=255,
        null=False,
        blank=False,
    )
    value = fields.CharField(
        verbose_name=_('Value'),
        max_length=255,
        null=False,
        blank=False,
    )
    records = SettingManager()

    class Meta:
        db_table = 'billing_setting'
        default_related_name = 'settings'
        unique_together = (
            ('store', 'name')
        )
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    def __unicode__(self):
        return '%(id)d: %(name)s => %(value)s' % {
            'id': self.id,
            'name': self.name,
            'value': self.value,
        }


class Category(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    store = models.ForeignKey(
        Store,
        related_name='categories',
        null=False,
        blank=False,
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
    )
    is_active = fields.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    create_date = fields.DateTimeField(
        verbose_name=_('Create Date'),
        null=False,
        blank=True,
        auto_now_add=True,
    )
    update_date = fields.DateTimeField(
        verbose_name=_('Update Date'),
        null=True,
        blank=True,
        auto_now=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_category'
        default_related_name = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        if self.store.default_language is not None:
            return CategoryLang.records.get(
                category=self,
                language=self.store.default_language,
            ).title
        else:
            return str(self.id)


class CategoryLang(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='langs',
        null=False,
        blank=False,
    )
    language = models.ForeignKey(
        Language,
        related_name='categories',
        null=False,
        blank=False,
    )
    title = fields.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    description = fields.TextField(
        verbose_name=_('Description'),
        null=False,
        blank=True,
    )
    url_key = fields.CharField(
        verbose_name=_('URL Key'),
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )
    meta_title = fields.CharField(
        verbose_name=_('Meta Title'),
        max_length=255,
        null=False,
        blank=True,
    )
    meta_description = fields.CharField(
        verbose_name=_('Meta Description'),
        max_length=255,
        null=False,
        blank=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_category_lang'
        default_related_name = 'langs'
        verbose_name = _('Category Language')
        verbose_name_plural = _('Category Languages')

    def __unicode__(self):
        return '%(id)d: %(lang)s => %(title)s' % {
            'id': self.id,
            'lang': self.language.title,
            'title': self.title,
        }


class Product(models.Model):
    Payment_Types = (
        (0, _('Free')),
        (1, _('One-Time')),
        (2, _('Recurring')),
    )
    Payment_Terms = (
        (0, _('One-Time')),
        (1, _('Hourly')),
        (24, _('Daily')),
    )
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    store = models.ForeignKey(
        Store,
        related_name='products',
        null=False,
        blank=False,
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        null=False,
        blank=False,
    )
    quantity = fields.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=1,
    )
    enable_stock_control = fields.BooleanField(
        verbose_name=_('Enable Stock Control'),
        null=False,
        blank=False,
        default=False,
    )
    payment_types = fields.PositiveSmallIntegerField(
        verbose_name=_('Payment Type'),
        choices=Payment_Types,
        null=False,
        blank=False,
        default=2,
    )
    is_active = fields.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
        db_index=True,
    )
    create_date = fields.DateTimeField(
        verbose_name=_('Create Date'),
        null=False,
        blank=True,
        auto_now_add=True,
    )
    update_date = fields.DateTimeField(
        verbose_name=_('Update Date'),
        null=True,
        blank=True,
        auto_now=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_product'
        default_related_name = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        if self.store.default_language is not None:
            return ProductLang.records.get(
                product=self,
                language=self.store.default_language,
            ).title
        else:
            return str(self.id)


class ProductLang(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    product = models.ForeignKey(
        Product,
        related_name='langs',
        null=False,
        blank=False,
    )
    language = models.ForeignKey(
        Language,
        related_name='products',
        null=False,
        blank=False,
    )
    title = fields.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    description = fields.TextField(
        verbose_name=_('Description'),
        null=False,
        blank=True,
    )
    url_key = fields.CharField(
        verbose_name=_('URL Key'),
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
    )
    meta_title = fields.CharField(
        verbose_name=_('Meta Title'),
        max_length=255,
        null=False,
        blank=True,
    )
    meta_description = fields.CharField(
        verbose_name=_('Meta Description'),
        max_length=255,
        null=False,
        blank=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_product_lang'
        default_related_name = 'langs'
        verbose_name = _('Product Language')
        verbose_name_plural = _('Product Languages')

    def __unicode__(self):
        return '%(id)d: %(lang)s => %(title)s' % {
            'id': self.id,
            'lang': self.language.title,
            'title': self.title,
        }


class ProductPricing(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    product = models.ForeignKey(
        Product,
        related_name='pricing',
        null=False,
        blank=False,
    )
    currency = models.ForeignKey(
        Currency,
        related_name='pricing',
        null=False,
        blank=False,
    )
    onetime_setup_fee = fields.DecimalField(
        verbose_name=_('One Time (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    onetime = fields.DecimalField(
        verbose_name=_('One Time'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    onetime_cost = fields.DecimalField(
        verbose_name=_('One Time (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    hourly_setup_fee = fields.DecimalField(
        verbose_name=_('Hourly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    hourly = fields.DecimalField(
        verbose_name=_('Hourly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    hourly_cost = fields.DecimalField(
        verbose_name=_('Hourly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    daily_setup_fee = fields.DecimalField(
        verbose_name=_('Daily (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    daily = fields.DecimalField(
        verbose_name=_('Daily'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    daily_cost = fields.DecimalField(
        verbose_name=_('Daily (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    weekly_setup_fee = fields.DecimalField(
        verbose_name=_('Weekly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    weekly = fields.DecimalField(
        verbose_name=_('Weekly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    weekly_cost = fields.DecimalField(
        verbose_name=_('Weekly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    monthly_setup_fee = fields.DecimalField(
        verbose_name=_('Monthly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    monthly = fields.DecimalField(
        verbose_name=_('Monthly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    monthly_cost = fields.DecimalField(
        verbose_name=_('Monthly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    quarterly_setup_fee = fields.DecimalField(
        verbose_name=_('Quarterly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    quarterly = fields.DecimalField(
        verbose_name=_('Quarterly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    quarterly_cost = fields.DecimalField(
        verbose_name=_('Quarterly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    semi_annually_setup_fee = fields.DecimalField(
        verbose_name=_('Semi-Annually (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    semi_annually = fields.DecimalField(
        verbose_name=_('Semi-Annually'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    semi_annually_cost = fields.DecimalField(
        verbose_name=_('Semi-Annually (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    annually_setup_fee = fields.DecimalField(
        verbose_name=_('Annually (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    annually = fields.DecimalField(
        verbose_name=_('Annually'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    annually_cost = fields.DecimalField(
        verbose_name=_('Annually (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    biennially_setup_fee = fields.DecimalField(
        verbose_name=_('Biennially (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    biennially = fields.DecimalField(
        verbose_name=_('Biennially'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    biennially_cost = fields.DecimalField(
        verbose_name=_('Biennially (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    triennially_setup_fee = fields.DecimalField(
        verbose_name=_('Triennially (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    triennially = fields.DecimalField(
        verbose_name=_('Triennially'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=-1,
    )
    triennially_cost = fields.DecimalField(
        verbose_name=_('Triennially (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_product_pricing'
        default_related_name = 'pricing'
        unique_together = (
            ('product', 'currency')
        )
        verbose_name = _('Product Pricing')
        verbose_name_plural = _('Product Pricing')


class Cart(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    user = models.ForeignKey(
        User,
        related_name='carts',
        null=False,
        blank=False,
    )
    currency = models.ForeignKey(
        Currency,
        related_name='carts',
        null=False,
        blank=False,
    )
    product = models.ManyToManyField(
        Product,
        through='CartItem',
        through_fields=('cart', 'product'),
    )
    total_amount = fields.DecimalField(
        verbose_name=_('Total Amount'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    create_date = models.DateTimeField(
        verbose_name=_('Create Date'),
        null=False,
        blank=False,
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name=_('Update Date'),
        null=True,
        blank=True,
        auto_now=True,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_cart'
        default_related_name = 'carts'
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __unicode__(self):
        return str(self.id)


class CartItem(models.Model):
    id = fields.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    product = models.ForeignKey(
        Product,
        related_name='items',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    term = fields.PositiveSmallIntegerField(
        verbose_name=_('Term'),
        null=False,
        blank=False,
        choices=Product.Payment_Terms,
    )
    unit_price = fields.DecimalField(
        verbose_name=_('Unit Price'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=False,
    )
    quantity = fields.PositiveSmallIntegerField(
        verbose_name=_('Quantity'),
        null=False,
        blank=False,
        default=1,
    )
    item_price = fields.DecimalField(
        verbose_name=_('Item Price'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=False,
    )
    records = models.Manager()

    class Meta:
        db_table = 'billing_cart_item'
        default_related_name = 'items'
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __unicode__(self):
        return str(self.id)
