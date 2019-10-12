from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
import re
from django.utils import timezone

UserModel = get_user_model()


class Sex(models.Model):
    """ Пол. Заполняется Админом. """
    sex_word = models.CharField(max_length=1)

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.sex_word


class Citizenship(models.Model):
    """ Список стран СНГ. Заполняется Админом. """
    country_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Страна / Гражданство'
        verbose_name_plural = 'Страна / Гражданство'

    def __str__(self):
        return self.country_word


class FamilyState(models.Model):
    """ Семейное положение клиента. Заполняется Админом. """
    state_word = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Семейное положение'
        verbose_name_plural = 'Семейное положение'

    def __str__(self):
        return self.state_word


class Children(models.Model):
    """ Дети клиента. Заполняется Админом. """
    children_word = models.CharField(max_length=3)

    class Meta:
        verbose_name = 'Дети'
        verbose_name_plural = 'Дети'

    def __str__(self):
        return self.children_word


class City(models.Model):
    """ Список городов СНГ. Заполняется Админом. """
    city_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city_word


class Certificate(models.Model):
    """ Сертификат: ссылка или картинка.
    ForeignKey = Несколько сертификатов может относиться к одному образованию. """
    education = models.ForeignKey(to='Education', on_delete=models.CASCADE)

    img = models.ImageField(blank=True, null=True, verbose_name='certificate_img')
    link = models.URLField(blank=True, null=True, max_length=100, verbose_name='certificate_link')


class EducationWord(models.Model):
    """ Список учебных заведений. Заполняется Админом + может вводиться клиентом. """
    education_word = models.CharField(max_length=100, verbose_name='education_word')

    class Meta:
        verbose_name = 'Учебное заведение'
        verbose_name_plural = 'Учебные заведения'

    def __str__(self):
        return self.education_word


class Education(models.Model):
    """ Образование / Курсы / Университеты / Коледжы.
    ForeignKey = несколько образований у одного Клиента."""
    client_edu = models.ForeignKey(to='Client', on_delete=models.CASCADE)

    institution = models.CharField(max_length=100, null=True, blank=True, verbose_name='institution')
    subject_area = models.CharField(max_length=100, null=True, blank=True, verbose_name='Предметная область')
    specialization = models.CharField(max_length=100, null=True, blank=True, verbose_name='Специализация')
    qualification = models.CharField(max_length=100, null=True, blank=True, verbose_name='Квалификация')
    date_start = models.DateField(null=True, blank=True, verbose_name='дата начала')
    date_end = models.DateField(null=True, blank=True, verbose_name='дата окончания')


class SkillsWord(models.Model):
    """ Список навыков. Заполняется Админом + может вводиться клиентом. """
    skills_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.skills_word


class Skills(models.Model):
    """ Навыки. ForeignKey = несколько навыков у одного Клиента. """
    client_skills = models.ForeignKey(to='Client', on_delete=models.CASCADE)

    skill = models.CharField(max_length=100, blank=True, null=True)


class Sphere(models.Model):
    """ Сфера деятельности. Заполняется Админом.
    ManyToMany отношение с Опытом. """
    sphere_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'

    def __str__(self):
        return self.sphere_word


class Experience(models.Model):
    """ Опыт работы. ForeignKey = несколько видов опыта работы у одного Клиента. """
    client_exp = models.ForeignKey(to='Client', on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='organisation')
    sphere = models.ManyToManyField(Sphere, verbose_name='sphere')  # ??? not more 3
    position = models.CharField(max_length=100, null=True, blank=True, verbose_name='position')
    start_date = models.DateField(null=True, blank=True, verbose_name='start_date')
    end_date = models.DateField(null=True, blank=True, verbose_name='end_date')
    duties = models.TextField(max_length=3000, null=True, blank=True, verbose_name='duties')

    def __str__(self):
        return self.name


class CvWord(models.Model):
    """ Список должностей. Заполняется Админом + может вводиться клиентом. """
    position_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.position_word


class Employment(models.Model):
    """ Тип занятости. Заполняется Админом. """
    employment = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Занятость'
        verbose_name_plural = 'Занятость'

    def __str__(self):
        return self.employment


