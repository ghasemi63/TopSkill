from .models import Student, Score
from .fields import RestrictedFileField
from .views import DocumentFile
from django import forms
from django.utils.translation import gettext_lazy as _


class SearchStudentForm(forms.Form):
    class Meta:
        model = Student
        fields = "__all__"


class DocumentForm(forms.ModelForm):
    upload = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    upload_file = RestrictedFileField(content_types=['image/png', 'image/jpeg', 'application/pdf', 'application/zip'],
                                      max_upload_size=2000000)

    class Meta:
        model = DocumentFile
        fields = {'document_get_date', 'upload_file', 'upload_name'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['upload_file'].widget.attrs.update(
            {'accept': '.pdf, .jpg, .png '},
        ),


class ScoreForm(forms.ModelForm):
    score = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=True)
    province_score = forms.FloatField(min_value=0, required=False, label='استان', )
    judge1 = forms.FloatField(min_value=0, required=False, label='امتیاز', )
    judge2 = forms.FloatField(min_value=0, required=False, label='امتیاز', )
    judge3 = forms.FloatField(min_value=0, required=False, label='امتیاز', )
    description = forms.CharField(max_length=150, required=False, label=_('Description'),
                                  widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}))

    class Meta:
        model = Score
        fields = ['province_score', 'judge1', 'judge2', 'judge3', 'description']

    def __init__(self, *args, **kwargs):
        self.fields['province_score'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
        self.fields['judge1'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
        self.fields['judge2'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
        self.fields['judge3'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
        super().__init__(*args, **kwargs)
