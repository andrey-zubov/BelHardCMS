


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='', verbose_name='certificate_img')),
                ('link', models.URLField(blank=True, max_length=100, null=True, verbose_name='certificate_link')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
            },
        ),
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children_word', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Citizenship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('lastname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('date_born', models.DateField(blank=True, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True, verbose_name='Улица')),
                ('house', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер дома')),
                ('flat', models.CharField(blank=True, max_length=10, null=True, verbose_name='Квартира')),
                ('telegram_link', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ник в телеграмме')),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('link_linkedin', models.URLField(blank=True, null=True)),
                ('skype', models.CharField(blank=True, max_length=100, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='')),
                ('children', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Children')),
                ('citizenship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='citizenship', to='client.Citizenship')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country', to='client.Citizenship')),
            ],
        ),
        migrations.CreateModel(
            name='CvWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employment', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_word', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex_word', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkillsWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sphere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sphere_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TimeJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_job_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TypeSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_word', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(

            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('salary', models.CharField(max_length=20)),
                ('organization', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, null=True)),
                ('employment', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(max_length=1000)),
                ('skills', models.CharField(max_length=100, null=True)),
                ('requirements', models.TextField(max_length=1000, null=True)),
                ('duties', models.TextField(max_length=1000, null=True)),
                ('conditions', models.TextField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(

            name='Telephone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('time', models.DateTimeField()),

                ('comment', models.TextField(blank=True, max_length=300)),
                ('status', models.BooleanField(default=False)),
                ('endtime', models.DateTimeField(blank=True, null=True)),
                ('checkstatus', models.BooleanField(default=True)),
                ('readtask', models.BooleanField(default=False)),

                ('date', models.DateField()),
                ('comment', models.TextField(blank=True, max_length=300)),
                ('status', models.BooleanField(default=None)),

                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtask', to='client.Tasks')),
            ],
        ),
        migrations.CreateModel(

            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', models.BooleanField(default=True)),
                ('tasks', models.BooleanField(default=True)),
                ('suggestions', models.BooleanField(default=True)),
                ('meetings', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),

            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('sum_all_vacancies', models.DecimalField(decimal_places=0, max_digits=3)),
                ('vacancies_accept', models.ManyToManyField(blank=True, related_name='accept_for_resume', to='client.Vacancy')),
                ('vacancies_in_waiting', models.ManyToManyField(blank=True, related_name='in_waiting_for_resume', to='client.Vacancy')),
                ('vacancies_reject', models.ManyToManyField(blank=True, related_name='reject_for_resume', to='client.Vacancy')),

            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=3000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата сообщения')),

                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано')),

                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Chat', verbose_name='Чат')),
            ],
            options={
                'ordering': ['pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='organisation')),
                ('position', models.CharField(blank=True, max_length=100, null=True, verbose_name='position')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start_date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end_date')),
                ('duties', models.TextField(blank=True, max_length=3000, null=True, verbose_name='duties')),
                ('sphere', models.ManyToManyField(to='client.Sphere', verbose_name='sphere')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(blank=True, max_length=100, null=True)),
                ('subject_area', models.CharField(blank=True, max_length=100, null=True, verbose_name='Предметная область')),
                ('specialization', models.CharField(blank=True, max_length=100, null=True, verbose_name='Специализация')),
                ('qualification', models.CharField(blank=True, max_length=100, null=True, verbose_name='Квалификация')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='дата начала')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='дата окончания')),
                ('certificate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Certificate')),
            ],
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('salary', models.CharField(max_length=10, null=True)),
                ('employment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Employment')),
                ('time_job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.TimeJob')),
                ('type_salary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.TypeSalary')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='cv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.CV'),
        ),
        migrations.AddField(
            model_name='client',
            name='education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Education'),
        ),
        migrations.AddField(
            model_name='client',
            name='family_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.FamilyState'),
        ),
        migrations.AddField(
            model_name='client',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Experience'),
        ),
        migrations.AddField(
            model_name='client',
            name='sex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Sex'),
        ),
        migrations.AddField(
            model_name='client',
            name='skills',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Skills'),
        ),
        migrations.AddField(
            model_name='client',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.State'),
        ),
        migrations.AddField(
            model_name='client',
            name='user_client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=3000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('opinion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='client.Opinion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
