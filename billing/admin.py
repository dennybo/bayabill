from django.contrib import admin

from .models import Language, Currency, Country, Store

admin.site.register(Language)
admin.site.register(Currency)
admin.site.register(Country)
admin.site.register(Store)
