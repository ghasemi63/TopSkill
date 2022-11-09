from .models import TSStudent, Score

from .views import DocumentFile
from django import forms


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
    score = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=True)
    province_score = forms.FloatField(min_value=0, required=False, label='استان', )
    judge1 = forms.FloatField(min_value=0, required=False, label='امتیاز', )
    judge2 = forms.FloatField(min_value=0, required=False, label='امتیاز', )
    judge3 = forms.FloatField(min_value=0, required=False, label='امتیاز', )

    class Meta:
        model = Score
        fields = ['province_score', 'judge1', 'judge2', 'judge3']
        # fields = ['ostan_judg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
