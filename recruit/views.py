from time import perf_counter
from collections import defaultdict

from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
from django.db.models.functions import Lower
from django.db.models import Q

from client.edit.check_clients import (load_client_img)
from client.models import (CV, JobInterviews, FilesForJobInterviews, Vacancy,
                           State)
from client.models import (Chat, Message, Tasks, UserModel, SubTasks, Settings,
                           Client, Opinion, Answer, Employer, Direction)
from recruit.edit_pages.check_recruit import (recruit_check)
from recruit.edit_pages.r_forms import (RecruitUploadImgForm)
from recruit.edit_pages.r_pages_get import (recruit_edit_page_get,
                                            recruit_experience_page_get,
                                            recruit_education_page_get,
                                            recruit_show_page_get)
from recruit.edit_pages.r_pages_get import (recruit_skills_page_get)
from recruit.edit_pages.r_pages_post import (photo_page_post, recruit_skills_page_post,
                                             recruit_education_page_post)
from recruit.edit_pages.r_pages_post import (recruit_edit_page_post,
                                             recruit_experience_page_post)
from recruit.models import (Recruiter)

from .models import *  # TODO fix *

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """


# There is Poland's views #
def recruit_main_page(request):  # TeamRome
    recruit_instance = recruit_check(request.user)
    response = {'recruit_img': load_client_img(recruit_instance),
                'data': 'foo()',
                }
    return render(request, template_name='recruit/recruit_main_template.html',
                  context=response)


def recruiter_base(request):
    return render(request, template_name='recruit/recruiter_base.html', )


def base_of_applicants(request):
    # applicants = Client.objects.all()
    own_status = 'all'

    # Для проверки на наличие в списке избранного
    recruiter = Recruiter.objects.get(recruiter=request.user)
    owner_list = Client.objects.filter(own_recruiter=recruiter)
    owner_range = len(owner_list)
    url_check = 'base_of_applicants'
    clients_after_search = client_filtration(request, own_status)
    applicants = clients_after_search
    return render(request,
                  template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants,
                           'owner_list': owner_list,
                           'owner_range': owner_range,
                           'url_check': url_check,
                           })


class ApplicantDet(View):
    """ Детальный просмотр профиля соискателя. """
    def get(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        resumes = applicant_user.cv_set.all()
        vacancies = Vacancy.objects.all()
        user = applicant_user.user_client
        user_id = user.id
        user_activ_tasks = Tasks.objects.filter(user=user, status=False)
        return render(request, 'recruit/recruiter_applicant.html',
                      context={'applicant_user': applicant_user,
                               'resumes': resumes, 'vacancies': vacancies,
                               'user_id': user_id,
                               'user_activ_tasks': user_activ_tasks})

    def post(self, request, id_a):
        """ Отправка соискателю вакансии на рассмотрение (с фронта). """
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        resume = CV.objects.get(id=response['id_cv'])
        vacancies_id = request.POST.getlist('id_v')

        for id_v in vacancies_id:
            vacancy = Vacancy.objects.get(id=id_v)
            resume.vacancies_in_waiting.add(vacancy)
            resume.notification.add(vacancy)
        return redirect(applicant_user.get_absolute_url())


class ApplicantCVDet(View):
    def get(self, request, id_a, id_c):
        cv = CV.objects.get(id=id_c)
        cv_v_in_w = cv.vacancies_in_waiting.all()
        cv_v_a = cv.vacancies_accept.all()
        cv_v_r = cv.vacancies_reject.all()
        applicant = Client.objects.get(id=id_a)
        vacancies = Vacancy.objects.filter(direction=cv.direction)
        sum_cv = cv_v_in_w | cv_v_a | cv_v_r
        return render(request, 'recruit/recruit_applicant_cv_det.html',
                      context={'cv': cv, 'sum_cv': sum_cv,
                               'applicant': applicant, 'vacancies': vacancies})


def check_flag(request):
    # print('check_flag', request.GET.get('check_flag'))
    return HttpResponse('Done!')


class CreateJobInterview(View):
    def get(self, request, id_a):
        """Вывод на экран подтвержденных вакансий"""
        applicant_user = Client.objects.get(id=id_a)
        if CV.objects.filter(client_cv=applicant_user):
            accepted_vacancies = applicant_user.cv_set.all()[
                0].vacancies_accept.all()
            for resume in applicant_user.cv_set.all()[1:]:
                accepted_vacancies |= resume.vacancies_accept.all()
        else:
            accepted_vacancies = None
        return render(request, 'recruit/recruiter_tasks_for_applicant.html',
                      context={'applicant_user': applicant_user,
                               'accepted_vacancies': accepted_vacancies})

    def post(self, request, id_a):
        """ Создание собеседования для клиента """
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST

        files = request.FILES.getlist('files')
        j = JobInterviews(
            client=applicant_user,
            name=response.get('name'),
            jobinterviewtime=response.get('time'),
            jobinterviewdate=response.get('date'),
            interview_author=recruit_check(request.user),
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
                f = FilesForJobInterviews(
                    add_file=file,
                    jobinterviews_files=j,
                )
                f.save()
        return redirect(applicant_user.get_tasks_url())


class EditJobInterview(View):
    def post(self, request, id_a):
        """ Редактирование собеседования """
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        files = request.FILES.getlist('files')
        j = JobInterviews.objects.get(id=request.POST['id_job_edit'])
        j.name = response.get('name')
        j.jobinterviewtime = response.get('time')
        j.jobinterviewdate = response.get('date')
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
                f = FilesForJobInterviews(
                    add_file=file,
                    jobinterviews_files=j,
                )
                f.save()
        return redirect(applicant_user.get_tasks_url())


class DelJobInterview(View):
    """ Удаление собеседования """
    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        j = JobInterviews.objects.get(id=request.POST['id_job'])
        j.delete()
        return redirect(applicant_user.get_tasks_url())


class Employers(View):
    """ Вывод на экран базы работодателей.
    Поиск по базе и вывод результата на экран. """
    def get(self, request):
        search_name = request.GET.get('search_name', '')
        found_name = ''
        all_values = request.GET.get('all_values')
        if all_values:
            employers = Employer.objects.all().order_by(Lower('name'))
        else:
            if search_name:
                employers = Employer.objects.filter(
                    name__icontains=search_name).order_by(Lower('name'))
                found_name = search_name
            else:
                employers = Employer.objects.all().order_by(Lower('name'))
        return render(request, 'recruit/recruiter_employers.html',
                      context={'employers': employers,
                               'found_name': found_name})

    def post(self, request):
        """ Создание карточки работодателя. """
        files = request.FILES.get('files')
        response = request.POST
        e = Employer(
            name=response['name'],
            address=response['address'],
            description=response['description'],
        )
        if files:
            e.image = files
        e.save()
        return redirect('employers_url')


class EmployerDet(View):
    """ Детальный просмотр карточки работодалеля. """
    def get(self, request, id_e):
        employer = Employer.objects.get(id=id_e)
        empl_vacancies = employer.vacancies.all()
        return render(request, 'recruit/recruiter_employer_detail.html',
                      context={'employer': employer,
                               'empl_vacancies': empl_vacancies})

    def post(self, request, id_e):
        """ Редактирование карточки работодателя. """
        response = request.POST
        e = Employer.objects.get(id=id_e)
        e.name = response['name']
        e.address = response['address']
        e.description = response['description']
        if request.FILES.get('files'):
            e.image.delete()
            e.image = request.FILES['files']
        e.save()
        return redirect(e.get_absolute_url())


class EmployerDel(View):
    """ Удаление карточки работодателя """
    def post(self, request, id_e):
        e = Employer.objects.get(id=request.POST['id_emp'])
        e.delete()
        return redirect('employers_url')


class Vacancies(View):
    def get(self, request):
        """ Вывод на экран базы работодателей.
            Поиск и вывод результата на экран. """
        search_direct = request.GET.get('search_direction', '')
        search_state = request.GET.get('search_state')
        found_direct = ''
        found_state = ''
        all_values = request.GET.get('all_values')
        if all_values:
            vacancies = Vacancy.objects.all().order_by(Lower('organization'))
        else:
            if search_direct and search_state:
                vacancies = Vacancy.objects.filter(
                    Q(direction=search_direct) | Q(state__icontains=search_state)
                ).order_by(Lower('organization'))
                found_direct = search_direct
                found_state = search_state
            elif search_direct:
                vacancies = Vacancy.objects.filter(
                    direction=search_direct).order_by(Lower('organization'))
                found_direct = int(search_direct)
            elif search_state:
                vacancies = Vacancy.objects.filter(
                    state__icontains=search_state).order_by(Lower('organization'))
                found_state = search_state
            else:
                vacancies = Vacancy.objects.all().order_by(Lower('organization'))
        directions = Direction.objects.all().order_by('direction_word')
        return render(request, 'recruit/recruiter_vacancies.html',
                      context={'vacancies': vacancies,
                               'directions': directions,
                               'found_direct': found_direct,
                               'found_state': found_state})

    def post(self, request):
        """ Создание карточки вакансии. """
        response = request.POST
        v = Vacancy(
            state=response['position'],
            salary=response['salary'],
            employment=response['employment'],
            description=response['description'],
            skills=response['skills'],
            requirements=response['requirements'],
            duties=response['duties'],
            conditions=response['conditions'],
        )

        if response.get('id_empl'):
            e = Employer.objects.get(id=response['id_empl'])
            v.employer = e
            v.organization = e.name
            v.address = e.address
            v.save()
            v.direction.add(Direction.objects.get(id=response['direction']))
            return redirect('employer_det_url', id_e=response['id_empl'])
        else:
            if response['organization'] in \
                    [e.name for e in Employer.objects.all()]:
                v.organization = Employer.objects.get(
                    name=response['organization']).name
                v.employer = Employer.objects.get(
                    name=response['organization'])
                v.save()
                v.direction.add(Direction.objects.get(id=response['direction']))
                return redirect('vacancies_url')
            else:
                e = Employer(name=response['organization'],
                             address=response['address'])
                e.save()
                v.organization = e.name
                v.address = e.address
                v.employer = e
                v.save()
                v.direction.add(Direction.objects.get(id=response['direction']))
                return redirect('vacancies_url')


class VacancyDet(View):
    def get(self, request, id_v):
        # print('VacancyDet', request.GET.get('check_flag'))
        vacancy = Vacancy.objects.get(id=id_v)
        directions = Direction.objects.all().order_by('direction_word')
        return render(request, 'recruit/recruiter_vacancy_detail.html',
                      context={'vacancy': vacancy, 'directions': directions})

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
        v.direction.clear()
        v.direction.add(Direction.objects.get(id=response['direction']))
        v.save()

        return redirect(v.get_absolute_url2())


class DelVacancy(View):
    def post(self, request, id_v):
        v = Vacancy.objects.get(id=request.POST['id_vac'])
        v.delete()
        return redirect('vacancies_url')


# End Poland's views #


def recruit_chat(request):
    chat_list = Chat.objects.filter(members=request.user)
    for chat in chat_list:
        mes = chat.members.all()
        for m in mes:
            print(m.username)
    context = {'user': request.user, 'chats': chat_list}
    return render(request=request, template_name='recruit/recruit_chat.html',
                  context=context)


def get_messages(request):
    chat_id = (request.GET['chat_id'])
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(
            author=request.user).update(is_read=True)

    send2 = []
    for s in messages:
        send2.append(
            {'author_id': s.author.id, 'user_id': request.user.id,
             'author_first_name': s.author.first_name,
             'author_last_name': s.author.last_name, 'message': s.message,
             'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def send_message(request):
    chat = Chat.objects.get(id=request.GET['chat_id'])
    mes = Message(chat=chat, author=request.user,
                  message=request.GET['message'])
    members = chat.members.all()
    mes.save()

    for m in members:
        if m != request.user:
            try:
                if Settings.objects.get(user=m).email_messages:
                    send_email = EmailMessage('HR-system',
                                              'У вас новое сообщение',
                                              to=[str(m.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')

    send = {'author_id': mes.author.id, 'user_id': request.user.id,
            'author_first_name': mes.author.first_name,
            'author_last_name': mes.author.last_name, 'message': mes.message,
            'message_id': mes.id,
            'pub_date': mes.pub_date.ctime()}

    return JsonResponse(send, safe=False)


def chat_update(request):
    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(id=request.GET['chat_id'])
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(
            author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username,
             'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def check_mes(request):
    chat = Chat.objects.filter(members=request.user)
    send = []
    for c in chat:
        unread_messages = len(
            Message.objects.filter(chat=c, is_read=False).exclude(
                author=request.user))
        new_dict = {'chat_id': c.id, 'count': unread_messages}
        send.append(new_dict)

    return JsonResponse(send, safe=False)


class pattern_task(View):
    '''Назначение новых и шаблонных задач рекрутером-клиенту.'''
    def get(self, request):
        client_id = request.GET['user_id']
        pattern_tasks = RecruitPatternClient.objects.all()
        check = 1
        client_ac = Client.objects.get(id=client_id)
        client_user = client_ac.user_client
        client_activ_tasks = Tasks.objects.filter(user=client_user, status=False)

        return render(request, template_name='recruit/pattern_task.html', context={'client_id': client_id,
                                                                                   'pattern_tasks': pattern_tasks,
                                                                                   'client': client_user,
                                                                                   'check': check,
                                                                                   'client_activ_tasks': client_activ_tasks})

    def post(self, request):
        if 'form1' in request.POST:
            client_id = request.POST['user_id']
            client_ac = Client.objects.get(id=client_id)
            client_user = client_ac.user_client
            client_activ_tasks = Tasks.objects.filter(user=client_user, status=False)
            pattern_tasks = RecruitPatternClient.objects.all()
            chosen_task = RecruitPatternClient.objects.get(title=request.POST['pattern_task'])
            chosen_id = chosen_task.id
            check = 2
            return render(request, template_name='recruit/pattern_task.html', context={'client_id': client_id,
                                                                                       'pattern_tasks': pattern_tasks,
                                                                                       'check': check,
                                                                                       'task': chosen_task,
                                                                                       'task_id': chosen_id,
                                                                                       'client_activ_tasks': client_activ_tasks})

        if 'form2' in request.POST:
            client = Client.objects.get(id=request.POST['user_id'])
            client_user = client.user_client

            newtask = Tasks.objects.create()
            newtask.user = client_user
            newtask.title = request.POST['task_title']
            newtask.comment = str(request.POST['task_comment'])
            newtask.save()

            try: # если использован шаблон
                pattern_id = request.POST['pattern_used']
                pattern = RecruitPatternClient.objects.get(id=pattern_id)
                all_subs = pattern.show_all

                reqpost = request.POST
                for sub in all_subs: # изменить шаблонные
                    try:
                        sub_text = request.POST['subtask_' + str(sub.id)]
                        newsubtask = SubTasks(title=sub_text, task=newtask)
                        print('first', sub, str('subtask_' + str(sub.id)))
                    except:
                        try:
                            i += 1
                            print('i:', i)
                            newsubtask = SubTasks(title=reqpost['task_subtask' + str(i)], task=newtask)
                        except:
                            break
                    newsubtask.save()
                    print(str(newsubtask))
            except:
                pass

            i = 0
            while True: # добавление новых
                i += 1
                try:
                    # return HttpResponse('task_subtask' + str(i))
                    sub_text = request.POST['task_subtask' + str(i)]
                    newsubtask = SubTasks(title=sub_text, task=newtask)
                except:
                    if i == 1:
                        continue
                    else:
                        break
                newsubtask.save()

            try:
                if Settings.objects.get(user=client).email_messages:
                    send_email = EmailMessage('HR-system', 'У вас новая задача', to=[str(client.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')
            return redirect(client.get_add_client_task())
        else:
            return HttpResponse('ОШИБКА В НАЗВАНИИ ФФОРЫФ')


class change_task(View):
    def get(self, request, id_t):
        task = Tasks.objects.get(id=id_t)
        sub_len = len(task.show_all)
        return render(request, template_name='recruit/change_client_task.html', context={'task_id': id_t,
                                                                                         'task': task,
                                                                                         'sub_len': sub_len})

    def post(self, request, id_t):
        task = Tasks.objects.get(id=id_t)
        task_user = task.user
        client = Client.objects.get(user_client=task_user)
        task.title = request.POST['task_title']
        task.comment = str(request.POST['task_comment'])
        subtasks = task.show_all
        task.save()


        for sub in subtasks:
            sub.title = request.POST['subtask_' + str(sub.id)]
            sub.save()


        return redirect(client.get_add_client_task())



class client_task_adding(View):

    def get(self, request, id_a):
        client = Client.objects.get(id=id_a)
        client_user = client.user_client #ссылается на UserModel
        client_activ_tasks = Tasks.objects.filter(user=client_user, status=False) #просмотр активных задач клинета
        client_closed_tasks = Tasks.objects.filter(user=client_user, status=True)
        return render(request, template_name='recruit/adding_task_to_client.html', context={'client':client,
                                                                                            'client_user': client_user,
                                                                                            'client_activ_tasks':client_activ_tasks,
                                                                                            'client_closed_tasks': client_closed_tasks})


    def post(self, request, id_a):
        client = Client.objects.get(id=id_a)
        client_user = client.user_client
        newtask = Tasks.objects.create()
        newtask.user = client_user
        newtask.title = request.POST['task_title']
        newtask.comment = str(request.POST['task_comment'])
        newtask.save()
        i = 1
        reqpost = request.POST
        while True:
            try:
                newsubtask = SubTasks(title=reqpost['task_subtask' + str(i)], task=newtask)
            except:
                break
            i += 1
            newsubtask.save()

        try:
            if Settings.objects.get(user=client).email_messages:
                send_email = EmailMessage('HR-system', 'У вас новая задача', to=[str(client.email)])
                send_email.send()
        except Exception:
            print('Exception: нет адреса электронной почты')
        return redirect(client.get_add_client_task())

# список избранных клиентов, для рекрутера
def favorites(request):
    own_status = Recruiter.objects.get(recruiter=request.user)
    # own_status = recruit
    clients = client_filtration(request, own_status)
    context = {'applicants': clients}

    return render(request, template_name='recruit/favorites.html',
                  context=context)


# обработка избранного рекрутера
def check_favor(request):
    client_id = (request.GET['client'])
    client = Client.objects.get(id=client_id)
    recruit_id = (request.GET['recruit'])
    recruit = Recruiter.objects.get(
        recruiter=UserModel.objects.get(id=recruit_id))
    if client.is_reserved == True:

        client.is_reserved = False
        client.own_recruiter = None
        chat = Chat.objects.get(members=client.user_client)
        chat.members.remove(recruit.recruiter)
    else:
        client.is_reserved = True
        client.own_recruiter = recruit
        chat = Chat.objects.get(members=client.user_client)
        chat.members.add(recruit.recruiter)
    client.save()
    return HttpResponse(client_id)


# список незарезервированных клиентов, для рекрутера
def recruit_base(request):
    applicants = Client.objects.all()
    own_status = None
    clients_after_search = client_filtration(request, own_status)
    context = {'free_clients': clients_after_search, 'applicants': applicants}
    return render(request, template_name='recruit/recruit_base.html',
                  context=context)


# функция поиска по списку клиентов, для рекрутера
def client_filtration(request, own_status):
    recruit = Recruiter.objects.get(recruiter=request.user)
    search_request = request.GET.get('recruit_search', '')
    clients_after_search = set()
    if search_request:
        search_params = search_request.split(' ')
        print(search_params)
        clients = Client.objects.all()

        for s in search_params:
            users_for_first_name_list = UserModel.objects.filter(
                first_name__contains=s)
            users_for_last_name_list = UserModel.objects.filter(
                last_name__contains=s)
            users_for_patronymic = clients.filter(patronymic__contains=s)
            try:
                users_for_state = clients.filter(
                    state__contains=State.objects.get(state_word=s))
                clients_after_search.update(users_for_state)
            except:
                print('ясно')
            users_for_first_name = set()
            users_for_last_name = set()
            for u in users_for_first_name_list:
                users_for_first_name.add(clients.get(user_client=u))
            for u in users_for_last_name_list:
                users_for_last_name.add(clients.get(user_client=u))

            clients_after_search.update(users_for_first_name)
            clients_after_search.update(users_for_last_name)
            clients_after_search.update(users_for_patronymic)
    else:
        if own_status == 'all':
            clients_after_search = Client.objects.all()
            return clients_after_search
        clients_after_search = Client.objects.filter(own_recruiter=own_status)

    return clients_after_search


class RecruitProfile(TemplateView):  # TeamRome
    template_name = 'recruit/recruit_profile.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_show_page_get(recruit_instance),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        pass


class RecruitEditMain(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_edit_main.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_edit_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_edit_page_post(recruit_instance, request)
        return redirect(to='/recruit/profile/')


class RecruitEditExperience(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_edit_experience.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    "data": recruit_experience_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_experience_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit/')


class RecruitEditEducation(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_edit_education.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_education_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_education_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit/')


class RecruitEditSkills(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_skills.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_skills_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_skills_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit')


class RecruitEditPhoto(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_photo.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'form': RecruitUploadImgForm(),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        photo_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit')


class RecruitShowSkills(TemplateView):  # TeamRome
    template_name = 'recruit/show/show_skills.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_skills_page_get(recruit_instance),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)


class RecruitShowEducation(TemplateView):  # TeamRome
    template_name = 'recruit/show/show_education.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_education_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)


class RecruitShowExperience(TemplateView):  # TeamRome
    template_name = 'recruit/show/show_experience.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    "data": recruit_experience_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)


def recruiters_tasks(request):
    me = Recruiter.objects.get(recruiter=request.user)
    all_tasks = RecruitersTasks.objects.all()
    my_tasks = RecruitersTasks.objects.filter(recruiters=me)
    free_tasks = RecruitersTasks.objects.filter(recruiters=None)
    my_tasks_new = my_tasks.filter(status=False)
    my_tasks_old = my_tasks.filter(status=True)


    return render(request=request, template_name='recruit/recruiters_tasks.html', context={'all_tasks': all_tasks,
                                                                                           'my_tasks': my_tasks,
                                                                                           'free_tasks': free_tasks,
                                                                                           'me': me,
                                                                                           'my_tasks_new': my_tasks_new,
                                                                                           'my_tasks_old': my_tasks_old})


def recruit_chooose_task(request):
    choice = int(request.GET['choice'])
    my_id = request.GET['my_id']
    user = UserModel.objects.get(id=my_id)
    recruiter = Recruiter.objects.get(recruiter=user)
    task_id = request.GET['task_id']
    rec_task = RecruitersTasks.objects.get(id=task_id)

    if choice == 1:
        rec_task.recruiters = recruiter
        rec_task.save()

    return HttpResponse()


def recruit_check_task(request):
    my_id = request.GET['my_id']
    task_id = request.GET['task_id']
    this_task = RecruitersTasks.objects.get(id=task_id)
    if this_task.status == False:
        this_task.status = True
    else:
        this_task.status = False
    this_task.save()

    return HttpResponse()

class OpinionDeleteAdmin(View):
    def get(self, request, pk):
        opinion = get_object_or_404(Opinion, pk=pk)
        return render(request, 'recruit/opinion_admin_delete.html',
                          context={'opinion': opinion})

    def post(self, request, pk):
        opinion = Opinion.objects.filter(pk=pk)
        opinion.delete()
        return redirect(reverse('clients_opinions'))


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
            return redirect('clients_opinions')
    return render(request, 'recruit/opinion_answer_admin_create.html',
                  context={'form': form, 'opinion': opinion, "answer": answer})

