from django.contrib import admin
from .models import TSStudent, Student, Score, StudentJudgment, DocumentFile


# Register your models here.
@admin.register(TSStudent)
class TSStudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentJudgment)
class StudentJudgmentAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentFile)
class DocumentAdmin(admin.ModelAdmin):
    pass
