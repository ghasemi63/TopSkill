from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django_sendfile import sendfile

from .models import TSStudent, Student, LevelingIndex, DocumentFile, Score, StudentJudgment
from .forms import DocumentForm, ScoreForm


# Create your views here.
@login_required
def indexView(request):
    contex = TSStudent.objects.all()
    return render(request, 'index.html', {'context': contex})


@login_required
def autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        national = Student.objects.filter(NationalCode__contains=term)
        return JsonResponse(list(national.values()), safe=False)
    else:
        print('the condition is false')
    return render(request, 'search_student.html')


@login_required
def submit_student(request):
    if request.method == 'POST':
        form = request.POST.get('nationalcodeid', False)
        if form:
            stu_na = Student.objects.get(id=form)
            ts_na = TSStudent.objects.filter(studentnumber__exact=stu_na.StudentNumber)
            if ts_na:
                na = 'اطلاعات دانشجوی مورد نظر قبلاْ وارد شده است.'
                return render(request, 'search_student.html', {'warning': na})
            else:
                ts = TSStudent.objects.create(
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
                    StudentJudgment.objects.get(user__position=2, user_id=request.user.id,
                                                student_id=ts.id)
                except:
                    StudentJudgment.objects.create(user_id=request.user.id,
                                                   student_id=ts.id, judgment_level=2, status=True)
                return render(request, 'index.html', {'context': TSStudent.objects.all()})
    else:
        na = 'اطلاعات وارد شده به روش امن ارسال نشده است.'
        return render(request, 'search_student.html', {'warning': na})


@login_required
def student_detail(request, pk):
    detail = get_object_or_404(TSStudent, id=pk)
    level = LevelingIndex.objects.all()
    return render(request, 'Student_detail.html', {'detail': detail, 'level': level})


@login_required
def document_score(request, user_id, doc_id):
    """
    evaluate post method from submit form
    """
    if request.method == 'POST':
        if request.POST.get('score'):
            form = ScoreForm(request.POST)
            if form.is_valid():
                bf = Score.objects.get(student_id=user_id, levelingindex_id=doc_id)
                cd = bf.student.studentjudgment_set.all()
                for x in cd:
                    if x.judgment_level == '2':
                        bf.ostan_judg = form.cleaned_data.get('ostan_judg')
                        bf.save()
                        score_ostan_judg = Score.objects.filter(student_id=user_id).aggregate(summs=Sum('ostan_judg'))
                        var = TSStudent.objects.get(id=user_id)
                        var.ostan_judgs = score_ostan_judg['summs']
                        var.save()
                    elif x.judgment_level == '11':
                        bf.setad_judge1 = form.cleaned_data.get('setad_judge1')
                        bf.save()
                        score_ostan_judg = Score.objects.filter(student_id=user_id).aggregate(summs=Sum('setad_judge1'))
                        var = TSStudent.objects.get(id=user_id)
                        var.setad_judges1 = score_ostan_judg['summs']
                        var.save()
                    elif x.judgment_level == '12':
                        bf.setad_judge2 = form.cleaned_data.get('setad_judge2')
                        bf.save()
                        score_ostan_judg = Score.objects.filter(student_id=user_id).aggregate(summs=Sum('setad_judge2'))
                        var = TSStudent.objects.get(id=user_id)
                        var.setad_judges2 = score_ostan_judg['summs']
                        var.save()
                    elif x.judgment_level == '13':
                        bf.setad_judge3 = form.cleaned_data.get('setad_judge3')
                        bf.save()
                        score_ostan_judg = Score.objects.filter(student_id=user_id).aggregate(summs=Sum('setad_judge3'))
                        var = TSStudent.objects.get(id=user_id)
                        var.setad_judges3 = score_ostan_judg['summs']
                        var.save()
                # next = request.POST.get('next', '/')
                messages.error(request, form.errors)
                return redirect('TopSkill:document_score', user_id=user_id, doc_id=doc_id)

            else:
                return messages.error(request, form.errors)
        elif request.POST.get('upload'):
            # next = request.GET.get('next')
            if request.FILES:
                sc = Score.objects.get(student_id=user_id, levelingindex_id=doc_id)
                form = DocumentForm(request.POST, request.FILES)
                if form.is_valid():
                    df = DocumentFile.objects.create(score=sc, creator_id=request.user.id)
                    df.upload_file = form.cleaned_data['upload_file']
                    df.duc_data = form.cleaned_data['duc_data']
                    df.upload_name = form.cleaned_data['upload_name']
                    df.save()
                    messages.success(request, 'مدارک مورد نظر بارگذاری شد.')
                    return redirect('TopSkill:document_score', user_id=user_id, doc_id=doc_id)
                else:
                    df = DocumentFile.objects.filter(score=sc)
                    messages.error(request, 'لطفاْ فایل مناسب را بارگذاری کنید.')
                    return redirect(request, 'document_score.html', {'df': df})
    else:
        ts, create = StudentJudgment.objects.get_or_create(student_id=user_id, user_id=request.user.id)
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
        return render(request, 'document_score.html',
                      {'form': form, 'upload_form': upload_form, 'contex': score_record, 'df': df})


def tsdelete(request, pk):
    td = get_object_or_404(TSStudent, id=pk)
    td.delete()
    return HttpResponseRedirect('/')


@login_required()
def document_delete(request, pk):
    df = get_object_or_404(DocumentFile, id=pk)
    df.delete()
    url = request.POST.get('next', '/')
    messages.success(request, url)
    messages.success(request, "فایل مورد نظر حذف شد.")
    return HttpResponseRedirect(url)


@login_required()
def download_file(request, file_id):
    obj = DocumentFile.objects.get(id=file_id)
    return sendfile(request, obj.upload_file.path)
