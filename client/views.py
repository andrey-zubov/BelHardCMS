import logging
from collections import defaultdict
from time import perf_counter

from PIL import Image
from django.contrib import auth
from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import csrf

from django.urls import reverse
from django.views import View
from django.http import HttpResponse

from .models import Vacancy, Resume

from .forms import UploadImgForm, AddSkillForm, AddSkillFormSet, OpinionForm, AnswerForm, MessageForm

from django.views.generic import View, TemplateView


from BelHardCRM.settings import MEDIA_URL
from client.work_with_db import (load_client_img, load_edit_page, client_check, load_skills_page, load_education_page,
                                 load_cv_edition_page)
from .forms import OpinionForm, AnswerForm, MessageForm
from .forms import UploadImgForm, EducationFormSet, CertificateFormSet
from .models import *
from .utility import (check_input_str, check_home_number, check_telegram, check_phone, pars_cv_request,
                      pars_edu_request, pars_exp_request)


def client_main_page(request):  #!!!!!!!!!!!!!!!!!!!!!Alert 
    response = csrf(request)

    readtask = len(Tasks.objects.filter(user = request.user, readtask=False))
    chat = Chat.objects.get(members=request.user)
    unread_messages = len(Message.objects.filter(chat=chat, is_read=False).exclude(author=request.user))
    settings = Settings.objects.get(user=request.user)
    context = {'unread_messages': unread_messages, 'readtask': readtask, 'settings': settings}

   
    #Poland
    resumes = Resume.objects.all()
    notification = 0
    for resume in resumes:
        notification += resume.notification.count()
    response['notification'] = notification
    response['status'] = 1 if Settings.objects.get().tumbler_on_off == 'on' else 0

    client_instance = client_check(request.user)
    response['client_img'] = load_client_img(client_instance)
    context.update(response)
    return render(request=request, template_name='client/client_main_page.html', context=context)



def client_profile(request):
    response = csrf(request)
    client_instance = client_check(request.user)
    response['client_img'] = load_client_img(client_instance)

    return render(request=request, template_name='client/client_profile.html', context=response)


def client_edit_main(request):
    response = csrf(request)

    client_instance = client_check(request.user)

    if request.method == 'POST':
        time_0 = perf_counter()
        print('client_edit_main - request.POST')

        """ Входные данные для сохранения: """
        user = request.user
        user_name = check_input_str(request.POST['client_first_name'])
        last_name = check_input_str(request.POST['client_last_name'])
        patronymic = check_input_str(request.POST['client_middle_name'])
        sex = Sex.objects.get(sex_word=request.POST['sex']) if request.POST['sex'] else None
        date = request.POST['date_born'] if request.POST['date_born'] else None
        citizenship = Citizenship.objects.get(country_word=request.POST['citizenship']) if request.POST[
            'citizenship'] else None
        family_state = FamilyState.objects.get(state_word=request.POST['family_state']) if request.POST[
            'family_state'] else None
        children = Children.objects.get(children_word=request.POST['children']) if request.POST['children'] else None
        country = Citizenship.objects.get(country_word=request.POST['country']) if request.POST['country'] else None
        city = City.objects.get(city_word=request.POST['city']) if request.POST['city'] else None
        street = check_input_str(request.POST['street'])
        house = check_home_number(request.POST['house'])
        flat = check_home_number(request.POST['flat'])
        telegram_link = check_telegram(request.POST['telegram_link'])
        skype = check_input_str(request.POST['skype_id'])
        email = request.POST['email']
        link_linkedin = request.POST['link_linkedin']
        state = State.objects.get(state_word=request.POST['state']) if request.POST['state'] else None

        print(user_name, last_name, patronymic, sex, date, citizenship, family_state, children, country, city,
              street, house, flat, telegram_link, skype, email, link_linkedin, state)

        if not client_instance:
            """ Если карточки нету - создаём. """
            print('User Profile DO NOT exists - creating!')

            client = Client(
                user_client=user,
                name=user_name,
                last_name=last_name,
                patronymic=patronymic,
                sex=sex,
                date_born=date,
                citizenship=citizenship,
                family_state=family_state,
                children=children,
                country=country,
                city=city,
                street=street,
                house=house,
                flat=flat,
                telegram_link=telegram_link,
                skype=skype,
                email=email,
                link_linkedin=link_linkedin,
                state=state,
            )
            client.save()
        else:
            """ Если карточка есть - достаём из БД Объект = Клиент_id.
            Перезаписываем (изменяем) существующие данныев. """
            print('User Profile exists - Overwriting user data')

            client = client_instance
            client.name = user_name
            client.last_name = last_name
            client.patronymic = patronymic
            client.sex = sex
            client.date_born = date
            client.citizenship = citizenship
            client.family_state = family_state
            client.children = children
            client.country = country
            client.city = city
            client.street = street
            client.house = house
            client.flat = flat
            client.telegram_link = telegram_link
            client.skype = skype
            client.email = email
            client.link_linkedin = link_linkedin
            client.state = state
            client.save()

        """ Сохранение телефонных номеров клиента """
        tel = request.POST.getlist('phone')
        print("tel: %s" % tel)
        for t in tel:
            t = check_phone(t)
            if t:
                phone = Telephone(
                    client_phone=client,
                    telephone_number=t
                )
                phone.save()

        print('client_edit_main - OK; TIME: %s' % (perf_counter() - time_0))
        return redirect(to='/client/profile')
    else:
        print('client_edit_main - request.GET')

        """ Загрузка из БД списков для выбора и данных клиента"""
        response['client_img'] = load_client_img(client_instance)
        response['data'] = load_edit_page(client_instance)

    return render(request=request, template_name='client/client_edit_main.html', context=response)


