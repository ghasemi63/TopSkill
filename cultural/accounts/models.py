from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_jalali.db import models as jmodels


# Create your models here.
class Positions(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Name of the positions'), null=False)

    class Meta:
        verbose_name = _("position")
        verbose_name_plural = _("user_positions")

    def __str__(self):
        return str(self.name)


class Province(models.Model):
    province_id = models.IntegerField(primary_key=True, serialize=True, verbose_name='ID')
    province_title = models.CharField(max_length=30, verbose_name=_('Province'))
    position_province = models.ForeignKey(Positions, on_delete=models.CASCADE, verbose_name=_("position province"),
                                          related_name='position_province')

    class Meta:
        ordering = ['province_id']
        verbose_name = _("province")
        verbose_name_plural = _("provinces")

    def __str__(self):
        return self.province_title


class Center(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    center_title = models.CharField(max_length=150, verbose_name=_('Name of the training center'), null=True)
    center_title_id = models.CharField(max_length=64, verbose_name=_('Code of the training center'), null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_('Province'),
                                 related_name="province_relations")

    class Meta:
        verbose_name = _("center")
        verbose_name_plural = _("centers")

    def __str__(self):
        return self.center_title


class CulturalUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    POST_CHOICES = [
        ('1', 'دانشجو'),
        ('2', 'کارشناس مرکز'),
        ('3', 'کارشناس استان'),
        ('4', 'کارشناس ستاد'),
        ('5', 'داور'),
        ('20', 'مدیر'),
    ]
    user = models.OneToOneField(CulturalUser, on_delete=models.CASCADE)
    nationalcode = models.CharField(max_length=10, verbose_name='کد ملی')
    birth_date = jmodels.jDateField(verbose_name='تاریخ تولد', null=True, blank=True)
    post = models.CharField(max_length=2, verbose_name='رده دسترسی', choices=POST_CHOICES, default=1)
    profile_image = models.ImageField(upload_to=f'profile/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")


if not hasattr(Group, 'position'):
    position_group = models.ForeignKey(Positions, on_delete=models.CASCADE, verbose_name=_("position relations"),
                                       related_name='position_relations', null=True, blank=True)
    position_group.contribute_to_class(Group, 'position')


class Group(Group):
    class Meta:
        proxy = True

    def myFunction(self):
        return True
