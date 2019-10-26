from time import perf_counter
from collections import defaultdict
from client.models import Client, CV, JobInterviews, FilesForJobInterviews, Vacancy
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import FormView
from django.template.context_processors import csrf

from django.urls import reverse
from django.http import HttpResponse
from .models import *

# There is Poland's views #################################################################################


def recruiter_main_page(request):
    return render(request, template_name='recruit/recruit_main_template.html', )


def recruiter_base(request):
    return render(request, template_name='recruit/recruiter_base.html', )


def base_of_applicants(request):
    applicants = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants})

class ApplicantDet(View):
    def get(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        resumes = applicant_user.cv_set.all()
        return render(request, 'recruit/recruiter_applicant.html',
                      context={'applicant_user': applicant_user, 'resumes': resumes})

    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        resume = CV.objects.get(id=response['id_cv'])
        vacancy_id = request.POST.getlist('id_v')
        # vacancy = Vacancy.objects.get(id=response['id_v'])

        return redirect(applicant_user.get_absolute_url())


class CreateJobInterview(View):
    def get(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        if CV.objects.filter(client_cv=applicant_user):
            accepted_vacancies = applicant_user.cv_set.all()[0].vacancies_accept.all()
            for resume in applicant_user.cv_set.all()[1:]:
                accepted_vacancies |= resume.vacancies_accept.all()
            # print(accepted_vacancies)
        else:
            accepted_vacancies = None
        return render(request, 'recruit/recruiter_tasks_for_applicant.html',
                      context={'applicant_user': applicant_user, 'accepted_vacancies': accepted_vacancies})

    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        files = request.FILES.getlist('files')
        j = JobInterviews(
            client=applicant_user,
            name=response.get('name'),
            jobinterviewtime=response.get('time'),
            jobinterviewdate=response.get('date'),
            # interview_author=Recruiter.objects.get(id=), ################ Filling in this field will be automatic
            # period_of_execution= ###############################          I don't know why is this field needed
            position=response.get('position'),
            organization=response.get('organization'),
            responsible_person=response.get('responsible_person'),
            contact_responsible_person_1str=response.get('phone'),
            contact_responsible_person_2str=response.get('telegram'),
            location=response.get('address'),
            additional_information=response.get('addition'),
        )
        if response.get('vacancy'):
            j.vacancies = Vacancy.objects.get(id=int(response.get('vacancy')))
        j.save()
        if files:
            for file in files:
                # print(file)
                f = FilesForJobInterviews(
                    add_file=file,
                    jobinterviews_files=j,
                )
                f.save()
        return redirect(applicant_user.get_tasks_url())


class EditJobInterview(View):
    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        files = request.FILES.getlist('files')
        # print(request.POST['id_job_edit'])
        j = JobInterviews.objects.get(id=request.POST['id_job_edit'])
        j.name = response.get('name')
        j.jobinterviewtime = response.get('time')
        j.jobinterviewdate = response.get('date')
        # interview_author=Recruiter.objects.get(id=) ################ Filling in this field will be automatic
        # period_of_execution= ###############################          I don't know why is this field needed
        j.position = response.get('position')
        j.organization = response.get('organization')
        j.responsible_person = response.get('responsible_person')
        j.contact_responsible_person_1str = response.get('phone')
        j.contact_responsible_person_2str = response.get('telegram')
        j.location = response.get('address')
        j.additional_information = response.get('addition')

        if response.get('vacancy'):
            j.vacancies = Vacancy.objects.get(id=int(response.get('vacancy')))
        j.save()
        if files:
            for file in files:
                # print(file)
                f = FilesForJobInterviews(
                    add_file=file,
                    jobinterviews_files=j,
                )
                f.save()
        return redirect(applicant_user.get_tasks_url())


class DelJobInterview(View):
    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        j = JobInterviews.objects.get(id=request.POST['id_job'])
        j.delete()
        return redirect(applicant_user.get_tasks_url())


class Vacancies(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return render(request, 'recruit/recruiter_vacancies.html', context={'vacancies': vacancies})

    def post(self, request):
        response = request.POST
        v = Vacancy(
            state=response['position'],
            salary=response['salary'],
            organization=response['organization'],
            address=response['address'],
            employment=response['employment'],
            description=response['description'],
            skills=response['skills'],
            requirements=response['requirements'],
            duties=response['duties'],
            conditions=response['conditions'],
        )
        v.save()
        return redirect('vacancies_url')


class VacancyDet(View):
    def get(self, request, id_v):
        vacancy = Vacancy.objects.get(id=id_v)
        return render(request, 'recruit/recruiter_vacancy_detail.html', context={'vacancy': vacancy})

    def post(self, request, id_v):
        response = request.POST
        v = Vacancy.objects.get(id=id_v)

        v.state = response['position']
        v.salary = response['salary']
        v.organization = response['organization']
        v.address = response['address']
        v.employment = response['employment']
        v.description = response['description']
        v.skills = response['skills']
        v.requirements = response['requirements']
        v.duties = response['duties']
        v.conditions = response['conditions']

        v.save()

        return redirect(v.get_absolute_url2())


class DelVacancy(View):
    def post(self, request, id_v):
        v = Vacancy.objects.get(id=request.POST['id_vac'])
        v.delete()
        return redirect('vacancies_url')


# End Poland's views #######################################################################################


def recruit_chat(request):
    chat_list = Chat.objects.filter(members=request.user)
    for chat in chat_list:
        mes = chat.members.all()
        for m in mes:
            print(m.username)
    context = {'user': request.user, 'chats': chat_list}
    return render(request=request, template_name='recruit/recruit_chat.html', context=context)


def get_messages(request):
    chat_id = (request.GET['chat_id'])
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in messages:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def send_message(request):
    chat = Chat.objects.get(id=request.GET['chat_id'])
    mes = Message(chat=chat, author=request.user, message=request.GET['message'])
    members = chat.members.all()
    mes.save()

    for m in members:
        if m != request.user:
            try:
                if Settings.objects.get(user=m).email_messages:
                    send_email = EmailMessage('HR-system', 'У вас новое сообщение', to=[str(m.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')

    send = {'author_id': mes.author.id, 'author_name': mes.author.username, 'message': mes.message, 'message_id': mes.id,
             'pub_date': mes.pub_date.ctime()}
    return JsonResponse(send, safe=False)


def chat_update(request):

    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(id=request.GET['chat_id'])
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def check_mes(request):
    chat = Chat.objects.filter(members=request.user)
    send = []
    for c in chat:
        unread_messages = len(Message.objects.filter(chat=c, is_read=False).exclude(author=request.user))
        new_dict = {'chat_id': c.id, 'count': unread_messages}
        send.append(new_dict)

    return JsonResponse(send, safe=False)


def add_task(request):
    context = {}
    context['users_list'] = UserModel.objects.all()
    #context['newtask'] = newtask
    return render(request=request, template_name='recruit/add_task.html', context=context)


def add_new_task(requset):
    try:
        user = UserModel.objects.get(username=requset.POST['name'])
    except UserModel.DoesNotExist: #TODO сделать проверку в отправек формы?
        return HttpResponse('Необходимо задать юзера')
    newtask = Tasks.objects.create()
    newtask.user = user
    newtask.title = requset.POST['task_title']
    newtask.comment = str(requset.POST['task_comment'])
    #newtask.time = datetime.now() TODO
    newtask.save()
    i = 1
    reqpost = requset.POST
    while True:
        try:
            newsubtask = SubTasks(title=reqpost['task_subtask' + str(i)], task=newtask)
        except:
            break
        i += 1
        newsubtask.save()

        try:
            if Settings.objects.get(user=user).email_messages:
                send_email = EmailMessage('HR-system', 'У вас новая задача', to=[str(user.email)])
                send_email.send()
        except Exception:
            print('Exception: нет адреса электронной почты')

    return redirect(to='add_task')



