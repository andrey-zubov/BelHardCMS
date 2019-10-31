from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views




urlpatterns = [
    # TeamPoland ##################################################
    path('', views.recruiter_main_page, name='recruiter_url'),     # There is of recruiter's main page
    path('base/', views.recruiter_base, name='base_url'),
    path('base/base_of_clients/', views.base_of_applicants, name='base_of_clients'),
    path('base/base_of_clients/<id_a>/', views.ApplicantDet.as_view(), name='applicant_url'),
    path('base/base_of_clients/<id_a>/tasks/', views.CreateJobInterview.as_view(), name='applicant_tasks_url'),
    path('base/base_of_clients/<id_a>/edit_job_interview/', views.EditJobInterview.as_view(), name='applicant_edit_interviews_url'),
    path('base/base_of_clients/<id_a>/del_job_interview/', views.DelJobInterview.as_view(), name='applicant_del_interviews_url'),

    path('base/vacancies/', views.Vacancies.as_view(), name='vacancies_url'),
    path('base/vacancies/<id_v>/', views.VacancyDet.as_view(), name='vacancy_recr_url'),
    path('base/vacancies/<id_v>/del_vacancy/', views.DelVacancy.as_view(), name='vacancy_del_recr_url'),
    # End TeamPoland ###############################################

    path('chat/', login_required(views.recruit_chat), name='contact_with_clients'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('chat_update/', views.chat_update, name='chat_update'),
    path('check_mes/', views.check_mes, name='check_mes'),

    #path('', views.recruit_main_page, name='main_page'),
    path('add_task', views.add_task, name='add_task'),
    path(r'add_new_task',views.add_new_task),
    path(r'favorites/', views.favorites, name='favorites'),
    path(r'checkfavor/', views.check_favor, name='check_favor'),
    path('base1/', views.recruit_base, name='recruit_base'),
    path(r'client_filtration/', views.client_filtration, name='client_filtration'),

]