import logging
from collections import defaultdict
from time import perf_counter


# TeamRome
def recruit_edit_page_get(client):
    """ views.py RecruitEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных Recruit. """
    try:
        print("edit_page_get()")
        time_0 = perf_counter()
        response = defaultdict()

        #

        print('\trecruit_edit_page_get() - OK; Time: %s' % (perf_counter() - time_0))
        return response
    except Exception as ex:
        logging.error("Exception in - recruit_edit_page_get()\n %s" % ex)
        return None
