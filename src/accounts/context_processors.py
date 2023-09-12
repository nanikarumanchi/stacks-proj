from .forms import LoginForm, RegisterForm


def login_context(request):
    login_form = LoginForm()
    registration_form = RegisterForm()
    context = {
        'login_form': login_form,
        'registration_form': registration_form
    }
    return context
