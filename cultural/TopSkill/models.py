import jdatetime
import os
from django.db import models
from django.shortcuts import reverse
import uuid
from django_jalali.db import models as jmodels
from accounts.models import CulturalUser


# Create your models here.
# def duc_time_validate(self, date):
#     if date < self.tsstudent.ts_termcode:
#         raise forms.ValidationError(
#             message='تاریخ گواهی باید بعد از تاریخ شروع تحصیل دانشجو باشد.',
#             code='date_error'
#         )


# class AllStudent(models.Model):
#     FirstName = models.CharField(max_length=150, null=True, blank=True)
#     LastName = models.CharField(max_length=150, null=True, blank=True)
#     FatherName = models.CharField(max_length=150, null=True, blank=True)
#     NationalCode = models.CharField(max_length=10, null=True, blank=True)
#     IdentificationNumber = models.CharField(max_length=10, null=True, blank=True)
#     MarriageStatusId = models.CharField(max_length=1, null=True, blank=True)
#     MarriageStatusTitle = models.CharField(max_length=60, null=True, )
#     Email = models.CharField(max_length=100, null=True, blank=True)
#     Phone = models.CharField(max_length=11, null=True, blank=True)
#     Mobile = models.CharField(max_length=11, null=True, blank=True)
#     Address = models.CharField(max_length=300, null=True, blank=True)
#     TermCode = models.CharField(max_length=30, null=True, blank=True)
#     CenterProvinceId = models.CharField(max_length=20, null=True, blank=True)
#     CenterProvinceTitle = models.CharField(max_length=50, null=True, blank=True)
#     SajadCenterId = models.CharField(max_length=50, null=True, blank=True)
#     CenterTitle = models.CharField(max_length=250, null=True, blank=True)
#     SubStudyLevelId = models.CharField(max_length=10, null=True, blank=True)
#     SubStudyLevelTitle = models.CharField(max_length=20, null=True, blank=True)
#     StudyLevelId = models.CharField(max_length=10, null=True, blank=True)
#     StudyLevelTitle = models.CharField(max_length=40, null=True, blank=True)
#     CourseStudyId = models.CharField(max_length=70, null=True, blank=True)
#     CourseStudyTitle = models.CharField(max_length=70, null=True, blank=True)
#     RegistryGroupId = models.CharField(max_length=10, null=True, blank=True)
#     RegistryGroupTitle = models.CharField(max_length=50, null=True, blank=True)
#     GenderId = models.CharField(max_length=10, null=True, blank=True)
#     GenderTitle = models.CharField(max_length=30, null=True, blank=True)
#     StudentNumber = models.CharField(max_length=140, null=True, blank=True)
#     CenterId = models.CharField(max_length=40, null=True, blank=True)
#
#     def __str__(self):
#         return self.StudentNumber

