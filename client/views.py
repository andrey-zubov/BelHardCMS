from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse
from django.views import View

from .forms import UploadImgForm, AddSkillForm, AddSkillFormSet, OpinionForm, AnswerForm, MessageForm
from .models import *

from django.views.generic import View
from django.contrib import auth


def client_main_page(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'  # test client icon

    return render(request=request,
                  template_name='client/client_main_page.html',
                  context=response)


def client_profile(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    return render(request=request,
                  template_name='client/client_profile.html',
                  context=response)


def client_edit_main(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'
    response['sex'] = Sex.objects.all()  # for a test

    if request.method == 'POST':
        print('client_edit_main - request.POST')

        client = Client(
            name=request.POST['client_first_name'].title(),  # вАленТиН -> Валентин
            lastname=request.POST['client_last_name'].title(),
            patronymic=request.POST['client_middle_name'].title(),
            sex=Sex(sex_word=request.POST['sex']),  # .save()
            date_born=request.POST['date_born'],  # mast be NOT ''
            citizenship=Citizenship(country_word=request.POST['citizenship']),  # .save()
            family_state=FamilyState(state_word=request.POST['family_state']),  # .save()
            children=Children(children_word=request.POST['children']),  # .save()
            country=Citizenship(country_word=request.POST['country']),  # .save()
            city=City(city_word=request.POST['city']),  # .save()
            street=request.POST['street'],
            house=request.POST['house'],
            flat=request.POST['flat'],
            telegram_link=request.POST['telegram_link'],
            skype=request.POST['skype_id'],
            email=request.POST['email'],
            link_linkedin=request.POST['link_linkedin'],
            state=State(state_word=request.POST['state']),  # .save()
        )
        # client.save()  # TODO uncomment after 'UserLogin' module done!!!

        tel = request.POST.getlist('phone')
        for t in tel:
            Telephone(telephone_number=t).save()

        print(
            request.POST['client_first_name'].title(),
            request.POST['client_last_name'].title(),
            request.POST['client_middle_name'].title(),
            request.POST['sex'],
            request.POST['date_born'],
            request.POST['citizenship'],
            request.POST['family_state'],
            request.POST['children'],
            request.POST['country'],
            request.POST['city'],
            request.POST['street'],
            request.POST['house'],
            request.POST['flat'],
            request.POST.getlist('phone'),
            request.POST['telegram_link'],
            request.POST['skype_id'],
            request.POST['email'],
            request.POST['link_linkedin'],
            request.POST['state'],
        )

        print('client_edit_main - OK')

        return redirect(to='/client/profile')
    else:
        print('client_edit_main - request.GET')

    return render(request=request,
                  template_name='client/client_edit_main.html',
                  context=response)


def client_edit_skills(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'
    myformset = AddSkillFormSet()

    if request.method == 'POST':
        print("client_edit_skills - request.POST")

        skills_arr = request.POST.getlist('skill')
        print("skill: %s" % skills_arr)

        if any(skills_arr):
            for s in skills_arr:
                skill = Client(skills=Skills(skills=s))  # Skill().save())
                # skill.save()  # TODO uncomment after 'UserLogin' module done!!!
        else:
            print('No skills')

        # -------- test code ---------------------------
        form = AddSkillForm(request.POST)
        response['form'] = form
        if form.is_valid():
            print('skill form.is_valid()')
            # form.save()
            # return redirect(to='/client/edit')

        # -------- Работающий test code с FormSet !!! ---------------------------
        form_set = AddSkillFormSet(request.POST)
        if form_set.is_valid():
            print('set is valid - OK')
            for f in form_set:
                # extract name='skill' from each form and save
                skill = f.cleaned_data.get('skills')
                if skill:
                    print('skill from form_set: %s' % skill)
                    # Skills(skills=skill).save()  # TODO uncomment after 'UserLogin' module done!!!

        return redirect(to='/client/edit')
    else:
        print('client_edit_skills - request.GET')
        response['myformset'] = myformset
        response['form'] = AddSkillForm

    return render(request=request,
                  template_name='client/client_edit_skills.html',
                  context=response)


def client_edit_photo(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print('client_edit_photo - request.POST')

        form = UploadImgForm(request.POST, request.FILES)
        response['form'] = form

        if form.is_valid():
            # form.save()  # TODO uncomment after 'UserLogin' module done!!!
            print('client save photo - OK')
            return redirect(to='/client/edit')
    else:
        print('client_edit_photo - request.GET')
        response['form'] = UploadImgForm()

    return render(request=request,
                  template_name='client/client_edit_photo.html',
                  context=response)


def client_edit_cv(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        cv = CV(
            position=request.POST['position'],
            time_job=TimeJob(time_job_word=request.POST['time_job']),  # .save(),
            salary=request.POST['salary'],
            type_salary=TypeSalary(type_word=request.POST['type_salary']),  # .save(),
        )
        # cv.save()  # TODO uncomment after 'UserLogin' module done!!!
        print(
            request.POST['position'],
            request.POST['time_job'],
            request.POST['salary'],
            request.POST['type_salary']
        )

        return redirect(to='/client/edit')

    return render(request, 'client/client_edit_cv.html', response)


def client_edit_education(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print("save_client_education - request.POST")

        education = Education(
            education=request.POST['education'],
            subject_area=request.POST['subject_area'],
            specialization=request.POST['specialization'],
            qualification=request.POST['qualification'],
            date_start=request.POST['date_start'],  # mast be NOT ''
            date_end=request.POST['date_end'],  # mast be NOT ''
            certificate=Certificate(
                img=request.POST['certificate_img'],
                link=request.POST['certificate_url']
            ),  # .save(),
        )
        # education.save()  # TODO uncomment after 'UserLogin' module done!!!

        print(
            request.POST['education'],
            request.POST['subject_area'],
            request.POST['specialization'],
            request.POST['qualification'],
            request.POST['date_start'],
            request.POST['date_end'],
            request.POST['certificate_img'],
            request.POST['certificate_url'],
        )

        return redirect('/client/edit')
    else:
        print('client_edit_education - request.GET')

    return render(request, 'client/client_edit_education.html', response)


def client_edit_experience(request):
    response = csrf(request)
    response['client_img'] = '/media/user_1.png'

    if request.method == 'POST':
        print("save_client_edit_experience - request POST")

        experiences = Experience(
            name=request.POST['experience_1'],
            # TODO Error:
            #  Direct assignment to the forward side of a many-to-many set is prohibited. Use sphere.set() instead.
            # sphere=Sphere(sphere_word=request.POST.getlist('experience_2')),
            position=request.POST['experience_3'],
            start_date=request.POST['exp_date_start'],
            end_date=request.POST['exp_date_end'],
            duties=request.POST['experience_4'],
        )
        # experiences.save()  # TODO uncomment after 'UserLogin' module done!!!
        print(
            request.POST['experience_1'],
            request.POST.getlist('experience_2'),
            request.POST['experience_3'],
            request.POST['exp_date_start'],
            request.POST['exp_date_end'],
            request.POST['experience_4'],
        )

        return redirect('/client/edit')

    return render(request, 'client/client_edit_experience.html', response)

class MessagesView(View):
    def get(self, request):
        try:
            chat = Chat.objects.get(members=request.user)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'client/client_chat.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

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
    return render(request, 'opinion/index.html', context={'opinion' : opinion})

def answer_create(request, pk):
    opinion = get_object_or_404(Opinion, id=pk)
    answer = Answer.objects.filter(pk = pk)
    form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.opinion = opinion
            form.user = request.user
            form.save()
            return redirect('opinion_detail', pk)
    return render(request, 'opinion/answer_create.html', context={'form':form, 'opinion':opinion, "answer" : answer})

class OpinionCreate(View):
    def get(self, request):
        form = OpinionForm()
        return render(request,'opinion/opinion_create.html', context={'form':form})

    def post(self, request):
        form = OpinionForm(request.POST)

        if form.is_valid():
            new_opinion = form.save(commit=False)
            new_opinion.user = request.user
            new_opinion.save()
            return redirect('opinion_detail', pk = new_opinion.pk)
        return render(request, 'opinion/opinion_create.html', context={'form' : form})

def opinion_detail(request, pk):
    opinion = get_object_or_404(Opinion, pk=pk)
    return render(request, 'opinion/opinion_detail.html', {'opinion': opinion})


class OpinionDelete(View):
    def get(self, request, pk):
        opinion = Opinion.objects.filter(pk = pk)
        return render(request, 'opinion/opinion_delete.html', context={'opinion' : opinion})

    def post(self, request, pk):
        opinion = Opinion.objects.filter(pk = pk)
        opinion.delete()
        return redirect(reverse('opinion_list'))



def client_login(request):      #ввести логин/пароль -> зайти в систему
    res = csrf(request)
    res['url'] = 'login'
    if request.POST:
        password = request.POST['password']
        user = request.POST['user']
        u = auth.authenticate(username=user, password=password)
        if u:
            auth.login(request, u)
            return redirect('/')               #переадресация после авторизации
        else:
            res['error'] = "Неверный login/пароль"
            return render(request, 'registration.html', res)
    else:
        return render(request, 'registration.html', res)


def client_logout(request):     #выйти из системы, возврат на стартовую страницу
    auth.logout(request)
    return redirect('/')      #вставить редирект куда требуется


def tasks(request):
    task = Tasks.objects.filter(user=request.user, status=True)
    task_false = Tasks.objects.filter(user=request.user, status=False) #status=False)
    print(task[0].show_all[0].title)


    return render(request, 'client/tasks.html', context = {'task' : task,  'task_false': task_false})



