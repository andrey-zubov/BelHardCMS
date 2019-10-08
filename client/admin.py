from django.contrib import admin

from .models import *



class User(admin.StackedInline):
    admin.site.register(CV)


class Subtasks_Inline(admin.StackedInline):

    model = SubTasks
    extra = 1


class Tasks_Admin(admin.ModelAdmin):

    inlines = [Subtasks_Inline]
    readonly_fields = ['endtime']


class CVAdmin(admin.ModelAdmin):
    list_display = (
        'client_cv', 'position', 'employment', 'time_job', 'salary', 'type_salary',
    )
    list_display_links = (
        'client_cv', 'position', 'employment', 'time_job', 'salary', 'type_salary',
    )
    search_fields = (
        'client_cv', 'position', 'employment', 'time_job', 'salary', 'type_salary',
    )



admin.site.register(CV, CVAdmin)


class VacancyAdmin(admin.ModelAdmin):

    list_display = (
        'state', 'organization', 'slug', 'address', 'employment', 'description',
        'skills', 'requirements', 'duties', 'conditions',
    )
    list_display_links = (
        'state', 'organization', 'description',
    )
    search_fields = (
        'state', 'organization', 'description',
    )


admin.site.register(Vacancy, VacancyAdmin)


class SettingsAdmin(admin.ModelAdmin):

    list_display = ('user', 'messages', 'tasks', 'suggestions', 'meetings', )
    list_display_links = ('user', 'messages', 'tasks', 'suggestions', 'meetings', )
    search_fields = ('user', 'messages', 'tasks', 'suggestions', 'meetings', )


admin.site.register(Settings, SettingsAdmin)


admin.site.register(Help)



admin.site.register(Opinion)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(Tasks, Tasks_Admin)
admin.site.register(Message)


class SexAdmin(admin.ModelAdmin):
    model = Sex


class CitizenshipAdmin(admin.ModelAdmin):
    model = Citizenship


class FamilyStateAdmin(admin.ModelAdmin):
    model = FamilyState


class ChildrenAdmin(admin.ModelAdmin):
    model = Children


class CityAdmin(admin.ModelAdmin):
    model = City


class EducationWordAdmin(admin.ModelAdmin):
    model = EducationWord


class SkillsWordAdmin(admin.ModelAdmin):
    model = SkillsWord


class SphereAdmin(admin.ModelAdmin):
    model = Sphere


class CvWordAdmin(admin.ModelAdmin):
    model = CvWord


class EmploymentAdmin(admin.ModelAdmin):
    model = Employment


class TimeJobAdmin(admin.ModelAdmin):
    model = TimeJob


class TypeSalaryAdmin(admin.ModelAdmin):
    model = TypeSalary


class StateAdmin(admin.ModelAdmin):
    model = State

admin.site.register(Sex, SexAdmin)
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(FamilyState, FamilyStateAdmin)
admin.site.register(Children, ChildrenAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(EducationWord, EducationWordAdmin)
admin.site.register(SkillsWord, SkillsWordAdmin)
admin.site.register(Sphere, SphereAdmin)
admin.site.register(CvWord, CvWordAdmin)
admin.site.register(Employment, EmploymentAdmin)
admin.site.register(TimeJob, TimeJobAdmin)
admin.site.register(TypeSalary, TypeSalaryAdmin)
admin.site.register(State, StateAdmin)
