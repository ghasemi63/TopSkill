import os
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from django_sendfile import sendfile
from django.views.generic import TemplateView
from django.conf import settings
from django.utils.translation import gettext as _
import shutil
from .models import Student, AllStudent, LevelingIndex, DocumentFile, Score, JudgmentStatus
from .forms import DocumentForm, ScoreForm
from .functions import toastrMessagePure, toastrMessageForm


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'topskill/index.html'


@login_required
@permission_required(perm='TopSkill.view_student', login_url='/')
def studentsView(request):
    contex = Student.objects.all()
    return render(request, 'topskill/students.html', {'context': contex})


@login_required
@permission_required(perm='TopSkill.view_allstudent')
def autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        national = AllStudent.objects.filter(NationalCode__contains=term)
        return JsonResponse(list(national.values()), safe=False)
    else:
        pass
    return render(request, 'topskill/search_student.html')


"""
ثبت اطلاعات دانشجویان در دیتابیس شخصی
"""


@login_required
@permission_required(perm='TopSkill.add_student')
def submit_student(request):
    if request.method == 'POST':
        form = request.POST.get('nationalcodeid')
        if form:
            stu_na = AllStudent.objects.get(id=form)
            s_na = Student.objects.filter(studentnumber__exact=stu_na.StudentNumber)
            if s_na:
                messages.warning(request, toastrMessagePure(_("The desired student's information has already been "
                                                            "entered.")))
                return render(request, 'topskill/search_student.html')
            else:
                s = Student.objects.create(
                    firstname=stu_na.FirstName,
                    lastname=stu_na.LastName,
                    fathername=stu_na.FatherName,
                    sex=stu_na.GenderId,
                    nationalcode=stu_na.NationalCode,
                    studentnumber=stu_na.StudentNumber,
                    course_study_title=stu_na.CourseStudyTitle,
                    center_province_id=stu_na.CenterProvinceId,
                    center_province_title=stu_na.CenterProvinceTitle,
                    center_title=stu_na.CenterTitle,
                    substudy_level_title=stu_na.SubStudyLevelTitle,
                    centerId=stu_na.CenterId,
                    education_group=stu_na.StudyLevelId,
                    user_id=request.user.id
                )
                try:
                    JudgmentStatus.objects.get(user__position=2, user_id=request.user.id,
                                               student_id=s.id)
                except:
                    JudgmentStatus.objects.create(user_id=request.user.id,
                                                  student_id=s.id, judgment_level=2, status=True)
                return render(request, 'topskill/students.html', {'context': Student.objects.all()})
        else:
            messages.error(request, toastrMessagePure(_("Please select a student.")))
            return render(request, 'topskill/search_student.html')
    else:
        messages.error(request, toastrMessagePure(
            _("The method of sending information is not safe and it is not possible to record data.")))
        return render(request, 'topskill/search_student.html')


@login_required
@permission_required(perm='TopSkill.view_student')
def student_detail(request, pk):
    detail = get_object_or_404(Student, id=pk)
    level = LevelingIndex.objects.all()
    return render(request, 'topskill/Student_detail.html', {'detail': detail, 'level': level})


"""
ثبت امتیاز گواهی دانشجو و بارگذاری تصویر مدارک دانشجو 
"""


