from django import forms
from client.models import JobInterviews


# class FileFieldForm(forms.ModelForm):
#     class Meta:
#         model = FilesForJobInterviews
#         fields = ['add_file']
#
#     file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class JobInterviewsForm(forms.ModelForm):
    class Meta:
        model = JobInterviews
        fields = [
            'done_interview',
            'cv',
            'period_of_execution',
            'position',
            'name',
            'responsible_person',
            'contact_responsible_person_1str',
            'contact_responsible_person_2str',
            'location',
            'additional_information',
            # 'files_for_jobinterview',
        ]
#     client = models.ForeignKey(to='Client', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Соискатель')
#     cv = models.ForeignKey(to='CV', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Резюме')
#     name = models.CharField(max_length=50, verbose_name='Наименование')
#     interview_author = models.CharField(max_length=50, verbose_name='Автор собеседования', blank=True, null=True)
#     time_of_creation = models.DateTimeField(blank=True, null=True, verbose_name='Время создания')
#     period_of_execution = models.DateTimeField(blank=True, null=True, verbose_name='Срок исполнения')
#     reminder = models.DateTimeField(blank=True, null=True, verbose_name='Напоминание')
#     position = models.CharField(max_length=50, verbose_name='Предполагаемая должность')
#     organization = models.CharField(max_length=50, verbose_name='Организация')
#     responsible_person = models.CharField(max_length=50, verbose_name='Ответственное лицо')
#     contact_responsible_person_1str = models.CharField(max_length=50,
#                                                        verbose_name='Контакты ответственного лица (1-я строчка)')
#     contact_responsible_person_2str = models.CharField(max_length=50, blank=True, null=True,
#                                                        verbose_name='Контакты ответственного лица (2-я строчка)')
#     location = models.CharField(max_length=50, verbose_name='Место проведения')
#     additional_information = models.TextField(max_length=3000, blank=True, null=True,
#                                               verbose_name='Дополнительная информация')
#     # add_file = models.FileField(verbose_name='Вложения', blank=True, null=True)
#     status = models.BooleanField(default=False)  # статус собеседования, на которое ещё не ходили
#     check_status = models.BooleanField(default=True)  # статус активен, если можем после успешного собеседования
#     # в течении 60 сек вернуть в статус активных собеседований
# #     done_interview = models.BooleanField(default=False)  # успешно пройденное собеседование