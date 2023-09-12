from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

User = get_user_model()


def guest_view(request):
    guest_form = GuestForm(request.POST or None)
    context = {
        'guest_form': guest_form,
        'registration': False,
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if guest_form.is_valid():
        email = guest_form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    redirect('home_detail:home_detail_home')


def login_page_fbv(request):
    login_form = LoginForm(request.POST or None)
    context = {
        'login_form': login_form,
        'registration': False,
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if login_form.is_valid():
        context['login_form'] = login_form
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect('home_detail:home_detail_home')
        else:
            context['login_form'] = LoginForm()  # TODO to run login correctly
            return render(request, 'accounts/login_register.html', context)
    else:
        context['login_form'] = LoginForm()

    return render(request, 'base/navbar.html', context)
    # return render(request, 'accounts/login_register.html', context)


def logout_fbv(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')


def register_fbv(request):
    register_form = RegisterForm(request.POST or None)
    context = {
        'register_form': register_form,
        'registration': True,
    }
    if register_form.is_valid():
        context['register_form'] = register_form
        email = register_form.cleaned_data.get('email')
        username = register_form.cleaned_data.get('username')
        password = register_form.cleaned_data.get('password')
        new_user = User.objects.create_user(email=email, username=username, password=password)
        return redirect('home_detail:home_detail_home')
    return render(request, 'base/navbar.html', context)

# class LoginPlace(TemplateView):
#     template_name = 'accounts/login_register.html'
#     login_form = LoginForm
#
#     def get_context_data(self, **kwargs):
#         request = self.request
#         context = super(LoginPlace, self).get_context_data(**kwargs)
#         context['login_form'] = self.login_form()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         login_form = self.login_form(request.POST or None)
#         if login_form.is_valid():
#             print(login_form.cleaned_data)
#         return redirect('account:account_login')
