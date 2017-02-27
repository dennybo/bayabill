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

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return str(self.id)


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
