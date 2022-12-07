from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from .models import CulturalUser, Province, Center, Profile
from .forms import CulturalUserCreationForms, CulturalUserChangeForms


# Register your models here.
# @admin.register(CulturalUser)
# class CulturalUserAdmin(BaseUserAdmin):
#     add_form = CulturalUserCreationForms
#     form = CulturalUserChangeForms
#     model = CulturalUser

@admin.register(CulturalUser)
class CulturalUserAdmin(BaseUserAdmin):
    list_display = ('username','email')
    # fieldsets = (
    #     (None, {'fields': ('username', 'password', 'password')}),
        # ('Personal info', {'fields': ('profile__birth_date',)}),
        # ('Position And Post', {'fields': ('position', 'post',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
    # )
    pass


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
