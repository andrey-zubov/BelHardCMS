from client.edit.log_color import (log_info, log_error)
from client.edit.utility import try_except, time_it
from recruit.models import (Recruit)


# TeamRome
@try_except
@time_it
def recruit_check(user):
    """ список карточек c id recruit. """
    users_id_list = [i['user_recruit_id'] for i in Recruit.objects.all().values()]
    log_info("\trecruit_id_list: %s" % users_id_list)
    """ Current Recruit """
    log_info("\trecruit_name: %s, user_recruit_id: %s" % (user, user.id))
    if user.id in users_id_list:
        recruit = Recruit.objects.get(user_recruit=user)
        log_info("\trecruit_id: %s" % recruit.id)
        return recruit
    else:
        log_error('\tUser Profile DO NOT exists')
        return None



def load_recruit_img(recruit):

    if recruit:
        if recruit.img:
            return "%s%s" % (MEDIA_URL, recruit.img)
    return '/media/user_1.png'