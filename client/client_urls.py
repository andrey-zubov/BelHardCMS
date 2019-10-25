from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .edit.load_data_list import (SkillsDataList, InstitutionDataList, CvPositionDataList)
from .views import *


urlpatterns = [
    path('', views.client_main_page, name='client'),  # main client page
    path('profile', views.client_profile, name='client_profile'),

    # Team Rome (start) - Edit Forms URLs
    path('edit/', views.ClientEditMain.as_view(), name='client_edit'),
    path('edit/skills/', views.ClientEditSkills.as_view(), name='client_edit_skills'),
    path('edit/photo/', views.ClientEditPhoto.as_view(), name='client_edit_photo'),
    path('edit/cv/', views.ClientEditCv.as_view(), name='client_edit_cv'),
    path('edit/education/', views.ClientEditEducation.as_view(), name='client_edit_education'),
    path('edit/experience/', views.ClientEditExperience.as_view(), name='client_edit_experience'),
    path('edit/form_edu/', views.FormEducation.as_view(), name='form_edu'),
    path('edit/skills_data_list/', SkillsDataList.as_view(), name='skills_data_list'),
    path('edit/institution_data_list/', InstitutionDataList.as_view(), name='institution_data_list'),
    path('edit/cv_position_data_list/', CvPositionDataList.as_view(), name='cv_position_data_list'),
    # Team Rome (end)

    path('chat/', login_required(views.MessagesView.as_view()), name='contact_with_centre'),
    path(r'opinion/', opinion_list, name='opinion_list'),
    path(r'opinion/create/', OpinionCreate.as_view(), name='opinion_create'),
    path(r'opinion/<int:pk>/', opinion_detail, name='opinion_detail'),
    path(r'opinion/edit/<int:pk>/', answer_create, name='opinion_answer'),
    path(r'opinion/edit/<int:pk>/delete/', OpinionDelete.as_view(), name='opinion_delete'),
    path('login/', client_login, name='login'),
    path('logout/', client_logout, name='logout'),
    path('tasks/', tasks, name='tasks_list'),

    # path('edit/form_edu/', views.form_education, name='form_edu'),
    path(r'checktask/', views.checktask),
    path(r'checknotifications/', views.checknotifications),
    path(r'settings/', views.settings_menu, name='settings_menu'),
    path(r'settingsset/', views.set_settings, name='settings_set'),

    # Poland urls (start)
    path('cvs/', ResumesList.as_view(), name='resumes_list_url'),
    path('cv_detail/<id_c>/', ResumeDetail.as_view(), name='resume_detail_url'),
    path('cv/<id_c>/accepted_vacancies/', AcceptedVacancies.as_view(), name='accepted_vacancies_url'),
    path('cv/<id_c>/rejected_vacancies/', RejectedVacancies.as_view(), name='rejected_vacancies_url'),
    path('cv/vacancy/<id_v>/', VacancyDetail.as_view(), name='vacancy_detail_url'),
    path('accept_reject/', accept_reject),
    path('help/', help_list, name='help_list_url'),
    path('viewed/', viewed),
    path('admin_jobinterviews/', admin_jobinterviews),
    path('interviews/', interviews_list, name='interviews_list_url'),
    path(r'checkinterviews/', views.checkinterviews),
    path('upload', views.upload, name='client_cv_upload'),
    path('upload', views.upload, name='upload'),

    # # Poland urls (end)




]
