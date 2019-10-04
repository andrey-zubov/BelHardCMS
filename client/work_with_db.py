import logging
from collections import defaultdict
from time import perf_counter

from BelHardCRM.settings import MEDIA_URL
from client.models import (Client, Sex, Citizenship, FamilyState, Children, City, State, Telephone, Skills, Education,
                           Certificate, CV)
from client.utility import check_if_str


def client_check(user):
    try:
        """ список карточек c id клиента. """
        users_id_list = [i['user_client_id'] for i in Client.objects.all().values()]
        print("client_id_list: %s" % users_id_list)

        """ Current User """
        print("user_name: %s, user_client_id: %s" % (user, user.id))

        if user.id in users_id_list:
            client = Client.objects.get(user_client=user)
            print("user_id: %s" % client.id)
            return client
        else:
            logging.warning('User Profile DO NOT exists')
            return None
    except Exception as ex:
        logging.error('Exception in client_check()\n%s' % ex)
        return None


def load_client_img(client):
    """ Show Client Img in the Navigation Bar.
    Img loaded from DB, if user do not have img - load default. """
    try:
        if client:
            if client.img:
                return "%s%s" % (MEDIA_URL, client.img)
        return '/media/user_1.png'
    except Exception as ex:
        logging.error("Exception in - load_client_img()\n%s" % ex)
        return '/media/user_1.png'


def load_edit_page(client):
    """ TBA """
    try:
        time_0 = perf_counter()
        print("load_edit_page()")
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

        print('TIME load_edit_page(): %s' % (perf_counter() - time_0))
        return response

    except Exception as ex:
        logging.error("Exception in - load_edit_page()\n %s" % ex)
        return None


def load_skills_page(client):
    """ TBA """
    try:
        time_0 = perf_counter()
        print("load_skills_page()")
        response = defaultdict()

        if client:
            skills_arr = [i['skill'] for i in Skills.objects.filter(client_skills=client).values()]
            response['cl_skill'] = skills_arr

        print('TIME load_skills_page(): %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in load_skills_page()\n%s" % ex)
        return None


def load_education_page(client):
    """ TBA """
    try:
        time_0 = perf_counter()
        print("load_education_page()")
        response = defaultdict()
        if client:
            edus = [i for i in Education.objects.filter(client_edu=client).values()]
            response['cl_edu'] = edus

            edu_id = [e['id'] for e in response['cl_edu']]
            certs = [[c for c in Certificate.objects.filter(education_id=i).values()] for i in edu_id]
            # print(certs)

            for e in edus:
                # print("e: %s" % e)
                for c in certs:
                    # print("c: %s" % c)
                    if c[0]['education_id'] == e['id']:
                        e['img'] = "%s%s" % (MEDIA_URL, c[0]['img'])
                        e['link'] = c[0]['link']
            # print("cl_edu: %s" % response['cl_edu'])

        print('TIME load_education_page(): %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in load_education_page()\n%s" % ex)
        return None


def load_cv_edition_page(client):
    try:
        response = defaultdict()
        if client:
            cvs = [i for i in CV.objects.filter(client_cv=client).values()]
            response['cl_cvs'] = cvs
            print("cl_cvs: %s" % response['cl_cvs'])
        return response
    except Exception as ex:
        logging.error("Exception in load_cv_page()\n%s" % ex)
        return None
