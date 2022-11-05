from .models import TSStudent, DocumentFile, Score, LevelingIndex, StudentJudgment
from django_jalali.forms import jDateInput
from django.core.exceptions import ValidationError
from .views import DocumentFile
from django import forms
from .fields import MultiFileField


class SearchStudentForm(forms.Form):
    class Meta:
        model = TSStudent
        fields = "__all__"


class DocumentForm(forms.ModelForm):
    upload = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = DocumentFile
        fields = {'duc_data', 'upload_file', 'upload_name'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['upload_file'].widget.attrs.update(
            {'accept': '.pdf, .jpg, .zip'},
        ),


class ScoreForm(forms.ModelForm):
    score = forms.BooleanField(widget=forms.HiddenInput,required=False,  initial=True)
    ostan_judg = forms.FloatField(min_value=0, required=False, label='استان', )
    setad_judge1 = forms.FloatField(min_value=0, required=False, label='امتیاز', )
    setad_judge2 = forms.FloatField(min_value=0, required=False, label='امتیاز', )
    setad_judge3 = forms.FloatField(min_value=0, required=False, label='امتیاز', )

    # judgment = forms.FloatField(min_value=0, required=False, label='امتیاز', )

    class Meta:
        model = Score
        fields = ['ostan_judg', 'setad_judge1', 'setad_judge2', 'setad_judge3']
        # fields = ['ostan_judg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ostan_judg'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
        self.fields['setad_judge1'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
        self.fields['setad_judge2'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
        self.fields['setad_judge3'].widget.attrs.update(
            {'max': self.instance.max_value},
        ),
