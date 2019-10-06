from time import perf_counter

from client.edit.edit_forms import (UploadImgForm, EducationFormSet, CertificateFormSet)
from client.edit.utility import (check_input_str, check_phone, check_home_number, check_telegram)
from client.models import (Skills, Telephone, Sex, Citizenship, FamilyState, Children, City, State, Client)


def edit_page_post(client_instance, request):
    """ TBA """
    time_0 = perf_counter()

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
    if any(tel):
        Telephone.objects.all().delete()
        # print("tel: %s" % tel)
    for t in tel:
        t = check_phone(t)
        if t:
            phone = Telephone(
                client_phone=client,
                telephone_number=t
            )
            phone.save()

    print('edit_page_post() - OK; TIME: %s' % (perf_counter() - time_0))


def skills_page_post(client_instance, request):
    skills_arr = request.POST.getlist('skill') if request.POST.getlist('skill') else None

    if any(skills_arr):
        Skills.objects.all().delete()
        # print("skill: %s" % skills_arr)
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


def photo_page_post(client_instance, request):
    """ в БД сохраняется УНИКАЛЬНОЕ имя картинки (пр: user_2_EntrmQR.png) в папке MEDIA_URL = '/media/' """
    form = UploadImgForm(request.POST, request.FILES)
    if form.is_valid():
        img = form.cleaned_data.get('img')
        client_instance.img = img
        client_instance.save()


def form_edu_post(client_instance, request):
    print("FormEducation.POST: %s" % request.POST)

    form_set_edu = EducationFormSet(request.POST)
    form_set_cert = CertificateFormSet(request.POST, request.FILES)

    edu_inst = None
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
    else:
        print("FormSet_Edu not Valid")

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