class LevelingIndex(models.Model):
    title = models.CharField(max_length=300, verbose_name='موضوع گواهی')
    description = models.CharField(max_length=3000, verbose_name='توضیحات', null=True)
    leveling_index_category_id = models.PositiveIntegerField(verbose_name='طبقه بندی موضوعات')
    min_score = models.CharField(verbose_name='حداقل امتیاز', max_length=4)
    max_score = models.CharField(verbose_name='حداکثر امتیاز', max_length=4, null=True)
    status = models.BooleanField(verbose_name='وضعیت گزینه', null=True, default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class Student(models.Model):
    EDUCATION_GROUP_TITLE = [
        ('1', 'مدیریت و خدمات اجتماعی'),
        ('2', 'صنعت'),
        ('3', 'کشاورزی'),
        ('4', 'فرهنگ و هنر'),
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(CulturalUser, on_delete=models.RESTRICT)
    ts_year = models.CharField(max_length=4, default='1401', verbose_name='دوره جشنواره')
    created_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت رکورد شمسی')
    firstname = models.CharField(max_length=150, verbose_name='نام')
    lastname = models.CharField(max_length=150, verbose_name='نام خانوادگی')
    fathername = models.CharField(max_length=15, verbose_name='نام پدر')
    sex = models.CharField(max_length=1, choices=[('1', 'زن'), ('2', 'مرد'), ], verbose_name='جنسیت')
    nationalcode = models.CharField(max_length=10, null=False, blank=False, verbose_name='شناسه ملی')
    studentnumber = models.CharField(max_length=15, blank=False, null=False, help_text='شماره دانشجویی 14 رقمی',
                                     verbose_name='شماره دانشچویی')
    education_group = models.CharField(max_length=1, choices=EDUCATION_GROUP_TITLE, default=None,
                                       verbose_name='گروه آموزشی')
    course_study_title = models.CharField(max_length=150, verbose_name='رشته تحصیلی')
    substudy_level_title = models.CharField(max_length=50, verbose_name='مقطع تحصیلی')
    center_id = models.CharField(max_length=64, verbose_name='کد مرکز')
    center_title = models.CharField(max_length=200, verbose_name='مرکز آموزش')
    center_province_id = models.CharField(max_length=2, verbose_name='کد استان')
    center_province_title = models.CharField(max_length=40, verbose_name='استان')
    status = models.BooleanField(verbose_name='وضعیت پرونده', choices=[(False, 'غیرفعال'), (True, 'فعال')],
                                 default=True)
    province_score = models.FloatField(verbose_name='امتیاز استان', blank=True, default=0, max_length=2)
    judge1 = models.FloatField(verbose_name='محموع امتیاز داوری اول', blank=True, default=0, max_length=2)
    judge2 = models.FloatField(verbose_name='مجموع امتیاز داوری دوم', blank=True, default=0, max_length=2)
    judge3 = models.FloatField(verbose_name='مجموع امتیاز داوری نهایی', blank=True, default=0, max_length=2)

    objects = models.Manager()
    leveling_manager = LevelingIndex.objects.all()

    def save(self, *args, **kwargs):
        self.province_score = round(self.province_score, 2)
        self.judge1 = round(self.judge1, 2)
        self.judge2 = round(self.judge2, 2)
        self.judge3 = round(self.judge3, 2)
        super(Student, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو')
    levelingindex = models.ForeignKey(LevelingIndex, on_delete=models.CASCADE, verbose_name='موضوع')
    province_score = models.FloatField(max_length=2, verbose_name='امتیاز استان', blank=True, default=0)
    judge1 = models.FloatField(max_length=2, verbose_name='امتیاز داور اول', blank=True, default=0)
    judge2 = models.FloatField(max_length=2, verbose_name='امتیاز داور دوم', blank=True, default=0)
    judge3 = models.FloatField(max_length=2, verbose_name='امتیاز داور سوم', blank=True, default=0)
    min_value = models.CharField(max_length=4, verbose_name='حداقل امتیاز', default=0)
    max_value = models.CharField(max_length=4, verbose_name='حدکثر امتیاز', default=0)

    def save(self, *args, **kwargs):
        self.province_score = round(self.province_score, 2)
        self.judge1 = round(self.judge1, 2)
        self.judge2 = round(self.judge2, 2)
        self.judge3 = round(self.judge3, 2)
        super(Score, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('TopSkill:document_score', kwargs=[str(self.id)])

    def __str__(self):
        return f'{self.student.firstname} {self.student.lastname}'


class DocumentFile(models.Model):
    creator = models.ForeignKey(CulturalUser, on_delete=models.RESTRICT, verbose_name='کابر ثبت کننده')
    created_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت رکورد شمسی')
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    document_get_date = jmodels.jDateField(verbose_name='تاریخ گواهی',
                                           default=jdatetime.date.today)

    def content_file_name(self, filename):
        ext = filename.split('.')[-1]
        filename = self.score.student.nationalcode
        filename = "%s/%s/%s.%s" % (self.score.student.nationalcode,
                                    self.score.student.studentnumber, filename, ext)
        return os.path.join('doc', filename)

    upload_file = models.FileField(verbose_name='گواهی', upload_to=content_file_name)
    upload_name = models.CharField(max_length=50, blank=False, verbose_name='عنوان گواهی')

    def __str__(self):
        return self.score.student.firstname

    def get_absolute_url(self):
        return reverse('TopSkill:document_delete', args=[str(self.id)])


class JudgmentStatus(models.Model):
    FOLDER_POSITION = [
        ('1', 'مرکز آموزش'),
        ('2', 'استان'),
        ('3', 'دبیرخانه ستاد'),
        ('11', 'داور اول'),
        ('12', 'داور دوم'),
        ('13', 'داور سوم'),
        ('14', 'داور چهارم'),
    ]
    user = models.ForeignKey(CulturalUser, on_delete=models.CASCADE, verbose_name='کاربر')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانشجو')
    judgment_level = models.CharField(max_length=2, choices=FOLDER_POSITION, verbose_name='محل پرونده')
    status = models.BooleanField(verbose_name='وضعیت کلی مرحله داوری', default=True)
    referral = models.BooleanField(verbose_name='اتمام داوری', default=False)

    def __str__(self):
        return f'{self.student.firstname} {self.student.lastname}'


class StudentFolder(models.Model):
    REFERRAL_STAGE_CHOICES = [
        ('4', 'دبیرخانه مرکزی'),
        ('5', 'در دست داوری'),
    ]
    JUDGMENT_GROUP = [
        ('1', 'آموزشی'),
        ('2', 'پژوهشی'),
        ('3', 'مهارتی'),
        ('4', 'فرهنگی'),
        ('5', 'امتیاز افزوده'),
    ]
    judgmentstatus = models.ForeignKey(JudgmentStatus, on_delete=models.CASCADE, verbose_name='وضعیت پرونده')
    referee_status = models.CharField(max_length=2, choices=REFERRAL_STAGE_CHOICES, verbose_name='وضعیت داوری')
    referee_level = models.CharField(max_length=1, verbose_name='مرحله داوری')
    judgment_score_sum = models.CharField(max_length=2, choices=JUDGMENT_GROUP, blank=False)
    judge_score_sum = models.FloatField(max_length=2, verbose_name='جمع امتیاز گروه', blank=True, default=0)

    def __str__(self):
        return self.judgmentstatus
