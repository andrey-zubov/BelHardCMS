from time import perf_counter

from django.shortcuts import redirect, render, get_object_or_404
from client.models import Client

from django.template.context_processors import csrf
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
    return render(request, 'recruit/recruiter_tasks_for_applicant.html', context={'applicant_user': applicant_user})
