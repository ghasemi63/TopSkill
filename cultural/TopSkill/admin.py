from django.contrib import admin
from .models import AllStudent, Student, Score, JudgmentStatus, DocumentFile


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
