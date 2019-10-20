from BelHardCRM.settings import MEDIA_URL
from client.edit.log_color import (log_info, log_error)
from client.edit.utility import try_except, time_it
from client.models import Client


# TeamRome
@try_except
@time_it
def client_check(user):
    """ список карточек c id клиента. """
    users_id_list = [i['user_client_id'] for i in Client.objects.all().values()]
    log_info("\tclient_id_list: %s" % users_id_list)
    """ Current User """
    log_info("\tuser_name: %s, user_client_id: %s" % (user, user.id))
    if user.id in users_id_list:
        client = Client.objects.get(user_client=user)
        log_info("\tuser_id: %s" % client.id)
        return client
    else:
        log_error('\tUser Profile DO NOT exists')
        return None


# TeamRome
@try_except
def load_client_img(client):
    """ Show Client Img in the Navigation Bar.
    Img loaded from DB, if user do not have img - load default. """
    if client:
        if client.img:
            return "%s%s" % (MEDIA_URL, client.img)
    return '/media/user_1.png'
