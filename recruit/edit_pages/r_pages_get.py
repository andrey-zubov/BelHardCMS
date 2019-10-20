from collections import defaultdict

from client.edit.utility import (time_it, try_except)


# TeamRome
@try_except
@time_it
def recruit_edit_page_get(client):
    """ views.py RecruitEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных Recruit. """
    response = defaultdict()

    #

    return response
