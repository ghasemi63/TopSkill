from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
# from django.db import transaction
from django.contrib import messages

from .forms import CulturalUserCreationForms, CulturalUserLoginForm, CaptchaForm
from .models import Profile


# from .forms import CulturalAuthenticationForm
# Create your views here.


class SignUpView(CreateView):
    form_class = CulturalUserCreationForms
    success_url = reverse_lazy("login")
    template_name = 'accounts/registration/signup.html'


# class CulturalLoginView(LoginView):
#     authentication_form = CulturalUserLoginForm
#     success_url = reverse_lazy('/')
#     template_name = 'registration/login.html'

def login_view(request):
    if request.POST:
        captcha = CaptchaForm(request.POST)
        if captcha.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('TopSkill:index')
            else:
                # Return an 'invalid login' error message.
                captcha = CaptchaForm()
                form = CulturalUserLoginForm()
                context = {'error': 'نام کاربری یا گذرواژه صحیح نیست', 'form': form, 'captcha': captcha}
                return render(request, 'accounts/registration/login.html', context)
        else:
            captcha = CaptchaForm()
            form = CulturalUserLoginForm()
            context = {'error': 'کد کنترلی وارد شده صحیح نیست', 'form': form, 'captcha': captcha}
            return render(request, 'accounts/registration/login.html', context)
    else:
        captcha = CaptchaForm()
        form = CulturalUserLoginForm()
        context = {'form': form, 'captcha': captcha}
        return render(request, 'accounts/registration/login.html', context)


def cultural_logout(request):
    print(f'Loggin out {request.user}')
    logout(request)
    print(request.user)
    return HttpResponseRedirect('/')

class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
