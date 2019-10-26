from collections import defaultdict

from client.edit.utility import (time_it, try_except)
from client.models import (Sphere, Sex, Citizenship, FamilyState, Children, City, State)
from recruit.models import (RecruitExperience, UserModel, RecruitTelephone)


@try_except
@time_it
def recruit_edit_page_get(recruit):  # TeamRome
    """ views.py RecruitEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных Recruit. """
    response = defaultdict()
    # default select fields
    response['sex'] = Sex.objects.all()
    response['citizenship'] = Citizenship.objects.all()
    response['family_state'] = reversed(FamilyState.objects.all())
    response['children'] = reversed(Children.objects.all())
    response['country'] = response['citizenship']
    response['city'] = reversed(City.objects.all())
    response['state'] = reversed(State.objects.all())

    if recruit:
        user_model = UserModel.objects.get(id=recruit.user_recruit_id)
        response['user_model'] = {
            "first_name": user_model.first_name,
            "last_name": user_model.last_name,
            "email": user_model.email,
        }
        phone_arr = [i.telephone_number for i in RecruitTelephone.objects.filter(recruit_phone=recruit)]
        response['recruit_phone'] = phone_arr
        response['recruit'] = recruit

    return response


@try_except
@time_it
def recruit_experience_page_get(recruit):  # TeamRome
    response = defaultdict()
    response['sphere'] = Sphere.objects.all()
    if recruit:
        exp = RecruitExperience.objects.filter(recruit_exp=recruit)
        exp_dict = [i for i in exp.values()]
        response['rec_exp'] = exp_dict

        for i, e in enumerate(exp):
            sphere = [i['sphere_word'] for i in e.sphere.values()]
            exp_dict[i]['sphere'] = sphere

    return response



def experience_page_get(recruit):

    response = defaultdict()
    response['sphere'] = RecruitEducation.objects.filter(recruit_exp=recruit)
    if recruit:
        exp = RecruitExperience.objects.filter(recruit_exp=recruit)
        exp_dict = [i for i in exp.values()]
        response['rec_exp'] = exp_dict

        for i, e in enumerate(exp):
            sphere = [i['sphere_word'] for i in e.sphere.values()]
            exp_dict[i]['sphere'] = sphere

    return response


