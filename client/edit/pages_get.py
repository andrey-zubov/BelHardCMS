import calendar
from collections import defaultdict

from datetime import datetime, timedelta
from datetime import date



from BelHardCRM.settings import MEDIA_URL
from client.edit.utility import (time_it, try_except)
from client.models import (Sex, Citizenship, FamilyState, Children, City, State, Telephone, Skills, Education,
                           Certificate, CV, Experience, Employment, TimeJob, TypeSalary, UserModel, Sphere, Direction)


@try_except
@time_it
def edit_page_get(client):  # TeamRome
    """ views.py ClientEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных клиента. """
    response = defaultdict()
    # default select fields
    response['sex'] = Sex.objects.all()
    response['citizenship'] = Citizenship.objects.all()
    response['family_state'] = reversed(FamilyState.objects.all())
    response['children'] = reversed(Children.objects.all())
    response['country'] = response['citizenship']
    response['city'] = reversed(City.objects.all())
    response['state'] = reversed(State.objects.all())

    if client:
        user_model = UserModel.objects.get(id=client.user_client_id)
        response['user_model'] = {
            "first_name": user_model.first_name,
            "last_name": user_model.last_name,
            "email": user_model.email,
        }
        phone_arr = [i['telephone_number'] for i in Telephone.objects.filter(client_phone=client).values()]
        response['cl_phone'] = phone_arr
        response['client'] = client

    return response


@try_except
@time_it
def skills_page_get(client):  # TeamRome
    """" views.py ClientEditSkills(TemplateView) GET method.  """
    response = defaultdict()
    if client:
        skills_arr = [i.skill for i in Skills.objects.filter(client_skills=client)]
        response['cl_skill'] = skills_arr

    return response


@try_except
@time_it
def education_page_get(client):  # TeamRome
    """" views.py ClientEditEducation(TemplateView) GET method.  """
    response = defaultdict()
    if client:
        edus = [i for i in Education.objects.filter(client_edu=client).values()]
        response['cl_edu'] = edus
        edu_id = [e['id'] for e in response['cl_edu']]
        certs = [[c for c in Certificate.objects.filter(education_id=i).values()] for i in edu_id]
        # print("\tcerts: %s" % certs)
        for e in edus:
            # print("\te: %s" % e)
            for c in certs:
                # print("\tc: %s" % c)
                if c:
                    if c[0]['education_id'] == e['id']:
                        for cert in c:
                            cert['img'] = "%s%s" % (MEDIA_URL, cert['img'])
                        e['cert'] = c
        # print("\tcl_edu: %s" % response['cl_edu'])
    return response


@try_except
@time_it
def cv_page_get(client):  # TeamRome
    """" views.py ClientEditCv(TemplateView) GET method. """
    response = defaultdict()
    # default select fields
    response['employment'] = Employment.objects.all()
    response['time_job'] = TimeJob.objects.all()
    response['type_salary'] = TypeSalary.objects.all()
    response['direction'] = Direction.objects.all()

    if client:
        cvs = CV.objects.filter(client_cv=client)
        cvs_val = [i for i in cvs.values()]
        response['cl_cvs'] = cvs_val

        for c in cvs_val:
            # add more keys to response['cl_cvs'] dictionary
            c['cl_employment'] = Employment.objects.get(id=c['employment_id']).employment
            c['cl_time_job'] = TimeJob.objects.get(id=c['time_job_id']).time_job_word
            c['cl_type_salary'] = TypeSalary.objects.get(id=c['type_salary_id']).type_word
            c['cl_direction'] = Direction.objects.get(id=c['direction_id']).direction_word

    return response


@try_except
@time_it
def experience_page_get(client):  # TeamRome
    """" views.py ClientEditExperience(TemplateView) GET method. """
    response = defaultdict()
    response['sphere'] = Sphere.objects.all()
    if client:
        exp = Experience.objects.filter(client_exp=client)
        exp_dict = [i for i in exp.values()]
        response['cl_exp'] = exp_dict

        for i, e in enumerate(exp):
            sphere = [i['sphere_word'] for i in e.sphere.values()]
            exp_dict[i]['sphere'] = sphere

    return response


@try_except
@time_it
def show_profile(client):  # TeamRome
    response = defaultdict()

    if client:
        edus = [i for i in Education.objects.filter(client_edu=client).values('institution', 'qualification')]
        response['cl_edu_profile'] = edus
        exp = [i for i in
               Experience.objects.filter(client_exp=client).values('start_date', 'end_date', 'position', 'name')]
        response['cl_exp_profile'] = exp
        cvs = [i for i in CV.objects.filter(client_cv=client).values('position')]
        response['cl_cvs_profile'] = cvs
        skills_arr = [i for i in Skills.objects.filter(client_skills=client).values('skill')]
        response['cl_skill_profile'] = skills_arr

        user_model = UserModel.objects.get(id=client.user_client_id)

        response['user_model'] = {
            "first_name": user_model.first_name,
            "last_name": user_model.last_name,
            "email": user_model.email,

        }
        phone_arr = [i for i in Telephone.objects.filter(client_phone=client).values("telephone_number")]
        response['cl_phone'] = phone_arr
        # response["client"] = Client.objects.filter(user_client=client)
        response["client"] = client

        now = datetime.now().strftime("%d.%m.%Y")
        date_format = "%d.%m.%Y"
        d1 = datetime.strptime(now, date_format)
        data_b = client.date_born
        # print(data_b, type(data_b))

        age = None
        if data_b:
            #dt_now = datetime.date.today()
            dt_now = datetime.date(d1)
            ly = calendar.leapdays(data_b.year, dt_now.year)
            age = int(((dt_now - data_b).days - ly) / 365)
        response["age"] = age
        goda = [2, 3, 4]
        a = str(age)[1]

        if int(a) == 1:
            k = 'год'
        elif int(a) in goda:
            k = 'года'
        else:
            k = "лет"
        response["nameage"] = k

        print(a, k, response["nameage"])

        c = str(client.children)
        if len(c) == 4:
            g = 'дети'
        else:
            g = 'детей'
        response["namechild"] = g

        print(c, g)





    return response
