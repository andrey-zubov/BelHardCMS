from django import forms
from django.forms import formset_factory  # modelformset_factory


from .models import Client, Skills, Experience, Message, Opinion, Answer


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


AddSkillFormSet = formset_factory(AddSkillForm)


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

        widgets={'title' : forms.TextInput(attrs={'class':'form-control'}),
                 'text' : forms.TextInput(attrs={'class':'form-control'}),
            }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text',]
