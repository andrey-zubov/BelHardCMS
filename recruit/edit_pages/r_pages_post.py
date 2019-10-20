from time import perf_counter

from client.edit.parsers import (pars_exp_request, pars_edu_request)


# TeamRome
def recruit_edit_page_post(recruit_instance, request):
    """ views.py RecruitEditMain(TemplateView) POST method. """
    print("recruit_edit_page_post()")
    time_0 = perf_counter()

    #
    arr_edu = pars_edu_request(request.POST, request.FILES)  # list of dictionaries
    arr_exp = pars_exp_request(request.POST)  # list of dictionaries

    print('\trecruit_edit_page_post() - OK; TIME: %s' % (perf_counter() - time_0))
