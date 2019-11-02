from django import forms

from client.models import (Client)


class UploadImgForm(forms.ModelForm):  # TeamRome
    class Meta:
        model = Client
        fields = ('img',)

        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
