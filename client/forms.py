from django import forms
from django.forms import formset_factory, inlineformset_factory

from .models import Client, Skills, Experience, Education, Certificate

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


class AddSkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ('skills',)

        widgets = {
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
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


class EducationForm(forms.ModelForm):
    """ Test Code - Module Form Set """

    class Meta:
        model = Education
        fields = ('education', 'subject_area', 'specialization',
                  'qualification', 'date_start', 'date_end')

        widgets = {
            'education': forms.TextInput(attrs={'class': 'form-control'}),
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


class CertificateForm(forms.ModelForm):
    """ Test Code - Module Form Set """

    class Meta:
        model = Certificate
        fields = ('img', 'link',)

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
inlineEduCert = inlineformset_factory(Certificate, Education, fields=('education', 'subject_area', 'specialization',
                                                                      'qualification', 'date_start', 'date_end',
                                                                      'certificate'))
