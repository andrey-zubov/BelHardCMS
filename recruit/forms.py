from django import forms
from client.models import FilesForJobInterviews


class FileFieldForm(forms.ModelForm):
    class Meta:
        model = FilesForJobInterviews
        fields = ['add_file']

    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
