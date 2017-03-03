from django.db import models
from django.utils.translation import ugettext_lazy as _


class Language(models.Model):
    id = models.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    iso_code = models.CharField(
        verbose_name=_('ISO Code'),
        max_length=2,
        null=False,
        blank=False,
        unique=True,
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
    )

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return self.title


class Currency(models.Model):
    id = models.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    iso_code = models.CharField(
        verbose_name=_('ISO Code'),
        max_length=3,
        null=False,
        blank=False,
        unique=True,
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    prefix = models.CharField(
        verbose_name=_('Prefix'),
        max_length=255,
        null=True,
        blank=True,
    )
    suffix = models.CharField(
        verbose_name=_('Suffix'),
        max_length=255,
        null=True,
        blank=True,
    )
    rate = models.DecimalField(
        verbose_name=_('Conversion Rate'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=False,
        default=1,
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
    )

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.iso_code


class Country(models.Model):
    id = models.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    iso_code = models.CharField(
        verbose_name=_('ISO Code'),
        max_length=2,
        null=False,
        blank=False,
        unique=True,
    )
    title = models.CharField(
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
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
    )

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.title


class Store(models.Model):
    id = models.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    url = models.URLField(
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
    ssl_enabled = models.BooleanField(
        verbose_name=_('SSL Enabled'),
        null=False,
        blank=False,
        default=True,
    )
    is_default = models.BooleanField(
        verbose_name=_('Is Default'),
        null=False,
        blank=False,
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
    )

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return self.title


class Category(models.Model):
    id = models.AutoField(
        verbose_name=_('ID'),
        primary_key=True,
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
    )
    store = models.ForeignKey(
        Store,
        related_name='categories',
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
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

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        category_lang = CategoryLang.objects.get(
            category=self,
            language=self.store.default_language,
        )
        return category_lang.title


class CategoryLang(models.Model):
    id = models.AutoField(
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
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
    )
    url_key = models.CharField(
        verbose_name=_('URL Key'),
        max_length=255,
        null=False,
        blank=False,
    )
    meta_title = models.CharField(
        verbose_name=_('Meta Title'),
        max_length=255,
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        verbose_name=_('Meta Description'),
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Product(models.Model):
    Payment_Types = (
        ('free', _('Free')),
        ('onetime', _('One-Time')),
        ('recurring', _('Recurring')),
    )
    id = models.AutoField(
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
    payment_types = models.CharField(
        verbose_name=_('Payment Type'),
        max_length=16,
        choices=Payment_Types,
        null=False,
        blank=False,
        default='recurring',
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        null=False,
        blank=False,
        default=True,
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

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        product_lang = ProductLang.objects.get(
            product=self,
            language=self.store.default_language,
        )
        return product_lang.title


class ProductLang(models.Model):
    id = models.AutoField(
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
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
    )
    url_key = models.CharField(
        verbose_name=_('URL Key'),
        max_length=255,
        null=False,
        blank=False,
    )
    meta_title = models.CharField(
        verbose_name=_('Meta Title'),
        max_length=255,
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        verbose_name=_('Meta Description'),
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class ProductPricing(models.Model):
    id = models.AutoField(
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
    onetime_setup_fee = models.DecimalField(
        verbose_name=_('One Time (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    onetime = models.DecimalField(
        verbose_name=_('One Time'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    onetime_cost = models.DecimalField(
        verbose_name=_('One Time (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    hourly_setup_fee = models.DecimalField(
        verbose_name=_('Hourly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    hourly = models.DecimalField(
        verbose_name=_('Hourly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    hourly_cost = models.DecimalField(
        verbose_name=_('Hourly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    daily_setup_fee = models.DecimalField(
        verbose_name=_('Daily (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    daily = models.DecimalField(
        verbose_name=_('Daily'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    daily_cost = models.DecimalField(
        verbose_name=_('Daily (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    weekly_setup_fee = models.DecimalField(
        verbose_name=_('Weekly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    weekly = models.DecimalField(
        verbose_name=_('Weekly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    weekly_cost = models.DecimalField(
        verbose_name=_('Weekly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    monthly_setup_fee = models.DecimalField(
        verbose_name=_('Monthly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    monthly = models.DecimalField(
        verbose_name=_('Monthly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    monthly_cost = models.DecimalField(
        verbose_name=_('Monthly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    quarterly_setup_fee = models.DecimalField(
        verbose_name=_('Quarterly (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    quarterly = models.DecimalField(
        verbose_name=_('Quarterly'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    quarterly_cost = models.DecimalField(
        verbose_name=_('Quarterly (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    semi_annually_setup_fee = models.DecimalField(
        verbose_name=_('Semi-Annually (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    semi_annually = models.DecimalField(
        verbose_name=_('Semi-Annually'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    semi_annually_cost = models.DecimalField(
        verbose_name=_('Semi-Annually (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    annually_setup_fee = models.DecimalField(
        verbose_name=_('Annually (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    annually = models.DecimalField(
        verbose_name=_('Annually'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    annually_cost = models.DecimalField(
        verbose_name=_('Annually (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    biennially_setup_fee = models.DecimalField(
        verbose_name=_('Biennially (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    biennially = models.DecimalField(
        verbose_name=_('Biennially'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    biennially_cost = models.DecimalField(
        verbose_name=_('Biennially (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    triennially_setup_fee = models.DecimalField(
        verbose_name=_('Triennially (Setup Fee)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    triennially = models.DecimalField(
        verbose_name=_('Triennially'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
    triennially_cost = models.DecimalField(
        verbose_name=_('Triennially (Cost)'),
        max_digits=10,
        decimal_places=4,
        null=False,
        blank=True,
        default=0,
    )
