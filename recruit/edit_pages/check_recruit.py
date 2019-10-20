import logging

from client.edit.utility import try_except
from recruit.models import (Recruit)


@try_except
def recruit_check(user):
    """ список карточек c id recruit. """
    users_id_list = [i['user_recruit_id'] for i in Recruit.objects.all().values()]
    print("recruit_id_list: %s" % users_id_list)
    """ Current Recruit """
    print("recruit_name: %s, user_recruit_id: %s" % (user, user.id))
    if user.id in users_id_list:
        recruit = Recruit.objects.get(user_recruit=user)
        print("recruit_id: %s" % recruit.id)
        return recruit
    else:
        logging.warning('User Profile DO NOT exists')
        return None
