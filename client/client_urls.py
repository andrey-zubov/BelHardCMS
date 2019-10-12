from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.client_main_page, name='client'),  # main client page
    path('profile', views.client_profile, name='client_profile'),
    path('edit', views.client_edit_main, name='client_edit'),
    path('edit/skills', views.client_edit_skills, name='client_edit_skills'),
    path('edit/photo', views.client_edit_photo, name='client_edit_photo'),
    path('edit/cv', views.client_edit_cv, name='client_edit_cv'),
    path('edit/education', views.client_edit_education, name='client_edit_education'),
    path('edit/experience', views.client_edit_experience, name='client_edit_experience'),

    path('chat/', login_required(views.MessagesView.as_view()), name='contact_with_centre'),
    path(r'opinion/', opinion_list, name='opinion_list'),
    path(r'opinion/create/', OpinionCreate.as_view(), name='opinion_create'),
    path(r'opinion/<int:pk>/', opinion_detail, name='opinion_detail'),
    path(r'opinion/edit/<int:pk>/', answer_create, name='opinion_answer'),
    path(r'opinion/edit/<int:pk>/delete/', OpinionDelete.as_view(), name='opinion_delete'),
    path('login/', client_login),
    path('logout/', client_logout),
    path('tasks/', tasks, name='tasks_list'),

    # path('edit/form_edu/', views.form_education, name='form_edu'),
    path(r'checktask/', views.checktask),
    path(r'checknotifications/', views.checknotifications),
    path(r'settings/', views.settings_menu, name='settings_menu'),
    path(r'settingsset/', views.set_settings, name='settings_set'),

    # Poland urls
    path('cvs/', ResumesList.as_view(), name='resumes_list_url'),
    path('cv_detail/<id_c>/', ResumeDetail.as_view(), name='resume_detail_url'),
    path('cv/<id_c>/accepted_vacancies/', AcceptedVacancies.as_view(), name='accepted_vacancies_url'),
    path('cv/<id_c>/rejected_vacancies/', RejectedVacancies.as_view(), name='rejected_vacancies_url'),
    path('cv/vacancy/<id_v>/', VacancyDetail.as_view(), name='vacancy_detail_url'),
    path('accept_reject/', views.accept_reject),
    path('help/', help_list, name='help_list_url'),
    path('viewed/', views.viewed),
    path('admin_jobinterviews/', views.admin_jobinterviews),



]
