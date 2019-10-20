from time import perf_counter


# TeamRome
def recruit_edit_page_post(recruit_instance, request):
    """ views.py RecruitEditMain(TemplateView) POST method. """
    print("recruit_edit_page_post()")
    time_0 = perf_counter()

    #

    print('\trecruit_edit_page_post() - OK; TIME: %s' % (perf_counter() - time_0))
