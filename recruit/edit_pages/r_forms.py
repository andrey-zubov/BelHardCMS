from django import forms

from recruit.models import (Recruiter)


class RecruitUploadImgForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ('img',)

        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
