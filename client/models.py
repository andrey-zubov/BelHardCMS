

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
import re

from django.utils import timezone

UserModel = get_user_model()


class Sex(models.Model):
    sex_word = models.CharField(max_length=1)


class Citizenship(models.Model):
    country_word = models.CharField(max_length=100)


class FamilyState(models.Model):
    state_word = models.CharField(max_length=20)


class Children(models.Model):
    children_word = models.CharField(max_length=3)


class City(models.Model):
    city_word = models.CharField(max_length=100)


class Certificate(models.Model):
    img = models.ImageField(blank=True, null=True, verbose_name='certificate_img')  # ?????????????????????
    link = models.URLField(max_length=100, verbose_name='certificate_link',
                           blank=True, null=True)


class EducationWord(models.CharField):
    education_word = models.CharField(max_length=100)


class Education(models.Model):
    education = models.CharField(max_length=100)  # ?????????????????????
    subject_area = models.CharField(max_length=100, verbose_name='Предметная область')
    specialization = models.CharField(max_length=100, verbose_name='Специализация')
    qualification = models.CharField(max_length=100, verbose_name='Квалификация')
    date_start = models.DateField(null=True, blank=True, verbose_name='дата начала')
    date_end = models.DateField(null=True, blank=True, verbose_name='дата окончания')
    certificate = models.ForeignKey(Certificate, null=True, blank=True, on_delete=models.SET_NULL)


class SkillsWord(models.Model):
    skills_word = models.CharField(max_length=100)  # ?????????????????????


class Skills(models.Model):
    skills = models.CharField(max_length=100, blank=True, null=True)  # ?????????????????????


class Sphere(models.Model):
    sphere_word = models.CharField(max_length=100)


class Experience(models.Model):
    name = models.CharField(max_length=100)
    sphere = models.ManyToManyField(Sphere)  # ??? not more 3
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    duties = models.TextField(max_length=3000)


class CvWord(models.Model):
    position_word = models.CharField(max_length=100)  # ?????????????????????


class Employment(models.Model):
    employment = models.CharField(max_length=100)


class TimeJob(models.Model):
    time_job_word = models.CharField(max_length=100)


class TypeSalary(models.Model):
    type_word = models.CharField(max_length=8)


class CV(models.Model):
    position = models.CharField(max_length=100)  # ?????????????????????
    employment = models.ForeignKey(Employment, on_delete=models.SET_NULL, null=True)
    time_job = models.ForeignKey(TimeJob, on_delete=models.SET_NULL, null=True)
    salary = models.CharField(max_length=10, null=True)
    type_salary = models.ForeignKey(TypeSalary, on_delete=models.SET_NULL, null=True)


class State(models.Model):
    state_word = models.CharField(max_length=100)


class Client(models.Model):
    user_client = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Имя')
    lastname = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')

    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True, blank=True)
    date_born = models.DateField(null=True, blank=True)
    citizenship = models.ForeignKey(Citizenship, related_name='citizenship', on_delete=models.SET_NULL,
                                    null=True, blank=True)
    family_state = models.ForeignKey(FamilyState, on_delete=models.SET_NULL, null=True, blank=True)
    children = models.ForeignKey(Children, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Citizenship, related_name='country', on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    street = models.CharField(max_length=100, verbose_name='Улица', null=True, blank=True)
    house = models.CharField(max_length=100, verbose_name='Номер дома', null=True, blank=True)
    flat = models.CharField(max_length=10, verbose_name='Квартира', null=True, blank=True)

    telegram_link = models.CharField(max_length=100, blank=True, null=True,
                                     verbose_name='Ник в телеграмме')  # при верстке учесть @
    email = models.EmailField(max_length=200, null=True, blank=True)
    link_linkedin = models.URLField(max_length=200, null=True, blank=True)
    skype = models.CharField(max_length=100, null=True, blank=True)

    # education fields
    education = models.ForeignKey(Education, on_delete=models.SET_NULL, null=True, blank=True)
    # skills
    skills = models.ForeignKey(Skills, on_delete=models.SET_NULL, null=True, blank=True)
    # exp
    organization = models.ForeignKey(Experience, on_delete=models.SET_NULL, null=True, blank=True)
    # rez
    cv = models.ForeignKey(CV, on_delete=models.SET_NULL, null=True, blank=True)
    # img
    img = models.ImageField(blank=True, null=True)

    # state
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.lastname, self.patronymic)

    def delete(self, *args, **kwargs):
        self.img.delete()
        # add client_CV.pdf
        # add certificate.pdf
        super().delete(*args, **kwargs)


class Telephone(models.Model):
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        pattern = "^[+]{1}[0-9]{1,20}$"
        tel = self.telephone_number
        if re.match(pattern=pattern, string=tel):
            print("phone to save: %s" % tel)
            # super().save(*args, **kwargs)   # TODO uncomment after 'UserLogin' module done!!!
        else:
            print("incorrect phone number")


class Chat(models.Model):
    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    members = models.ManyToManyField(UserModel, verbose_name="Участник")


class Message(models.Model):

    class Meta:
        ordering = ['pub_date']

    chat = models.ForeignKey(Chat, verbose_name="Чат", on_delete=models.CASCADE, )
    author = models.ForeignKey(UserModel, verbose_name="Пользователь", on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Сообщение")
    pub_date = models.DateTimeField(verbose_name='Дата сообщения', default=timezone.now)
    is_readed = models.BooleanField(verbose_name='Прочитано', default=False)



class Opinion(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)

    def get_adres(self):
        return reverse('opinion_detail', kwargs={'pk': self.pk})

    def opinion_delete(self):
        return reverse('opinion_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title[:10]

class Answer(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    opinion = models.OneToOneField(Opinion, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10]

class Tasks(models.Model):
    title = models.CharField(max_length=30, verbose_name='Имя задачи')
    text = models.TextField(null=True, verbose_name='Текст задачи')
    date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    date_end = models.DateField(verbose_name='Дата окончания задачи')
   # sub = models.ForeignKey('Subtasks', on_delete=models.PROTECT, null=True)


class Subtasks(models.Model):
    text = models.CharField(max_length=200, verbose_name='подзадача')
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text


