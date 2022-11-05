from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError

from accounts.models import CulturalUser


# class CulturalUserCreationForms(UserCreationForm):
#
#     class Meta:
#         model = CulturalUser
#         fields = ['username', 'email']
#
#
# class CulturalUserChangeForms(UserChangeForm):
#
#     class Meta:
#         model = CulturalUser
#         fields = ['username', 'email']

class CulturalUserCreationForms(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = CulturalUser
        # fields = ('username', 'province', 'profile_image')
        fields = '__all__'
        labels = {
            'password1': 'گذرواژه',
            'password2': 'تکرار گذرواژه',
            'password': 'گذرواژه',
            'username': 'نام کاربری',
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه ها یکسان نیستند.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CulturalUserChangeForms(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CulturalUser
        # fields = ('username', 'password', 'province', 'is_active', 'is_admin')
        fields = '__all__'
        labels = {
            'password': 'گذرواژه',
            'username': 'نام کاربری',
        }


class CulturalAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


