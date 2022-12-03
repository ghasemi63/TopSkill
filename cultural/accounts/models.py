from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group
from django.db import models
from django_jalali.db import models as jmodels


# Create your models here.
class Province(models.Model):
    province_id = models.IntegerField(primary_key=True, serialize=True, verbose_name='ID')
    province_title = models.CharField(max_length=30, verbose_name='استان')

    class Meta:
        ordering = ['province_id']

    def __str__(self):
        return self.province_title


class Center(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    center_title = models.CharField(max_length=150, verbose_name='نام مرکز آموزش', null=True)
    center_title_id = models.CharField(max_length=64, verbose_name='کد مرکز آموزش', null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='استان')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.center_title


class CulturalUser(AbstractUser):
    # PROVINCE_CHOICES = list(Province.objects.values_list('province_id', 'province_title'))
    # CENTER_CHOICES = list(Center.objects.values_list('id', 'center_title'))
    email = models.EmailField(verbose_name='email address', max_length=255, )
    nationalcode = models.CharField(max_length=10, verbose_name='کد ملی')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Profile(models.Model):
    POSITION_CHOICES = [
        ('1', 'مرکز آموزش'),
        ('2', 'استان'),
        ('3', 'ستاد'),
    ]
    POST_CHOICES = [
        ('1', 'دانشجو'),
        ('2', 'کارشناس مرکز'),
        ('3', 'کارشناس استان'),
        ('4', 'کارشناس ستاد'),
        ('5', 'داور'),
        ('20', 'مدیر'),
    ]
    user = models.OneToOneField(CulturalUser, on_delete=models.CASCADE)
    birth_date = jmodels.jDateField(verbose_name='تاریخ تولد', null=True, blank=True)
    province = models.ManyToManyField(Province, blank=True)
    center = models.ManyToManyField(Center, blank=True)
    position = models.CharField(max_length=2, verbose_name='سطح دسترسی', choices=POSITION_CHOICES, default=1)
    post = models.CharField(max_length=2, verbose_name='رده دسترسی', choices=POST_CHOICES, default=1)
    profile_image = models.ImageField(upload_to=f'profile/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.username
