from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin

from .models import CulturalUser, Province, Center, Profile
from .forms import CulturalUserCreationForms, CulturalUserChangeForms


# Register your models here.
# @admin.register(CulturalUser)
# class CulturalUserAdmin(BaseUserAdmin):
#     add_form = CulturalUserCreationForms
#     form = CulturalUserChangeForms
#     model = CulturalUser


class CulturalUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = CulturalUserChangeForms
    # add_form = CulturalUserCreationForms
    #
    # # The fields to be used in displaying the User model.
    # # These override the definitions on the base UserAdmin
    # # that reference specific fields on auth.User.
    # list_display = ('username', 'birth_date', 'is_admin', 'profile_image', 'province')
    # list_filter = ('is_admin',)
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Personal info', {'fields': ('birth_date', 'profile_image', 'province', 'center')}),
    #     ('Position And Post', {'fields': ('position', 'post',)}),
    #     ('Permissions', {'fields': ('is_admin',)}),
    # )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'province', 'birth_date', 'password1', 'password2'),
    #     }),
    # )
    # search_fields = ('username',)
    # ordering = ('username',)
    # filter_horizontal = ()
    pass


# Now register the new UserAdmin...
admin.site.register(CulturalUser, CulturalUserAdmin)


# admin.site.register(CulturalUser, BaseUserAdmin)


# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
