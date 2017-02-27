from django.contrib import admin

from .models import Language, Currency, Country, Store, Category, CategoryLang


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'iso_code', 'title', 'is_active']
    list_display_links = ['iso_code', 'title']
    search_fields = ['iso_code', 'title']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'iso_code', 'title',
                    'prefix', 'suffix', 'rate', 'is_active']
    list_display_links = ['iso_code', 'title']
    search_fields = ['iso_code', 'title']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'iso_code', 'title',
                    'default_language', 'default_currency', 'is_active']
    list_display_links = ['iso_code', 'title']
    search_fields = ['iso_code', 'title']


class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'default_language',
                    'default_currency', 'default_country', 'is_default', 'is_active']
    list_display_links = ['title']
    search_fields = ['title']


class CategoryInline(admin.StackedInline):
    model = CategoryLang


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent', 'store', 'is_active']
    inlines = [CategoryInline]

admin.site.register(Language, LanguageAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Category, CategoryAdmin)
