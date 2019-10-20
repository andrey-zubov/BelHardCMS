from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from client.edit.check_clients import (load_client_img)
from client.models import (Chat, Message, Settings)
from recruit.edit_pages.check_recruit import (recruit_check)
from recruit.edit_pages.r_forms import (RecruitUploadImgForm)
from recruit.edit_pages.r_pages_get import (recruit_edit_page_get)
from recruit.edit_pages.r_pages_post import (recruit_edit_page_post)


def recruit_main_page(request):
    recruit_instance = recruit_check(request.user)
    response = {'recruit_img': load_client_img(recruit_instance),
                'data': 'foo()',
                }
    return render(request, template_name='recruit/recruit_main_template.html', context=response)


def recruit_profile(request):
    recruit_instance = recruit_check(request.user)
    response = {'recruit_img': load_client_img(recruit_instance),
                'data': 'foo()',
                }
    return render(request=request, template_name='recruit/recruit_profile.html', context=response)


def recruit_chat(request):
    chat_list = Chat.objects.filter(members=request.user)
    for chat in chat_list:
        mes = chat.members.all()
        for m in mes:
            print(m.username)
    context = {'user': request.user, 'chats': chat_list}
    return render(request=request, template_name='recruit/recruit_chat.html', context=context)


def get_messages(request):
    chat_id = (request.GET['chat_id'])
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in messages:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def send_message(request):
    chat = Chat.objects.get(id=request.GET['chat_id'])
    mes = Message(chat=chat, author=request.user, message=request.GET['message'])
    members = chat.members.all()
    mes.save()

    for m in members:
        if m != request.user:
            try:
                if Settings.objects.get(user=m).email_messages:
                    send_email = EmailMessage('HR-system', 'У вас новое сообщение', to=[str(m.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')

    send = {'author_id': mes.author.id, 'author_name': mes.author.username, 'message': mes.message,
            'message_id': mes.id,
            'pub_date': mes.pub_date.ctime()}
    return JsonResponse(send, safe=False)


def chat_update(request):
    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(id=request.GET['chat_id'])
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def check_mes(request):
    chat = Chat.objects.filter(members=request.user)
    send = []
    for c in chat:
        unread_messages = len(Message.objects.filter(chat=c, is_read=False).exclude(author=request.user))
        new_dict = {'chat_id': c.id, 'count': unread_messages}
        send.append(new_dict)

    return JsonResponse(send, safe=False)


# TeamRome
class RecruitEditMain(TemplateView):
    template_name = 'recruit/edit_pages/recruit_edit_main.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_edit_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_edit_page_post(recruit_instance, request)
        return redirect(to='/recruit/profile/')


# TeamRome
class RecruitEditExperience(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    "data": 'foo()',
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        'foo()'
        return redirect(to='/recruit/edit/')


# TeamRome
class RecruitEditEducation(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': 'foo()',
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        'foo()'
        return redirect(to='/recruit/edit/')


# TeamRome
class RecruitEditSkills(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': 'foo()',
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        'foo()'
        return redirect(to='/recruit/edit/')


# TeamRome
class RecruitEditPhoto(TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'form': RecruitUploadImgForm(),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        'foo()'
        return redirect(to='/recruit/edit/')
