from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from billing.models import Category, CategoryLang, Language, Store, Product, ProductLang


def index(request):
    return HttpResponse('Hello')


def category(request, url_key):
    store = Store.records.get(name=request.site.name)
    try:
        language = Language.records.get(iso_code=request.LANGUAGE_CODE)
        category = CategoryLang.records.get(
            category__store=store,
            language=language,
            url_key=url_key,
        )
        return HttpResponse(category.title)
    except Language.DoesNotExist:
        raise Http404(_('Content is not available in this language.'))
    except CategoryLang.DoesNotExist:
        raise Http404(_('Category you are looking for does not exist.'))


def product(request, category_url_key, url_key):
    store = Store.records.get(name=request.site.name)
    try:
        language = Language.records.get(iso_code=request.LANGUAGE_CODE)
        product = ProductLang.records.get(
            product__store=store,
            language=language,
            url_key=url_key,
        )
        return HttpResponse(product.title)
    except Language.DoesNotExist:
        raise Http404(_('Content is not available in this language.'))
    except ProductLang.DoesNotExist:
        raise Http404(_('Product you are looking for does not exist.'))
