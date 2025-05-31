from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from ..models import COMPONENTS


def get_components_total():
    total_components = 0
    for component in COMPONENTS:
        total_components += component.objects.count()
    # naive int flooring
    return int(total_components / 10) * 10


def home(request):
    components_total = get_components_total()
    context = {'components_total': components_total}
    return render(request, 'pickpcparts/home.html', context)


class BootstrapSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class BootstrapLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


def login(request):
    if request.method == 'POST':
        form = BootstrapLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                _login(request, user)
                return redirect('home')
    else:
        form = BootstrapLoginForm()

    login_failed = request.method == 'POST' and not form.is_valid()
    return render(request, 'pickpcparts/login.html', {
        'form': form,
        'login_failed': login_failed
    })


def logout(request):
    if request.method == 'POST':
        _logout(request)
    return redirect('home')


class SignUpView(CreateView):
    form_class = BootstrapSignUpForm
    template_name = 'pickpcparts/signup.html'

    def get_success_url(self):
        return '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
