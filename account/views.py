from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render

from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('account:signin')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {
        'form': form
    })
