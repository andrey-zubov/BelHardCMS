from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from recruit import recruit_url

from django.urls import reverse
from django.utils.timezone import utc
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from client.edit.check_clients import (client_check, load_client_img)
from client.edit.edit_forms import (EducationFormSet, CertificateForm, SabClassFormSet, UploadImgForm)
from client.edit.pages_get import (edit_page_get, skills_page_get, cv_page_get, education_page_get, experience_page_get)
from client.edit.pages_post import (skills_page_post, edit_page_post, photo_page_post, form_edu_post,
                                    education_page_post, cv_page_post, experience_page_post)
from client.forms import (OpinionForm, AnswerForm, MessageForm)
from client.models import *


from django.views.generic import View, TemplateView
from django.views.generic import TemplateView

from client.edit.check_clients import (client_check, load_client_img)
from client.edit.edit_forms import (EducationFormSet, CertificateForm, SabClassFormSet, UploadImgForm)
from client.edit.pages_get import (edit_page_get, skills_page_get, cv_page_get, education_page_get, experience_page_get)
from client.edit.pages_post import (skills_page_post, edit_page_post, photo_page_post, form_edu_post,
                                    education_page_post, cv_page_post, experience_page_post)
from client.forms import (OpinionForm, AnswerForm, MessageForm)
from client.models import *


def client_main_page(request):  # !!!!!!!!!!!!!!!!!!!!!Alert
    response = csrf(request)

    readtask = len(Tasks.objects.filter(user=request.user, readtask=False))
    chat = Chat.objects.get(members=request.user)
    unread_messages = len(Message.objects.filter(chat=chat, is_read=False).exclude(author=request.user))
    settings = Settings.objects.get(user=request.user)
    context = {'unread_messages': unread_messages, 'readtask': readtask, 'settings': settings}

    # Poland
    resumes = Resume.objects.all()
    suggestions = 0
    for resume in resumes:
        suggestions += resume.notification.count()
    response['unread_suggestions'] = suggestions
    client_instance = client_check(request.user)
    response['client_img'] = load_client_img(client_instance)
    context.update(response)
    print(context['unread_suggestions'])
    return render(request=request, template_name='client/main_template_client.html', context=context)


def client_profile(request):
    client_instance = client_check(request.user)
    response = {'client_img': load_client_img(client_instance),
                }
    return render(request=request, template_name='client/client_profile.html', context=response)


# TeamRome
class ClientEditMain(TemplateView):
    template_name = 'client/edit_forms/client_edit_main.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': edit_page_get(client_instance),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        client_instance = client_check(request.user)
        edit_page_post(client_instance, request)
        return redirect(to='/client/profile')


# TeamRome
class ClientEditSkills(TemplateView):
    template_name = 'client/edit_forms/client_edit_skills.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': skills_page_get(client_instance),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        client_instance = client_check(request.user)
        skills_page_post(client_instance, request)
        return redirect(to='/client/edit')


# TeamRome
class ClientEditPhoto(TemplateView):
    template_name = 'client/edit_forms/client_edit_photo.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'form': UploadImgForm(),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        client_instance = client_check(request.user)
        photo_page_post(client_instance, request)
        return redirect(to='/client/edit')


# TeamRome
class ClientEditCv(TemplateView):
    template_name = 'client/edit_forms/client_edit_cv.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': cv_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        client_instance = client_check(request.user)
        cv_page_post(client_instance, request)
        return redirect(to='/client/edit')


# TeamRome
class ClientEditEducation(TemplateView):
    template_name = 'client/edit_forms/client_edit_education.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': education_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        client_instance = client_check(request.user)
        education_page_post(client_instance, request)
        return redirect('/client/edit')


# TeamRome
class ClientEditExperience(TemplateView):
    template_name = 'client/edit_forms/client_edit_experience.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    "data": experience_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        client_instance = client_check(request.user)
        experience_page_post(client_instance, request)
        return redirect('/client/edit')


class MessagesView(View):
    def get(self, request):
        try:
            chat = Chat.objects.get(members=request.user)
            if request.user in chat.members.all():
                chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        unread_messages = len(Message.objects.filter(chat=chat, is_read=False).exclude(author=request.user))
        context = {'user_profile': request.user,
                   'unread_messages': unread_messages,
                   'chat': chat,
                   'form': MessageForm()}
        client_instance = client_check(request.user)
        context['client_img'] = load_client_img(client_instance)
        return render(request, 'client/client_chat.html', context)

    def post(self, request):
        form = MessageForm(data=request.POST)
        chat = Chat.objects.get(members=request.user)
        print(form)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat.id
            message.author = request.user
            message.save()
        return redirect(reverse('contact_with_centre'))


def opinion_list(request):
    opinion = Opinion.objects.all()
    return render(request, 'opinion/index.html', context={'opinion': opinion})


