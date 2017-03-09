from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='home',
    ),
    url(
        r'^(?P<category_url_key>[\w-]+)/(?P<url_key>[\w-]+)',
        views.product,
        name='product',
    ),
    url(
        r'^(?P<url_key>[\w-]+)',
        views.category,
        name='category',
    ),
]
