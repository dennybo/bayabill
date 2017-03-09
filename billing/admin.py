from django.contrib import admin
from django.contrib.sites.models import Site

from account.models import User
from .models import Language, Currency, Country, Store, Setting, Category, CategoryLang, Product, ProductLang, ProductPricing, Cart, CartItem


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'iso_code', 'is_active']
    list_display_links = ['iso_code', 'title']
    search_fields = ['iso_code', 'title']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'iso_code',
                    'prefix', 'suffix', 'rate', 'is_active']
    list_display_links = ['iso_code', 'title']
    search_fields = ['iso_code', 'title']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'iso_code',
                    'default_language', 'default_currency', 'is_active']
    list_display_links = ['iso_code', 'title']
    search_fields = ['iso_code', 'title']


class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'default_language',
                    'default_currency', 'default_country', 'is_default', 'is_active']
    list_display_links = ['name']
    search_fields = ['name']


class SettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'value', 'store']
    list_display_links = ['name', 'value']
    search_fields = ['name', 'value']


class CategoryLangInline(admin.StackedInline):
    model = CategoryLang


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'parent', 'store', 'is_active']
    list_display_links = ['title']
    inlines = [CategoryLangInline]

    def title(self, obj):
        return CategoryLang.records.get(
            category=obj,
            language=obj.store.default_language,
        ).title


class ProductLangInline(admin.StackedInline):
    model = ProductLang


class ProductPricingInline(admin.StackedInline):
    model = ProductPricing


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'store', 'is_active']
    list_display_links = ['title']
    inlines = [ProductLangInline, ProductPricingInline]

    def title(self, obj):
        return ProductLang.records.get(
            product=obj,
            language=obj.store.default_language,
        ).title


class CartItemInline(admin.StackedInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'currency', 'total_amount']
    list_display_links = ['user']
    search_fields = ['user']
    inlines = [CartItemInline]

admin.site.unregister(Site)
admin.site.register(User)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
