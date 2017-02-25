from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^signup',
        views.signup,
        name='signup'
        ),
    url(r'^signin',
        auth_views.login,
        {
            'template_name': 'account/signin.html',
        },
        name='signin'
        ),
    url(r'^signout',
        auth_views.logout,
        name='signout'
        ),
    url(r'^forgot-password',
        auth_views.password_reset,
        {
            'post_reset_redirect': 'account:forgot_password_done',
        },
        name='forgot_password',
        ),
    url(r'^forgot-password-done',
        auth_views.password_reset_done,
        name='forgot_password_done'
        ),
    url(r'^reset-password/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)',
        auth_views.password_reset_confirm,
        {
            'post_reset_redirect': 'account:reset_password_done',
        },
        name='reset_password',
        ),
    url(r'^reset-password-done',
        auth_views.password_reset_complete,
        name='reset_password_done',
        ),
]
