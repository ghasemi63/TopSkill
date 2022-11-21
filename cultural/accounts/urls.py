from django.urls import path, re_path, include
from django.conf import settings
from . import views
from .forms import CulturalUserLoginForm

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.cultural_logout, name='logout'),
]
