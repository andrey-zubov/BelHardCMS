import logging

from BelHardCRM.settings import MEDIA_URL
from client.edit.utility import try_except
from client.models import Client


@try_except
def client_check(user):
    """ список карточек c id клиента. """
    users_id_list = [i['user_client_id'] for i in Client.objects.all().values()]
    print("client_id_list: %s" % users_id_list)
    """ Current User """
    print("user_name: %s, user_client_id: %s" % (user, user.id))
    if user.id in users_id_list:
        client = Client.objects.get(user_client=user)
        print("user_id: %s" % client.id)
        return client
    else:
        logging.warning('User Profile DO NOT exists')
        return None


@try_except
def load_client_img(client):
    """ Show Client Img in the Navigation Bar.
    Img loaded from DB, if user do not have img - load default. """
    if client:
        if client.img:
            return "%s%s" % (MEDIA_URL, client.img)
    return '/media/user_1.png'
