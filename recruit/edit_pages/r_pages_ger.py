from collections import defaultdict

from client.edit.utility import (time_it, try_except)


# TeamRome
@try_except("recruit_edit_page_get()")
@time_it("recruit_edit_page_get()")
def recruit_edit_page_get(client):
    """ views.py RecruitEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных Recruit. """
    response = defaultdict()

    #

    return response
