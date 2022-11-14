from django.urls import path, re_path
from django.conf import settings
from . import views
from .forms import CulturalUserLoginForm

app_name = 'accounts'
urlpatterns = [
    path("login/", views.CulturalLoginView.as_view(), name="login"),
    # path("signup/", views.SignUpView.as_view(), name="signup"),
]
