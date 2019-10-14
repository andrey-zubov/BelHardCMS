from django import forms

from client.models import Message, Opinion, Answer


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