def client_edit_skills(request):
    response = csrf(request)

    client_instance = client_check(request.user)

    if request.method == 'POST':
        print("client_edit_skills - request.POST")

        skills_arr = request.POST.getlist('skill') if request.POST.getlist('skill') else None
        print("skill: %s" % skills_arr)

        if any(skills_arr):
            for s in skills_arr:
                if s:
                    """ ОБЪЕДИНЕНИЕ модуля Навыки с конкретным залогиненым клиентом!!! """
                    skill = Skills(
                        client_skills=client_instance,
                        skill=check_input_str(s)
                    )
                    skill.save()
        else:
            print("No skills")

        return redirect(to='/client/edit')
    else:
        print('client_edit_skills - request.GET')
        response['client_img'] = load_client_img(client_instance)
        response['data'] = load_skills_page(client_instance)

    return render(request=request, template_name='client/client_edit_skills.html', context=response)


def client_edit_photo(request):
    response = csrf(request)
    client_instance = client_check(request.user)

    if request.method == 'POST':
        print('client_edit_photo - request.POST')

        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('img')
            client_instance.img = img
            client_instance.save()
            """
            в БД сохраняется УНИКАЛЬНОЕ имя картинки (пр. user_2_EntrmQR.png)
            в папке MEDIA_URL = '/media/'
            """
            print('client save photo - OK')
            return redirect(to='/client/edit')
    else:
        print('client_edit_photo - request.GET')
        response['client_img'] = load_client_img(client_instance)
        response['form'] = UploadImgForm()

    return render(request=request, template_name='client/client_edit_photo.html', context=response)


def client_edit_cv(request):
    response = csrf(request)
    client_instance = client_check(request.user)

    if request.method == 'POST':
        print('client_edit_cv - request.POST')

        arr_cv = pars_cv_request(request.POST)
        for cvs in arr_cv:
            position = cvs['position']
            employment = Employment.objects.get(employment=request.POST['employment'])
            time_job = TimeJob.objects.get(time_job_word=request.POST['time_job'])
            salary = cvs['salary']
            type_salary = TypeSalary.objects.get(type_word=request.POST['type_salary'])

            if any([position, employment, time_job, salary, type_salary]):
                cv = CV(
                    client_cv=client_instance,
                    position=position,
                    employment=employment,
                    time_job=time_job,
                    salary=salary,
                    type_salary=type_salary,
                )
                cv.save()

                print("CV Form - OK\n", position, employment, time_job, salary, type_salary)
            else:
                print('Cv form is Empty')
        return redirect(to='/client/edit')
    else:
        print('client_edit_cv - request.GET')
        response['client_img'] = load_client_img(client_instance)
        response['data'] = load_cv_edition_page(client_instance)

    return render(request, 'client/client_edit_cv.html', response)


