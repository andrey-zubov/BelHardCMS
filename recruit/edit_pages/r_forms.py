from django import forms

from recruit.models import (Recruit)


class RecruitUploadImgForm(forms.ModelForm):
    class Meta:
        model = Recruit
        fields = ('img',)

        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
