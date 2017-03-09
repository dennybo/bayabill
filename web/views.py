from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from billing.models import Category, CategoryLang, Language, Product, ProductLang, ProductPricing, Store


def index(request):
    return HttpResponse('Hello')


def category(request, url_key):
    store = Store.records.get(name=request.site.name)
    try:
        language = Language.records.get(iso_code=request.LANGUAGE_CODE)
        category = CategoryLang.records.select_related('category').get(
            category__store=store,
            language=language,
            url_key=url_key,
        )
        products = ProductLang.records.filter(
            product__category=category.category,
            language=language,
        )
        return render(request, 'web/category.html', {
            'page_description': category.meta_description,
            'category': category,
            'products': products,
        })
    except Language.DoesNotExist:
        raise Http404(_('Content is not available in this language.'))
    except CategoryLang.DoesNotExist:
        raise Http404(_('Category you are looking for does not exist.'))


def product(request, category_url_key, url_key):
    store = Store.records.get(name=request.site.name)
    try:
        language = Language.records.get(iso_code=request.LANGUAGE_CODE)
        product = ProductLang.records.select_related('product').get(
            product__store=store,
            language=language,
            url_key=url_key,
        )
        return render(request, 'web/product.html', {
            'page_description': product.meta_description,
            'product': product,
        })
    except Language.DoesNotExist:
        raise Http404(_('Content is not available in this language.'))
    except ProductLang.DoesNotExist:
        raise Http404(_('Product you are looking for does not exist.'))