def client_edit_education(request):
    response = csrf(request)
    client_instance = client_check(request.user)

    if request.method == 'POST':
        print("save_client_education - request.POST")

        arr_edu = pars_edu_request(request.POST, request.FILES)
        for edus in arr_edu:
            institution = edus['institution']
            subject_area = edus['subject_area']
            specialization = edus['specialization']
            qualification = edus['qualification']
            date_start = edus['date_start']
            date_end = edus['date_end']
            link = edus['certificate_url']
            img = edus['certificate_img']

            if any([institution, subject_area, specialization, qualification,
                    date_start, date_end, img, link]):

                education = Education(
                    client_edu=client_instance,
                    institution=institution,
                    subject_area=subject_area,
                    specialization=specialization,
                    qualification=qualification,
                    date_start=date_start if date_start else None,
                    date_end=date_end if date_end else None
                )
                education.save()

                certificate = Certificate(
                    education=education,
                    img=img,
                    link=link
                )
                certificate.save()

                print("Education Form - OK\n", institution, subject_area, specialization, qualification,
                      date_start if date_start else None, date_end if date_end else None, img, link)
            else:
                print('Education Form is Empty')

        return redirect('/client/edit')
    else:
        print('client_edit_education - request.GET')
        response['client_img'] = load_client_img(client_instance)
        response['data'] = load_education_page(client_instance)

    return render(request, 'client/client_edit_education.html', response)


def client_edit_experience(request):
    response = csrf(request)
    response['client_img'] = load_client_img(request.user)

    if request.method == 'POST':
        print("save_client_edit_experience - request POST")

        arr = pars_exp_request(request.POST)
        for dic in arr:
            organisation = dic['experience_1']
            position = dic['experience_3']
            start_date = dic['exp_date_start']
            end_date = dic['exp_date_end']
            duties = dic['experience_4']

            if any([organisation, position, start_date, end_date, duties]):
                client = Client.objects.get(user_client=request.user)

                experiences = Experience(
                    client_exp=client,
                    name=organisation,
                    position=position,
                    start_date=start_date if start_date else None,
                    end_date=end_date if end_date else None,
                    duties=duties if duties else None
                )
                experiences.save()

                spheres = dic['experience_2']
                for s in spheres:
                    if s:
                        """ Save ManyToManyField 'sphere' """
                        sp = Sphere(sphere_word=s)
                        sp.save()
                        experiences.sphere.add(sp)

                print("Experience Form - OK\n", organisation, spheres, position, start_date if start_date else None,
                      end_date if end_date else None, duties if duties else None)
            else:
                print('Experience Form is Empty')

        return redirect('/client/edit')
    else:
        print('save_client_edit_experience - request GET')

    return render(request, 'client/client_edit_experience.html', response)


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
        context = {'user_profile': request.user, 'unread_messages': unread_messages, 'chat': chat, 'form': MessageForm()}

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
        return render(request, 'opinion/opinion_create.html', context={'form': form})

    def post(self, request):
        form = OpinionForm(request.POST)

        if form.is_valid():
            new_opinion = form.save(commit=False)
            new_opinion.user = request.user
            new_opinion.save()
            return redirect('opinion_detail', pk=new_opinion.pk)
        return render(request, 'opinion/opinion_create.html', context={'form': form})


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
            return redirect('/')  # переадресация после авторизации
        else:
            res['error'] = "Неверный login/пароль"
            return render(request, 'registration.html', res)
    else:
        return render(request, 'registration.html', res)


def client_logout(request):  # выйти из системы, возврат на стартовую страницу
    auth.logout(request)
    return redirect('/')  # вставить редирект куда требуется


def tasks(request):

    task = Tasks.objects.filter(user=request.user, status=False)
    task_false = Tasks.objects.filter(user=request.user, status=True) #status=False)
    task_false = sorted(task_false, key=lambda x:x.endtime,  reverse=True)
    return render(request, 'client/tasks.html', context = {'task' : task,  'task_false': task_false})


class FormEducation(TemplateView):
    template_name = 'client/form_edu.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = defaultdict()

        load_data = load_education_page(client_instance)['cl_edu']
        # load_data_edu = Education.objects.filter(client_edu=client_instance).values()
        # edu_id = [e['id'] for e in load_data_edu]
        # load_data_cert = [[c for c in Certificate.objects.filter(education_id=i).values()] for i in edu_id]
        # print(load_data_cert[0])

        response['client_img'] = load_client_img(client_instance)
        response['edu_form'] = EducationFormSet(initial=load_data)
        response['certificate'] = CertificateFormSet(initial=load_data)

        return render(request, self.template_name, response)

    def post(self, request):
        print("FormEducation.POST: %s" % request.POST)
        client_instance = client_check(request.user)
        edu_inst = None
        form_set_edu = EducationFormSet(request.POST)
        form_set_cert = CertificateFormSet(request.POST, request.FILES)

        if form_set_edu.is_valid():
            print('FormSet_Edu - OK')
            for f in form_set_edu:
                f_items = f.cleaned_data.items()
                print("edu_items: %s" % f_items)
                if f_items:
                    """ edu_inst - unsaved model instance!
                    It gives you ability to attach data to the instance before saving to the DB! """
                    edu_inst = f.save(commit=False)
                    """ attach ForeignKey == Client instance """
                    edu_inst.client_edu = client_instance
                    """ Save Education instance """
                    edu_inst.save()

        if form_set_cert.is_valid():
            print("FormSet_Cert - OK")
            for c in form_set_cert:
                c_items = c.cleaned_data.items()
                print('cert_items: %s' % c_items)
                if c_items:
                    cert_inst = c.save(commit=False)
                    """ attach ForeignKey == Education instance """
                    cert_inst.education = edu_inst
                    cert_inst.save()
        else:
            print("FormSet_Cert not Valid")

        return redirect(to='/client/edit/form_edu')

    else:
        response['edu_form'] = EducationFormSet()
        response['certificate'] = CertificateFormSet()
        response['inlineEduCert'] = inlineEduCert()

    return render(request, 'client/form_edu.html', response)


