from django.contrib.auth.decorators import login_required
from django.urls import path

from recruit.views import (base_of_applicants, CreateJobInterview, applicant, EditJobInterview, DelJobInterview,
                           recruit_chat, get_messages, send_message, chat_update, check_mes, recruit_main_page,
                           add_task, add_new_task, favorites, check_favor, recruit_base, RecruitProfile,
                           RecruitEditMain, RecruitEditExperience, RecruitEditSkills, RecruitEditPhoto,
                           RecruitEditEducation)

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """

urlpatterns = [
    # TeamPoland ##################################################
    # path('', views.recruiter_main_page, name='recruiter_url'),     # There is of recruiter's main page
    # path('base/', views.recruiter_base, name='base_url'),
    path('base_of_clients/', base_of_applicants, name='base_of_clients'),
    path('base_of_clients/<id_a>/', applicant, name='applicant_url'),
    path('base_of_clients/<id_a>/tasks/', CreateJobInterview.as_view(), name='applicant_tasks_url'),
    path('base_of_clients/<id_a>/edit_job_interview/', EditJobInterview.as_view(),
         name='applicant_edit_interviews_url'),
    path('base_of_clients/<id_a>/del_job_interview/', DelJobInterview.as_view(),
         name='applicant_del_interviews_url'),
    # End TeamPoland ###############################################

    path('chat/', login_required(recruit_chat), name='contact_with_clients'),
    path('get_messages/', get_messages, name='get_messages'),
    path('send_message/', send_message, name='send_message'),
    path('chat_update/', chat_update, name='chat_update'),
    path('check_mes/', check_mes, name='check_mes'),

    path('', recruit_main_page, name='main_page'),
    path('add_task', add_task, name='add_task'),
    path(r'add_new_task', add_new_task),
    path(r'favorites/', favorites, name='favorites'),
    path(r'checkfavor/', check_favor, name='check_favor'),
    path('base/', recruit_base, name='recruit_base'),

    # Team Rome (start)
    path('profile/', RecruitProfile.as_view(), name='recruit_profile'),
    path('edit/', RecruitEditMain.as_view(), name='recruit_edit'),
    path('edit/experience/', RecruitEditExperience.as_view(), name='recruit_edit_experience'),
    path('edit/skills/', RecruitEditSkills.as_view(), name='recruit_edit_skills'),
    path('edit/photo/', RecruitEditPhoto.as_view(), name='recruit_edit_photo'),
    path('edit/education/', RecruitEditEducation.as_view(), name='recruit_edit_education'),
    # Team Rome (end)
]
