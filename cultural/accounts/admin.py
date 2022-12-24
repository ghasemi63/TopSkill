from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission, ContentType
from django.utils.translation import gettext_lazy as _
from .models import CulturalUser, Province, Profile, Student, Center


# Register your models here.
# @admin.register(Privilege)
# class PrivilegeAdmin(admin.ModelAdmin):
#     search_fields = ("province", "center")
#     filter_horizontal = ("province", "center")


@admin.register(CulturalUser)
class CulturalUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "center",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "groups",
                    "user_permissions",
                    "center",
                ),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
        "center",
    )


# @admin.register(Province)
# class ProvinceAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Center)
# class CenterAdmin(admin.ModelAdmin):
#     pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Permission)
class UserPermissionsAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions", "center")


@admin.register(ContentType)
class UserContentAdmin(admin.ModelAdmin):
    pass

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     pass
