from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_jalali.db import models as jmodels


# Create your models here.
class Province(models.Model):
    province_id = models.IntegerField(primary_key=True, serialize=True, verbose_name='ID')
    province_title = models.CharField(max_length=30, verbose_name=_('Province'))

    class Meta:
        ordering = ['province_id']
        verbose_name = _("province")
        verbose_name_plural = _("provinces")

    def __str__(self):
        return self.province_title


class Center(models.Model):
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING, null=True, blank=True, )
    center_title = models.CharField(max_length=150, verbose_name=_('Name of the training center'), null=True)
    center_title_id = models.CharField(max_length=64, verbose_name=_('Code of the training center'), null=True)
    standard_code = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        ordering = ['province_id']
        verbose_name = _("center")
        verbose_name_plural = _("centers")

    def __str__(self):
        return f'{self.province.province_title}({self.center_title})'


class Student(models.Model):
    FirstName = models.CharField(max_length=150, null=True, blank=True)
    LastName = models.CharField(max_length=150, null=True, blank=True)
    FatherName = models.CharField(max_length=150, null=True, blank=True)
    nationalcode = models.CharField(max_length=10, null=True, blank=True)
    IdentificationNumber = models.CharField(max_length=10, null=True, blank=True)
    MarriageStatusId = models.CharField(max_length=1, null=True, blank=True)
    MarriageStatusTitle = models.CharField(max_length=60, null=True, )
    Email = models.CharField(max_length=100, null=True, blank=True)
    Phone = models.CharField(max_length=11, null=True, blank=True)
    Mobile = models.CharField(max_length=11, null=True, blank=True)
    Address = models.CharField(max_length=300, null=True, blank=True)
    TermCode = models.CharField(max_length=30, null=True, blank=True)
    center_province_id = models.CharField(max_length=20, null=True, blank=True)
    center_province_title = models.CharField(max_length=50, null=True, blank=True)
    StandardCode = models.CharField(max_length=50, null=True, blank=True)
    center_title = models.CharField(max_length=250, null=True, blank=True)
    SubStudyLevelId = models.CharField(max_length=10, null=True, blank=True)
    SubStudyLevelTitle = models.CharField(max_length=20, null=True, blank=True)
    StudyLevelId = models.CharField(max_length=10, null=True, blank=True)
    StudyLevelTitle = models.CharField(max_length=40, null=True, blank=True)
    CourseStudyId = models.CharField(max_length=70, null=True, blank=True)
    CourseStudyTitle = models.CharField(max_length=70, null=True, blank=True)
    RegistryGroupId = models.CharField(max_length=10, null=True, blank=True)
    RegistryGroupTitle = models.CharField(max_length=50, null=True, blank=True)
    GenderId = models.CharField(max_length=10, null=True, blank=True)
    GenderTitle = models.CharField(max_length=30, null=True, blank=True)
    studentnumber = models.CharField(max_length=140, null=True, blank=True)
    center_id = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.studentnumber


class CulturalUser(AbstractUser):
    center = models.ManyToManyField(Center, blank=True, related_name="user_to_center")
    is_active = models.BooleanField(default=True)

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


if not hasattr(Group, 'center'):
    FOLDER_POSITION = [
        ('1', 'دانشجو'),
        ('2', 'مرکز آموزش'),
        ('3', 'استان'),
        ('4', 'دبیرخانه ستاد'),
    ]
    access_level = models.CharField(max_length=2, choices=FOLDER_POSITION, blank=True,
                                    verbose_name=_("Centers access level"), )

    access_level.contribute_to_class(Group, 'access_level')
    center = models.ManyToManyField(Center, blank=True, verbose_name=_("Center privilege"),
                                    related_name="group_to_center")
    center.contribute_to_class(Group, 'center')


class Group(Group):
    class Meta:
        proxy = True

    # def myFunction(self):
    #     return True