@login_required
@permission_required(perm='TopSkill.view_documentfile')
def document_score(request, user_id, doc_id):
    """
ارزیابی صحت ارسال اطلاعات توسط متدهای POST OR GET
    """
    if request.method == 'POST':
        if request.POST.get('score'):
            form = ScoreForm(request.POST)
            if form.is_valid():
                bf = Score.objects.get(student_id=user_id, levelingindex_id=doc_id)
                cd = bf.student.judgmentstatus_set.all()
                for x in cd:
                    if x.judgment_level == '2':
                        bf.province_score = form.cleaned_data.get('province_score')
                        bf.save()
                        score_province_score = Score.objects.filter(student_id=user_id).aggregate(
                            sum=Sum('province_score'))
                        var = Student.objects.get(id=user_id)
                        var.province_score = score_province_score['sum']
                        var.save()
                    elif x.judgment_level == '11':
                        bf.judge1 = form.cleaned_data.get('judge1')
                        bf.save()
                        score_judge = Score.objects.filter(student_id=user_id).aggregate(sum=Sum('judge1'))
                        var = Student.objects.get(id=user_id)
                        var.judge1 = score_judge['sum']
                        var.save()
                    elif x.judgment_level == '12':
                        bf.judge2 = form.cleaned_data.get('judge2')
                        bf.save()
                        score_judge = Score.objects.filter(student_id=user_id).aggregate(sum=Sum('judge2'))
                        var = Student.objects.get(id=user_id)
                        var.judge2 = score_judge['sum']
                        var.save()
                    elif x.judgment_level == '13':
                        bf.judge3 = form.cleaned_data.get('judge3')
                        bf.save()
                        score_judge = Score.objects.filter(student_id=user_id).aggregate(sum=Sum('judge3'))
                        var = Student.objects.get(id=user_id)
                        var.judge3 = score_judge['sum']
                        var.save()
                messages.success(request, toastrMessagePure(_("Your score has been registered correctly.")))
                return redirect('TopSkill:document_score', user_id=user_id, doc_id=doc_id)
            else:
                message = [v for v in form.errors.values()]
                return messages.error(request, _(message))
        elif request.POST.get('upload'):
            if request.FILES:
                sc = Score.objects.get(student_id=user_id, levelingindex_id=doc_id)
                form = DocumentForm(request.POST, request.FILES)
                if form.is_valid():
                    df = DocumentFile.objects.create(score=sc, creator_id=request.user.id)
                    df.upload_file = form.cleaned_data['upload_file']
                    df.document_get_date = form.cleaned_data['document_get_date']
                    df.upload_name = form.cleaned_data['upload_name']
                    df.save()
                    messages.success(request, toastrMessagePure(_("The requested documents have been uploaded.")))
                    return redirect('TopSkill:document_score', user_id=user_id, doc_id=doc_id)
                else:
                    messages.warning(request, toastrMessageForm(form))
                    return redirect('TopSkill:document_score', user_id=user_id, doc_id=doc_id)
        else:
            messages.success(request, toastrMessagePure(_("The information you sent is incorrect.")))
            return redirect('TopSkill:document_score', user_id=user_id, doc_id=doc_id)
    else:
        ts, create = JudgmentStatus.objects.get_or_create(student_id=user_id, user_id=request.user.id)
        li = LevelingIndex.objects.get(id=doc_id)
        score_record, create = Score.objects.get_or_create(
            student_id=ts.student_id,
            levelingindex_id=doc_id,
            min_value=li.min_score,
            max_value=li.max_score,
        )
        form = ScoreForm(instance=score_record)
        sc = Score.objects.get(student_id=user_id, levelingindex_id=doc_id)
        df = DocumentFile.objects.filter(score=sc)
        upload_form = DocumentForm()
        return render(request, 'topskill/document_score.html',
                      {'form': form, 'upload_form': upload_form, 'contex': score_record, 'df': df})


@login_required()
@permission_required(perm='TopSkill.view_documentfile')
def download_file(request, file_id):
    obj = DocumentFile.objects.get(id=file_id)
    return sendfile(request, obj.upload_file.path)


"""
توضیحات گزینه های مدارک
"""


@login_required()
@permission_required(perm='TopSkill.view_levelingindex')
def description(request, id):
    try:
        desc = LevelingIndex.objects.get(id=id)
    except:
        return HttpResponseRedirect('/')
    else:
        return render(request, 'topskill/description.html', {'context': desc})


"""
Referral Arbitration 
پنل ارجاع داوری
"""


@login_required()
@permission_required(perm='TopSkill.add_studentfolder')
def referral_arbitration(request, stu_id):
    student = get_object_or_404(Student, stu_id)


"""
all delete objects
"""


@login_required()
@permission_required(perm='TopSkill.delete_documentfile')
def document_delete(request, pk):
    df = get_object_or_404(DocumentFile, id=pk)
    if request.POST:
        df.delete()
        if os.path.exists(df.upload_file.path):
            os.remove(df.upload_file.path)
            messages.warning(request, toastrMessagePure(_("The desired file was deleted.")))
        else:
            raise FileNotFoundError(_("The desired file has already been deleted."))
        return redirect(
            reverse('TopSkill:document_score',
                    kwargs={'user_id': df.score.student_id, 'doc_id': df.score.levelingindex_id}))
    else:
        return render(request, 'topskill/document_delete.html',
                      {'pk': pk, 'user_id': df.score.student_id, 'doc_id': df.score.levelingindex_id})


@login_required()
@permission_required(perm='TopSkill.delete_student')
def student_delete(request, pk):
    td = get_object_or_404(Student, id=pk)
    td.delete()
    try:
        shutil.rmtree(settings.MEDIA_ROOT + "/doc/" + td.nationalcode + "/")
    except:
        pass
    finally:
        messages.warning(request, toastrMessagePure(_("The desired folder was completely deleted.")))
    return redirect(reverse('TopSkill:students'))
