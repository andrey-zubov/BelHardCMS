from client.edit.parsers import (pars_exp_request, pars_edu_request)
from client.edit.utility import (time_it, try_except)


# TeamRome
@try_except("recruit_edit_page_post()")
@time_it("recruit_edit_page_post()")
def recruit_edit_page_post(recruit_instance, request):
    """ views.py RecruitEditMain(TemplateView) POST method. """
    #
    arr_edu = pars_edu_request(request.POST, request.FILES)  # list of dictionaries
    arr_exp = pars_exp_request(request.POST)  # list of dictionaries
