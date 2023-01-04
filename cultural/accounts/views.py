from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext
from django_sendfile import sendfile

from .forms import CulturalUserCreationForms, CulturalUserLoginForm, CaptchaForm
from .models import Profile
from .functions import privileges


# Create your views here.


class SignUpView(CreateView):
    form_class = CulturalUserCreationForms
    success_url = reverse_lazy("login")
    template_name = 'accounts/registration/signup.html'


def login_view(request):
    if request.POST:
        captcha = CaptchaForm(request.POST)
        if captcha.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if 'center_user' not in request.session:
                    request.session['center_user'] = privileges(request)
                    print(request.session['center_user'])
                # Redirect to a success page.
                return redirect('TopSkill:index')
            else:
                # Return an 'invalid login' error message.
                captcha = CaptchaForm()
                form = CulturalUserLoginForm()
                context = {'error': gettext('The username or password is incorrect'), 'form': form, 'captcha': captcha}
                return render(request, 'accounts/registration/login.html', context)
        else:
            captcha = CaptchaForm()
            form = CulturalUserLoginForm()
            context = {'error': gettext("The control code entered is not correct"), 'form': form, 'captcha': captcha}
            return render(request, 'accounts/registration/login.html', context)
    else:
        captcha = CaptchaForm()
        form = CulturalUserLoginForm()
        context = {'form': form, 'captcha': captcha}
        return render(request, 'accounts/registration/login.html', context)


def cultural_logout(request):
    # print(f'Logout {request.user}')
    logout(request)
    print(request.user)
    return HttpResponseRedirect('/')


class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'


@login_required()
def profile_image_display(request, file_id):
    obj = Profile.objects.get(user_id=file_id)
    return sendfile(request, obj.profile_image.path)