def answer_create(request, pk):
    opinion = get_object_or_404(Opinion, id=pk)
    answer = Answer.objects.filter(pk=pk)
    form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.opinion = opinion
            form.user = request.user
            form.save()
            return redirect('opinion_detail', pk)
    return render(request, 'opinion/answer_create.html', context={'form': form, 'opinion': opinion, "answer": answer})


class OpinionCreate(View):
    def get(self, request):
        form = OpinionForm()
        client_instance = client_check(request.user)
        return render(request, 'opinion/opinion_create.html', context={'form': form,
                                                                       'client_img':load_client_img(client_instance)})

    def post(self, request):
        form = OpinionForm(request.POST)

        if form.is_valid():
            new_opinion = form.save(commit=False)
            new_opinion.user = request.user
            new_opinion.save()
            return redirect('opinion_detail', pk=new_opinion.pk)
        client_instance = client_check(request.user)
        return render(request, 'opinion/opinion_create.html', context={'form': form,
                                                                       'client_img':load_client_img(client_instance)})


def opinion_detail(request, pk):
    opinion = get_object_or_404(Opinion, pk=pk)
    return render(request, 'opinion/opinion_detail.html', {'opinion': opinion})


class OpinionDelete(View):
    def get(self, request, pk):
        opinion = Opinion.objects.filter(pk=pk)
        return render(request, 'opinion/opinion_delete.html', context={'opinion': opinion})

    def post(self, request, pk):
        opinion = Opinion.objects.filter(pk=pk)
        opinion.delete()
        return redirect(reverse('opinion_list'))


def client_login(request):  # ввести логин/пароль -> зайти в систему
    res = csrf(request)
    res['url'] = 'login'
    if request.POST:
        password = request.POST['password']
        user = request.POST['user']
        u = auth.authenticate(username=user, password=password)
        if u:
            auth.login(request, u)
        else:
            res['error'] = "Неверный login/пароль"
            return render(request, 'registration.html', res)
    else:
        return render(request, 'registration.html', res)
    try:
        user_chat = Chat.objects.filter(members=request.user)
    except Chat.DoesNotExist:
        user_chat = Chat.objects.create()
        user_chat.members.add(request.user)  # TODO сюда добавить менеджера, которому, по дефолту, передают юзера
    try:
        user_settings = Settings.objects.get(user=request.user)
    except Settings.DoesNotExist:
        user_settings = Settings.objects.create(user=request.user)
    if u.groups.filter(name='Users').exists():
        return redirect('client')
    elif u.groups.filter(name='Recruiters').exists():
        return redirect('main_page')

def client_logout(request):  # выйти из системы, возврат на стартовую страницу
    auth.logout(request)
    return redirect(to='login')  # вставить редирект куда требуется


def tasks(request):
    task = Tasks.objects.filter(user=request.user, status=False)
    task_false = Tasks.objects.filter(user=request.user, status=True) #status=False)
    task_false = sorted(task_false, key=lambda x:x.endtime,  reverse=True)
    client_instance = client_check(request.user)
    return render(request, 'client/tasks.html', context = {'task' : task,
                                                        'task_false': task_false,
                                                           'client_img':load_client_img(client_instance)})