def load_client_img(req):
    """ Show Client Img in the Navigation Bar.
    Img loaded from DB, if user do not have img - load default. """
    try:
        print("user: %s, id: %s" % (req, req.id))
        client_img = Client.objects.get(user_client=req).img
        if client_img:
            logging.info("Client.img: %s" % client_img)
            return "%s%s" % (MEDIA_URL, client_img)
        else:
            return '/media/user_1.png'
    except Exception as ex:
        logging.error("Exception in - load_client_img()\n %s" % ex)
        return '/media/user_1.png'



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
    #data = {'unread_mes': unread_messages, 'unread_task': readtask}
    data = [unread_messages, readtask]

    return HttpResponse(data)


def settings_menu(request):
    settings = Settings.objects.get(user=request.user)
    context = {'settings': settings, }
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

    settings.save()

    return HttpResponse(settings)


#Poland's views

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
    return render(request, 'client/client_resumes.html', context={'resumes': resumes})


def resume_detail(request, slug):
    resume = Resume.objects.get(slug__iexact=slug)
    return render(request, 'client/client_resume_detail.html', context={'resume': resume})


def accepted_vacancies(request, slug):########################
    resume = Resume.objects.get(slug__iexact=slug)
    return render(request, 'client/client_accepted_vacancies.html', context={'resume': resume})


def rejected_vacancies(request, slug):##############################
    resume = Resume.objects.get(slug__iexact=slug)
    return render(request, 'client/client_rejected_vacancies.html', context={'resume': resume})


def accept_reject(request):#

    if request.GET['flag'] == 'accept' and Vacancy.objects.get(slug__iexact=request.GET['slug']).in_waiting_for_resume.all():
        print(request.GET['slug'], 1)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).in_waiting_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_accept.add(v)
        r.vacancies_in_waiting.remove(v)
        r.save()
        return HttpResponse('accept_server')

    elif request.GET['flag'] == 'reject' and Vacancy.objects.get(slug__iexact=request.GET['slug']).in_waiting_for_resume.all():
        print(request.GET['slug'], 2)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).in_waiting_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_reject.add(v)
        r.vacancies_in_waiting.remove(v)
        r.save()
        return HttpResponse('reject_server')

    elif request.GET['flag'] == 'accept' and Vacancy.objects.get(slug__iexact=request.GET['slug']).reject_for_resume.all():
        print(request.GET['slug'], 3)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).reject_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_accept.add(v)
        r.vacancies_reject.remove(v)
        r.save()
        return HttpResponse('accept_server')

    elif request.GET['flag'] == 'reject' and Vacancy.objects.get(slug__iexact=request.GET['slug']).accept_for_resume.all():
        print(request.GET['slug'], 4)
        r = Vacancy.objects.get(slug__iexact=request.GET['slug']).accept_for_resume.get()
        v = Vacancy.objects.get(slug__iexact=request.GET['slug'])
        r.vacancies_reject.add(v)
        r.vacancies_accept.remove(v)
        r.save()
        return HttpResponse('reject_server')


def help_list(request):
    faqs = Help.objects.all()
    return render(request, 'client/help.html', context={'faqs': faqs})


def settings_list(request):
    settings = Settings.objects.all()
    status = 1 if Settings.objects.get().tumbler_on_off == 'on' else 0
    print('status = ', status)
    return render(request, 'client/settings.html', context={'settings': settings, 'status': status })


#def settings_on_off(request):
    #status = 1 if SettingsNotification.objects.get().tumbler_on_off == 'on' else 0
    #print('status = ', status)
    #return render(request, 'client/client_settings.html', context={'status': status})


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

#End Poland's views


