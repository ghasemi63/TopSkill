import self as self
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


class CulturalUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given user, and password.
        """
        if not username:
            raise ValueError('لطفاْ نام کاربری را وارد کنید!')

        user = self.model(username=username, )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CulturalUser(AbstractUser, PermissionsMixin):
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
    # PROVINCE_CHOICES = list(Province.objects.values_list('province_id', 'province_title'))
    # CENTER_CHOICES = list(Center.objects.values_list('id', 'center_title'))
    email = models.EmailField(verbose_name='email address', max_length=255, )
    nationalcode = models.CharField(max_length=10, verbose_name='کد ملی')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, null=True, blank=True)
    birth_date = jmodels.jDateField(verbose_name='تاریخ تولد', null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.RESTRICT, verbose_name='شناسه استان', default=1)
    center = models.ForeignKey(Center, on_delete=models.RESTRICT, verbose_name='مرکز آموزشی', default=1)
    position = models.CharField(max_length=2, verbose_name='سطح دسترسی', choices=POSITION_CHOICES, default=1)
    post = models.CharField(max_length=2, verbose_name='رده دسترسی', choices=POST_CHOICES, default=1)
    profile_image = models.ImageField(upload_to=f'profile/', null=True, blank=True)

    objects = CulturalUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