# TeamRome
class FormEducation(TemplateView):
    template_name = 'client/edit_forms/form_edu.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        load_data = education_page_get(client_instance)['cl_edu']

        response = {'client_img': load_client_img(client_instance),
                    'edu_form': EducationFormSet(initial=load_data),
                    # 'certificate': CertificateFormSet(initial=load_data),
                    'certificate': CertificateForm(initial=load_data[0]),
                    'sab_class_form': SabClassFormSet(initial=load_data),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        client_instance = client_check(request.user)
        form_edu_post(client_instance, request)
        return redirect(to='/client/edit/form_edu')


def checktask(request):
    id = (request.GET['id'])
    task = Tasks.objects.get(id=id)

    if task.status == False:
        task.status = True
        task.endtime = timezone.now()
    else:
        task.status = False
        task.endtime = None
    task.save()
    return HttpResponse(task)


def checknotifications(request):
    chat = Chat.objects.get(members=request.user)
    unread_messages = len(Message.objects.filter(chat=chat, is_read=False).exclude(author=request.user))
    readtask = len(Tasks.objects.filter(user=request.user, readtask=False))
    resumes = Resume.objects.all()
    suggestions = 0
    for resume in resumes:
        suggestions += resume.notification.count()

    data = [unread_messages, readtask, suggestions]

    return HttpResponse(data)


def settings_menu(request):
    settings = Settings.objects.get(user=request.user)
    context = {'settings': settings, }
    client_instance = client_check(request.user)
    context['client_img'] = load_client_img(client_instance)
    return render(request=request, template_name='client/client_settings.html', context=context)


def set_settings(request):
    setting = request.GET['setting']
    status = request.GET['state'] == 'true'
    settings = Settings.objects.get(user=request.user)

    if setting == 'messages':
        settings.messages = status
    elif setting == 'tasks':
        settings.tasks = status
    elif setting == 'suggestions':
        settings.suggestions = status
    elif setting == 'meetings':
        settings.meetings = status
    elif setting == 'reviews':
        settings.reviews = status
    elif setting == 'email_messages':
        settings.email_messages = status
    elif setting == 'email_tasks':
        settings.email_tasks = status
    elif setting == 'email_suggestions':
        settings.email_suggestions = status
    elif setting == 'email_meetings':
        settings.email_meetings = status
    elif setting == 'email_reviews':
        settings.email_reviews = status

    settings.save()

    return HttpResponse(settings)


def chat_update(request):

    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(members=request.user)
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append({'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id, 'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


# Poland's views

def vacancies_list(request, slug):
    resume = Resume.objects.get(slug__iexact=slug)
    return render(request, 'client/client_vacancies.html', context={'resume': resume})


def vacancy_detail(request, slug):
    vacancy = Vacancy.objects.get(slug__iexact=slug)
    first_flag = 1 if bool(vacancy.in_waiting_for_resume.all() or vacancy.reject_for_resume.all()) else 0
    second_flag = 1 if bool(vacancy.in_waiting_for_resume.all() or vacancy.accept_for_resume.all()) else 0
    return render(request, 'client/client_vacancy_detail.html', context={
        'vacancy': vacancy,
        'first_flag': first_flag,
        'second_flag': second_flag
    })


def resumes_list(request):
    resumes = Resume.objects.all()
    client_instance = client_check(request.user)
    return render(request, 'client/client_resumes.html', context={'resumes': resumes,
                                                                  'client_img':load_client_img(client_instance)})


def resume_detail(request, slug):
    resume = Resume.objects.get(slug__iexact=slug)
    return render(request, 'client/client_resume_detail.html', context={'resume': resume})


def accepted_vacancies(request, slug):  ########################
    resume = Resume.objects.get(slug__iexact=slug)
    return render(request, 'client/client_accepted_vacancies.html', context={'resume': resume})


def rejected_vacancies(request, slug):  ##############################
    resume = Resume.objects.get(slug__iexact=slug)
    return render(request, 'client/client_rejected_vacancies.html', context={'resume': resume})


def accept_reject(request):  #

    if request.GET['flag'] == 'accept' and Vacancy.objects.get(
            slug__iexact=request.GET['slug']).in_waiting_for_resume.all():
        print(request.GET['slug'], 1)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).in_waiting_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_accept.add(v)
        r.vacancies_in_waiting.remove(v)
        r.save()
        return HttpResponse('accept_server')

    elif request.GET['flag'] == 'reject' and Vacancy.objects.get(
            slug__iexact=request.GET['slug']).in_waiting_for_resume.all():
        print(request.GET['slug'], 2)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).in_waiting_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_reject.add(v)
        r.vacancies_in_waiting.remove(v)
        r.save()
        return HttpResponse('reject_server')

    elif request.GET['flag'] == 'accept' and Vacancy.objects.get(
            slug__iexact=request.GET['slug']).reject_for_resume.all():
        print(request.GET['slug'], 3)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).reject_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_accept.add(v)
        r.vacancies_reject.remove(v)
        r.save()
        return HttpResponse('accept_server')

    elif request.GET['flag'] == 'reject' and Vacancy.objects.get(
            slug__iexact=request.GET['slug']).accept_for_resume.all():
        print(request.GET['slug'], 4)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).accept_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_reject.add(v)
        r.vacancies_accept.remove(v)
        r.save()
        return HttpResponse('reject_server')


def help_list(request):
    faqs = Help.objects.all()
    client_instance = client_check(request.user)
    return render(request, 'client/help.html', context={'faqs': faqs,
                                                        'client_img':load_client_img(client_instance)})


def settings_list(request):
    settings = Settings.objects.all()
    status = 1 if Settings.objects.get().tumbler_on_off == 'on' else 0
    print('status = ', status)
    return render(request, 'client/settings.html', context={'settings': settings, 'status': status})


# def settings_on_off(request):
# status = 1 if SettingsNotification.objects.get().tumbler_on_off == 'on' else 0
# print('status = ', status)
# return render(request, 'client/client_settings.html', context={'status': status})


def on_off(request):
    status = Settings.objects.get()
    status.tumbler_on_off = request.GET['status']
    print(status.tumbler_on_off)
    status.save()
    return HttpResponse(status.tumbler_on_off)


def viewed(request):
    if request.GET['action'] == 'clear':
        resumes = Resume.objects.all()
        for resume in resumes:
            r = resume
            r.notification.clear()
        return HttpResponse('cleared')

# End Poland's views
