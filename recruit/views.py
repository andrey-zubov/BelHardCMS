from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from client.models import Chat, Message, Tasks, UserModel, SubTasks
from datetime import datetime

def recruit_main_page(request):
    return render(request, template_name='recruit/recruit_main_template.html')

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
    mes.save()
    send = {'author_id': mes.author.id, 'author_name': mes.author.username, 'message': mes.message, 'message_id': mes.id,
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


def add_task(request):
    context = {}
    context['users_list'] = UserModel.objects.all()
    #context['newtask'] = newtask
    return render(request=request, template_name='recruit/add_task.html', context=context)


def add_new_task(requset):
    try:
        user = UserModel.objects.get(username=requset.POST['name'])
    except UserModel.DoesNotExist: #TODO сделать проверку в отправек формы?
        return HttpResponse('Необходимо задать юзера')
    newtask = Tasks.objects.create()
    newtask.user = user
    newtask.title = requset.POST['task_title']
    newtask.comment = str(requset.POST['task_comment'])
    #newtask.time = datetime.now()
    newtask.save()
    newsubtask = SubTasks(title=requset.POST['task_subtask'], task=newtask) #TODO расширить список подзадач
    newsubtask.save()

    return redirect(to='add_task')