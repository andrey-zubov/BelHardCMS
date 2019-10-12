from time import perf_counter

from django.shortcuts import redirect, render, get_object_or_404
from client.models import Client

from django.template.context_processors import csrf
from .forms import FileFieldForm
from django.views.generic.edit import FormView

from django.urls import reverse
from django.http import HttpResponse
from .models import *


def recruiter_main_page(request):
    return render(request=request, template_name='recruit/main_template_recruiter.html', )


def base_of_applicants(request):
    applicants = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants})


def applicant(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    return render(request, 'recruit/recruiter_applicant.html', context={'applicant_user': applicant_user})


def applicant_tasks(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    response = csrf(request)
    response['applicant_user'] = applicant_user
    if request.method == 'POST':
        response['form'] = FileFieldForm()

    else:
        response['form'] = FileFieldForm()

    return render(request, 'recruit/recruiter_tasks_for_applicant.html', context=response)

"""
class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'recruit/recruiter_tasks_for_applicant.html'  # Replace with your template.
    success_url = 'applicant_tasks_url'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def uploading_files(request):
    pass"""
