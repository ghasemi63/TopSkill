from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext_noop
from django_jalali.db import models as jmodels


# Create your models here.
class Province(models.Model):
    province_id = models.IntegerField(primary_key=True, serialize=True, verbose_name='ID')
    province_title = models.CharField(max_length=30, verbose_name=_('Province'))

    class Meta:
        ordering = ['province_id']

    def __str__(self):
        return self.province_title


class Center(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    center_title = models.CharField(max_length=150, verbose_name=_('Name of the training center'), null=True)
    center_title_id = models.CharField(max_length=64, verbose_name=_('Code of the training center'), null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_('Province'))

    class Meta:
        verbose_name = _("center")
        verbose_name_plural = _("centers")

    def __str__(self):
        return self.center_title

    def natural_key(self):
        return (self.center_title,)


class CulturalUser(AbstractUser):
    pass


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


class UserPositions(models.Model):
    class Position(models.TextChoices):
        UNIVERSITY_STUDENT = '1', _('University student')
        TRAINING_CENTER = '2', _('Training center')
        PROVINCE = '3', _('Province')
        CENTRAL_OFFICE = '4', _('Central office')

    user = models.ForeignKey(CulturalUser, on_delete=models.CASCADE, verbose_name=_('User'))
    position = models.CharField(max_length=2, verbose_name=_('Access level'), choices=Position.choices,
                                default=Position.UNIVERSITY_STUDENT)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    center = models.ForeignKey(Center, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.position
