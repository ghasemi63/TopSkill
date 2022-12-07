from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AllStudent, Student, Score, JudgmentStatus, DocumentFile, CulturalUser


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(AllStudent)
class AllStudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(JudgmentStatus)
class JudgmentStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentFile)
class DocumentAdmin(admin.ModelAdmin):
    pass
