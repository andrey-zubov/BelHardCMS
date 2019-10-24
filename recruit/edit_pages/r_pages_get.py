from collections import defaultdict

from client.edit.utility import (time_it, try_except)
from client.models import (Sphere)
from recruit.models import (RecruitExperience)


# TeamRome
@try_except
@time_it
def recruit_edit_page_get(recruit):
    """ views.py RecruitEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных Recruit. """
    response = defaultdict()
    #
    return response


# TeamRome
@try_except
@time_it
def recruit_experience_page_get(recruit):
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
