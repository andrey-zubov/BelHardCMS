import logging
from collections import defaultdict
from time import perf_counter

from BelHardCRM.settings import MEDIA_URL
from client.edit.utility import check_if_str
from client.models import (Sex, Citizenship, FamilyState, Children, City, State, Telephone, Skills, Education,
                           Certificate, CV, Experience, Employment, TimeJob, TypeSalary)


# TeamRome
def edit_page_get(client):
    """ views.py ClientEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных клиента. """
    try:
        print("edit_page_get()")
        time_0 = perf_counter()
        response = defaultdict()

        # default select fields
        response['sex'] = Sex.objects.all()
        response['citizenship'] = Citizenship.objects.all()
        response['family_state'] = reversed(FamilyState.objects.all())
        response['children'] = reversed(Children.objects.all())
        response['country'] = response['citizenship']
        response['city'] = reversed(City.objects.all())
        response['state'] = reversed(State.objects.all())

        #
        if client:
            print(client)
            response['cl_name'] = client.name
            response['cl_last_name'] = client.last_name
            response['cl_patronymic'] = client.patronymic
            response['cl_sex'] = check_if_str(client.sex, '')
            response['cl_date_born'] = check_if_str(client.date_born, '')
            response['cl_citizenship'] = check_if_str(client.citizenship, '')
            response['cl_family_state'] = check_if_str(client.family_state, '')
            response['cl_children'] = check_if_str(client.children, '')
            response['cl_country'] = check_if_str(client.country, '')
            response['cl_city'] = check_if_str(client.city, '')
            response['cl_street'] = check_if_str(client.street, '')
            response['cl_house'] = check_if_str(client.house, '')
            response['cl_flat'] = check_if_str(client.flat, '')
            phone_arr = [i['telephone_number'] for i in Telephone.objects.filter(client_phone=client).values()]
            response['cl_phone'] = phone_arr
            response['cl_telegram'] = check_if_str(client.telegram_link, '@')
            response['cl_email'] = check_if_str(client.email, '')
            response['cl_linkedin'] = check_if_str(client.link_linkedin, '')
            response['cl_skype'] = check_if_str(client.skype, '')
            response['cl_state'] = check_if_str(client.state, '')

        print('TIME edit_page_get(): %s' % (perf_counter() - time_0))
        return response

    except Exception as ex:
        logging.error("Exception in - edit_page_get()\n %s" % ex)
        return None


# TeamRome
def skills_page_get(client):
    """" views.py ClientEditSkills(TemplateView) GET method.  """
    try:
        print("skills_page_get()")
        time_0 = perf_counter()
        response = defaultdict()

        if client:
            skills_arr = [i['skill'] for i in Skills.objects.filter(client_skills=client).values()]
            response['cl_skill'] = skills_arr

        print('TIME skills_page_get(): %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in skills_page_get()\n%s" % ex)
        return None


# TeamRome
def education_page_get(client):
    """" views.py ClientEditEducation(TemplateView) GET method.  """
    try:
        print("education_page_get()")
        time_0 = perf_counter()
        response = defaultdict()
        if client:
            # edus = [i for i in Education.objects.filter(client_edu=client).values()]
            edus = []
            for i in Education.objects.filter(client_edu=client).values():
                edus.append(i)
            response['cl_edu'] = edus
            # edu_id = [e['id'] for e in response['cl_edu']]
            edu_id = []
            for e in response['cl_edu']:
                edu_id.append(e['id'])
            # certs = [[c for c in Certificate.objects.filter(education_id=i).values()] for i in edu_id]
            certs = []
            for i in edu_id:
                certss = []
                for c in Certificate.objects.filter(education_id=i).values():
                    certss.append(c)
                certs.append(certss)

            for e in edus:
                # print("e: %s" % e)
                for c in certs:
                    # print("c: %s" % c)
                    if c[0]['education_id'] == e['id']:
                        e['img'] = "%s%s" % (MEDIA_URL, c[0]['img'])
                        e['link'] = c[0]['link']
                        e['show_img'] = "%s%s" % (MEDIA_URL, c[0]['img'])
            # print("cl_edu: %s" % response['cl_edu'])
        print('TIME education_page_get(): %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in education_page_get()\n%s" % ex)
        return None


# TeamRome
def cv_page_get(client):
    """" views.py ClientEditCv(TemplateView) GET method. """
    try:
        print("cv_page_get()")
        response = defaultdict()

        pass

        return response
    except Exception as ex:
        logging.error("Exception in cv_page_get()\n%s" % ex)
        return None


# TeamRome
def experience_page_get(client):
    """" views.py ClientEditExperience(TemplateView) GET method. """
    try:
        print("experience_page_get()")
        response = defaultdict()
        if client:
            exp = Experience.objects.filter(client_exp=client)
            print("exp: %s" % exp)

            exp_dict = [i for i in exp.values()]
            print("exp_dict: %s" % exp_dict)
            response['cl_exp'] = exp_dict

            for i, e in enumerate(exp):
                print("e: %s" % e)
                # print("e.values(): %s" % e.values())
                sphere = e.sphere.values()
                print("sphere: %s" % sphere)
                exp_dict[i]['sphere'] = sphere
            # sphere = [s.sphere.values() for s in exp]

            print("response: %s" % response)
        return response
    except Exception as ex:
        logging.error("Exception in experience_page_get()\n%s" % ex)
        return None
