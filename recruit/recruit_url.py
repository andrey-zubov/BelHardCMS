from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


from recruit import views
from . import views


urlpatterns = [
    path('', views.recruiter_main_page, name='recruiter_url'),     # There is of recruiter's main page
    path('base_of_clients/', views.base_of_applicants, name='base_of_clients'),
    path('base_of_clients/<id_a>/', views.applicant, name='applicant_url'),
    path('base_of_clients/<id_a>/tasks/', views.applicant_tasks, name='applicant_tasks_url'),
    # path('uploading_files/', views.uploading_files),

    path('chat/', login_required(views.recruit_chat), name='contact_with_clients'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('chat_update/', views.chat_update, name='chat_update'),
    path('check_mes/', views.check_mes, name='check_mes'),
    path('', views.recruit_main_page, name='main_page'),

    path('', views.recruiter_main_page, name='recruiter_url'),     # There is of recruiter's main page
    path('base_of_clients/', views.base_of_applicants, name='base_of_clients'),
    path('base_of_clients/<id_a>/', views.applicant, name='applicant_url'),
    path('base_of_clients/<id_a>/tasks/', views.applicant_tasks, name='applicant_tasks_url'),
    # path('uploading_files/', views.uploading_files),

]