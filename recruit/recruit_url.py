from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views



urlpatterns = [
    # Poland ##################################################
    path('', views.recruiter_main_page, name='recruiter_url'),     # There is of recruiter's main page
    path('base_of_clients/', views.base_of_applicants, name='base_of_clients'),
    path('base_of_clients/<id_a>/', views.applicant, name='applicant_url'),
    path('base_of_clients/<id_a>/tasks/', views.CreateJobInterview.as_view(), name='applicant_tasks_url'),
    path('test/', views.Test.as_view(), name='test_url'),
    # path('uploading_files/', views.uploading_files),
    # End Poland ###############################################

    path('chat/', login_required(views.recruit_chat), name='contact_with_clients'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('chat_update/', views.chat_update, name='chat_update'),
    path('check_mes/', views.check_mes, name='check_mes'),


]