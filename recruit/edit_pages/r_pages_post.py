from client.edit.parsers import (pars_exp_request, pars_edu_request)
from client.edit.utility import (time_it, try_except)


# TeamRome
from client.models import Experience, Sphere
from recruit.models import RecruitExperience


@try_except
@time_it
def recruit_edit_page_post(recruit_instance, request):
    """ views.py RecruitEditMain(TemplateView) POST method. """
    #
@try_except
@time_it
def experience_page_post(recruit_instance, request):
    """" views.py ClientEditExperience(TemplateView) POST method. """
    arr = pars_exp_request(request.POST)  # list of dictionaries

    if any(arr):
        """ Delete old data for this client. Bug fix for duplicate date save. """
        RecruitExperience.objects.filter(recruit_exp=recruit_instance).delete()
        for dic in arr:
            if any(dic.values()):
                """ If this dictionary hes any values? than take them and save to Exp. instance. """
                organisation = dic['experience_1']
                position = dic['experience_3']
                start_date = dic['exp_date_start']
                end_date = dic['exp_date_end']
                duties = dic['experience_4']

                experiences = RecruitExperience(
                    recruit_exp=recruit_instance,
                    name=organisation,
                    position=position,
                    start_date=start_date,
                    end_date=end_date,
                    duties=duties,
                )
                experiences.save()

                spheres = dic['experience_2']
                for s in spheres:
                    if s:
                        """ Save ManyToManyField 'sphere' """
                        sp = Sphere.objects.get(id=s)
                        sp.save()
                        experiences.sphere.add(sp)


            else:
                print('\tExperience Form is Empty')
    else:
        print('\tExperience Parser is Empty')