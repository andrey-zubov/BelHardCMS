from django.contrib.auth import get_user_model
from django.db import models

from client.models import (Citizenship, Sex, FamilyState, Children, City, State, Sphere)

UserModel = get_user_model()


# TeamRome
class Recruit(models.Model):
    user_recruit = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True, blank=True)
    date_born = models.DateField(null=True, blank=True)
    r_citizenship = models.ForeignKey(Citizenship, related_name='r_citizenship', on_delete=models.SET_NULL,
                                      null=True, blank=True)
    family_state = models.ForeignKey(FamilyState, on_delete=models.SET_NULL, null=True, blank=True)
    children = models.ForeignKey(Children, on_delete=models.SET_NULL, null=True, blank=True)
    r_country = models.ForeignKey(Citizenship, related_name='r_country', on_delete=models.SET_NULL, blank=True,
                                  null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    street = models.CharField(max_length=100, verbose_name='Улица', null=True, blank=True)
    house = models.CharField(max_length=100, verbose_name='Номер дома', null=True, blank=True)
    flat = models.CharField(max_length=10, verbose_name='Квартира', null=True, blank=True)
    telegram_link = models.CharField(max_length=100, blank=True, null=True,
                                     verbose_name='Ник в телеграмме')  # при верстке учесть @
    link_linkedin = models.URLField(max_length=200, null=True, blank=True)
    skype = models.CharField(max_length=100, null=True, blank=True)
    img = models.ImageField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)


# TeamRome
class RecruitExperience(models.Model):
    """ Опыт работы. ForeignKey = несколько видов опыта работы у одного recruit. """
    recruit_exp = models.ForeignKey(to='Recruit', on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='organisation')
    sphere = models.ManyToManyField(Sphere, verbose_name='sphere')  # ??? not more 3
    position = models.CharField(max_length=100, null=True, blank=True, verbose_name='position')
    start_date = models.DateField(null=True, blank=True, verbose_name='start_date')
    end_date = models.DateField(null=True, blank=True, verbose_name='end_date')
    duties = models.TextField(max_length=3000, null=True, blank=True, verbose_name='duties')


# TeamRome
class RecruitEducation(models.Model):
    """ Образование / Курсы / Университеты / Коледжы.
        ForeignKey = несколько образований у одного recruit."""
    recruit_edu = models.ForeignKey(to='Recruit', on_delete=models.CASCADE)

    institution = models.CharField(max_length=100, null=True, blank=True, verbose_name='institution')
    subject_area = models.CharField(max_length=100, null=True, blank=True, verbose_name='Предметная область')
    specialization = models.CharField(max_length=100, null=True, blank=True, verbose_name='Специализация')
    qualification = models.CharField(max_length=100, null=True, blank=True, verbose_name='Квалификация')
    date_start = models.DateField(null=True, blank=True, verbose_name='дата начала')
    date_end = models.DateField(null=True, blank=True, verbose_name='дата окончания')


class RecruitSkills(models.Model):
    """ Навыки. ForeignKey = несколько навыков у одного recruit. """
    recruit_skills = models.ForeignKey(to='Recruit', on_delete=models.CASCADE)

    skill = models.CharField(max_length=100, blank=True, null=True)


