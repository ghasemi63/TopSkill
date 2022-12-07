from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _
from .models import CulturalUser, Province, Center, Profile, UserPositions, AnonymousCu, AnonymousUser
from .forms import CulturalUserCreationForms, CulturalUserChangeForms


# Register your models here.
@admin.register(UserPositions)
class UserPositionsAdmin(admin.ModelAdmin):
    # search_fields = ("position",)
    # ordering = ("position",)
    # filter_horizontal = ("position",)
    #
    # def formfield_for_manytomany(self, db_field, request=None, **kwargs):
    #     if db_field.name == "province":
    #         qs = kwargs.get("queryset", db_field.remote_field.model.objects)
    #         # Avoid a major performance hit resolving permission names which
    #         # triggers a content_type load:
    #         kwargs["queryset"] = qs.select_related("content_type")
    #     return super().formfield_for_manytomany(db_field, request=request, **kwargs)
    pass


@admin.register(CulturalUser)
class CulturalUserAdmin(BaseUserAdmin, AnonymousCu):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
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
                "fields": ("username", "password1", "password2"),
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
    )


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

# @admin.register(UserPositions)
# class UserPositionsAdmin(admin.ModelAdmin):
#     list_display = ('user', 'position')