class TimeJob(models.Model):
    """ График работы. Заполняется Админом. """
    time_job_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'График работы'

    def __str__(self):
        return self.time_job_word


class TypeSalary(models.Model):
    """ Вид валюты. Заполняется Админом. """
    type_word = models.CharField(max_length=8)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюта'

    def __str__(self):
        return self.type_word


class CV(models.Model):
    """ Резюме. ForeignKey = Несколько резюме у одного клиента. """
    client_cv = models.ForeignKey(to='Client', on_delete=models.CASCADE)

    position = models.CharField(max_length=100, null=True, blank=True)
    employment = models.ForeignKey(Employment, on_delete=models.SET_NULL, null=True, blank=True)
    time_job = models.ForeignKey(TimeJob, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.CharField(max_length=10, null=True, blank=True)
    type_salary = models.ForeignKey(TypeSalary, on_delete=models.SET_NULL, null=True, blank=True)
    # There is Poland's upgrade
    vacancies_in_waiting = models.ManyToManyField('Vacancy', blank=True, related_name='in_waiting_for_resume')
    vacancies_accept = models.ManyToManyField('Vacancy', blank=True, related_name='accept_for_resume')
    vacancies_reject = models.ManyToManyField('Vacancy', blank=True, related_name='reject_for_resume')
    notification = models.ManyToManyField('Vacancy', blank=True, related_name='notifications_for_resume')

    def __str__(self):
        return '{}'.format(self.position)

    def get_absolute_url(self):
        return reverse('resume_detail_url', kwargs={'id_c': self.id})

    def get_accept_url(self):
        return reverse('accepted_vacancies_url', kwargs={'id_c': self.id})

    def get_reject_url(self):
        return reverse('rejected_vacancies_url', kwargs={'id_c': self.id})

    def get_vacancies_list_url(self):
        return reverse('vacancies_list_url', kwargs={'id_c': self.id})

    # end upgrade from Poland


class State(models.Model):
    """ Стутус клиента. """
    state_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Стутус клиента'
        verbose_name_plural = 'Стутус клиента'

    def __str__(self):
        return self.state_word


# #####Poland Task 1 & 2 #############################################################################################


class Vacancy(models.Model):
    state = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    salary = models.CharField(max_length=20)
    organization = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    employment = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1000)
    skills = models.CharField(max_length=100, null=True)
    requirements = models.TextField(max_length=1000, null=True)
    duties = models.TextField(max_length=1000, null=True)
    conditions = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.state

    def get_absolute_url(self):
        return reverse('vacancy_detail_url', kwargs={'id_v': self.id})


"""class Resume(models.Model): ##Test table
    state = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    vacancies_in_waiting = models.ManyToManyField('Vacancy', blank=True, related_name='in_waiting_for_resume')
    vacancies_accept = models.ManyToManyField('Vacancy', blank=True, related_name='accept_for_resume')
    vacancies_reject = models.ManyToManyField('Vacancy', blank=True, related_name='reject_for_resume')
    notification = models.ManyToManyField('Vacancy', blank=True, related_name='notifications_for_resume')

    def __str__(self):
        return self.state

    def get_absolute_url(self):
        return reverse('resume_detail_url', kwargs={'id': self.id})

    def get_accept_url(self):
        return reverse('accepted_vacancies_url', kwargs={'id': self.id})

    def get_reject_url(self):
        return reverse('rejected_vacancies_url', kwargs={'id': self.id})

    def get_vacancies_list_url(self):
        return reverse('vacancies_list_url', kwargs={'id': self.id})"""


class Help(models.Model):
    question = models.TextField(max_length=1000)
    answer = models.TextField(max_length=1000)

    def __str__(self):
        return self.question


