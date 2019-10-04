from string import Template

from django import forms
from django.forms import formset_factory
from django.utils.safestring import mark_safe

from .models import Client, Skills, Experience, Message, Opinion, Answer, Education, Certificate

# special field names for the Formsets
# https://docs.djangoproject.com/en/2.2/topics/forms/formsets/
TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'
ORDERING_FIELD_NAME = 'ORDER'
DELETION_FIELD_NAME = 'DELETE'
# default minimum number of forms in a formset
DEFAULT_MIN_NUM = 0
# default maximum number of forms in a formset, to prevent memory exhaustion
DEFAULT_MAX_NUM = 1000


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('img',)

        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class UploadCertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('img',)

        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class AddSkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ('skill',)

        widgets = {
            'skill': forms.TextInput(attrs={'class': 'form-control'}),
        }

        data = {
            # each form field data with a proper index form
            'myformset-0-raw': 'my raw field string',

            # form status, number of forms
            'myformset-INITIAL_FORMS': 1,
            'myformset-TOTAL_FORMS': 2,
        }


class AddExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ('name',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}


class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['title', 'text']

        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'text': forms.TextInput(attrs={'class': 'form-control'}),
                   }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', ]


class EducationForm(forms.ModelForm):
    """ Test Code - Module Form Set """

    class Meta:
        model = Education
        fields = ('institution', 'subject_area', 'specialization',
                  'qualification', 'date_start', 'date_end',)

        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_area': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        data = {
            # each form field data with a proper index form
            'edu_form-0-raw': 'edu_form',
            # form status, number of forms
            'edu_form-INITIAL_FORMS': 1,
            'edu_form-TOTAL_FORMS': 2,
        }


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html = Template("""<img src="$link" alt="img" class="m-sm-1" height="100">""")
        return mark_safe(html.substitute(link=value))


class CertificateForm(forms.ModelForm):
    """ Test Code - Module Form Set """
    show_img = forms.ImageField(widget=PictureWidget)

    class Meta:
        model = Certificate
        fields = ('show_img', 'img', 'link',)

        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }

        data = {
            # each form field data with a proper index form
            'cert_form-0-raw': 'cert_form',
            # form status, number of forms
            'cert_form-INITIAL_FORMS': 1,
            'cert_form-TOTAL_FORMS': 2,
        }


AddSkillFormSet = formset_factory(AddSkillForm)
EducationFormSet = formset_factory(EducationForm)
CertificateFormSet = formset_factory(CertificateForm)
# inlineEduCert = inlineformset_factory(Education, Certificate,
#                                       fields=('education', 'img', 'link',))
