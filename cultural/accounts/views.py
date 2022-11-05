from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.contrib import messages

from .forms import CulturalUserCreationForms, CulturalAuthenticationForm
# Create your views here.


class SignUpView(CreateView):
    form_class = CulturalUserCreationForms
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'


class CulturalLoginView(LoginView):
    authentication_form = CulturalAuthenticationForm
    success_url = reverse_lazy('/')
    template_name = 'registration/login.html'