class JobInterviews(models.Model):
    client = models.ForeignKey(to='Client', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Соискатель')
    cv = models.ForeignKey(to='CV', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Резюме')
    name = models.CharField(max_length=50, verbose_name='Наименование')
    interview_author = models.CharField(max_length=50, verbose_name='Автор собеседования', blank=True, null=True)
    time_of_creation = models.DateTimeField(blank=True, null=True, verbose_name='Время создания')
    period_of_execution = models.DateTimeField(blank=True, null=True, verbose_name='Срок исполнения')
    reminder = models.DateTimeField(blank=True, null=True, verbose_name='Напоминание')
    position = models.CharField(max_length=50, verbose_name='Предполагаемая должность')
    organization = models.CharField(max_length=50, verbose_name='Организация')
    responsible_person = models.CharField(max_length=50, verbose_name='Ответственное лицо')
    contact_responsible_person_1str = models.CharField(max_length=50,
                                                       verbose_name='Контакты ответственного лица (1-я строчка)')
    contact_responsible_person_2str = models.CharField(max_length=50, blank=True, null=True,
                                                       verbose_name='Контакты ответственного лица (2-я строчка)')
    location = models.CharField(max_length=50, verbose_name='Место проведения')
    additional_information = models.TextField(max_length=3000, blank=True, null=True,
                                              verbose_name='Дополнительная информация')
    # add_file = models.FileField(verbose_name='Вложения', blank=True, null=True)
    status = models.BooleanField(default=False)  # статус собеседования, на которое ещё не ходили
    check_status = models.BooleanField(default=True)  # статус активен, если можем после успешного собеседования
    # в течении 60 сек вернуть в статус активных собеседований
    done_interview = models.BooleanField(default=False)  # успешно пройденное собеседование

    # @property
    # def show_all(self):
    # return self.subjobinterview.all()

    @property
    def check_time(self):
        if self.period_of_execution is not None:
            active_time = timezone.now() - self.period_of_execution
            if not self.check_status:
                pass
            elif str(active_time)[2:4] >= '01':
                self.check_status = False
            self.save()

    @property
    def check_readstatus(self):
        if not self.done_interview:
            self.done_interview = True
            self.save()

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #    return reverse('applicant_url', kwargs={'id_a': self.id})


class FilesForJobInterviews(models.Model):
    jobinterviews_files = models.ForeignKey(to='JobInterviews', on_delete=models.CASCADE)
    add_file = models.FileField(verbose_name='Вложения', blank=True, null=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

#########End Poland Task 1 & 2 ##############


class Client(models.Model):
    user_client = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
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
    img = models.ImageField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    # resumes
    resumes = models.ForeignKey(CV, on_delete=models.SET_NULL, null=True, blank=True)  # СвязьCV

    def __str__(self):
        return "%s %s %s" % (self.last_name, self.name, self.patronymic)

    def delete(self, *args, **kwargs):
        self.img.delete()
        # add client_CV.pdf
        # add certificate.pdf
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('applicant_url', kwargs={'id_a': self.id})

    def get_tasks_url(self):
        return reverse('applicant_tasks_url', kwargs={'id_a': self.id})


class Telephone(models.Model):
    """ Номера телефонов. ForeignKey = несколько телефонов у одного Клиента. """
    client_phone = models.ForeignKey(to='Client', on_delete=models.CASCADE)

    telephone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.telephone_number


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
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)


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
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    title = models.TextField(max_length=200)
    time = models.DateTimeField()
    comment = models.TextField(max_length=300, blank=True)
    status = models.BooleanField(default=False)  # задача, которая не выполнена
    endtime = models.DateTimeField(blank=True, null=True)
    checkstatus = models.BooleanField(
        default=True)  # статус активен, если можем после выоплнения задачи в течении 60 сек вернуть в активную задачу
    readtask = models.BooleanField(default=False)

    @property
    def show_all(self):
        return self.subtask.all()

    @property
    def checktime(self):
        if self.endtime != None:
            akttime = timezone.now() - self.endtime
            if self.checkstatus == False:
                pass
            elif str(akttime)[2:4] >= '01':
                self.checkstatus = False
            self.save()

    @property
    def check_readstatus(self):
        if self.readtask == False:
            self.readtask = True
            self.save()


class SubTasks(models.Model):
    title = models.TextField(max_length=100)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="subtask")
    status = models.BooleanField(default=True)  # активная задача

    # def __str__(self):
    #    return self.title

    # def __str__(self):
    #    return self.telephone_number


class Settings(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    messages = models.BooleanField(default=True)
    tasks = models.BooleanField(default=True)
    suggestions = models.BooleanField(default=True)
    meetings = models.BooleanField(default=True)
