from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )
    confirm = forms.CharField(
        label=_('Confirm'),
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm',)

    def clean_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm']:
            raise forms.ValidationError(
                _('Password and confirm password does not match.'))
        return cd['confirm']
