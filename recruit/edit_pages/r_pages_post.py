from client.edit.parsers import (pars_exp_request, pars_edu_request)
from client.edit.utility import (time_it, try_except)


# TeamRome
@try_except
@time_it
def recruit_edit_page_post(recruit_instance, request):
    """ views.py RecruitEditMain(TemplateView) POST method. """
    #
